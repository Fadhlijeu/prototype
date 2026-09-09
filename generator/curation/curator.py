import os
import re
import json
import shutil
import subprocess
from typing import Dict, Any, List, Optional
from ..engine.queue_manager import QueueManager

class Curator:
    """
    Human Decision & Curation Gateway:
    Provides review, approval, rejection, and automated deployment
    of generated components into the core design system.
    """

    def __init__(self, root_dir: str = None, queue_manager: QueueManager = None):
        self.root_dir = root_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.queue = queue_manager or QueueManager(os.path.join(self.root_dir, "generator", "queue"))
        self.glass_dir = os.path.join(self.root_dir, "ui", "components", "glass")
        self.rebuild_script = os.path.join(self.root_dir, "scripts", "rebuild_all.py")

    def list_pending(self) -> List[Dict[str, Any]]:
        return self.queue.get_pending_items()

    def get_preview_path(self, item_id: str) -> Optional[str]:
        item_path = self.queue.get_item_path(item_id, "pending")
        if not item_path:
            return None
        idx_path = os.path.join(item_path, "index.html")
        return idx_path if os.path.exists(idx_path) else item_path

    def approve_and_deploy(self, item_id: str, auto_rebuild: bool = True) -> Dict[str, Any]:
        """
        Accepts candidate UI:
        1. Moves to approved queue.
        2. Copies files to ui/components/glass/{slug}/.
        3. Registers component in scripts/rebuild_all.py.
        4. Triggers rebuild_all.py so showcase reflects the new addition.
        """
        item_path = self.queue.get_item_path(item_id, "pending")
        if not item_path:
            return {"success": False, "error": f"Item {item_id} not found in pending queue"}

        meta_file = os.path.join(item_path, "queue_meta.json")
        manifest_file = os.path.join(item_path, "manifest.json")

        meta = {}
        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)

        manifest = {}
        if os.path.exists(manifest_file):
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)

        slug = manifest.get("slug") or meta.get("slug") or item_id.split("-", 1)[-1]
        title = manifest.get("title", slug.replace("-", " ").title())
        category = manifest.get("category", "inputs")
        badge = manifest.get("badge", "Molecule")

        # 1. Target directory in ui/components/glass/{slug}
        target_dir = os.path.join(self.glass_dir, slug)
        os.makedirs(target_dir, exist_ok=True)

        # Copy component files (ignore queue_meta.json)
        copied_files = []
        for file_name in os.listdir(item_path):
            if file_name in ["queue_meta.json"]:
                continue
            src_file = os.path.join(item_path, file_name)
            if file_name.endswith(".html") and file_name != "index.html":
                dst_name = f"{slug}.html"
            else:
                dst_name = file_name
            dst_file = os.path.join(target_dir, dst_name)
            shutil.copy2(src_file, dst_file)
            copied_files.append(dst_name)

        # 2. Transition state in queue
        approved_dir = self.queue.approve(item_id)

        # 3. Register in scripts/rebuild_all.py
        self._register_in_rebuild_script(slug, title, category, badge)

        # 4. Optional Rebuild
        rebuild_output = ""
        if auto_rebuild and os.path.exists(self.rebuild_script):
            try:
                res = subprocess.run(["python", self.rebuild_script], capture_output=True, text=True, cwd=self.root_dir, check=True)
                rebuild_output = res.stdout
            except Exception as e:
                rebuild_output = f"Rebuild warning: {str(e)}"

        return {
            "success": True,
            "item_id": item_id,
            "slug": slug,
            "title": title,
            "deployed_to": target_dir,
            "copied_files": copied_files,
            "rebuild": rebuild_output
        }

    def reject(self, item_id: str, reason: str = "Human rejection") -> Dict[str, Any]:
        res = self.queue.reject(item_id, reason)
        if res is None:
            return {
                "success": False,
                "item_id": item_id,
                "error": f"Item {item_id} not found in pending queue — nothing rejected (state may be stale, pull latest main first).",
            }
        return {
            "success": True,
            "item_id": item_id,
            "rejected_dir": res
        }

    def _register_in_rebuild_script(self, slug: str, title: str, category: str, badge: str):
        if not os.path.exists(self.rebuild_script):
            return

        with open(self.rebuild_script, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if already registered
        if f'("{slug}"' in content:
            return

        filter_cat = category.lower()
        if filter_cat not in ["inputs", "cards", "navigation", "overlays", "telemetry", "scenery"]:
            filter_cat = "inputs"

        new_entry = f'    ("{slug}", "{title}", "{category.title()}", "{badge}", "{filter_cat}"),\n'

        # Insert into glass_components_metadata = [ ... ]
        pattern = r"(glass_components_metadata\s*=\s*\[\n)"
        if re.search(pattern, content):
            updated = re.sub(pattern, r"\g<1>" + new_entry, content, count=1)
            with open(self.rebuild_script, "w", encoding="utf-8") as f:
                f.write(updated)
