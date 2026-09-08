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
        "buttons": ["button", "fab", "action button", "pill button", "button group", "cta"],
        "sliders": ["slider", "stepper", "scrubber", "range", "trackbar", "dial control"],
        "controls": ["toggle", "switch", "checkbox", "radio", "selector", "segmented control"],
        "cards": ["card", "panel", "folder", "storage", "profile", "preview", "widget", "container"],
        "navigation": ["dock", "bar", "nav", "tab", "menu", "sidebar", "breadcrumb", "pagination"],
        "telemetry": ["chart", "meter", "progress", "stat", "gauge", "graph", "histogram", "audio visualizer"],
        "overlays": ["modal", "dialog", "drawer", "sheet", "popup", "bottom sheet"],
        "feedback": ["toast", "notification", "alert", "badge", "tooltip", "status", "banner"],
        "dashboards": ["dashboard", "analytics", "command center", "metrics board", "kpi", "admin panel", "workbench"],
        "scenery": ["scenery", "scene", "screenery", "composition", "full screen", "composite", "layout collection", "showcase scene", "workspace"],
        "other": ["other", "lainnya", "bebas", "custom", "experimental", "hybrid", "creative", "misc", "novelty"]
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

    AUTONOMOUS_THEMES = {
        "telemetry": [
            ("Neon Cyan Frequency Visualizer", "ambient-pulse", "Molecule"),
            ("Dual Arc Specular Latency Gauge", "specular-frosted", "Molecule"),
            ("Fluctuating Mesh Server Telemetry", "aurora-gradient-glow", "Organism"),
            ("Bioluminescent Hardware Radar", "ambient-pulse", "Molecule"),
            ("Obsidian High-Precision Dial Meter", "minimal-obsidian", "Molecule")
        ],
        "sliders": [
            ("Magnetic Haptic Precision Slider", "spring-interactive", "Molecule"),
            ("Refraction Density Optical Scrubber", "liquid-refraction", "Molecule"),
            ("Specular Dual Range Fader", "specular-frosted", "Molecule"),
            ("Quantum Level Stepper Control", "minimal-obsidian", "Molecule"),
            ("Electric Blue Ambient Slider", "aurora-gradient-glow", "Molecule")
        ],
        "controls": [
            ("Segmented Frosted Capsule Switch", "segmented-glass", "Atomic"),
            ("Tactile Obsidian Power Rocker", "minimal-obsidian", "Atomic"),
            ("Spring Pill Mode Switcher", "spring-interactive", "Atomic"),
            ("Biometric Holographic Toggle", "aurora-gradient-glow", "Atomic"),
            ("Liquid State Segmented Pill", "liquid-refraction", "Atomic")
        ],
        "buttons": [
            ("Specular Action Speed Dial", "floating-elevated", "Molecule"),
            ("Expandable Frosted Glass FAB", "spring-interactive", "Molecule"),
            ("Micro-Elevation Action Pill", "specular-frosted", "Atomic"),
            ("Magenta Ambient Trigger Dial", "aurora-gradient-glow", "Molecule"),
            ("Holographic Radial Launch Button", "floating-elevated", "Molecule")
        ],
        "navigation": [
            ("Frosted Capsule Dock Bar", "floating-elevated", "Molecule"),
            ("Liquid Spring Breadcrumb Trail", "spring-interactive", "Molecule"),
            ("Segmented Obsidian Tab Rail", "segmented-glass", "Molecule"),
            ("Radial Compass Navigation Node", "floating-elevated", "Molecule"),
            ("Specular Horizontal Pill Nav", "specular-frosted", "Molecule")
        ],
        "dashboards": [
            ("Obsidian Telemetry Command Matrix", "minimal-obsidian", "Composite Scenery"),
            ("Realtime Mesh Metrics Cockpit", "aurora-gradient-glow", "Composite Scenery"),
            ("Multi-Cluster System Dashboard", "segmented-glass", "Composite Scenery")
        ],
        "scenery": [
            ("Glass Scenery Workstation Viewport", "specular-frosted", "Composite Scenery"),
            ("Cybernetic Multi-Widget Viewport", "liquid-refraction", "Composite Scenery"),
            ("Modular Environment Scenery Hub", "floating-elevated", "Composite Scenery")
        ],
        "feedback": [
            ("Glass Password Strength Glowing Meter", "ambient-pulse", "Molecule"),
            ("Solar Amber Notification Pill", "aurora-gradient-glow", "Molecule"),
            ("Refractive Glass Banner Alert", "specular-frosted", "Molecule")
        ],
        "inputs": [
            ("Intelligent Semantic Prompt Bar", "specular-frosted", "Molecule"),
            ("Aurora Floating Command Search Bar", "aurora-gradient-glow", "Molecule"),
            ("Tag-Clustered Glass Input Field", "spring-interactive", "Molecule")
        ],
        "other": [
            ("Experimental Radial Command Wheel", "floating-elevated", "Creative Freeform"),
            ("Holographic Zero-Gravity Dial", "aurora-gradient-glow", "Creative Freeform"),
            ("Prismatic Glass Resonance Orb", "liquid-refraction", "Creative Freeform")
        ]
    }

    def __init__(self, existing_slugs: List[str] = None):
        self.existing_slugs = set(existing_slugs or [])

    def classify_intent(self, prompt: str) -> Dict[str, Any]:
        """
        Classifies prompt into structured generation parameters.
        Enforces system policy constraints (family='glass', theme='dark').
        """
        prompt_lower = prompt.lower()

        # Check if this is an open-ended autonomous directive (e.g. from Google Apps Script)
        is_autonomous = any(kw in prompt_lower for kw in [
            "anda adalah", "secara bebas", "ai web engineer", "creative frontend",
            "autonomous ui", "lead design system", "bebas memilih", "beragam opsi",
            "pilih secara bebas", "autonomous glass ui exploration"
        ])

        if is_autonomous:
            # Check if prompt targets a category
            target_cat = None
            for cat in self.CATEGORIES.keys():
                if f"kategori '{cat}'" in prompt_lower or f"kategori {cat}" in prompt_lower or f"category '{cat}'" in prompt_lower:
                    target_cat = cat
                    break

            if not target_cat:
                # Rotate across categories to guarantee variety
                all_cats = list(self.AUTONOMOUS_THEMES.keys())
                random.shuffle(all_cats)
                target_cat = all_cats[0]

            pool = self.AUTONOMOUS_THEMES.get(target_cat, self.AUTONOMOUS_THEMES["other"])
            # Filter pool to items not yet in existing_slugs
            candidates = [
                c for c in pool
                if re.sub(r"[^a-z0-9]+", "-", c[0].lower()).strip("-") not in self.existing_slugs
            ]
            chosen = random.choice(candidates) if candidates else random.choice(pool)

            title = chosen[0]
            variation = chosen[1]
            atomic_level = chosen[2]
            detected_category = target_cat
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

            counter = 2
            orig = slug
            while slug in self.existing_slugs:
                slug = f"{orig}-v{counter}"
                counter += 1

            self.existing_slugs.add(slug)

            return {
                "title": title,
                "slug": slug,
                "category": detected_category,
                "variation": variation,
                "atomic_level": atomic_level,
                "family": "glass",
                "theme": "dark",
                "icon": self.CATEGORIES.get(detected_category, ["sparkles"])[0],
                "raw_prompt": prompt
            }

        # 1. Determine category for specific user prompts
        detected_category = "inputs"
        max_matches = 0
        for cat, keywords in self.CATEGORIES.items():
            matches = sum(1 for kw in keywords if kw in prompt_lower)
            if matches > max_matches:
                max_matches = matches
                detected_category = cat

        if max_matches == 0:
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
        if detected_category in ["controls", "buttons", "inputs"]:
            atomic_level = "Atomic"
        elif detected_category in ["sliders", "cards", "navigation", "telemetry", "feedback"]:
            atomic_level = "Molecule"
        elif detected_category in ["overlays"]:
            atomic_level = "Organism"
        elif detected_category in ["dashboards", "scenery"]:
            atomic_level = "Composite Scenery"
        else:
            atomic_level = "Creative Freeform"

        # 4. Generate human-readable title and clean kebab slug
        stop_words = {
            "buat", "bikin", "make", "create", "bebas", "desain", "dan", "untuk", "the", "yang",
            "anda", "adalah", "you", "are", "senior", "lead", "architect", "engineer", "technologist",
            "ciptakan", "sebuah", "rancang", "tentukan", "options", "pilih", "secara", "mandiri", "kreatif",
            "dengan", "ada", "bisa", "kamu", "terdapat", "prototype", "system", "component", "komponen", "web"
        }
        words = re.findall(r"\b[a-zA-Z]{3,}\b", prompt)
        filtered_words = [w.capitalize() for w in words if w.lower() not in stop_words]

        var_label = variation.replace("-", " ").title()
        cat_label = detected_category.rstrip("s").title()

        if len(filtered_words) >= 2:
            title_base = " ".join(filtered_words[:3])
        elif len(filtered_words) == 1:
            title_base = f"{filtered_words[0]} {cat_label}"
        else:
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
            "buttons": ["sparkles", "zap", "check", "play", "plus"],
            "sliders": ["sliders", "sliders-horizontal", "gauge", "disc"],
            "cards": ["layout", "folder", "hard-drive", "cpu", "layers"],
            "navigation": ["compass", "grid", "home", "menu", "arrow-right"],
            "controls": ["toggle-right", "check", "play", "circle", "power"],
            "overlays": ["maximize-2", "x", "info", "shield", "external-link"],
            "feedback": ["bell", "alert-circle", "check-circle-2", "flame"],
            "telemetry": ["activity", "bar-chart-2", "trending-up", "gauge"],
            "dashboards": ["layout-dashboard", "kanban", "pie-chart", "bar-chart-3"],
            "scenery": ["monitor", "palette", "sparkles", "columns", "box"],
            "other": ["sparkles", "wand-2", "shapes", "gem"]
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
