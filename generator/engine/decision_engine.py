import re
import random
from typing import Dict, Any, List

class DecisionEngine:
    """
    AI Decision Layer:
    Interprets user prompt or autonomous directive, extracting strict constraints
    and choosing creative variation, category, purpose, and manifest metadata.
    """

    CATEGORIES = {
        "inputs": ["input", "login", "form", "search", "password", "textarea", "prompt", "chat", "pill"],
        "cards": ["card", "panel", "folder", "storage", "profile", "preview", "widget", "container"],
        "navigation": ["dock", "bar", "nav", "tab", "menu", "sidebar", "breadcrumb", "pagination"],
        "controls": ["button", "toggle", "switch", "checkbox", "radio", "slider", "stepper"],
        "overlays": ["modal", "dialog", "drawer", "sheet", "popup", "bottom sheet"],
        "feedback": ["toast", "notification", "alert", "badge", "tooltip", "status", "banner"],
        "telemetry": ["chart", "meter", "progress", "stat", "gauge", "graph", "histogram"],
    }

    VARIATIONS = [
        "specular-frosted",
        "aurora-gradient-glow",
        "liquid-refraction",
        "floating-elevated",
        "minimal-obsidian",
        "spring-interactive",
        "segmented-glass",
        "ambient-pulse",
    ]

    ATOMIC_LEVELS = ["Atomic", "Molecule", "Organism"]

    def __init__(self, existing_slugs: List[str] = None):
        self.existing_slugs = existing_slugs or []

    def classify_intent(self, prompt: str) -> Dict[str, Any]:
        """
        Classifies prompt into structured generation parameters.
        Enforces system policy constraints (family='glass', theme='dark').
        """
        prompt_lower = prompt.lower()

        # 1. Determine category
        detected_category = "inputs"
        max_matches = 0
        for cat, keywords in self.CATEGORIES.items():
            matches = sum(1 for kw in keywords if kw in prompt_lower)
            if matches > max_matches:
                max_matches = matches
                detected_category = cat

        if max_matches == 0:
            # Autonomous random selection favoring underrepresented categories
            detected_category = random.choice(list(self.CATEGORIES.keys()))

        # 2. Determine variation style
        variation = None
        for var in self.VARIATIONS:
            if any(part in prompt_lower for part in var.split("-")):
                variation = var
                break
        if not variation:
            variation = random.choice(self.VARIATIONS)

        # 3. Determine atomic hierarchy
        if detected_category in ["controls", "feedback"]:
            atomic_level = "Atomic"
        elif detected_category in ["overlays", "navigation"]:
            atomic_level = "Organism"
        else:
            atomic_level = "Molecule"

        # 4. Generate human-readable title and clean kebab slug
        words = re.findall(r"\b[a-zA-Z]{3,}\b", prompt)
        filtered_words = [w.capitalize() for w in words if w.lower() not in ["buat", "bikin", "make", "create", "bebas", "desain", "dan", "untuk", "the", "yang"]]
        
        if len(filtered_words) >= 2:
            title_base = " ".join(filtered_words[:3])
        else:
            var_label = variation.replace("-", " ").title()
            cat_label = detected_category.rstrip("s").title()
            title_base = f"{var_label} {cat_label}"

        title = f"Glass {title_base}" if "glass" not in title_base.lower() else title_base
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

        # Avoid collision with existing slugs
        counter = 2
        original_slug = slug
        while slug in self.existing_slugs:
            slug = f"{original_slug}-v{counter}"
            counter += 1

        # Suggested icons
        icon_map = {
            "inputs": ["sparkles", "search", "send", "at-sign", "lock"],
            "cards": ["layout", "folder", "hard-drive", "cpu", "layers"],
            "navigation": ["compass", "grid", "home", "menu", "arrow-right"],
            "controls": ["sliders", "toggle-right", "check", "play", "zap"],
            "overlays": ["maximize-2", "x", "info", "shield", "external-link"],
            "feedback": ["bell", "alert-circle", "check-circle-2", "flame"],
            "telemetry": ["activity", "bar-chart-2", "trending-up", "gauge"],
        }
        icons = icon_map.get(detected_category, ["sparkles", "star"])

        # Extract tags
        tags = ["glass", "dark", detected_category, variation]
        for w in filtered_words:
            tag_candidate = w.lower()
            if tag_candidate not in tags and len(tag_candidate) > 2:
                tags.append(tag_candidate)

        return {
            "family": "glass",
            "theme": "dark",
            "title": title,
            "slug": slug,
            "category": detected_category,
            "variation": variation,
            "atomic_level": atomic_level,
            "icons": icons,
            "tags": tags,
            "raw_prompt": prompt,
        }
