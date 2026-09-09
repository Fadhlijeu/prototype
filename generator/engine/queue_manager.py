import os
import json
import shutil
import time
from typing import Dict, Any, List, Optional

class QueueManager:
    """
    Review Queue & Lifecycle State Engine:
    Manages transitions across states:
    GENERATING -> VALIDATING -> DUPLICATE -> PENDING_REVIEW -> APPROVED / REJECTED.
    Enforces max_pending_review limits to prevent generation overflows.
    """

    MAX_PENDING = 100

    def __init__(self, queue_root: str = None):
        if not queue_root:
            queue_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "queue"))
        self.queue_root = queue_root
        self.pending_dir = os.path.join(self.queue_root, "pending")
        self.approved_dir = os.path.join(self.queue_root, "approved")
        self.rejected_dir = os.path.join(self.queue_root, "rejected")
        self._ensure_dirs()

    def _ensure_dirs(self):
        for d in [self.pending_dir, self.approved_dir, self.rejected_dir]:
            os.makedirs(d, exist_ok=True)

    def is_queue_full(self) -> bool:
        """Returns True if pending review items reach or exceed MAX_PENDING limit."""
        return len(self.get_pending_items()) >= self.MAX_PENDING

    def enqueue_pending(self, decompiled: Dict[str, Any], validation: Dict[str, Any], router_meta: Dict[str, Any]) -> str:
        """Saves a successfully generated and validated component into pending review."""
        slug = decompiled.get("slug", "glass-widget")
        item_id = f"{int(time.time())}-{slug}"
        item_dir = os.path.join(self.pending_dir, item_id)
        os.makedirs(item_dir, exist_ok=True)

        # Write decompiled files
        with open(os.path.join(item_dir, decompiled.get("standalone_file", f"{slug}.html")), "w", encoding="utf-8") as f:
            f.write(decompiled.get("standalone_content", ""))

        with open(os.path.join(item_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(decompiled.get("index_html", ""))

        with open(os.path.join(item_dir, "index.css"), "w", encoding="utf-8") as f:
            f.write(decompiled.get("index_css", ""))

        with open(os.path.join(item_dir, "index.js"), "w", encoding="utf-8") as f:
            f.write(decompiled.get("index_js", ""))

        with open(os.path.join(item_dir, "manifest.json"), "w", encoding="utf-8") as f:
            f.write(decompiled.get("manifest_json", "{}"))

        # Write queue metadata
        meta = {
            "item_id": item_id,
            "slug": slug,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "PENDING_REVIEW",
            "validation": validation,
            "router": router_meta,
        }
        with open(os.path.join(item_dir, "queue_meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return item_id

    def get_pending_items(self) -> List[Dict[str, Any]]:
        """Returns all items currently in PENDING_REVIEW state."""
        items = []
        if not os.path.exists(self.pending_dir):
            return items

        for entry in sorted(os.listdir(self.pending_dir)):
            item_dir = os.path.join(self.pending_dir, entry)
            meta_path = os.path.join(item_dir, "queue_meta.json")
            if os.path.isdir(item_dir) and os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    items.append(meta)
                except Exception:
                    pass
        return items

    def get_item_path(self, item_id: str, state: str = "pending") -> Optional[str]:
        target_dir = getattr(self, f"{state}_dir", self.pending_dir)
        item_path = os.path.join(target_dir, item_id)
        return item_path if os.path.exists(item_path) else None

    def approve(self, item_id: str) -> Optional[str]:
        """Moves item from pending to approved."""
        src = os.path.join(self.pending_dir, item_id)
        if not os.path.exists(src):
            return None
        dest = os.path.join(self.approved_dir, item_id)
        shutil.move(src, dest)

        # Update status
        meta_path = os.path.join(dest, "queue_meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            meta["status"] = "APPROVED"
            meta["approved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
        return dest

    def reject(self, item_id: str, reason: str = "Human curator decision") -> Optional[str]:
        """Archives item from pending queue into rejected/ (audit trail, not purge).

        Moves the whole item directory pending/<id> -> rejected/<id> and writes
        queue_meta.json status=REJECTED with reason + rejected_at timestamp.
        Returns destination path, or None if item was not found in pending.
        """
        import datetime
        src = os.path.join(self.pending_dir, item_id)
        if not os.path.isdir(src):
            return None
        dest = os.path.join(self.rejected_dir, item_id)
        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)
        shutil.move(src, dest)
        meta_path = os.path.join(dest, "queue_meta.json")
        try:
            meta = {}
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            meta["status"] = "REJECTED"
            meta["rejected_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            meta["reject_reason"] = reason
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
        except Exception:
            pass
        # Persist audit note alongside the archived files
        try:
            with open(os.path.join(dest, "rejection.json"), "w", encoding="utf-8") as f:
                json.dump({"item_id": item_id, "reason": reason,
                           "rejected_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                          f, indent=2)
        except Exception:
            pass
        return dest

    def _count_valid_items(self, folder: str) -> int:
        if not os.path.exists(folder):
            return 0
        return len([e for e in os.listdir(folder) if os.path.isdir(os.path.join(folder, e))])

    def get_stats(self) -> Dict[str, int]:
        return {
            "pending": self._count_valid_items(self.pending_dir),
            "approved": self._count_valid_items(self.approved_dir),
            "rejected": self._count_valid_items(self.rejected_dir),
        }

    def export_web_manifest(self, output_path: str):
        """Exports all pending review items to a single JSON manifest for the Generator Lab web UI."""
        pending_list = []
        for meta in self.get_pending_items():
            item_id = meta.get("item_id", "")
            slug = meta.get("slug", "")
            item_dir = os.path.join(self.pending_dir, item_id)
            preview_file = os.path.join(item_dir, f"{slug}.html")
            if not os.path.exists(preview_file):
                preview_file = os.path.join(item_dir, "index.html")

            preview_html = ""
            if os.path.exists(preview_file):
                try:
                    with open(preview_file, "r", encoding="utf-8") as f:
                        preview_html = f.read()
                except Exception:
                    pass

            manifest_file = os.path.join(item_dir, "manifest.json")
            manifest_data = {}
            if os.path.exists(manifest_file):
                try:
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        manifest_data = json.load(f)
                except Exception:
                    pass

            pending_list.append({
                "id": item_id,
                "title": manifest_data.get("title", slug.replace("-", " ").title()),
                "slug": slug,
                "category": manifest_data.get("category", "other"),
                "variation": manifest_data.get("variation", "frosted-glass"),
                "score": meta.get("validation", {}).get("score", 95),
                "provider": f"{meta.get('router', {}).get('provider', 'ai')}:{meta.get('router', {}).get('model', 'model')}",
                "createdAt": meta.get("created_at", time.strftime("%Y-%m-%d %H:%M:%S")),
                "previewHtml": preview_html
            })

        data = {
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pending": pending_list
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Also write queue.js for file:// protocol support without CORS restrictions
        js_path = os.path.splitext(output_path)[0] + ".js"
        with open(js_path, "w", encoding="utf-8") as f:
            f.write("window.PROTOTYPE_CLOUD_QUEUE = " + json.dumps(data, indent=2) + ";\n")
