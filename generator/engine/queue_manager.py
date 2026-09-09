import os
import json
import shutil
import time
from typing import Dict, Any, List, Optional

class QueueManager:
    """
    Review Queue & Lifecycle State Engine:
    Manages authoritative state transitions across component lifecycle:
    GENERATING -> VALIDATING -> NOVELTY_CHECK -> PENDING_REVIEW -> APPROVED (PUBLISHED) / REJECTED (ARCHIVED).
    Maintains authoritative queue metadata and exports comprehensive web manifest for Generator Lab.
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

        # Write authoritative queue metadata
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

    def _read_queue_dir(self, directory: str) -> List[Dict[str, Any]]:
        items = []
        if not os.path.exists(directory):
            return items
        for entry in sorted(os.listdir(directory)):
            item_dir = os.path.join(directory, entry)
            if not os.path.isdir(item_dir):
                continue
            meta_path = os.path.join(item_dir, "queue_meta.json")
            meta = {}
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except Exception:
                    pass
            if not meta.get("item_id"):
                meta["item_id"] = entry
            if not meta.get("slug"):
                meta["slug"] = entry.split("-", 1)[1] if "-" in entry else entry
            items.append(meta)
        return items

    def get_pending_items(self) -> List[Dict[str, Any]]:
        """Returns all items currently in PENDING_REVIEW state."""
        return self._read_queue_dir(self.pending_dir)

    def get_approved_items(self) -> List[Dict[str, Any]]:
        """Returns all items currently in APPROVED state."""
        return self._read_queue_dir(self.approved_dir)

    def get_rejected_items(self) -> List[Dict[str, Any]]:
        """Returns all archived items currently in REJECTED state."""
        return self._read_queue_dir(self.rejected_dir)

    def get_rejected_signatures(self) -> List[Dict[str, Any]]:
        """Returns negative memory: concepts, slugs, and reasons of rejected components."""
        signatures = []
        for it in self.get_rejected_items():
            signatures.append({
                "item_id": it.get("item_id"),
                "slug": it.get("slug"),
                "reason": it.get("reject_reason", "Curator rejection"),
                "rejected_at": it.get("rejected_at")
            })
        return signatures

    def get_item_path(self, item_id: str, state: str = "pending") -> Optional[str]:
        target_dir = getattr(self, f"{state}_dir", self.pending_dir)
        item_path = os.path.join(target_dir, item_id)
        return item_path if os.path.exists(item_path) else None

    def approve(self, item_id: str, published_path: str = None) -> Optional[str]:
        """Moves item from pending to approved and records authoritative approval timestamp."""
        src = os.path.join(self.pending_dir, item_id)
        if not os.path.exists(src):
            return None
        dest = os.path.join(self.approved_dir, item_id)
        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)
        shutil.move(src, dest)

        # Update authoritative status
        meta_path = os.path.join(dest, "queue_meta.json")
        meta = {}
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                pass
        meta["status"] = "APPROVED"
        meta["approved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if published_path:
            meta["published_path"] = published_path
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return dest

    def reject(self, item_id: str, reason: str = "Human curator decision") -> Optional[str]:
        """
        Archives item from pending queue into rejected/ directory.
        Creates rejection.json audit trail and updates queue_meta.json.
        """
        src = os.path.join(self.pending_dir, item_id)
        if not os.path.isdir(src):
            return None
        dest = os.path.join(self.rejected_dir, item_id)
        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)
        shutil.move(src, dest)

        meta_path = os.path.join(dest, "queue_meta.json")
        meta = {}
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                pass
        meta["status"] = "REJECTED"
        meta["rejected_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        meta["reject_reason"] = reason
        meta["reason"] = reason
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        # Persist explicit rejection.json for negative memory
        try:
            with open(os.path.join(dest, "rejection.json"), "w", encoding="utf-8") as f:
                json.dump({
                    "item_id": item_id,
                    "status": "REJECTED",
                    "reason": reason,
                    "reject_reason": reason,
                    "rejected_at": meta["rejected_at"],
                    "slug": meta.get("slug", "")
                }, f, indent=2)
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

    def _build_manifest_card(self, meta: Dict[str, Any], folder: str) -> Dict[str, Any]:
        item_id = meta.get("item_id", "")
        slug = meta.get("slug", "")
        item_dir = os.path.join(folder, item_id)
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

        return {
            "id": item_id,
            "title": manifest_data.get("title", slug.replace("-", " ").title()),
            "slug": slug,
            "category": manifest_data.get("category", "other"),
            "variation": manifest_data.get("variation", "frosted-glass"),
            "score": meta.get("validation", {}).get("score", 95),
            "provider": f"{meta.get('router', {}).get('provider', 'ai')}:{meta.get('router', {}).get('model', 'model')}",
            "status": meta.get("status", "PENDING_REVIEW"),
            "createdAt": meta.get("created_at", time.strftime("%Y-%m-%d %H:%M:%S")),
            "approvedAt": meta.get("approved_at"),
            "rejectedAt": meta.get("rejected_at"),
            "rejectReason": meta.get("reject_reason"),
            "previewHtml": preview_html
        }

    def export_web_manifest(self, output_path: str):
        """
        Exports authoritative state (pending, approved, and rejected)
        to a single JSON manifest for the Generator Lab web UI.
        """
        pending_list = [self._build_manifest_card(m, self.pending_dir) for m in self.get_pending_items()]
        approved_list = [self._build_manifest_card(m, self.approved_dir) for m in self.get_approved_items()]
        rejected_list = [self._build_manifest_card(m, self.rejected_dir) for m in self.get_rejected_items()]

        data = {
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pending": pending_list,
            "approved": approved_list,
            "rejected": rejected_list,
            "stats": self.get_stats()
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Also write queue.js for file:// protocol support without CORS restrictions
        js_path = os.path.splitext(output_path)[0] + ".js"
        with open(js_path, "w", encoding="utf-8") as f:
            f.write("window.PROTOTYPE_CLOUD_QUEUE = " + json.dumps(data, indent=2) + ";\n")
