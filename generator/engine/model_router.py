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
        """High-fidelity generator conforming strictly to STYLE_SPEC.md 5-layer Dark Glass architecture."""
        title_match = re.search(r"Title:\s*([^\n\r]+)", user_prompt)
        slug_match = re.search(r"Slug:\s*([^\n\r]+)", user_prompt)
        cat_match = re.search(r"Category:\s*([^\n\r]+)", user_prompt)

        title = title_match.group(1).strip() if title_match else "Glass Dynamic Widget"
        slug = slug_match.group(1).strip() if slug_match else re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        category = cat_match.group(1).strip().lower() if cat_match else "other"

        is_scenery = category in ["scenery", "dashboards"]
        container_width = "680px" if is_scenery else "440px"

        if category == "inputs":
            widget_inner = f"""
            <div class="widget-header">
                <span class="widget-eyebrow"><i data-lucide="terminal" style="width:14px;height:14px;"></i> Interactive Input</span>
                <span class="widget-badge active">Online</span>
            </div>
            <h2 class="widget-title">{title}</h2>
            <div class="glass-input-cluster">
                <i data-lucide="sparkles" class="input-icon"></i>
                <input type="text" class="glass-input-field" placeholder="Ketik direktif atau pencarian..." value="Specular aurora gradient" aria-label="{title}">
                <button type="button" class="glass-btn-primary" aria-label="Submit">
                    <i data-lucide="arrow-right"></i>
                </button>
            </div>
            """
        elif category == "sliders":
            widget_inner = f"""
            <div class="widget-header">
                <span class="widget-eyebrow"><i data-lucide="sliders" style="width:14px;height:14px;"></i> Precision Controller</span>
                <span class="widget-badge" id="slider-badge">74%</span>
            </div>
            <h2 class="widget-title">{title}</h2>
            <div style="display:flex;flex-direction:column;gap:12px;margin-top:8px;">
                <div style="display:flex;justify-content:space-between;font-size:12px;color:rgba(255,255,255,0.6);">
                    <span>Refraction Density</span>
                    <span id="slider-val" style="color:#60A5FA;font-weight:700;">74%</span>
                </div>
                <input type="range" min="0" max="100" value="74" class="glass-range-input" oninput="document.getElementById('slider-val').innerText = this.value + '%'; document.getElementById('slider-badge').innerText = this.value + '%'">
            </div>
            """
        elif category == "navigation":
            widget_inner = f"""
            <div class="widget-header">
                <span class="widget-eyebrow"><i data-lucide="compass" style="width:14px;height:14px;"></i> Breadcrumb &amp; Navigation</span>
                <span class="widget-badge active">Active Node</span>
            </div>
            <h2 class="widget-title">{title}</h2>
            <nav class="glass-nav-cluster" aria-label="{title}">
                <span class="nav-item"><i data-lucide="home" style="width:14px;height:14px;"></i> Home</span>
                <span class="nav-sep">/</span>
                <span class="nav-item">Components</span>
                <span class="nav-sep">/</span>
                <span class="nav-item active">{title}</span>
            </nav>
            """
        elif category == "telemetry":
            widget_inner = f"""
            <div class="widget-header">
                <span class="widget-eyebrow"><i data-lucide="activity" style="width:14px;height:14px;"></i> Live Telemetry Node</span>
                <span class="widget-badge active">99.98%</span>
            </div>
            <h2 class="widget-title">{title}</h2>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px;">
                <div class="sub-stat-box">
                    <span class="sub-stat-label">Throughput</span>
                    <span class="sub-stat-val">1.4 GB/s</span>
                </div>
                <div class="sub-stat-box">
                    <span class="sub-stat-label">Latency</span>
                    <span class="sub-stat-val" style="color:#34D399;">12 ms</span>
                </div>
            </div>
            """
        elif is_scenery:
            widget_inner = f"""
            <div class="widget-header">
                <span class="widget-eyebrow"><i data-lucide="layers" style="width:14px;height:14px;"></i> Workstation Scenery Viewport</span>
                <span class="widget-badge active">Composite</span>
            </div>
            <h2 class="widget-title">{title}</h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:10px;">
                <div class="sub-stat-box">
                    <span class="sub-stat-label"><i data-lucide="cpu" style="width:12px;height:12px;"></i> Core Compute</span>
                    <span class="sub-stat-val">3.8 GHz</span>
                </div>
                <div class="sub-stat-box">
                    <span class="sub-stat-label"><i data-lucide="database" style="width:12px;height:12px;"></i> Memory Mesh</span>
                    <span class="sub-stat-val" style="color:#60A5FA;">16.4 GB</span>
                </div>
                <div class="sub-stat-box">
                    <span class="sub-stat-label"><i data-lucide="shield-check" style="width:12px;height:12px;"></i> Security Layer</span>
                    <span class="sub-stat-val" style="color:#34D399;">Shielded</span>
                </div>
            </div>
            """
        else:
            widget_inner = f"""
            <div class="widget-header">
                <span class="widget-eyebrow"><i data-lucide="sparkles" style="width:14px;height:14px;"></i> Creative UI Molecule</span>
                <span class="widget-badge active">Ready</span>
            </div>
            <h2 class="widget-title">{title}</h2>
            <div style="display:flex;align-items:center;gap:12px;margin-top:8px;">
                <button type="button" class="glass-btn-primary" id="btn-action">
                    <i data-lucide="zap"></i> Trigger Action
                </button>
                <button type="button" class="glass-btn-secondary">
                    <i data-lucide="sliders"></i> Configure
                </button>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Glass Dark Premium</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css.css">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --bg-page: #0A0A0A;
            --glass-card: rgba(255, 255, 255, 0.06);
            --glass-border-top: rgba(255, 255, 255, 0.22);
            --glass-border-side: rgba(255, 255, 255, 0.10);
            --glass-border-bottom: rgba(255, 255, 255, 0.04);
            --text-primary: #FFFFFF;
            --text-secondary: rgba(255, 255, 255, 0.65);
            --aurora-1: rgba(70, 110, 220, 0.65);
            --aurora-2: rgba(40, 60, 160, 0.55);
            --aurora-3: rgba(140, 70, 230, 0.45);
            --ease-spring: cubic-bezier(0.32, 0.72, 0, 1);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background: var(--bg-page);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}

        /* 5-LAYER GLASS CARD ARCHITECTURE (from STYLE_SPEC.md) */
        .glass-card-wrapper {{
            position: relative;
            width: 100%;
            max-width: {container_width};
            transition: transform 0.3s var(--ease-spring);
        }}

        .glass-card-wrapper:hover {{
            transform: translateY(-4px);
        }}

        /* Layer 4: 3D Shadow Card */
        .layer-4-shadow {{
            position: absolute;
            top: 12px; left: 0; right: 0; bottom: -12px;
            background: rgba(25, 45, 110, 0.5);
            border-radius: 32px;
            filter: blur(30px);
            transform: scale(0.96) translateY(12px);
            z-index: -2;
            transition: all 0.4s var(--ease-spring);
        }}

        .glass-card-wrapper:hover .layer-4-shadow {{
            transform: scale(0.98) translateY(16px);
            filter: blur(40px);
        }}

        /* Layer 3: Aurora Mesh Gradient */
        .layer-3-aurora {{
            position: absolute;
            inset: 0;
            border-radius: 28px;
            overflow: hidden;
            z-index: -1;
            contain: layout style paint;
        }}

        .aurora-blob {{
            position: absolute;
            filter: blur(40px);
            animation: auroraMorph 10s infinite alternate ease-in-out;
        }}

        .blob-1 {{ top: -10%; left: -10%; width: 70%; height: 70%; background: radial-gradient(circle, var(--aurora-1) 0%, transparent 70%); }}
        .blob-2 {{ bottom: -20%; right: -10%; width: 80%; height: 80%; background: radial-gradient(circle, var(--aurora-2) 0%, transparent 60%); animation-delay: -3s; }}
        .blob-3 {{ top: 10%; right: 20%; width: 60%; height: 60%; background: radial-gradient(circle, var(--aurora-3) 0%, transparent 60%); animation-delay: -6s; }}

        @keyframes auroraMorph {{
            0% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: translate(0, 0) scale(1); }}
            50% {{ transform: translate(5%, 10%) scale(1.05); }}
            100% {{ border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; transform: translate(-5%, -5%) scale(0.95); }}
        }}

        /* Layer 2: Main Glass Card with Asymmetric Borders */
        .layer-2-glass {{
            position: relative;
            width: 100%;
            padding: 24px 28px;
            background: var(--glass-card);
            backdrop-filter: blur(30px) saturate(160%);
            -webkit-backdrop-filter: blur(30px) saturate(160%);
            border-radius: 28px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.08);
            border: 1px solid transparent;
            border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side);
            border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            overflow: hidden;
            z-index: 1;
        }}

        /* Layer 1: Noise Texture Overlay */
        .layer-2-glass::before {{
            content: "";
            position: absolute;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
            opacity: 0.04;
            mix-blend-mode: overlay;
            pointer-events: none;
            z-index: 0;
        }}

        /* Layer 0: Content Elements */
        .widget-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }}

        .widget-eyebrow {{
            font-size: 11.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .widget-badge {{
            padding: 3px 9px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.08);
            color: #E5E7EB;
        }}

        .widget-badge.active {{
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .widget-title {{
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.01em;
            color: var(--text-primary);
            margin-bottom: 12px;
        }}

        /* Specific Widgets */
        .glass-input-cluster {{
            position: relative;
            display: flex;
            align-items: center;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            padding: 4px 6px 4px 14px;
            gap: 8px;
        }}

        .glass-input-field {{
            flex: 1;
            background: transparent;
            border: none;
            color: #FFFFFF;
            font-size: 13.5px;
            outline: none;
        }}

        .input-icon {{
            color: #60A5FA;
            width: 16px;
            height: 16px;
        }}

        .glass-btn-primary {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 18px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            background: linear-gradient(135deg, #4A7BF7 0%, #2E5FD9 100%);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #FFFFFF;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.35);
            transition: all 0.2s var(--ease-spring);
        }}

        .glass-btn-primary:hover {{
            filter: brightness(1.15);
            transform: translateY(-1px);
        }}

        .glass-btn-secondary {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 16px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #E5E7EB;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .glass-btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
        }}

        .glass-range-input {{
            width: 100%;
            accent-color: #3B82F6;
            cursor: pointer;
        }}

        .glass-nav-cluster {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .nav-item {{ cursor: pointer; transition: color 0.15s; display: inline-flex; align-items: center; gap: 5px; }}
        .nav-item:hover {{ color: #FFFFFF; }}
        .nav-item.active {{ color: #60A5FA; font-weight: 600; }}
        .nav-sep {{ color: rgba(255, 255, 255, 0.2); }}

        .sub-stat-box {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .sub-stat-label {{
            font-size: 11px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .sub-stat-val {{
            font-size: 16px;
            font-weight: 700;
            color: #FFFFFF;
        }}

        @media (prefers-reduced-motion: reduce) {{
            .aurora-blob, .glass-card-wrapper {{
                animation: none !important;
                transition: none !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="glass-card-wrapper">
        <div class="layer-4-shadow"></div>
        <div class="layer-3-aurora">
            <div class="aurora-blob blob-1"></div>
            <div class="aurora-blob blob-2"></div>
            <div class="aurora-blob blob-3"></div>
        </div>
        <div class="layer-2-glass">
            {widget_inner}
        </div>
    </div>

    <script id="component-manifest" type="application/json">
    {{
        "title": "{title}",
        "slug": "{slug}",
        "category": "{category}",
        "badge": "{'Organism' if is_scenery else 'Molecule'}",
        "variation": "aurora-gradient-glow",
        "tags": ["glass", "{category}", "interactive", "specular-depth"]
    }}
    </script>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            if (window.lucide) window.lucide.createIcons();
            const btn = document.getElementById('btn-action');
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

