# Autonomous Continuous Generation Directive

## Primary Objective
Read `skills/glass-ui.md` and `skills/component.md`. Continuously generate creative, high-fidelity UI variations that strictly follow the defined Dark Glass aesthetic. Explore diverse component categories, ergonomic micro-interactions, optical glass material physics, dynamic animations, and state representations. 

Avoid duplicates with the existing collection in `ui/components/glass/`. Prioritize fresh concepts, compound components, and accessibility-compliant interactive widgets.

---

## 3-Level Instruction Model

1. **Strict Constraints (Immutable)**:
   - Must belong to the `glass` family on a deep obsidian/space-black canvas (`#030712` / `var(--bg-main)`).
   - Must consume design tokens from `../css.css` (`var(--glass-surface-*)`, `var(--glass-border-specular)`, `var(--radius-*)`, etc.).
   - Pure Vanilla CSS & Vanilla JavaScript. Zero external frameworks.
   - Accessible keyboard focus (`:focus-visible`), ARIA roles, and `@media (prefers-reduced-motion: reduce)` support.
   - Use Lucide icons (`<i data-lucide="..."></i>`) initialized via `lucide.createIcons()`.

2. **Flexible Intent (Configurable by Prompt)**:
   - Component Category: Buttons, Form Inputs, Cards, Badges, Pickers, Navigations, Steppers, Overlays, or Data Displays.
   - Purpose: Workspace productivity, AI prompting, settings, dashboards, status indicators, or audio-visual feedback.

3. **Autonomous Exploration (Creative Space)**:
   - Visual treatments: Frosted glass, aurora gradients, glowing edges, specular highlights, liquid glass, refractive highlights.
   - Interaction states: Hover spring lifts, active press depression, smooth toggle states, fluid transitions.
   - Layout variations: Compact, floating, segmented, stacked, or minimal.

---

## Output Contract
Every generation cycle must output a self-contained HTML document containing:
- Embedded `<style>` block (pure CSS referencing design system tokens)
- Semantic HTML markup (`<button>`, `<input>`, `<article>`, `<dialog>`, etc.)
- Embedded `<script>` block for interactive logic, state toggling, and keyboard bindings
- JSON Metadata Manifest block inside `<script type="application/json" id="component-manifest">`
