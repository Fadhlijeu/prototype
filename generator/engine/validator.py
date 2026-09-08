import re
from typing import Dict, Any, List

class Validator:
    """
    Automated Quality Gate & Policy Enforcer:
    Validates HTML structure, CSS token usage, file size, accessibility,
    and checks for forbidden libraries before entering review queue.
    """

    MAX_BYTES = 102400  # 100KB

    def validate(self, decompiled: Dict[str, Any]) -> Dict[str, Any]:
        errors: List[str] = []
        warnings: List[str] = []
        score = 100

        html = decompiled.get("standalone_content", "")
        css = decompiled.get("index_css", "")
        js = decompiled.get("index_js", "")

        # 1. File Size Verification
        size_bytes = len(html.encode("utf-8"))
        if size_bytes > self.MAX_BYTES:
            errors.append(f"File size exceeds 100KB budget: {size_bytes} bytes")
            score -= 30

        # 2. HTML Basic Structure
        if "<!DOCTYPE html>" not in html and "<!doctype html>" not in html:
            warnings.append("Missing <!DOCTYPE html> declaration")
            score -= 5

        if "<body" not in html or "</body>" not in html:
            errors.append("Malformed HTML: Missing <body> tags")
            score -= 30

        # 3. Glass Aesthetic & Token Compliance
        has_glass_token = any(token in css or token in html for token in [
            "--glass-", "backdrop-filter", "blur(", "rgba(255, 255, 255,", "--bg-main"
        ])
        if not has_glass_token:
            errors.append("Component does not use design system tokens or glassmorphism attributes")
            score -= 35

        # 4. Forbidden Libraries
        forbidden = ["tailwindcss", "bootstrap.min.css", "jquery.min.js", "bootstrap.bundle"]
        for lib in forbidden:
            if lib in html.lower():
                errors.append(f"Contains forbidden external dependency: {lib}")
                score -= 40

        # 5. Accessibility Checks
        has_semantic_or_aria = any(attr in html.lower() for attr in [
            "aria-label", "aria-labelledby", "role=", "<button", "<input", "<label", "aria-checked"
        ])
        if not has_semantic_or_aria:
            warnings.append("Interactive elements should include ARIA labels or semantic roles")
            score -= 10

        # 6. Prefers-Reduced-Motion Check
        if "prefers-reduced-motion" not in css and "prefers-reduced-motion" not in html:
            warnings.append("Missing @media (prefers-reduced-motion: reduce) block in CSS")
            score -= 5

        # 7. Inline Event Handlers Check
        if re.search(r'\bonclick\s*=\s*["\']', html, re.IGNORECASE):
            warnings.append("Contains inline onclick attribute; prefer addEventListener in index.js")
            score -= 5

        is_valid = len(errors) == 0 and score >= 60

        return {
            "valid": is_valid,
            "score": max(0, score),
            "errors": errors,
            "warnings": warnings,
            "file_size_bytes": size_bytes,
        }
