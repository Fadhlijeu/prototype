import os
import re
from typing import Dict, Any, List, Tuple

class Deduplicator:
    """
    Similarity & Novelty Gate:
    Compares candidate component against existing GlassOS corpus to prevent
    generating duplicate or near-identical UI components.
    """

    def __init__(self, glass_dir: str = None):
        if not glass_dir:
            glass_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ui", "components", "glass"))
        self.glass_dir = glass_dir
        self.existing_components = self._scan_existing_components()

    def _scan_existing_components(self) -> List[Dict[str, Any]]:
        components = []
        if not os.path.exists(self.glass_dir):
            return components

        for item in os.listdir(self.glass_dir):
            item_path = os.path.join(self.glass_dir, item)
            if os.path.isdir(item_path):
                components.append({
                    "slug": item,
                    "title": item.replace("-", " ").title(),
                    "words": set(re.findall(r"\w+", item.lower()))
                })
        return components

    def get_existing_names(self) -> List[str]:
        return [c["title"] for c in self.existing_components]

    def get_existing_slugs(self) -> List[str]:
        return [c["slug"] for c in self.existing_components]

    def check_similarity(self, candidate_slug: str, candidate_title: str) -> Tuple[bool, float, str]:
        """
        Calculates Jaccard word similarity with existing corpus.
        Returns: (is_duplicate, similarity_score, matched_component)
        """
        cand_words = set(re.findall(r"\w+", candidate_slug.lower() + " " + candidate_title.lower()))
        # Remove common stop words
        cand_words = {w for w in cand_words if w not in ["glass", "dark", "ui", "component"]}

        if not cand_words:
            return False, 0.0, ""

        highest_sim = 0.0
        most_similar_comp = ""

        for comp in self.existing_components:
            comp_words = {w for w in comp["words"] if w not in ["glass", "dark", "ui", "component"]}
            if not comp_words:
                continue

            # Direct or substring slug match
            if candidate_slug == comp["slug"]:
                highest_sim = 1.0
                most_similar_comp = comp["slug"]
                break
            elif candidate_slug in comp["slug"] or comp["slug"] in candidate_slug:
                sim = 0.9
                if sim > highest_sim:
                    highest_sim = sim
                    most_similar_comp = comp["slug"]

            intersection = len(cand_words.intersection(comp_words))
            union = len(cand_words.union(comp_words))
            jaccard = intersection / union if union > 0 else 0.0

            if jaccard > highest_sim:
                highest_sim = jaccard
                most_similar_comp = comp["slug"]

        # Duplicate threshold: 0.80 (80% similarity with existing component)
        is_duplicate = highest_sim >= 0.80
        return is_duplicate, highest_sim, most_similar_comp
