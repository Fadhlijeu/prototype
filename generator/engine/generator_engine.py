import os
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
        self.glass_skill_path = os.path.join(self.root_dir, "skills", "glass-ui.md")
        self.css_tokens_path = os.path.join(self.root_dir, "ui", "components", "glass", "css.css")
        self.component_taxonomy_path = os.path.join(self.root_dir, "component.md")
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

        # 2. Glass UI design system rules (primary skill)
        glass_skill = self._read_context_file(self.glass_skill_path)
        if glass_skill:
            ctx["glass_skill"] = glass_skill

        # 3. CSS token definitions — the SINGLE SOURCE OF TRUTH for all design tokens
        css_tokens = self._read_context_file(self.css_tokens_path, max_chars=6000)
        if css_tokens:
            ctx["css_tokens"] = css_tokens

        # 4. Master component taxonomy — understand what exists, avoid duplicates
        taxonomy = self._read_context_file(self.component_taxonomy_path, max_chars=5000)
        if taxonomy:
            ctx["component_taxonomy"] = taxonomy

        # 5. Additional skills (component patterns, interaction models, etc.)
        extra_skills = self._load_all_skills()
        if extra_skills:
            ctx["extra_skills"] = extra_skills

        return ctx

    def build_prompts(self, spec: Dict[str, Any], existing_memory: list = None) -> Tuple[str, str]:
        """Constructs system prompt (with full project context) and detailed user generation instruction."""
        ctx = self._load_project_context()

        memory_str = ""
        if existing_memory:
            memory_str = "Existing collection names (AVOID generating duplicates of these):\n" + "\n".join(f"- {name}" for name in existing_memory[:25])

        # Build extra skills section
        extra_skills_str = ""
        for skill in ctx.get("extra_skills", []):
            extra_skills_str += f"\n### Skill Reference: {skill['name']}\n{skill['content']}\n"

        system_prompt = f"""You are the Autonomous UI Component Architect for this Prototype design system.
Your mission is to generate production-grade, accessible, dark glassmorphic web components.

=== GENERATION DIRECTIVE ===
{ctx.get('directive', 'Generate creative, high-fidelity glass UI components.')}

=== GLASS UI DESIGN SYSTEM RULES ===
{ctx.get('glass_skill', '')}

=== CSS DESIGN TOKENS (SINGLE SOURCE OF TRUTH) ===
The following is the ACTUAL css.css file from this project. Use these EXACT variable names in your generated components:

```css
{ctx.get('css_tokens', '/* css.css not found - use standard glass tokens */')}
```

=== MASTER COMPONENT TAXONOMY ===
Reference this to understand existing components and avoid duplication. Pick from categories that need new variations:

{ctx.get('component_taxonomy', '<!-- taxonomy not loaded -->')}

=== ADDITIONAL SKILL REFERENCES ===
{extra_skills_str if extra_skills_str else '(no additional skills loaded)'}

=== IMMUTABLE GENERATION RULES ===
1. Always output a single complete HTML file containing embedded <style>, semantic HTML, manifest JSON in <script id="component-manifest" type="application/json">, and interactive <script>.
2. Do NOT use external CSS frameworks (no Tailwind, no Bootstrap). Only Vanilla CSS.
3. Reference design system tokens from `../css.css` using EXACT variable names from the CSS Tokens section above (e.g. `var(--glass-surface-1)`, `var(--glass-border-specular)`, `var(--text-primary)`, `var(--accent-cyan)`).
4. Use Lucide icons: `<i data-lucide="..."></i>` and call `lucide.createIcons()`.
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

{memory_str}

Ensure the component is interactive, visually stunning, with subtle specular borders, ambient depth, and spring transitions. Include the component manifest JSON script tag.
"""
        return system_prompt, user_prompt

    def generate(self, spec: Dict[str, Any], existing_memory: list = None) -> Tuple[str, Dict[str, Any]]:
        """Executes generation pipeline and strips surrounding formatting."""
        system_prompt, user_prompt = self.build_prompts(spec, existing_memory)
        raw_output, router_meta = self.router.call_with_cascade(system_prompt, user_prompt)

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

