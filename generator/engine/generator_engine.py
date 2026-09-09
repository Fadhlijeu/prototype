import os
import random
import re
from typing import Dict, Any, List, Tuple
from .model_router import ModelRouter


class GeneratorEngine:
    """
    Core Generation Engine:
    Assembles system directives, design skills knowledge, and classified intent
    into high-fidelity prompts for the active Model Router.

    Context injection includes:
    - generator/config/directive.md       → Generation directives
    - skills/glass-ui.md                  → Glass UI design system rules
    - ui/components/glass/css.css         → Full CSS token definitions (source of truth)
    - component.md                        → Master component taxonomy + existing inventory
    - skills/*.md                         → All additional skill documents
    """

    def __init__(self, root_dir: str = None, model_router: ModelRouter = None):
        self.root_dir = root_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.router = model_router or ModelRouter()

        # Primary context file paths
        self.directive_path = os.path.join(self.root_dir, "generator", "config", "directive.md")
        self.style_spec_path = os.path.join(self.root_dir, "ui", "components", "glass", "STYLE_SPEC.md")
        self.glass_skill_path = os.path.join(self.root_dir, "skills", "glass-ui.md")
        self.css_tokens_path = os.path.join(self.root_dir, "ui", "components", "glass", "css.css")
        self.component_taxonomy_path = os.path.join(self.root_dir, "component.md")
        self.glass_components_dir = os.path.join(self.root_dir, "ui", "components", "glass")
        self.skills_dir = os.path.join(self.root_dir, "skills")

        # Backward compat alias
        self.skills_glass_path = self.glass_skill_path

    def _read_context_file(self, path: str, max_chars: int = 8000) -> str:
        """Reads a file safely, truncating to max_chars to stay within token budgets."""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content) > max_chars:
                content = content[:max_chars] + "\n...[truncated for context budget]"
            return content
        return ""

    def _load_exemplar_components(self) -> str:
        """Loads actual working HTML code from key components in ui/components/glass as real-world exemplars."""
        exemplar_slugs = ["aurora-storage-card", "chat-input-bar", "thinking-effort-selector", "ai-agent-scenery"]
        output = []

        for slug in exemplar_slugs:
            comp_file = os.path.join(self.glass_components_dir, slug, f"{slug}.html")
            if not os.path.exists(comp_file):
                comp_file = os.path.join(self.glass_components_dir, slug, "index.html")
            if os.path.exists(comp_file):
                code = self._read_context_file(comp_file, max_chars=3500)
                output.append(f"#### Reference Component: `{slug}`\n```html\n{code}\n```")

        return "\n\n".join(output)

    def _load_glass_directory_index(self) -> str:
        """Lists all component directories and files in ui/components/glass/ to provide full repository context."""
        if not os.path.isdir(self.glass_components_dir):
            return ""
        items = []
        for name in sorted(os.listdir(self.glass_components_dir)):
            full_path = os.path.join(self.glass_components_dir, name)
            if os.path.isdir(full_path):
                files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
                items.append(f"- `ui/components/glass/{name}/` (Files: {', '.join(files)})")
            elif os.path.isfile(full_path) and name in ["css.css", "STYLE_SPEC.md", "showcase.html"]:
                items.append(f"- `ui/components/glass/{name}` (Core system file)")
        return "\n".join(items)

    def _load_all_skills(self) -> List[Dict[str, str]]:
        """Loads all .md files from the skills/ directory (excluding glass-ui.md which is loaded separately)."""
        skills = []
        if not os.path.isdir(self.skills_dir):
            return skills
        for fname in sorted(os.listdir(self.skills_dir)):
            if not fname.endswith(".md"):
                continue
            if fname == "glass-ui.md":
                continue  # loaded separately with higher prominence
            fpath = os.path.join(self.skills_dir, fname)
            content = self._read_context_file(fpath, max_chars=4000)
            if content.strip():
                skills.append({"name": fname, "content": content})
        return skills

    def _load_project_context(self) -> Dict[str, str]:
        """
        Aggregates all project knowledge files that the AI should use as reference.
        Returns a dict with labeled sections ready for prompt injection.
        """
        ctx = {}

        # 1. Generator directives
        directive = self._read_context_file(self.directive_path)
        if directive:
            ctx["directive"] = directive

        # 2. Glass Dark Premium STYLE SPEC (STYLE_SPEC.md) - Crucial for 5-layer architecture & asymmetric borders
        style_spec = self._read_context_file(self.style_spec_path, max_chars=8000)
        if style_spec:
            ctx["style_spec"] = style_spec

        # 3. Glass UI design system rules (skills/glass-ui.md)
        glass_skill = self._read_context_file(self.glass_skill_path)
        if glass_skill:
            ctx["glass_skill"] = glass_skill

        # 4. CSS token definitions — the SINGLE SOURCE OF TRUTH for all design tokens (css.css)
        css_tokens = self._read_context_file(self.css_tokens_path, max_chars=6000)
        if css_tokens:
            ctx["css_tokens"] = css_tokens

        # 5. Master component taxonomy — understand what exists, avoid duplicates
        taxonomy = self._read_context_file(self.component_taxonomy_path, max_chars=5000)
        if taxonomy:
            ctx["component_taxonomy"] = taxonomy

        # 6. Real component references and directory structure from ui/components/glass/
        glass_index = self._load_glass_directory_index()
        if glass_index:
            ctx["glass_index"] = glass_index

        exemplars = self._load_exemplar_components()
        if exemplars:
            ctx["exemplars"] = exemplars

        # 7. Additional skills (component patterns, interaction models, etc.)
        extra_skills = self._load_all_skills()
        if extra_skills:
            ctx["extra_skills"] = extra_skills

        return ctx

    def build_prompts(self, spec: Dict[str, Any], existing_memory: list = None, negative_memory: list = None) -> Tuple[str, str]:
        """Constructs system prompt (with full project context, Master Design Directive, Variation Genome) and detailed user generation instruction."""
        ctx = self._load_project_context()

        memory_str = ""
        if existing_memory:
            memory_str = "Existing collection names (AVOID generating duplicates of these):\n" + "\n".join(f"- {name}" for name in existing_memory[:25])

        negative_str = ""
        if negative_memory:
            negative_items = []
            for item in negative_memory[:10]:
                if isinstance(item, dict):
                    slug = item.get("slug", "unknown")
                    reason = item.get("reason", "Monotonic/Repetitive design")
                    negative_items.append(f"- `{slug}`: Rejected reason: {reason}")
                elif isinstance(item, str):
                    negative_items.append(f"- `{item}`")
            if negative_items:
                negative_str = "\n=== REJECTED PAST DESIGNS (NEGATIVE MEMORY — DELIBERATELY AVOID) ===\n" + "\n".join(negative_items) + "\nDo NOT generate designs resembling the rejected patterns above.\n"

        genome = spec.get("genome", {})
        genome_str = ""
        if genome:
            import json
            genome_str = f"""
=== ASSIGNED VARIATION GENOME (MANDATORY STRUCTURAL IDENTITY) ===
You MUST construct this component according to this unique architectural DNA:
```json
{json.dumps(genome, indent=2)}
```
- Geometry: {genome.get('geometry')} (Do NOT use a generic 440px rectangular card!)
- Composition: {genome.get('composition')}
- Density & Orientation: {genome.get('density')}, {genome.get('orientation')}
- Interaction Model: {genome.get('interaction')} (Provide REAL working JS interaction!)
- Material & Depth: {genome.get('material')}, {genome.get('depth')}
- Palette: {genome.get('palette')} (Primary: {genome.get('primary_accent')}, Secondary: {genome.get('secondary_accent')}, Glow: {genome.get('glow_color')})
- Lighting & Border: {genome.get('lighting')}, {genome.get('border')}
- Information Architecture: {genome.get('information_architecture')}
- Target Novelty Score: {genome.get('novelty_target', 0.85)} (Must feel completely different from previous creations)
"""

        # Build extra skills section
        extra_skills_str = ""
        for skill in ctx.get("extra_skills", []):
            extra_skills_str += f"\n### Skill Reference: {skill['name']}\n{skill['content']}\n"

        system_prompt = f"""You are the Autonomous Senior UI/UX Engineer & Glassmorphism Design Technologist for this Prototype design system.
Your mission is to invent and generate production-grade, accessible, dark glassmorphic web components.

=== MASTER DESIGN DIRECTIVE (ANTI-SLOP & RADICAL NOVELTY) ===
Read and understand the project's design references before generating anything:
- `ui/components/glass/STYLE_SPEC.md`
- `ui/components/glass/css.css`
- existing components inside `ui/components/glass/`

The references define the visual language, material quality, interaction quality, and design-system constraints.
DO NOT copy an existing component.
DO NOT produce a near-duplicate.
DO NOT simply rename, recolor, resize, or rearrange an existing component.

Your task is to create a NEW design direction that belongs to the same design family.

PRESERVE:
- Material language (frosted dark glass, specular light, ambient depth)
- Visual polish and high aesthetic standards
- Glass quality and realistic optical refraction
- Lighting logic (directional top highlight, darker bottom)
- Typography discipline (Inter font, tabular numbers for metrics)
- Interaction quality (spring physics, haptic feedback feeling)
- Accessibility (ARIA labels, focus states, prefers-reduced-motion)
- Design-system compatibility (css.css tokens)

VARY AGGRESSIVELY:
- Silhouette and outer contours (NOT always a rectangle!)
- Geometry (radial, capsule dock, curved arc, modular split, floating nodes)
- Spatial composition and layout flow
- Information hierarchy and anatomy
- Interaction model (gestural, stepper, scrub, speed-dial, drag, flip)
- Control placement and control clusters
- Layering strategy and depth model
- Edge treatment and specular border accents
- Motion language and micro-animations
- Proportions, aspect ratio, density, and orientation

A generated component may be:
horizontal, vertical, radial, floating, nested, asymmetric, modular, split-pane, stacked, orbital, timeline-like, dial-like, ribbon-like, mesh-like, spatial, compact, or oversized.
DO NOT assume the component must be a rectangular card.
Use existing components as STYLE REFERENCES, not STRUCTURAL TEMPLATES.

Before writing code, internally decide:
1. What makes this component visually distinct?
2. What is its unique geometry?
3. What is its unique interaction model?
4. What is its unique spatial composition?
5. What is its unique color strategy?
6. What existing components does it resemble?
7. How will you deliberately avoid resembling them?

The final result must feel like: "same design universe, completely different invention."

=== GENERATION DIRECTIVE ===
{ctx.get('directive', 'Generate creative, high-fidelity glass UI components.')}

=== GLASS DARK PREMIUM STYLE SPECIFICATION ===
{ctx.get('style_spec', '')}

=== CSS DESIGN TOKENS (css.css - SINGLE SOURCE OF TRUTH) ===
{ctx.get('css_tokens', '/* css.css not found - use standard glass tokens */')}

=== REPOSITORY DIRECTORY CATALOGUE (ui/components/glass/) ===
The following components already exist in `ui/components/glass/`:
{ctx.get('glass_index', '')}

=== REAL REPOSITORY EXEMPLAR COMPONENTS ===
Study these existing components from the repository to match their polish, but create a NEW structural invention:
{ctx.get('exemplars', '')}

=== MASTER COMPONENT TAXONOMY ===
{ctx.get('component_taxonomy', '<!-- taxonomy not loaded -->')}

=== ADDITIONAL SKILL REFERENCES ===
{extra_skills_str if extra_skills_str else '(no additional skills loaded)'}

=== IMMUTABLE GENERATION RULES ===
1. Always output a single complete HTML file containing embedded <style>, semantic HTML, manifest JSON in <script id="component-manifest" type="application/json">, and interactive <script>.
2. Do NOT use external CSS frameworks (no Tailwind, no Bootstrap). Only Vanilla CSS.
3. Reference design system tokens from `../css.css` using EXACT variable names (e.g. `var(--glass-surface-1)`, `var(--glass-border-top)`, `var(--text-primary)`, `var(--accent-cyan)`).
4. Use Lucide icons: `<i data-lucide="..."></i>` with uniform 1.5px stroke width, and call `lucide.createIcons()`.
5. Implement `@media (prefers-reduced-motion: reduce)` to disable heavy animations.
6. Provide accessible ARIA attributes (`aria-label`, `role`, etc.).
7. Return pure HTML without unnecessary markdown explanations or conversational filler.
"""

        user_prompt = f"""Generate a new dark glassmorphic component for the Prototype design system with the following specifications:
- Title: {spec.get('title')}
- Slug: {spec.get('slug')}
- Category: {spec.get('category')}
- Variation Style: {spec.get('variation')}
- Hierarchy Level: {spec.get('atomic_level', 'Molecule')}
- Suggested Icons: {', '.join(spec.get('icons', []))}
- User Prompt Intent: {spec.get('raw_prompt')}
- Diversity Nonce: {random.randint(100000, 999999)}

{genome_str}

{memory_str}

{negative_str}

CRITICAL DIVERSITY RULES (values in STYLE_SPEC are MOOD ILLUSTRATIONS ONLY — NEVER copy them literally):
1. Invent fresh, vivid hex values conforming to the genome palette ({genome.get('palette', 'custom')}).
2. Randomize aurora blob positions (X: 15-85%, Y: 15-85%) and opacities (0.35-0.75).
3. Strictly implement the assigned geometry ('{genome.get('geometry', 'unique-form')}') — do NOT default to a generic 440px box.
4. Provide working interactive JavaScript so the component feels alive and responsive to clicks/drags/toggles.
Ensure the component includes the component manifest JSON script tag.
"""
        return system_prompt, user_prompt

    def generate(self, spec: Dict[str, Any], existing_memory: list = None, allow_mock: bool = False, force_provider: str = None, negative_memory: list = None) -> Tuple[str, Dict[str, Any]]:
        """Executes generation pipeline and strips surrounding formatting."""
        system_prompt, user_prompt = self.build_prompts(spec, existing_memory, negative_memory=negative_memory)
        raw_output, router_meta = self.router.call_with_cascade(system_prompt, user_prompt, allow_mock=allow_mock, force_provider=force_provider)

        # Clean markdown codeblocks if model enclosed output in ```html
        cleaned_html = self._clean_output(raw_output)
        return cleaned_html, router_meta

    def _clean_output(self, text: str) -> str:
        text = text.strip()
        # Remove leading ```html or ```
        match = re.search(r"^```(?:html)?\s*(.*?)\s*```$", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text

    def get_context_summary(self) -> Dict[str, Any]:
        """Debug helper: returns which context files were found and their sizes."""
        files = {
            "directive": self.directive_path,
            "glass_skill": self.glass_skill_path,
            "css_tokens": self.css_tokens_path,
            "component_taxonomy": self.component_taxonomy_path,
            "skills_dir": self.skills_dir,
        }
        summary = {}
        for key, path in files.items():
            if key == "skills_dir":
                summary[key] = {
                    "exists": os.path.isdir(path),
                    "files": [f for f in os.listdir(path) if f.endswith(".md")] if os.path.isdir(path) else []
                }
            else:
                summary[key] = {
                    "exists": os.path.exists(path),
                    "size_bytes": os.path.getsize(path) if os.path.exists(path) else 0,
                    "path": path
                }
        return summary

