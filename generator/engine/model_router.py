import os
import re
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, Tuple

class ModelRouter:
    """
    Model Router & Cascade Manager:
    Selects active provider and cascades across model pools (Gemini -> 9Router -> Mock)
    when quota is exhausted or rate limits are reached.
    """

    def __init__(self, config_path: Optional[str] = None):
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "models.json")
        self.config_path = config_path
        self.config = self._load_config()
        self.cooldowns: Dict[str, float] = {}

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"providers": []}

    def get_available_models(self) -> list:
        """Returns list of models sorted by priority that are currently eligible."""
        now = time.time()
        candidates = []
        providers = sorted(self.config.get("providers", []), key=lambda p: p.get("priority", 999))

        for provider in providers:
            p_id = provider["id"]
            env_key = provider.get("env_key")
            endpoint = provider.get("endpoint", "")
            api_key = os.environ.get(env_key) if env_key else None

            # Skip provider if required API key is missing (except mock provider)
            if env_key and not api_key:
                continue

            for model in provider.get("models", []):
                m_key = f"{p_id}:{model['model_id']}"
                if now < self.cooldowns.get(m_key, 0):
                    continue  # In cooldown

                candidates.append({
                    "provider_id": p_id,
                    "provider_name": provider["name"],
                    "model_id": model["model_id"],
                    "endpoint": provider.get("endpoint"),
                    "api_key": api_key,
                    "cooldown_seconds": provider.get("cooldown_seconds", 60),
                    "priority": provider.get("priority", 999) * 100 - model.get("priority", 0)
                })

        candidates.sort(key=lambda c: c["priority"])
        return candidates

    def mark_cooldown(self, provider_id: str, model_id: str, seconds: int = 60):
        """Marks a model as exhausted/rate-limited until cooldown period expires."""
        m_key = f"{provider_id}:{model_id}"
        self.cooldowns[m_key] = time.time() + seconds

    def call_with_cascade(self, system_prompt: str, user_prompt: str) -> Tuple[str, Dict[str, Any]]:
        """
        Attempts execution using the priority cascade.
        If a model fails or is rate limited, falls back to the next available provider.
        """
        available_models = self.get_available_models()

        if not available_models:
            # Absolute fallback to mock provider
            available_models = [{
                "provider_id": "mock",
                "provider_name": "Offline Simulation Provider",
                "model_id": "mock-glass-generator-v1",
                "endpoint": "local",
                "api_key": None,
                "cooldown_seconds": 0,
                "priority": 9999
            }]

        errors = []
        for model in available_models:
            provider_id = model["provider_id"]
            model_id = model["model_id"]
            try:
                if provider_id == "mock":
                    output = self._call_mock(system_prompt, user_prompt)
                    return output, {
                        "provider": provider_id,
                        "model": model_id,
                        "status": "success",
                        "cascaded_from": errors
                    }

                elif provider_id == "gemini":
                    output = self._call_gemini(model["endpoint"], model["model_id"], model["api_key"], system_prompt, user_prompt)
                    return output, {
                        "provider": provider_id,
                        "model": model_id,
                        "status": "success",
                        "cascaded_from": errors
                    }

                elif provider_id in ["9router", "tokenrouter"] or "chat/completions" in model.get("endpoint", "") or "v1" in model.get("endpoint", ""):
                    output = self._call_openai_compatible(model["endpoint"], model["model_id"], model["api_key"], system_prompt, user_prompt)
                    return output, {
                        "provider": provider_id,
                        "model": model_id,
                        "status": "success",
                        "cascaded_from": errors
                    }

            except Exception as e:
                err_msg = f"{provider_id}:{model_id} error: {str(e)}"
                errors.append(err_msg)
                # Mark model in cooldown
                self.mark_cooldown(provider_id, model_id, model.get("cooldown_seconds", 60))
                continue

        # If all failed, use deterministic mock generator
        fallback_output = self._call_mock(system_prompt, user_prompt)
        return fallback_output, {
            "provider": "mock-emergency-fallback",
            "model": "mock-glass-generator-v1",
            "status": "fallback",
            "cascaded_from": errors
        }

    def _call_gemini(self, endpoint: str, model_id: str, api_key: str, system_prompt: str, user_prompt: str) -> str:
        url = f"{endpoint}/{model_id}:generateContent?key={api_key}"
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096,
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_openai_compatible(self, endpoint: str, model_id: str, api_key: str, system_prompt: str, user_prompt: str) -> str:
        url = endpoint
        if not url.endswith("/chat/completions"):
            url = url.rstrip("/") + "/chat/completions"

        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    def _call_mock(self, system_prompt: str, user_prompt: str) -> str:
        """Deterministic offline mock generator for testing & CI without live keys."""
        title_match = re.search(r"Title:\s*([^\n\r]+)", user_prompt)
        slug_match = re.search(r"Slug:\s*([^\n\r]+)", user_prompt)
        cat_match = re.search(r"Category:\s*([^\n\r]+)", user_prompt)

        title = title_match.group(1).strip() if title_match else "Glass Dynamic Widget"
        slug = slug_match.group(1).strip() if slug_match else re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        category = cat_match.group(1).strip().lower() if cat_match else "other"

        # Adaptive layout depending on category (scenery/dashboard vs single widget)
        is_scenery = category in ["scenery", "dashboards"]
        canvas_style = "display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;width:100%;max-width:720px;" if is_scenery else "display:flex;align-items:center;justify-content:center;"

        if category == "navigation":
            widget_html = f"""
            <nav class="glass-widget-box" aria-label="{title}">
                <span class="glass-pill-icon"><i data-lucide="compass"></i></span>
                <span class="glass-pill-text">{title}</span>
                <span style="color:rgba(255,255,255,0.25);">/</span>
                <span style="color:var(--accent-cyan,#06B6D4);font-size:13px;">Active</span>
            </nav>"""
        elif category == "telemetry":
            widget_html = f"""
            <div class="glass-widget-box" role="status" aria-label="{title}">
                <span class="glass-pill-icon"><i data-lucide="gauge"></i></span>
                <span class="glass-pill-text">{title}</span>
                <div style="width:60px;height:6px;background:rgba(255,255,255,0.1);border-radius:9999px;overflow:hidden;">
                    <div style="width:78%;height:100%;background:linear-gradient(90deg,#06B6D4,#3B82F6);"></div>
                </div>
                <span style="font-size:12px;font-weight:700;color:#22D3EE;">78%</span>
            </div>"""
        elif category == "sliders":
            widget_html = f"""
            <div class="glass-widget-box" style="flex-direction:column;align-items:stretch;width:280px;gap:10px;">
                <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600;">
                    <span>{title}</span>
                    <span id="slider-val" style="color:#22D3EE;">65%</span>
                </div>
                <input type="range" min="0" max="100" value="65" style="accent-color:#06B6D4;width:100%;cursor:pointer;" oninput="document.getElementById('slider-val').innerText = this.value + '%'">
            </div>"""
        elif is_scenery:
            widget_html = f"""
            <div class="glass-widget-box" style="flex-direction:column;align-items:flex-start;gap:8px;">
                <span style="font-size:11px;color:#9CA3AF;text-transform:uppercase;">Composite Card A</span>
                <div style="display:flex;align-items:center;gap:8px;font-weight:700;"><i data-lucide="layers" style="color:#06B6D4;"></i> {title}</div>
            </div>
            <div class="glass-widget-box" style="flex-direction:column;align-items:flex-start;gap:8px;">
                <span style="font-size:11px;color:#9CA3AF;text-transform:uppercase;">Telemetry Node B</span>
                <div style="display:flex;align-items:center;gap:8px;font-weight:700;"><i data-lucide="activity" style="color:#10B981;"></i> 99.8% Sync</div>
            </div>"""
        else:
            widget_html = f"""
            <button type="button" class="glass-widget-box" id="sample-widget-btn" aria-label="{title}">
                <span class="glass-pill-icon"><i data-lucide="sparkles"></i></span>
                <span class="glass-pill-text">{title}</span>
            </button>"""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Dark Glass</title>
    <link rel="stylesheet" href="../css.css">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        .component-canvas {{
            {canvas_style}
            min-height: 220px;
            padding: 24px;
            background: var(--bg-main, #030712);
            box-sizing: border-box;
        }}
        .glass-widget-box {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 12px 22px;
            background: var(--glass-surface-1, rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid var(--glass-border-specular, rgba(255, 255, 255, 0.12));
            border-radius: var(--radius-lg, 16px);
            color: var(--text-primary, #f9fafb);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: pointer;
            box-sizing: border-box;
        }}
        .glass-widget-box:hover {{
            transform: translateY(-2px);
            background: var(--glass-surface-2, rgba(255, 255, 255, 0.08));
            border-color: rgba(6, 182, 212, 0.45);
            box-shadow: 0 12px 36px rgba(6, 182, 212, 0.2);
        }}
        .glass-pill-icon {{
            color: var(--accent-cyan, #06b6d4);
            display: flex;
            align-items: center;
        }}
        .glass-pill-text {{
            font-family: var(--font-sans, system-ui);
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.01em;
        }}
        @media (prefers-reduced-motion: reduce) {{
            .glass-widget-box {{
                transition: none !important;
                transform: none !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="component-canvas">
        {widget_html}
    </div>

    <script id="component-manifest" type="application/json">
    {{
        "title": "{title}",
        "slug": "{slug}",
        "category": "{category}",
        "badge": "{'Organism' if is_scenery else 'Molecule'}",
        "variation": "aurora-gradient-glow",
        "tags": ["glass", "{category}", "interactive"]
    }}
    </script>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            if (window.lucide) window.lucide.createIcons();
            const btn = document.getElementById('sample-widget-btn');
            if (btn) {{
                btn.addEventListener('click', () => {{
                    btn.classList.toggle('active');
                }});
            }}
        }});
    </script>
</body>
</html>
"""
