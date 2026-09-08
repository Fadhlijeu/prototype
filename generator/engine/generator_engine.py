import os
import re
from typing import Dict, Any, Tuple
from .model_router import ModelRouter

class GeneratorEngine:
    """
    Core Generation Engine:
    Assembles system directives, design skills knowledge, and classified intent
    into high-fidelity prompts for the active Model Router.
    """

    def __init__(self, root_dir: str = None, model_router: ModelRouter = None):
        self.root_dir = root_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.router = model_router or ModelRouter()
        self.skills_glass_path = os.path.join(self.root_dir, "skills", "glass-ui.md")
        self.directive_path = os.path.join(self.root_dir, "generator", "config", "directive.md")

    def _read_context_file(self, path: str) -> str:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def build_prompts(self, spec: Dict[str, Any], existing_memory: list = None) -> Tuple[str, str]:
        """Constructs system prompt and detailed user generation instruction."""
        glass_skill = self._read_context_file(self.skills_glass_path)
        directive = self._read_context_file(self.directive_path)

        memory_str = ""
        if existing_memory:
            memory_str = "Existing collection names (AVOID generating duplicates of these):\n" + "\n".join(f"- {name}" for name in existing_memory[:25])

        system_prompt = f"""You are the GlassOS Autonomous UI Component Architect.
Your mission is to generate production-grade, accessible, dark glassmorphic web components.

### Directive:
{directive}

### Glass UI System Rules & Token Usage:
{glass_skill}

### Rules:
1. Always output a single complete HTML file containing embedded <style>, semantic HTML, manifest JSON in <script id="component-manifest" type="application/json">, and interactive <script>.
2. Do NOT use external CSS frameworks (no Tailwind, no Bootstrap). Only Vanilla CSS.
3. Reference GlassOS tokens from `../css.css` (e.g. `var(--glass-surface-1)`, `var(--glass-border-specular)`, `var(--text-primary)`, `var(--accent-cyan)`).
4. Use Lucide icons: `<i data-lucide="..."></i>` and call `lucide.createIcons()`.
5. Implement `@media (prefers-reduced-motion: reduce)` to disable heavy animations.
6. Provide accessible ARIA attributes (`aria-label`, `role`, etc.).
7. Return pure HTML without unnecessary markdown explanations or conversational filler.
"""

        user_prompt = f"""Generate a new GlassOS component with the following specifications:
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
