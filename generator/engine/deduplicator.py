import os
import re
from typing import Dict, Any, List, Tuple

class Deduplicator:
    """
    Similarity & Novelty Gate:
    Compares candidate component against existing design system corpus to prevent
    generating duplicate or near-identical UI components.
    Uses both lexical (slug/title) and structural design fingerprinting (DOM, CSS tokens, layout models).
    """

    def __init__(self, glass_dir: str = None):
        if not glass_dir:
            glass_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ui", "components", "glass"))
        self.glass_dir = glass_dir
        self.existing_components = self._scan_existing_components()

    def _extract_design_fingerprint(self, html_content: str) -> Dict[str, Any]:
        """Extracts structural traits: DOM tags, layout models, colors, primitives, interactive elements."""
        if not html_content:
            return {}

        content_lower = html_content.lower()

        # 1. DOM tags frequency
        raw_tags = re.findall(r"<\s*([a-zA-Z0-9\-]+)", content_lower)
        excluded_tags = {"html", "head", "body", "meta", "title", "link", "script", "style"}
        tags = set(t for t in raw_tags if t not in excluded_tags)

        # 2. CSS property markers
        css_props = set()
        if "display: grid" in content_lower or "display:grid" in content_lower:
            css_props.add("display-grid")
        if "display: flex" in content_lower or "display:flex" in content_lower:
            css_props.add("display-flex")
        if "backdrop-filter" in content_lower:
            css_props.add("backdrop-filter")
        if "radial-gradient" in content_lower:
            css_props.add("radial-gradient")
        if "linear-gradient" in content_lower:
            css_props.add("linear-gradient")
        if "@keyframes" in content_lower:
            css_props.add("has-keyframes")

        # 3. Form factor & interactive primitives
        primitives = set()
        if "<input" in content_lower:
            if 'type="range"' in content_lower or "type='range'" in content_lower:
                primitives.add("range-slider")
            elif 'type="text"' in content_lower or "type='text'" in content_lower:
                primitives.add("text-input")
            elif 'type="checkbox"' in content_lower:
                primitives.add("checkbox")
            else:
                primitives.add("input")
        if "<button" in content_lower:
            primitives.add("button")
        if "<canvas" in content_lower:
            primitives.add("canvas")
        if "<svg" in content_lower:
            primitives.add("svg")
        if "data-lucide" in content_lower:
            primitives.add("lucide-icons")
        if "<nav" in content_lower:
            primitives.add("nav")

        # 4. Color hex values
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}\b", html_content))

        # 5. Radius and width signatures
        radius_match = re.findall(r"border-radius:\s*([^;]+);", content_lower)
        radii = set(r.strip() for r in radius_match)
        width_match = re.findall(r"max-width:\s*([^;]+);", content_lower)
        widths = set(w.strip() for w in width_match)

        return {
            "tags": tags,
            "css_props": css_props,
            "primitives": primitives,
            "hex_codes": hex_codes,
            "radii": radii,
            "widths": widths,
            "is_capsule": "9999px" in str(radii),
            "is_radial": "radial" in content_lower or "circle" in content_lower
        }

    def _scan_existing_components(self) -> List[Dict[str, Any]]:
        components = []
        if not os.path.exists(self.glass_dir):
            return components

        for item in os.listdir(self.glass_dir):
            item_path = os.path.join(self.glass_dir, item)
            if os.path.isdir(item_path):
                # Load component HTML content if present to extract fingerprint
                content = ""
                for candidate_file in [f"{item}.html", "index.html"]:
                    fpath = os.path.join(item_path, candidate_file)
                    if os.path.exists(fpath):
                        try:
                            with open(fpath, "r", encoding="utf-8") as f:
                                content = f.read(15000)
                            break
                        except Exception:
                            pass

                fp = self._extract_design_fingerprint(content)
                components.append({
                    "slug": item,
                    "title": item.replace("-", " ").title(),
                    "words": set(re.findall(r"\w+", item.lower())),
                    "fingerprint": fp
                })
        return components

    def get_existing_names(self) -> List[str]:
        return [c["title"] for c in self.existing_components]

    def get_existing_slugs(self) -> List[str]:
        return [c["slug"] for c in self.existing_components]

    def compute_structural_similarity(self, fp1: Dict[str, Any], fp2: Dict[str, Any]) -> float:
        """Calculates multi-axis structural similarity between two design fingerprints (0.0 to 1.0)."""
        if not fp1 or not fp2:
            return 0.0

        def jaccard(s1, s2):
            if not s1 and not s2:
                return 1.0
            if not s1 or not s2:
                return 0.0
            return len(s1.intersection(s2)) / len(s1.union(s2))

        # Weight distribution
        tag_sim = jaccard(fp1.get("tags", set()), fp2.get("tags", set()))
        css_sim = jaccard(fp1.get("css_props", set()), fp2.get("css_props", set()))
        prim_sim = jaccard(fp1.get("primitives", set()), fp2.get("primitives", set()))
        color_sim = jaccard(fp1.get("hex_codes", set()), fp2.get("hex_codes", set()))

        # Form factor match
        capsule_match = 1.0 if fp1.get("is_capsule") == fp2.get("is_capsule") else 0.0
        radial_match = 1.0 if fp1.get("is_radial") == fp2.get("is_radial") else 0.0
        form_sim = (capsule_match + radial_match) / 2.0

        structural_sim = (
            tag_sim * 0.25 +
            css_sim * 0.25 +
            prim_sim * 0.20 +
            color_sim * 0.15 +
            form_sim * 0.15
        )
        return round(structural_sim, 3)

    def check_similarity(self, candidate_slug: str, candidate_title: str, candidate_html: str = "") -> Tuple[bool, float, str]:
        """
        Calculates lexical (words) and structural (DOM, CSS tokens, layout) similarity.
        Returns: (is_duplicate, similarity_score, matched_component)
        """
        cand_words = set(re.findall(r"\w+", candidate_slug.lower() + " " + candidate_title.lower()))
        cand_words = {w for w in cand_words if w not in ["glass", "dark", "ui", "component"]}

        cand_fp = self._extract_design_fingerprint(candidate_html) if candidate_html else {}

        highest_sim = 0.0
        most_similar_comp = ""

        for comp in self.existing_components:
            comp_words = {w for w in comp["words"] if w not in ["glass", "dark", "ui", "component"]}

            # 1. Lexical slug/title similarity
            if candidate_slug == comp["slug"]:
                lexical_sim = 1.0
            elif candidate_slug in comp["slug"] or comp["slug"] in candidate_slug:
                lexical_sim = 0.85
            else:
                intersection = len(cand_words.intersection(comp_words))
                union = len(cand_words.union(comp_words))
                lexical_sim = intersection / union if union > 0 else 0.0

            # 2. Structural similarity
            struct_sim = 0.0
            if cand_fp and comp.get("fingerprint"):
                struct_sim = self.compute_structural_similarity(cand_fp, comp["fingerprint"])

            # Combined similarity: structural fingerprint weighted heavily if available
            if cand_fp and comp.get("fingerprint"):
                combined_sim = (lexical_sim * 0.35) + (struct_sim * 0.65)
            else:
                combined_sim = lexical_sim

            if combined_sim > highest_sim:
                highest_sim = combined_sim
                most_similar_comp = comp["slug"]

        highest_sim = round(highest_sim, 3)
        # Threshold: if combined similarity >= 0.72, flag as duplicate/too similar
        is_duplicate = highest_sim >= 0.72
        return is_duplicate, highest_sim, most_similar_comp

    def compute_novelty_score(self, candidate_slug: str, candidate_title: str, candidate_html: str = "") -> Dict[str, Any]:
        """
        Computes formal Novelty Score (0.00 = duplicate, 1.00 = entirely novel).
        Eligible for review if novelty_score >= 0.65.
        """
        is_dup, max_sim, matched_slug = self.check_similarity(candidate_slug, candidate_title, candidate_html)
        novelty = max(0.0, round(1.0 - max_sim, 3))
        return {
            "novelty_score": novelty,
            "similarity_score": max_sim,
            "most_similar_component": matched_slug,
            "is_novel": novelty >= 0.65,
            "status": "APPROVED_NOVELTY" if novelty >= 0.65 else "REJECTED_LOW_NOVELTY"
        }
