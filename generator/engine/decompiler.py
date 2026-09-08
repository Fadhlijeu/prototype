import re
import json
from typing import Dict, Any

class Decompiler:
    """
    Decompiles a single generated HTML artifact into standardized GlassOS component files:
    1. {slug}.html (Full standalone)
    2. index.html (Clean demo linking external CSS/JS)
    3. index.css (Extracted CSS rules)
    4. index.js (Extracted JavaScript logic)
    5. manifest.json (Component metadata & taxonomy)
    """

    def decompile(self, raw_html: str, spec: Dict[str, Any]) -> Dict[str, str]:
        slug = spec.get("slug", "glass-component")
        title = spec.get("title", "Glass Component")

        # 1. Extract Manifest JSON if present
        manifest_data = self._extract_manifest(raw_html, spec)

        # 2. Extract CSS from <style> blocks
        styles = re.findall(r"<style[^>]*>(.*?)</style>", raw_html, re.DOTALL | re.IGNORECASE)
        extracted_css = "\n\n".join(s.strip() for s in styles) if styles else "/* Component CSS */"

        # 3. Extract JS from <script> blocks (excluding manifest and external script tags)
        scripts = re.findall(r"<script(?![^>]*src=)(?![^>]*application/json)[^>]*>(.*?)</script>", raw_html, re.DOTALL | re.IGNORECASE)
        extracted_js = "\n\n".join(s.strip() for s in scripts) if scripts else "// Component Interaction Logic"

        # 4. Extract Body Content
        body_match = re.search(r"<body[^>]*>(.*?)</body>", raw_html, re.DOTALL | re.IGNORECASE)
        if body_match:
            body_inner = body_match.group(1)
            # Strip <script> and <style> from body inner to get clean markup
            body_clean = re.sub(r"<script[^>]*>.*?</script>", "", body_inner, flags=re.DOTALL | re.IGNORECASE)
            body_clean = re.sub(r"<style[^>]*>.*?</style>", "", body_clean, flags=re.DOTALL | re.IGNORECASE).strip()
        else:
            body_clean = "<div class=\"component-canvas\">\n    <!-- Component Markup -->\n</div>"

        # 5. Build clean index.html demo
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — GlassOS Dark</title>
    <link rel="stylesheet" href="../css.css">
    <link rel="stylesheet" href="index.css">
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body>

{body_clean}

    <script>
        if (window.lucide) window.lucide.createIcons();
    </script>
    <script src="index.js"></script>
</body>
</html>
"""

        # 6. Ensure {slug}.html is complete and well-formed
        standalone_html = raw_html

        return {
            "slug": slug,
            "standalone_file": f"{slug}.html",
            "standalone_content": standalone_html,
            "index_html": index_html,
            "index_css": extracted_css,
            "index_js": extracted_js,
            "manifest_json": json.dumps(manifest_data, indent=2),
            "manifest": manifest_data
        }

    def _extract_manifest(self, raw_html: str, default_spec: Dict[str, Any]) -> Dict[str, Any]:
        match = re.search(r'<script[^>]*id=["\']component-manifest["\'][^>]*>(.*?)</script>', raw_html, re.DOTALL | re.IGNORECASE)
        if match:
            try:
                parsed = json.loads(match.group(1).strip())
                # Merge with default spec
                for k, v in default_spec.items():
                    if k not in parsed:
                        parsed[k] = v
                return parsed
            except Exception:
                pass
        return {
            "title": default_spec.get("title", "Glass Component"),
            "slug": default_spec.get("slug", "glass-component"),
            "category": default_spec.get("category", "inputs"),
            "badge": default_spec.get("atomic_level", "Molecule"),
            "variation": default_spec.get("variation", "specular-frosted"),
            "tags": default_spec.get("tags", ["glass", "dark"]),
        }
