import os
import json

ROOT = r"d:\PROJECT\prototype"
GLASS_DIR = os.path.join(ROOT, "ui", "components", "glass")
RAW_DIR = os.path.join(ROOT, "ui", "components", "raw")
PROJECT_DIR = os.path.join(ROOT, "projects", "file-manager")

def safe_json_embed(data):
    s = json.dumps(data, ensure_ascii=False)
    # Valid RFC 8259 JSON escape for solidus: prevents any </script from breaking HTML parser
    return s.replace("</", "<\\/")

# ----------------------------------------------------------------------
# 1. BUILD GLASS SHOWCASE (ui/components/glass/showcase.html)
# ----------------------------------------------------------------------
print("1/4. Building Glass Showcase...")
with open(os.path.join(GLASS_DIR, "css.css"), "r", encoding="utf-8") as f:
    shared_css_code = f.read()

glass_components_metadata = [
    ("button-glass", "Glass Buttons Collection", "Action / Buttons", "Molecule", "inputs", False),
    ("chat-input-bar", "Glass Chat Input Bar", "Form Input / AI Prompt", "Molecule", "inputs", False),
    ("input-field-glass", "Glass Form Input Fields", "Form / Inputs", "Molecule", "inputs", False),
    ("prompt-pills-row", "Prompt Pills Quick Scroller", "Chips / Action Pills", "Molecule", "inputs", False),
    ("thinking-effort-selector", "Thinking Effort Selector", "Segmented Stepper", "Atomic", "inputs", False),
    ("toggle-switch-glass", "Glass Toggle Switch", "Control / Switch", "Atomic", "inputs", False),
    ("checkbox-glass", "Glass Checkbox & Radio", "Control / Checkbox", "Atomic", "inputs", False),
    ("dropdown-select-glass", "Glass Floating Dropdown", "Control / Select", "Molecule", "inputs", False),
    ("ai-model-selector", "AI Model Selector Card", "Selection Control", "Molecule", "cards", False),
    ("frosted-folder-card", "Frosted Folder Card", "File System / Card", "Molecule", "cards", False),
    ("aurora-storage-card", "Aurora Storage Card", "Data Display / Gauge", "Molecule", "cards", False),
    ("progress-bar-glass", "Glass Glowing Progress Bar", "Display / Progress", "Atomic", "cards", False),
    ("avatar-badge-glass", "Glass Avatar with Status", "Display / Avatar", "Atomic", "cards", False),
    ("glass-dock-navigation", "Floating Glass Dock", "Navigation / Spring Dock", "Molecule", "navigation", False),
    ("glass-sidepanel", "Productivity Glass Sidepanel", "Navigation / Desktop Drawer", "Organism", "navigation", True),
    ("swirl-bottom-sheet", "Swirl Refraction Bottom Sheet", "Overlay / Canvas 2D Refraction", "Organism", "overlays", True),
    ("modal-dialog-glass", "Glass Modal Dialog", "Overlay / Centered Dialog", "Molecule", "overlays", False),
    ("toast-notification-glass", "Glass Toast Notification", "Feedback / Toast Alert", "Molecule", "overlays", False),
    ("tooltip-glass", "Glass Micro Tooltip", "Feedback / Tooltip", "Atomic", "overlays", False),
    ("telemetry-activity-chart", "Telemetry Activity Chart", "Analytics / Bar Histogram", "Molecule", "telemetry", False),
    ("ai-agent-scenery", "AI Agent Studio Scenery", "Complete Workspace Scenery", "Scenery", "scenery", True)
]

glass_files_db = {"css.css": shared_css_code}
glass_cards_html = ""

for folder, title, cat, badge, filter_cat, is_tall in glass_components_metadata:
    folder_path = os.path.join(GLASS_DIR, folder)
    glass_files_db[folder] = {}
    
    aio_file = f"{folder}.html"
    aio_path = os.path.join(folder_path, aio_file)
    if os.path.exists(aio_path):
        with open(aio_path, "r", encoding="utf-8") as f:
            glass_files_db[folder][aio_file] = f.read()
    
    idx_path = os.path.join(folder_path, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            glass_files_db[folder]["index.html"] = f.read()
            
    css_path = os.path.join(folder_path, "index.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            glass_files_db[folder]["index.css"] = f.read()
            
    js_path = os.path.join(folder_path, "index.js")
    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as f:
            glass_files_db[folder]["index.js"] = f.read()

    tall_class = " tall" if is_tall else ""
    badge_class = "badge-type scenery" if badge == "Scenery" else "badge-type"
    card_id = f"card-{folder}"
    
    glass_cards_html += f"""
            <!-- Component: {title} -->
            <article class="component-card" data-cat="{filter_cat}" id="{card_id}">
                <div class="card-top">
                    <div class="card-meta-left">
                        <div class="card-name">{title}</div>
                        <div class="card-category">{cat}</div>
                    </div>
                    <span class="{badge_class}">{badge}</span>
                </div>
                <div class="card-resizer-toolbar">
                    <div class="viewport-presets">
                        <button class="btn-preset active" onclick="setCardWidth('{card_id}', '100%', this)">
                            <i data-lucide="maximize-2"></i> Full
                        </button>
                        <button class="btn-preset" onclick="setCardWidth('{card_id}', '640px', this)">
                            <i data-lucide="tablet"></i> 640px
                        </button>
                        <button class="btn-preset" onclick="setCardWidth('{card_id}', '375px', this)">
                            <i data-lucide="smartphone"></i> 375px
                        </button>
                    </div>
                    <div class="toolbar-right">
                        <button class="btn-action-tool" onclick="openComponentModal('{folder}', '{title}')">
                            <i data-lucide="code"></i> Kode Sumber
                        </button>
                        <button class="btn-action-tool highlight" onclick="quickCopyAllInOne('{folder}')" title="Salin kode file mandiri">
                            <i data-lucide="copy"></i> Salin
                        </button>
                    </div>
                </div>
                <div class="card-preview-zone{tall_class}">
                    <div class="preview-resizer-wrapper">
                        <iframe src="{folder}/{aio_file}" title="{title} Preview"></iframe>
                    </div>
                </div>
                <div class="card-bottom">
                    <span class="file-link-tag">ui/components/glass/{folder}/</span>
                    <a href="{folder}/{aio_file}" target="_blank" class="btn-view-solo" title="Buka file standalone all-in-one di tab baru">
                        <i data-lucide="external-link"></i> Solo File
                    </a>
                </div>
            </article>
"""

glass_escaped_json = safe_json_embed(glass_files_db)

glass_showcase_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glass Dark Premium Showroom — 21 All-in-One Components</title>
    <meta name="description" content="Koleksi 21 Komponen UI/UX Glass Dark Premium all-in-one mandiri dengan resize preview, multi-file code tabs, dan copy instant.">
    <link rel="icon" type="image/svg+xml" href="../../../favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --bg-page: #08080C;
            --glass-card: rgba(255, 255, 255, 0.05);
            --glass-card-hover: rgba(255, 255, 255, 0.08);
            --glass-border-top: rgba(255, 255, 255, 0.24);
            --glass-border-side: rgba(255, 255, 255, 0.10);
            --glass-border-bottom: rgba(255, 255, 255, 0.04);
            --text-primary: #FFFFFF;
            --text-secondary: rgba(255, 255, 255, 0.65);
            --text-muted: rgba(255, 255, 255, 0.38);
            --accent-cyan: #4A9EFF;
            --accent-blue: #3B82F6;
            --accent-purple: #8B5CF6;
            --ease-spring: cubic-bezier(0.34, 1.15, 0.64, 1);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background-color: var(--bg-page);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            position: relative;
        }}

        .ambient-mesh {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            pointer-events: none; z-index: 0; overflow: hidden;
        }}

        .blob {{
            position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.32;
            animation: float 22s infinite alternate ease-in-out;
        }}

        .blob-1 {{ width: 520px; height: 520px; background: radial-gradient(circle, #3B82F6 0%, transparent 70%); top: -150px; left: -120px; }}
        .blob-2 {{ width: 560px; height: 560px; background: radial-gradient(circle, #8B5CF6 0%, transparent 70%); top: 30%; right: -150px; animation-delay: -6s; }}
        .blob-3 {{ width: 480px; height: 480px; background: radial-gradient(circle, #06B6D4 0%, transparent 70%); bottom: -120px; left: 20%; animation-delay: -12s; }}

        @keyframes float {{
            0% {{ transform: translate(0, 0) scale(1); }}
            100% {{ transform: translate(60px, 40px) scale(1.08); }}
        }}

        /* Header Bar */
        .showcase-header {{
            position: sticky; top: 0; z-index: 50; padding: 14px 32px;
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(8, 8, 12, 0.75); display: flex; align-items: center; justify-content: space-between;
        }}

        .brand-cluster {{ display: flex; align-items: center; gap: 12px; }}

        .brand-badge {{
            width: 40px; height: 40px; border-radius: 12px;
            background: linear-gradient(135deg, rgba(74, 158, 255, 0.3), rgba(139, 92, 246, 0.3));
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
        }}
        .brand-badge svg {{ width: 22px; height: 22px; stroke-width: 1.5px; color: #FFFFFF; }}

        .brand-text h1 {{ font-size: 18px; font-weight: 700; letter-spacing: -0.02em; }}
        .brand-text h1 span {{ color: var(--accent-cyan); }}
        .brand-text p {{ font-size: 12px; color: var(--text-secondary); margin-top: 1px; }}

        .header-actions {{ display: flex; align-items: center; gap: 10px; }}

        .btn-top-link {{
            display: inline-flex; align-items: center; gap: 7px; padding: 8px 14px;
            border-radius: 10px; font-size: 12.5px; font-weight: 500; text-decoration: none;
            color: var(--text-secondary); background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08); transition: all 0.2s;
        }}
        .btn-top-link:hover {{ background: rgba(255, 255, 255, 0.09); color: #FFFFFF; border-color: rgba(255, 255, 255, 0.18); }}

        .btn-highlight-webapp {{
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(59, 130, 246, 0.25));
            border-color: rgba(6, 182, 212, 0.4); color: #67E8F9; font-weight: 600;
        }}
        .btn-highlight-webapp:hover {{
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.28), rgba(59, 130, 246, 0.4));
            color: #FFFFFF; border-color: rgba(6, 182, 212, 0.6);
        }}

        /* App Banner */
        .app-highlight-banner {{
            margin: 24px 32px 0; padding: 18px 24px; border-radius: 16px;
            background: linear-gradient(90deg, rgba(6, 182, 212, 0.12), rgba(59, 130, 246, 0.12));
            border: 1px solid rgba(6, 182, 212, 0.3);
            display: flex; align-items: center; justify-content: space-between; gap: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }}
        .banner-info {{ display: flex; align-items: center; gap: 14px; }}
        .banner-icon-badge {{
            width: 44px; height: 44px; border-radius: 12px; background: rgba(6, 182, 212, 0.2);
            border: 1px solid rgba(6, 182, 212, 0.4); display: flex; align-items: center; justify-content: center;
            color: #22D3EE; flex-shrink: 0;
        }}
        .banner-text h3 {{ font-size: 15px; font-weight: 600; color: #FFFFFF; }}
        .banner-text p {{ font-size: 12.5px; color: var(--text-secondary); margin-top: 2px; }}

        .btn-banner-cta {{
            display: inline-flex; align-items: center; gap: 8px; padding: 9px 18px;
            border-radius: 10px; font-size: 13px; font-weight: 600; text-decoration: none;
            background: linear-gradient(135deg, #06B6D4, #3B82F6); color: #FFFFFF;
            box-shadow: 0 4px 14px rgba(6, 182, 212, 0.35); transition: transform 0.2s; white-space: nowrap;
        }}
        .btn-banner-cta:hover {{ transform: scale(1.02); }}

        /* Filter Controls */
        .controls-bar {{
            padding: 20px 32px 10px; display: flex; align-items: center; justify-content: space-between;
            gap: 16px; flex-wrap: wrap; z-index: 10;
        }}
        .filter-tabs {{
            display: flex; align-items: center; gap: 6px; padding: 4px;
            background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
        }}
        .filter-tab {{
            padding: 6px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 500;
            background: transparent; border: none; color: var(--text-muted); cursor: pointer;
            transition: all 0.2s;
        }}
        .filter-tab:hover {{ color: var(--text-primary); }}
        .filter-tab.active {{ background: rgba(255, 255, 255, 0.12); color: #FFFFFF; font-weight: 600; }}

        .search-box {{
            display: flex; align-items: center; gap: 10px; padding: 8px 14px;
            border-radius: 12px; background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08); width: 260px;
        }}
        .search-box svg {{ color: var(--text-muted); width: 16px; height: 16px; }}
        .search-box input {{
            background: transparent; border: none; outline: none; font-size: 13px;
            color: #FFFFFF; width: 100%; font-family: inherit;
        }}

        /* Grid */
        .showcase-grid {{
            padding: 16px 32px 64px; display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 24px; z-index: 5;
        }}

        /* Component Card */
        .component-card {{
            position: relative; background: var(--glass-card); border-radius: 20px;
            border: 1px solid transparent; border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side); border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            display: flex; flex-direction: column; overflow: hidden;
            transition: border-color 0.25s, box-shadow 0.25s;
        }}
        .component-card:hover {{
            background: var(--glass-card-hover);
            border-top-color: rgba(255, 255, 255, 0.35);
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        }}

        .card-top {{
            padding: 14px 18px 12px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06); background: rgba(255, 255, 255, 0.02);
        }}
        .card-name {{ font-size: 14.5px; font-weight: 600; letter-spacing: -0.01em; }}
        .card-category {{ font-size: 11.5px; color: var(--text-muted); margin-top: 2px; }}

        .badge-type {{
            font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 6px;
            background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3);
        }}
        .badge-type.scenery {{
            background: rgba(139, 92, 246, 0.15); color: #C084FC; border-color: rgba(139, 92, 246, 0.3);
        }}

        .card-resizer-toolbar {{
            padding: 8px 18px; display: flex; align-items: center; justify-content: space-between;
            background: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }}
        .viewport-presets {{ display: flex; align-items: center; gap: 4px; }}
        .btn-preset {{
            padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 500;
            background: transparent; border: 1px solid rgba(255, 255, 255, 0.06);
            color: var(--text-muted); cursor: pointer; display: flex; align-items: center; gap: 4px;
            transition: all 0.15s;
        }}
        .btn-preset svg {{ width: 12px; height: 12px; }}
        .btn-preset:hover {{ color: var(--text-primary); border-color: rgba(255, 255, 255, 0.15); }}
        .btn-preset.active {{
            background: rgba(255, 255, 255, 0.1); color: #FFFFFF;
            border-color: rgba(255, 255, 255, 0.2); font-weight: 600;
        }}

        .toolbar-right {{ display: flex; align-items: center; gap: 6px; }}
        .btn-action-tool {{
            padding: 4px 10px; border-radius: 6px; font-size: 11.5px; font-weight: 500;
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; gap: 5px;
            transition: all 0.2s;
        }}
        .btn-action-tool svg {{ width: 12px; height: 12px; }}
        .btn-action-tool:hover {{ background: rgba(255, 255, 255, 0.12); color: #FFFFFF; }}
        .btn-action-tool.highlight {{
            background: rgba(74, 158, 255, 0.15); border-color: rgba(74, 158, 255, 0.35); color: #93C5FD;
        }}
        .btn-action-tool.highlight:hover {{
            background: rgba(74, 158, 255, 0.25); color: #FFFFFF;
        }}

        .card-preview-zone {{
            height: 380px; width: 100%; display: flex; align-items: center; justify-content: center;
            background: #050508; position: relative; overflow: hidden; padding: 12px;
        }}
        .card-preview-zone.tall {{ height: 560px; }}

        .preview-resizer-wrapper {{
            width: 100%; height: 100%; transition: max-width 0.35s var(--ease-spring);
            display: flex; align-items: center; justify-content: center; margin: 0 auto;
        }}

        .preview-resizer-wrapper iframe {{
            width: 100%; height: 100%; border: none; border-radius: 12px; background: #07070A;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        }}

        .card-bottom {{
            padding: 10px 18px; display: flex; align-items: center; justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.05); background: rgba(255, 255, 255, 0.015);
            font-size: 11.5px;
        }}
        .file-link-tag {{ font-family: 'JetBrains Mono', monospace; color: var(--text-muted); }}

        .btn-view-solo {{
            color: var(--accent-cyan); text-decoration: none; display: flex; align-items: center; gap: 4px;
            font-weight: 500; transition: color 0.15s;
        }}
        .btn-view-solo:hover {{ text-decoration: underline; color: #FFFFFF; }}
        .btn-view-solo svg {{ width: 12px; height: 12px; }}

        /* Modal Code Inspection */
        .modal-overlay {{
            position: fixed; inset: 0; z-index: 1000; background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            display: none; align-items: center; justify-content: center; padding: 24px;
        }}
        .modal-overlay.active {{ display: flex; }}

        .modal-card {{
            width: 100%; max-width: 900px; height: 82vh; background: #0A0A10; border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 24px 64px rgba(0, 0, 0, 0.8);
            display: flex; flex-direction: column; overflow: hidden;
        }}

        .modal-header {{
            padding: 16px 24px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: #12121A;
        }}
        .modal-title-wrap h3 {{ font-size: 16px; font-weight: 600; }}
        .modal-title-wrap p {{ font-size: 12px; color: var(--text-secondary); margin-top: 2px; }}

        .modal-header-actions {{ display: flex; align-items: center; gap: 10px; }}

        .modal-close-btn {{
            width: 34px; height: 34px; border-radius: 50%; background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12); color: var(--text-secondary); cursor: pointer;
            display: flex; align-items: center; justify-content: center; transition: all 0.2s;
        }}
        .modal-close-btn:hover {{ background: rgba(255, 255, 255, 0.15); color: #FFFFFF; }}

        /* Top Bar Tabs */
        .modal-tabs-bar {{
            display: flex; align-items: center; gap: 4px; padding: 8px 16px 0;
            background: #0B0B10; border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            overflow-x: auto; scrollbar-width: none;
        }}
        .modal-tabs-bar::-webkit-scrollbar {{ display: none; }}

        .code-tab-btn {{
            padding: 8px 16px; border-radius: 10px 10px 0 0;
            background: transparent; border: 1px solid transparent; border-bottom: none;
            color: var(--text-muted); font-size: 12.5px; font-family: 'JetBrains Mono', monospace;
            cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s;
            white-space: nowrap; position: relative; top: 1px;
        }}
        .code-tab-btn:hover {{ color: var(--text-primary); background: rgba(255, 255, 255, 0.03); }}
        .code-tab-btn.active {{
            background: #08080C; border-color: rgba(255, 255, 255, 0.12);
            color: #FFFFFF; font-weight: 600;
        }}
        .code-tab-btn.active::after {{
            content: ""; position: absolute; top: -1px; left: 0; right: 0; height: 2px;
            background: var(--accent-cyan); border-radius: 2px 2px 0 0;
        }}

        .tab-badge {{
            font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 6px;
            text-transform: uppercase; letter-spacing: 0.04em;
        }}
        .badge-aio {{ background: rgba(245, 158, 11, 0.18); color: #FBBF24; }}
        .badge-html {{ background: rgba(59, 130, 246, 0.18); color: #60A5FA; }}
        .badge-css {{ background: rgba(139, 92, 246, 0.18); color: #C084FC; }}
        .badge-js {{ background: rgba(234, 179, 8, 0.18); color: #FACC15; }}
        .badge-tokens {{ background: rgba(6, 182, 212, 0.18); color: #22D3EE; }}

        .modal-tab-subbar {{
            padding: 8px 24px; background: #08080C; border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: var(--text-muted);
        }}
        .subbar-file-path {{ font-family: 'JetBrains Mono', monospace; color: var(--accent-cyan); }}

        .modal-body {{
            flex: 1; overflow: auto; padding: 20px 24px; background: #08080C;
        }}
        .code-pre {{
            margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 12.5px;
            line-height: 1.6; color: #D1D5DB; white-space: pre-wrap; word-break: break-all;
        }}

        /* Toast */
        .toast-notification {{
            position: fixed; bottom: 32px; right: 32px; z-index: 2000;
            padding: 12px 20px; border-radius: 12px; background: #1E293B;
            border: 1px solid rgba(255, 255, 255, 0.15); color: #FFFFFF; font-size: 13.5px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5); display: flex; align-items: center; gap: 10px;
            transform: translateY(80px); opacity: 0; pointer-events: none;
            transition: all 0.3s var(--ease-spring);
        }}
        .toast-notification.active {{ transform: translateY(0); opacity: 1; }}
        .toast-notification svg {{ color: #4ADE80; width: 18px; height: 18px; }}

        @media (max-width: 768px) {{
            .showcase-header {{ padding: 12px 18px; }}
            .app-highlight-banner {{ margin: 16px 18px 0; flex-direction: column; align-items: flex-start; }}
            .controls-bar {{ padding: 16px 18px 8px; }}
            .showcase-grid {{ padding: 12px 18px 48px; grid-template-columns: 1fr; }}
            .modal-card {{ height: 92vh; margin: 12px; }}
        }}
    </style>
</head>
<body>

    <div class="ambient-mesh">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>

    <header class="showcase-header">
        <div class="brand-cluster">
            <div class="brand-badge">
                <i data-lucide="gem"></i>
            </div>
            <div class="brand-text">
                <h1>Glass<span>OS</span> Style Showroom</h1>
                <p>21 Komponen Glass Dark Premium All-in-One Mandiri</p>
            </div>
        </div>

        <div class="header-actions">
            <a href="../../../index.html" class="btn-top-link" title="Master Gateway Portal">
                <i data-lucide="home"></i> Gateway
            </a>
            <a href="../../../showcase.html" class="btn-top-link" title="Master Component Hub">
                <i data-lucide="layers"></i> Master Hub
            </a>
            <a href="../../../web-apps.html" class="btn-top-link btn-highlight-webapp" title="Buka Halaman Khusus Web Applications">
                <i data-lucide="folder-kanban"></i> Web Applications Studio
            </a>
            <a href="../raw/showcase.html" class="btn-top-link" title="Buka Showcase Raw HTML">
                <i data-lucide="code-2"></i> Raw HTML (9)
            </a>
        </div>
    </header>

    <!-- Web App Banner -->
    <div class="app-highlight-banner">
        <div class="banner-info">
            <div class="banner-icon-badge">
                <i data-lucide="cloud"></i>
            </div>
            <div class="banner-text">
                <h3>Sedang Mencari Aplikasi Web Jadi (Project Scenery)?</h3>
                <p>Proyek komposit utuh (seperti <strong>Cloud File Manager OS</strong>) telah dipisahkan ke halaman khusus Web Applications Studio agar tidak tercampur dengan komponen atom/molekul.</p>
            </div>
        </div>
        <a href="../../../web-apps.html" class="btn-banner-cta">
            <i data-lucide="folder-kanban"></i> Buka Web Applications Studio <i data-lucide="arrow-right"></i>
        </a>
    </div>

    <!-- Controls Bar -->
    <div class="controls-bar">
        <div class="filter-tabs">
            <button class="filter-tab active" onclick="filterCategory('all', this)">Semua (21)</button>
            <button class="filter-tab" onclick="filterCategory('inputs', this)">Inputs & Forms</button>
            <button class="filter-tab" onclick="filterCategory('cards', this)">Cards & Gauges</button>
            <button class="filter-tab" onclick="filterCategory('navigation', this)">Navigation</button>
            <button class="filter-tab" onclick="filterCategory('overlays', this)">Modals & Overlays</button>
            <button class="filter-tab" onclick="filterCategory('scenery', this)">Scenery (Full View)</button>
        </div>

        <div class="search-box">
            <i data-lucide="search"></i>
            <input type="text" id="searchInput" placeholder="Cari komponen glass..." oninput="handleSearch(this.value)">
        </div>
    </div>

    <!-- Main Grid -->
    <main class="showcase-grid" id="componentsGrid">
{glass_cards_html}
    </main>

    <!-- Code Modal -->
    <div class="modal-overlay" id="codeModal">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title-wrap">
                    <h3 id="modalComponentTitle">Glass Component Source</h3>
                    <p id="modalComponentPath">ui/components/glass/...</p>
                </div>
                <div class="modal-header-actions">
                    <button class="btn-action-tool highlight" onclick="copyCurrentModalCode()">
                        <i data-lucide="copy"></i> Salin File Ini
                    </button>
                    <button class="modal-close-btn" onclick="closeCodeModal()" title="Tutup Modal">
                        <i data-lucide="x"></i>
                    </button>
                </div>
            </div>

            <!-- Multi-file Tabs Bar -->
            <div class="modal-tabs-bar" id="modalTabsBar">
                <!-- Tabs dynamically rendered -->
            </div>

            <!-- Subbar details -->
            <div class="modal-tab-subbar">
                <span class="subbar-file-path" id="modalSubbarFilePath">...</span>
                <span id="modalSubbarStats">0 baris</span>
            </div>

            <div class="modal-body">
                <pre class="code-pre"><code id="modalCodeSnippet">Memuat kode...</code></pre>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div class="toast-notification" id="toast">
        <i data-lucide="check-circle-2"></i>
        <span id="toastMsg">Kode berhasil disalin ke clipboard!</span>
    </div>

    <!-- Data Island for Code Tabs -->
    <script type="application/json" id="glassData">
{glass_escaped_json}
    </script>

    <script>
        let COMP_DB = {{}};
        try {{
            const rawJson = document.getElementById('glassData').textContent;
            COMP_DB = JSON.parse(rawJson);
        }} catch(e) {{
            console.error('Failed to parse component database:', e);
        }}

        let activeFolder = "";
        let activeFile = "";

        lucide.createIcons();

        function filterCategory(cat, btn) {{
            document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
            btn.classList.add('active');

            const cards = document.querySelectorAll('.component-card');
            cards.forEach(card => {{
                if (cat === 'all' || card.dataset.cat === cat) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function handleSearch(query) {{
            query = query.toLowerCase().trim();
            const cards = document.querySelectorAll('.component-card');
            cards.forEach(card => {{
                const name = card.querySelector('.card-name').textContent.toLowerCase();
                const cat = card.querySelector('.card-category').textContent.toLowerCase();
                if (name.includes(query) || cat.includes(query)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function setCardWidth(cardId, width, btn) {{
            const card = document.getElementById(cardId);
            if (!card) return;
            card.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const wrapper = card.querySelector('.preview-resizer-wrapper');
            if (wrapper) wrapper.style.maxWidth = width;
        }}

        function openComponentModal(folder, title) {{
            activeFolder = folder;
            document.getElementById('modalComponentTitle').innerText = title;
            document.getElementById('modalComponentPath').innerText = `ui/components/glass/${{folder}}/`;

            const tabsBar = document.getElementById('modalTabsBar');
            tabsBar.innerHTML = '';

            const compFiles = COMP_DB[folder] || {{}};
            const aioFile = `${{folder}}.html`;
            const fileOrder = [aioFile, "index.html", "index.css", "index.js", "css.css"];

            let firstFile = null;

            fileOrder.forEach(fn => {{
                let fileCode = "";
                let badgeText = "";
                let badgeClass = "";

                if (fn === "css.css" && COMP_DB["css.css"]) {{
                    fileCode = COMP_DB["css.css"];
                    badgeText = "Shared Tokens";
                    badgeClass = "badge-tokens";
                }} else if (compFiles[fn] !== undefined) {{
                    fileCode = compFiles[fn];
                    if (fn === aioFile) {{
                        badgeText = "All-in-One";
                        badgeClass = "badge-aio";
                    }} else if (fn.endsWith('.html')) {{
                        badgeText = "HTML";
                        badgeClass = "badge-html";
                    }} else if (fn.endsWith('.css')) {{
                        badgeText = "CSS";
                        badgeClass = "badge-css";
                    }} else if (fn.endsWith('.js')) {{
                        badgeText = "JS";
                        badgeClass = "badge-js";
                    }}
                }}

                if (fileCode) {{
                    if (!firstFile) firstFile = fn;
                    const btn = document.createElement('button');
                    btn.className = "code-tab-btn";
                    btn.setAttribute('data-filename', fn);
                    btn.innerHTML = `<i data-lucide="${{getTabIcon(fn)}}"></i> ${{fn}} <span class="tab-badge ${{badgeClass}}">${{badgeText}}</span>`;
                    btn.onclick = () => switchCodeTab(fn);
                    tabsBar.appendChild(btn);
                }}
            }});

            document.getElementById('codeModal').classList.add('active');
            if (window.lucide) lucide.createIcons();

            if (firstFile) {{
                switchCodeTab(firstFile);
            }}
        }}

        function getTabIcon(fn) {{
            if (fn.endsWith('.html')) return 'file-code';
            if (fn.endsWith('.css')) return 'palette';
            if (fn.endsWith('.js')) return 'terminal';
            return 'file-text';
        }}

        function switchCodeTab(filename) {{
            activeFile = filename;
            document.querySelectorAll('.code-tab-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-filename') === filename);
            }});

            let code = "";
            if (filename === "css.css") {{
                code = COMP_DB["css.css"] || "";
                document.getElementById('modalSubbarFilePath').innerText = `ui/components/glass/css.css (Master Shared Tokens)`;
            }} else {{
                code = (COMP_DB[activeFolder] && COMP_DB[activeFolder][filename]) || "";
                document.getElementById('modalSubbarFilePath').innerText = `ui/components/glass/${{activeFolder}}/${{filename}}`;
            }}

            const lines = code ? code.split('\\n').length : 0;
            const kb = (new Blob([code]).size / 1024).toFixed(1);
            document.getElementById('modalSubbarStats').innerText = `${{lines}} baris (${{kb}} KB)`;

            document.getElementById('modalCodeSnippet').innerText = code;
        }}

        function closeCodeModal() {{
            document.getElementById('codeModal').classList.remove('active');
        }}

        async function copyCurrentModalCode() {{
            let code = "";
            if (activeFile === "css.css") {{
                code = COMP_DB["css.css"] || "";
            }} else {{
                code = (COMP_DB[activeFolder] && COMP_DB[activeFolder][activeFile]) || "";
            }}

            if (code) {{
                await navigator.clipboard.writeText(code);
                showToast(`File ${{activeFile}} berhasil disalin!`);
            }}
        }}

        async function quickCopyAllInOne(folder) {{
            const aioFile = `${{folder}}.html`;
            const code = (COMP_DB[folder] && COMP_DB[folder][aioFile]) || "";
            if (code) {{
                await navigator.clipboard.writeText(code);
                showToast(`Kode all-in-one ${{folder}} berhasil disalin!`);
            }} else {{
                showToast(`File all-in-one tidak ditemukan.`);
            }}
        }}

        function showToast(msg) {{
            const toast = document.getElementById('toast');
            document.getElementById('toastMsg').innerText = msg;
            toast.classList.add('active');
            setTimeout(() => toast.classList.remove('active'), 2500);
        }}

        document.getElementById('codeModal').addEventListener('click', (e) => {{
            if (e.target.id === 'codeModal') closeCodeModal();
        }});
    </script>
</body>
</html>
"""

with open(os.path.join(GLASS_DIR, "showcase.html"), "w", encoding="utf-8") as f:
    f.write(glass_showcase_content)

print("Glass showcase built successfully!")

# ----------------------------------------------------------------------
# 2. BUILD WEB APPS STUDIO (web-apps.html)
# ----------------------------------------------------------------------
print("2/4. Building Web Apps Studio (web-apps.html)...")
with open(os.path.join(PROJECT_DIR, "index.html"), "r", encoding="utf-8") as f:
    app_index_code = f.read()

with open(os.path.join(PROJECT_DIR, "PROJECT_SPEC.md"), "r", encoding="utf-8") as f:
    app_spec_code = f.read()

app_files_db = {
    "index.html": app_index_code,
    "PROJECT_SPEC.md": app_spec_code
}
app_escaped_json = safe_json_embed(app_files_db)

web_apps_html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GlassOS Web Applications Studio — Production Prototypes</title>
    <meta name="description" content="Showroom khusus Aplikasi Web Utuh (Ecosystem / Scenery level) berbasis tema Glass Dark Premium yang mengintegrasikan seluruh komponen UI/UX.">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --bg-page: #07070B;
            --glass-card: rgba(255, 255, 255, 0.05);
            --glass-card-hover: rgba(255, 255, 255, 0.08);
            --glass-border-top: rgba(255, 255, 255, 0.25);
            --glass-border-side: rgba(255, 255, 255, 0.10);
            --glass-border-bottom: rgba(255, 255, 255, 0.04);
            --text-primary: #FFFFFF;
            --text-secondary: rgba(255, 255, 255, 0.68);
            --text-muted: rgba(255, 255, 255, 0.40);
            --accent-cyan: #4A9EFF;
            --accent-blue: #3B82F6;
            --accent-purple: #8B5CF6;
            --ease-spring: cubic-bezier(0.34, 1.15, 0.64, 1);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background-color: var(--bg-page);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            position: relative;
        }}

        .ambient-mesh {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            pointer-events: none; z-index: 0; overflow: hidden;
        }}

        .blob {{
            position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.35;
            animation: float 24s infinite alternate ease-in-out;
        }}

        .blob-1 {{ width: 560px; height: 560px; background: radial-gradient(circle, #3B82F6 0%, transparent 70%); top: -180px; left: -140px; }}
        .blob-2 {{ width: 600px; height: 600px; background: radial-gradient(circle, #8B5CF6 0%, transparent 70%); top: 35%; right: -180px; animation-delay: -7s; }}
        .blob-3 {{ width: 500px; height: 500px; background: radial-gradient(circle, #06B6D4 0%, transparent 70%); bottom: -140px; left: 20%; animation-delay: -14s; }}

        @keyframes float {{
            0% {{ transform: translate(0, 0) scale(1); }}
            100% {{ transform: translate(70px, 45px) scale(1.08); }}
        }}

        /* Header Bar */
        .hub-header {{
            position: sticky; top: 0; z-index: 50; padding: 16px 32px;
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(7, 7, 11, 0.78); display: flex; align-items: center; justify-content: space-between;
        }}

        .brand-cluster {{ display: flex; align-items: center; gap: 12px; }}

        .brand-badge {{
            width: 42px; height: 42px; border-radius: 12px;
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            border: 1px solid rgba(255, 255, 255, 0.25);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
        }}
        .brand-badge svg {{ width: 22px; height: 22px; stroke-width: 1.5px; color: #FFFFFF; }}

        .brand-text h1 {{ font-size: 18px; font-weight: 700; letter-spacing: -0.02em; }}
        .brand-text h1 span {{ color: var(--accent-cyan); }}
        .brand-text p {{ font-size: 12px; color: var(--text-secondary); margin-top: 1px; }}

        .header-actions {{ display: flex; align-items: center; gap: 10px; }}

        .action-link-btn {{
            display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px;
            border-radius: 10px; font-size: 13px; font-weight: 500; text-decoration: none;
            color: var(--text-secondary); background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08); transition: all 0.2s;
        }}
        .action-link-btn:hover {{
            background: rgba(255, 255, 255, 0.09); color: #FFFFFF; border-color: rgba(255, 255, 255, 0.18);
        }}

        /* Main Hub */
        .hub-main {{
            flex: 1; padding: 32px; max-width: 1360px; margin: 0 auto; width: 100%; z-index: 5;
        }}

        /* Hero Banner */
        .hero-banner {{
            margin-bottom: 32px; text-align: center; max-width: 780px; margin-left: auto; margin-right: auto;
        }}
        .hero-tag {{
            display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px;
            border-radius: 20px; font-size: 11.5px; font-weight: 600; text-transform: uppercase;
            letter-spacing: 0.05em; background: rgba(59, 130, 246, 0.15); color: #60A5FA;
            border: 1px solid rgba(59, 130, 246, 0.3); margin-bottom: 12px;
        }}
        .hero-title {{
            font-size: 30px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 10px;
        }}
        .hero-desc {{
            font-size: 14.5px; line-height: 1.6; color: var(--text-secondary);
        }}

        /* Spotlight App Box */
        .app-showcase-box {{
            background: var(--glass-card); border-radius: 24px;
            border: 1px solid transparent; border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side); border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            padding: 24px; margin-bottom: 40px;
        }}

        .app-card-topbar {{
            display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;
            gap: 16px; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }}

        .app-meta-header {{ display: flex; align-items: center; gap: 14px; }}
        .app-icon-badge {{
            width: 48px; height: 48px; border-radius: 14px;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(6, 182, 212, 0.3));
            border: 1px solid rgba(59, 130, 246, 0.4); display: flex; align-items: center; justify-content: center;
            color: #38BDF8; box-shadow: 0 4px 16px rgba(56, 189, 248, 0.25);
        }}
        .app-icon-badge svg {{ width: 24px; height: 24px; }}

        .app-title-group h2 {{
            font-size: 19px; font-weight: 700; letter-spacing: -0.02em; display: flex; align-items: center; gap: 10px;
        }}
        .app-version-badge {{
            font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 6px;
            background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35);
        }}
        .app-title-group p {{ font-size: 13px; color: var(--text-secondary); margin-top: 3px; }}

        .app-controls-cluster {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}

        .viewport-selector {{
            display: flex; align-items: center; gap: 4px; padding: 4px;
            background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
        }}
        .vp-btn {{
            padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;
            background: transparent; border: none; color: var(--text-muted); cursor: pointer;
            display: flex; align-items: center; gap: 6px; transition: all 0.2s;
        }}
        .vp-btn svg {{ width: 14px; height: 14px; }}
        .vp-btn:hover {{ color: var(--text-primary); }}
        .vp-btn.active {{
            background: rgba(255, 255, 255, 0.12); color: #FFFFFF; font-weight: 600;
        }}

        .btn-tool-secondary {{
            padding: 7px 14px; border-radius: 10px; font-size: 12.5px; font-weight: 500;
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; gap: 6px;
            transition: all 0.2s;
        }}
        .btn-tool-secondary:hover {{
            background: rgba(255, 255, 255, 0.12); color: #FFFFFF;
        }}

        .btn-launch-primary {{
            padding: 8px 18px; border-radius: 10px; font-size: 13px; font-weight: 600;
            background: linear-gradient(135deg, #3B82F6, #2563EB); color: #FFFFFF; text-decoration: none;
            display: flex; align-items: center; gap: 7px; box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
            transition: transform 0.2s;
        }}
        .btn-launch-primary:hover {{ transform: scale(1.02); }}

        /* Live Preview Stage */
        .app-live-stage {{
            position: relative; width: 100%; height: 750px; background: #040407;
            border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.08);
            display: flex; align-items: center; justify-content: center; overflow: hidden;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
        }}

        .app-frame-wrapper {{
            width: 100%; height: 100%; transition: max-width 0.4s var(--ease-spring);
            margin: 0 auto; display: flex; align-items: center; justify-content: center;
        }}

        .app-frame-wrapper iframe {{
            width: 100%; height: 100%; border: none; border-radius: 14px;
        }}

        /* Architecture Section */
        .app-architecture-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px; margin-top: 24px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.06);
        }}

        .arch-col-title {{
            font-size: 14.5px; font-weight: 600; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
        }}
        .arch-desc {{ font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 12px; }}

        .components-pills-wrap {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .comp-link-pill {{
            display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px;
            border-radius: 8px; font-size: 12px; background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08); color: var(--text-secondary);
            text-decoration: none; transition: all 0.2s;
        }}
        .comp-link-pill:hover {{
            background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.3); color: #93C5FD;
        }}

        .spec-list {{ list-style: none; display: flex; flex-direction: column; gap: 8px; }}
        .spec-item {{
            display: flex; align-items: flex-start; gap: 10px; font-size: 12.5px; color: var(--text-secondary);
        }}
        .spec-item svg {{ width: 16px; height: 16px; color: #34D399; flex-shrink: 0; margin-top: 2px; }}

        /* Modal */
        .modal-overlay {{
            position: fixed; inset: 0; z-index: 1000; background: rgba(0, 0, 0, 0.78);
            backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
            display: none; align-items: center; justify-content: center; padding: 24px;
        }}
        .modal-overlay.active {{ display: flex; }}

        .modal-card {{
            width: 100%; max-width: 960px; height: 85vh; background: #09090F; border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 24px 64px rgba(0, 0, 0, 0.85);
            display: flex; flex-direction: column; overflow: hidden;
        }}

        .modal-header {{
            padding: 16px 24px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08); background: #111118;
        }}
        .modal-title-wrap h3 {{ font-size: 16px; font-weight: 600; }}
        .modal-title-wrap p {{ font-size: 12px; color: var(--text-secondary); margin-top: 2px; }}

        .modal-tabs-bar {{
            display: flex; align-items: center; gap: 4px; padding: 8px 16px 0;
            background: #0B0B10; border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .code-tab-btn {{
            padding: 8px 16px; border-radius: 10px 10px 0 0;
            background: transparent; border: 1px solid transparent; border-bottom: none;
            color: var(--text-muted); font-size: 12.5px; font-family: 'JetBrains Mono', monospace;
            cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s;
            position: relative; top: 1px;
        }}
        .code-tab-btn:hover {{ color: var(--text-primary); }}
        .code-tab-btn.active {{
            background: #08080C; border-color: rgba(255, 255, 255, 0.12);
            color: #FFFFFF; font-weight: 600;
        }}
        .code-tab-btn.active::after {{
            content: ""; position: absolute; top: -1px; left: 0; right: 0; height: 2px;
            background: var(--accent-cyan); border-radius: 2px 2px 0 0;
        }}

        .modal-tab-subbar {{
            padding: 8px 24px; background: #08080C; border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: var(--text-muted);
        }}
        .subbar-file-path {{ font-family: 'JetBrains Mono', monospace; color: var(--accent-cyan); }}

        .modal-body {{
            flex: 1; overflow: auto; padding: 20px 24px; background: #08080C;
        }}
        .code-pre {{
            margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 12px;
            line-height: 1.6; color: #D1D5DB; white-space: pre-wrap; word-break: break-all;
        }}

        .modal-close-btn {{
            width: 34px; height: 34px; border-radius: 50%; background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12); color: var(--text-secondary); cursor: pointer;
            display: flex; align-items: center; justify-content: center; transition: all 0.2s;
        }}
        .modal-close-btn:hover {{ background: rgba(255, 255, 255, 0.15); color: #FFFFFF; }}

        .toast-notification {{
            position: fixed; bottom: 32px; right: 32px; z-index: 2000;
            padding: 12px 20px; border-radius: 12px; background: #1E293B;
            border: 1px solid rgba(255, 255, 255, 0.15); color: #FFFFFF; font-size: 13.5px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5); display: flex; align-items: center; gap: 10px;
            transform: translateY(80px); opacity: 0; pointer-events: none;
            transition: all 0.3s var(--ease-spring);
        }}
        .toast-notification.active {{ transform: translateY(0); opacity: 1; }}
        .toast-notification svg {{ color: #4ADE80; width: 18px; height: 18px; }}
    </style>
</head>
<body>

    <div class="ambient-mesh">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>

    <header class="hub-header">
        <div class="brand-cluster">
            <div class="brand-badge">
                <i data-lucide="cloud"></i>
            </div>
            <div class="brand-text">
                <h1>Glass<span>OS</span> Web Applications Studio</h1>
                <p>Laboratorium Aplikasi Web Mandiri & Scenery Utuh</p>
            </div>
        </div>

        <div class="header-actions">
            <a href="index.html" class="action-link-btn" title="Master Gateway Portal">
                <i data-lucide="home"></i> Gateway
            </a>
            <a href="showcase.html" class="action-link-btn" title="Master Workbench Hub">
                <i data-lucide="layers"></i> Master Hub
            </a>
            <a href="ui/components/glass/showcase.html" class="action-link-btn" title="Koleksi Komponen Kaca">
                <i data-lucide="gem"></i> Glass Components (21)
            </a>
            <a href="projects/file-manager/index.html" target="_blank" class="action-link-btn" style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; border-color: rgba(59, 130, 246, 0.3);">
                <i data-lucide="external-link"></i> Launch Full Window
            </a>
        </div>
    </header>

    <main class="hub-main">

        <!-- Hero Banner -->
        <section class="hero-banner">
            <span class="hero-tag"><i data-lucide="sparkles"></i> Tingkat Sistem / Ecosystem Layer</span>
            <h2 class="hero-title">Aplikasi Web Interaktif Lengkap</h2>
            <p class="hero-desc">
                Halaman ini didedikasikan secara terpisah untuk <strong>Web Applications</strong> (proyek jadi utuh), bukan sekadar komponen terpisah (atom/molekul). Di sini Anda dapat menguji simulasi perangkat (Desktop, Tablet, Mobile), memeriksa integrasi arsitektur komponen, serta menjalankan aplikasi secara live.
            </p>
        </section>

        <!-- Project Spotlight Card: Cloud File Manager -->
        <section class="app-showcase-box" id="project-file-manager">
            
            <div class="app-card-topbar">
                <div class="app-meta-header">
                    <div class="app-icon-badge">
                        <i data-lucide="cloud"></i>
                    </div>
                    <div class="app-title-group">
                        <h2>
                            <span>GlassOS Cloud File Manager</span>
                            <span class="app-version-badge">v2.4 Production Ready</span>
                        </h2>
                        <p>Sistem Operasi Manajemen Berkas Awan & Produktivitas AI Berbasis Glass Dark Premium</p>
                    </div>
                </div>

                <div class="app-controls-cluster">
                    <div class="viewport-selector">
                        <button class="vp-btn active" onclick="setAppViewport('100%', this)">
                            <i data-lucide="monitor"></i> Desktop
                        </button>
                        <button class="vp-btn" onclick="setAppViewport('768px', this)">
                            <i data-lucide="tablet"></i> Tablet (768px)
                        </button>
                        <button class="vp-btn" onclick="setAppViewport('375px', this)">
                            <i data-lucide="smartphone"></i> Mobile (375px)
                        </button>
                    </div>

                    <button class="btn-tool-secondary" onclick="openAppModal('PROJECT_SPEC.md')">
                        <i data-lucide="book-open"></i> Spesifikasi
                    </button>
                    <button class="btn-tool-secondary" onclick="openAppModal('index.html')">
                        <i data-lucide="code"></i> Kode Sumber
                    </button>
                    <a href="projects/file-manager/index.html" target="_blank" class="btn-launch-primary">
                        <i data-lucide="external-link"></i> Jalankan Layar Penuh
                    </a>
                </div>
            </div>

            <!-- Live Interactive Stage -->
            <div class="app-live-stage">
                <div class="app-frame-wrapper" id="appFrameWrapper">
                    <iframe src="projects/file-manager/index.html" title="GlassOS Cloud File Manager Live Preview"></iframe>
                </div>
            </div>

            <!-- Architecture & Component Integration Map -->
            <div class="app-architecture-grid">
                <div>
                    <h3 class="arch-col-title">
                        <i data-lucide="boxes" style="color: var(--accent-cyan);"></i> Komponen Glass Terintegrasi
                    </h3>
                    <p class="arch-desc">
                        Aplikasi ini merakit lebih dari 12 komponen Glass Dark Premium yang saling terhubung secara reaktif:
                    </p>
                    <div class="components-pills-wrap">
                        <a href="ui/components/glass/showcase.html#card-glass-dock-navigation" class="comp-link-pill">
                            <i data-lucide="compass"></i> Floating Glass Dock
                        </a>
                        <a href="ui/components/glass/showcase.html#card-swirl-bottom-sheet" class="comp-link-pill">
                            <i data-lucide="layers"></i> Swirl Refraction Bottom Sheet
                        </a>
                        <a href="ui/components/glass/showcase.html#card-aurora-storage-card" class="comp-link-pill">
                            <i data-lucide="gauge"></i> Aurora Storage Card
                        </a>
                        <a href="ui/components/glass/showcase.html#card-frosted-folder-card" class="comp-link-pill">
                            <i data-lucide="folder"></i> Frosted Folder Card
                        </a>
                        <a href="ui/components/glass/showcase.html#card-telemetry-activity-chart" class="comp-link-pill">
                            <i data-lucide="bar-chart-2"></i> 12-Hour Activity Telemetry
                        </a>
                        <a href="ui/components/glass/showcase.html#card-button-glass" class="comp-link-pill">
                            <i data-lucide="sparkles"></i> Glass Buttons Collection
                        </a>
                        <a href="ui/components/glass/showcase.html#card-input-field-glass" class="comp-link-pill">
                            <i data-lucide="text-cursor-input"></i> Form Input Fields
                        </a>
                        <a href="ui/components/glass/showcase.html#card-toggle-switch-glass" class="comp-link-pill">
                            <i data-lucide="toggle-left"></i> Glass Toggle Switch
                        </a>
                        <a href="ui/components/glass/showcase.html#card-chat-input-bar" class="comp-link-pill">
                            <i data-lucide="message-square"></i> Glass Chat Input Bar
                        </a>
                        <a href="ui/components/glass/showcase.html#card-prompt-pills-row" class="comp-link-pill">
                            <i data-lucide="tag"></i> Prompt Pills Quick Scroller
                        </a>
                        <a href="ui/components/glass/showcase.html#card-ai-model-selector" class="comp-link-pill">
                            <i data-lucide="cpu"></i> AI Model Selector Card
                        </a>
                        <a href="ui/components/glass/showcase.html#card-thinking-effort-selector" class="comp-link-pill">
                            <i data-lucide="sliders"></i> Thinking Effort Selector
                        </a>
                    </div>
                </div>

                <div>
                    <h3 class="arch-col-title">
                        <i data-lucide="cpu" style="color: #A78BFA;"></i> Fitur Rekayasa & Arsitektur
                    </h3>
                    <ul class="spec-list">
                        <li class="spec-item">
                            <i data-lucide="check"></i>
                            <div><strong>Native Web Audio Synthesizer:</strong> Menghasilkan audio haptik procedural (pop, chime, tap) via AudioContext tanpa file MP3 eksternal.</div>
                        </li>
                        <li class="spec-item">
                            <i data-lucide="check"></i>
                            <div><strong>Asymmetric Lighting:</strong> Simulasi arah cahaya fisik dari atas menggunakan border-top 0.35 dan border-bottom 0.06.</div>
                        </li>
                        <li class="spec-item">
                            <i data-lucide="check"></i>
                            <div><strong>Canvas 2D Swirl Refraction:</strong> Shading refraksi matematis pada modal dialog pembuatan folder berkas.</div>
                        </li>
                        <li class="spec-item">
                            <i data-lucide="check"></i>
                            <div><strong>Zero-Dependency Vanilla Architecture:</strong> 100% berjalan tanpa bundle build tool (Vite/Webpack) sehingga sangat cepat dan bebas konfigurasi.</div>
                        </li>
                    </ul>
                </div>
            </div>

        </section>

    </main>

    <!-- Code & Spec Modal -->
    <div class="modal-overlay" id="appModal">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title-wrap">
                    <h3>GlassOS Cloud File Manager Source & Specs</h3>
                    <p>projects/file-manager/</p>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <button class="btn-tool-secondary" onclick="copyAppCode()">
                        <i data-lucide="copy"></i> Salin File Ini
                    </button>
                    <button class="modal-close-btn" onclick="closeAppModal()" title="Tutup Modal">
                        <i data-lucide="x"></i>
                    </button>
                </div>
            </div>

            <div class="modal-tabs-bar">
                <button class="code-tab-btn active" id="tab-btn-index" onclick="switchAppTab('index.html')">
                    <i data-lucide="file-code"></i> index.html (Aplikasi Lengkap)
                </button>
                <button class="code-tab-btn" id="tab-btn-spec" onclick="switchAppTab('PROJECT_SPEC.md')">
                    <i data-lucide="book-open"></i> PROJECT_SPEC.md (Spesifikasi Teknis)
                </button>
            </div>

            <div class="modal-tab-subbar">
                <span class="subbar-file-path" id="modalActiveFilePath">projects/file-manager/index.html</span>
                <span id="modalActiveFileStats">0 baris</span>
            </div>

            <div class="modal-body">
                <pre class="code-pre"><code id="modalAppCodeSnippet">Memuat kode...</code></pre>
            </div>
        </div>
    </div>

    <div class="toast-notification" id="toast">
        <i data-lucide="check-circle-2"></i>
        <span id="toastMsg">Kode berhasil disalin ke clipboard!</span>
    </div>

    <script type="application/json" id="appData">
{app_escaped_json}
    </script>

    <script>
        let APP_DB = {{}};
        try {{
            const rawAppJson = document.getElementById('appData').textContent;
            APP_DB = JSON.parse(rawAppJson);
        }} catch(e) {{
            console.error('Failed to parse app database:', e);
        }}

        let currentTab = "index.html";

        lucide.createIcons();

        function setAppViewport(width, btn) {{
            document.querySelectorAll('.vp-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('appFrameWrapper').style.maxWidth = width;
        }}

        function openAppModal(filename) {{
            document.getElementById('appModal').classList.add('active');
            switchAppTab(filename || 'index.html');
        }}

        function switchAppTab(filename) {{
            currentTab = filename;
            document.getElementById('tab-btn-index').classList.toggle('active', filename === 'index.html');
            document.getElementById('tab-btn-spec').classList.toggle('active', filename === 'PROJECT_SPEC.md');

            const code = APP_DB[filename] || "";
            document.getElementById('modalActiveFilePath').innerText = `projects/file-manager/${{filename}}`;
            
            const lines = code ? code.split('\\n').length : 0;
            const kb = (new Blob([code]).size / 1024).toFixed(1);
            document.getElementById('modalActiveFileStats').innerText = `${{lines}} baris (${{kb}} KB)`;

            document.getElementById('modalAppCodeSnippet').innerText = code;
        }}

        function closeAppModal() {{
            document.getElementById('appModal').classList.remove('active');
        }}

        async function copyAppCode() {{
            const code = APP_DB[currentTab] || "";
            if (code) {{
                await navigator.clipboard.writeText(code);
                showToast(`File ${{currentTab}} berhasil disalin!`);
            }}
        }}

        function showToast(msg) {{
            const toast = document.getElementById('toast');
            document.getElementById('toastMsg').innerText = msg;
            toast.classList.add('active');
            setTimeout(() => toast.classList.remove('active'), 2500);
        }}

        document.getElementById('appModal').addEventListener('click', (e) => {{
            if (e.target.id === 'appModal') closeAppModal();
        }});
    </script>
</body>
</html>
"""

with open(os.path.join(ROOT, "web-apps.html"), "w", encoding="utf-8") as f:
    f.write(web_apps_html_content)

print("web-apps.html rebuilt successfully!")

# ----------------------------------------------------------------------
# 3. BUILD ROOT SHOWCASE (showcase.html)
# ----------------------------------------------------------------------
print("3/4. Building Root Showcase (showcase.html)...")
root_showcase_content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Component Workbench Hub — GlassOS</title>
    <meta name="description" content="Master Hub & Index Laboratorium Komponen UI/UX GlassOS: Glass Dark Premium, Raw HTML, dan Web Applications.">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --bg-page: #08080C;
            --glass-card: rgba(255, 255, 255, 0.05);
            --glass-card-hover: rgba(255, 255, 255, 0.08);
            --glass-border-top: rgba(255, 255, 255, 0.24);
            --glass-border-side: rgba(255, 255, 255, 0.10);
            --glass-border-bottom: rgba(255, 255, 255, 0.04);
            --text-primary: #FFFFFF;
            --text-secondary: rgba(255, 255, 255, 0.65);
            --text-muted: rgba(255, 255, 255, 0.38);
            --accent-cyan: #4A9EFF;
            --accent-blue: #3B82F6;
            --accent-purple: #8B5CF6;
            --ease-spring: cubic-bezier(0.34, 1.15, 0.64, 1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: var(--bg-page);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            position: relative;
        }

        .ambient-mesh {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            pointer-events: none; z-index: 0; overflow: hidden;
        }

        .blob {
            position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.32;
            animation: float 22s infinite alternate ease-in-out;
        }

        .blob-1 { width: 520px; height: 520px; background: radial-gradient(circle, #3B82F6 0%, transparent 70%); top: -150px; left: -120px; }
        .blob-2 { width: 560px; height: 560px; background: radial-gradient(circle, #8B5CF6 0%, transparent 70%); top: 30%; right: -150px; animation-delay: -6s; }
        .blob-3 { width: 480px; height: 480px; background: radial-gradient(circle, #06B6D4 0%, transparent 70%); bottom: -120px; left: 20%; animation-delay: -12s; }

        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(60px, 40px) scale(1.08); }
        }

        .hub-header {
            position: sticky; top: 0; z-index: 50; padding: 16px 32px;
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(8, 8, 12, 0.75); display: flex; align-items: center; justify-content: space-between;
        }

        .brand-cluster { display: flex; align-items: center; gap: 12px; }

        .brand-badge {
            width: 40px; height: 40px; border-radius: 12px;
            background: linear-gradient(135deg, rgba(74, 158, 255, 0.3), rgba(139, 92, 246, 0.3));
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
        }
        .brand-badge svg { width: 22px; height: 22px; stroke-width: 1.5px; color: #FFFFFF; }

        .brand-text h1 { font-size: 18px; font-weight: 700; letter-spacing: -0.02em; }
        .brand-text h1 span { color: var(--accent-cyan); }
        .brand-text p { font-size: 12px; color: var(--text-secondary); margin-top: 1px; }

        .header-actions { display: flex; align-items: center; gap: 10px; }

        .action-link-btn {
            display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px;
            border-radius: 10px; font-size: 13px; font-weight: 500; text-decoration: none;
            color: var(--text-secondary); background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08); transition: all 0.2s;
        }
        .action-link-btn:hover {
            background: rgba(255, 255, 255, 0.09); color: #FFFFFF; border-color: rgba(255, 255, 255, 0.18);
        }
        .action-link-btn.highlight {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(59, 130, 246, 0.2));
            border-color: rgba(6, 182, 212, 0.35); color: #67E8F9; font-weight: 600;
        }
        .action-link-btn.highlight:hover {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.28), rgba(59, 130, 246, 0.35));
            color: #FFFFFF;
        }

        .hub-main {
            flex: 1; padding: 32px; max-width: 1280px; margin: 0 auto; width: 100%; z-index: 5;
        }

        .hero-banner {
            margin-bottom: 32px; text-align: center; max-width: 720px; margin-left: auto; margin-right: auto;
        }
        .hero-title {
            font-size: 28px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 8px;
        }
        .hero-desc {
            font-size: 14px; line-height: 1.6; color: var(--text-secondary);
        }

        .tier-header {
            display: flex; align-items: center; justify-content: space-between;
            margin: 28px 0 16px; padding-bottom: 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }
        .tier-title {
            font-size: 16px; font-weight: 600; letter-spacing: -0.01em; display: flex; align-items: center; gap: 8px;
        }
        .tier-badge {
            font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 6px;
            background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.12);
        }

        /* Web App Spotlight Card */
        .webapp-spotlight-card {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.02));
            border-radius: 20px; border: 1px solid transparent;
            border-top-color: rgba(6, 182, 212, 0.4);
            border-left-color: rgba(6, 182, 212, 0.2);
            border-right-color: rgba(59, 130, 246, 0.2);
            border-bottom-color: rgba(255, 255, 255, 0.05);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            padding: 24px; display: flex; align-items: center; justify-content: space-between;
            gap: 24px; flex-wrap: wrap; margin-bottom: 24px;
        }

        .spotlight-left { display: flex; align-items: center; gap: 18px; max-width: 760px; }
        .spotlight-icon-box {
            width: 56px; height: 56px; border-radius: 16px;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(59, 130, 246, 0.3));
            border: 1px solid rgba(6, 182, 212, 0.4); display: flex; align-items: center; justify-content: center;
            color: #38BDF8; flex-shrink: 0; box-shadow: 0 6px 20px rgba(6, 182, 212, 0.3);
        }
        .spotlight-icon-box svg { width: 28px; height: 28px; }

        .spotlight-info h3 { font-size: 18px; font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
        .spotlight-info p { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }

        .spotlight-tags-cluster { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
        .spotlight-tag {
            font-size: 11.5px; padding: 3px 8px; border-radius: 6px;
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-secondary); display: inline-flex; align-items: center; gap: 5px;
        }
        .spotlight-tag svg { width: 12px; height: 12px; color: var(--accent-cyan); }

        .spotlight-actions { display: flex; flex-direction: column; gap: 8px; flex-shrink: 0; }
        .btn-spotlight-cta {
            display: inline-flex; align-items: center; justify-content: center; gap: 8px;
            padding: 10px 20px; border-radius: 10px; font-size: 13px; font-weight: 600;
            background: linear-gradient(135deg, #06B6D4, #3B82F6); color: #FFFFFF; text-decoration: none;
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.35); transition: transform 0.2s;
        }
        .btn-spotlight-cta:hover { transform: scale(1.02); }

        .btn-spotlight-sec {
            display: inline-flex; align-items: center; justify-content: center; gap: 6px;
            padding: 8px 16px; border-radius: 10px; font-size: 12px; font-weight: 500;
            background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-secondary); text-decoration: none; transition: all 0.2s;
        }
        .btn-spotlight-sec:hover { background: rgba(255, 255, 255, 0.08); color: #FFFFFF; }

        /* Style Cards Grid */
        .style-cards-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 20px; margin-bottom: 24px;
        }

        .style-card {
            background: var(--glass-card); border-radius: 20px;
            border: 1px solid transparent; border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side); border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            padding: 24px; display: flex; flex-direction: column; justify-content: space-between;
            text-decoration: none; color: inherit; transition: all 0.25s;
        }
        .style-card:hover {
            background: var(--glass-card-hover); border-top-color: rgba(255, 255, 255, 0.35);
            transform: translateY(-2px); box-shadow: 0 18px 42px rgba(0, 0, 0, 0.55);
        }

        .card-icon {
            width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center;
            justify-content: center; margin-bottom: 14px;
        }
        .card-icon.purple {
            background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.4); color: #C084FC;
        }
        .card-icon.blue {
            background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); color: #60A5FA;
        }
        .card-icon svg { width: 22px; height: 22px; }

        .style-card h3 {
            font-size: 17px; font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between;
        }
        .count-tag {
            font-size: 11px; font-weight: 600; padding: 2px 7px; border-radius: 6px;
            background: rgba(255, 255, 255, 0.08); color: var(--text-secondary);
        }

        .style-card p {
            font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 16px;
        }

        .style-card-footer {
            display: flex; align-items: center; justify-content: space-between;
            padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 12.5px; font-weight: 500; color: var(--accent-cyan);
        }
        .style-card-footer svg { width: 14px; height: 14px; transition: transform 0.2s; }
        .style-card:hover .style-card-footer svg { transform: translateX(4px); }
    </style>
</head>
<body>

    <div class="ambient-mesh">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>

    <header class="hub-header">
        <div class="brand-cluster">
            <div class="brand-badge">
                <i data-lucide="layers"></i>
            </div>
            <div class="brand-text">
                <h1>Glass<span>OS</span> Master Hub</h1>
                <p>Katalog Terpadu Seluruh Ruang Kerja & Showcase</p>
            </div>
        </div>

        <div class="header-actions">
            <a href="index.html" class="action-link-btn" title="Master Gateway Portal">
                <i data-lucide="home"></i> Gateway
            </a>
            <a href="web-apps.html" class="action-link-btn highlight" title="Buka Showroom Web App">
                <i data-lucide="folder-kanban"></i> Web Apps Studio
            </a>
            <a href="component.md" class="action-link-btn" title="Audit Taksonomi Komponen Master">
                <i data-lucide="book-open"></i> Component.md
            </a>
        </div>
    </header>

    <main class="hub-main">

        <section class="hero-banner">
            <h2 class="hero-title">Laboratorium Komponen & Aplikasi Web</h2>
            <p class="hero-desc">
                Pilih ruang kerja yang ingin Anda jelajahi. Komponen terisolasi dalam pustaka gayanya masing-masing, sedangkan aplikasi komposit utuh berjalan di studio khusus.
            </p>
        </section>

        <!-- TIER 1: WEB APPLICATIONS -->
        <div class="tier-header">
            <div class="tier-title">
                <i data-lucide="folder-kanban" style="color: #38BDF8;"></i>
                <span>Tingkat 1: Aplikasi Web Utuh (Web Applications)</span>
            </div>
            <span class="tier-badge" style="background:rgba(6,182,212,0.15); border-color:rgba(6,182,212,0.3); color:#22D3EE;">Proyek Komposit</span>
        </div>

        <article class="webapp-spotlight-card">
            <div class="spotlight-left">
                <div class="spotlight-icon-box">
                    <i data-lucide="cloud"></i>
                </div>
                <div class="spotlight-info">
                    <h3>
                        <span>GlassOS Cloud File Manager OS</span>
                        <span style="font-size:12px; font-weight:600; padding:2px 8px; border-radius:8px; background:rgba(59,130,246,0.2); color:#60A5FA;">v2.4 Ready</span>
                    </h3>
                    <p>
                        Aplikasi web interaktif siap pakai yang dirakit utuh menggunakan komponen Glass Dark: manajemen berkas, storage telemetry circular gauge, navigasi dock bawah melayang dengan spring physics, dan modal sheet pembuatan folder. Berjalan pada halaman terpisah dengan simulator multi-viewport (Desktop, Tablet, Mobile).
                    </p>
                    <div class="spotlight-tags-cluster">
                        <span class="spotlight-tag"><i data-lucide="compass"></i> Spring Dock Nav</span>
                        <span class="spotlight-tag"><i data-lucide="gauge"></i> Storage Telemetry</span>
                        <span class="spotlight-tag"><i data-lucide="layers"></i> Swirl Bottom Sheet</span>
                        <span class="spotlight-tag"><i data-lucide="volume-2"></i> Audio Synthesizer</span>
                    </div>
                </div>
            </div>

            <div class="spotlight-actions">
                <a href="web-apps.html" class="btn-spotlight-cta">
                    <i data-lucide="layers"></i> Buka Showroom Web App <i data-lucide="arrow-right"></i>
                </a>
                <a href="projects/file-manager/index.html" target="_blank" class="btn-spotlight-sec">
                    <i data-lucide="external-link"></i> Jalankan Langsung
                </a>
                <a href="projects/file-manager/PROJECT_SPEC.md" class="btn-spotlight-sec">
                    <i data-lucide="book-open"></i> Spesifikasi Arsitektur
                </a>
            </div>
        </article>

        <!-- TIER 2: COMPONENT LIBRARIES -->
        <div class="tier-header">
            <div class="tier-title">
                <i data-lucide="layout-grid" style="color: #A78BFA;"></i>
                <span>Tingkat 2: Laboratorium Komponen UI (Component Libraries)</span>
            </div>
            <span class="tier-badge" style="background:rgba(139,92,246,0.15); border-color:rgba(139,92,246,0.3); color:#C084FC;">2 Gaya Desain</span>
        </div>

        <div class="style-cards-grid">

            <!-- Card 1: Glass Dark Premium -->
            <a href="ui/components/glass/showcase.html" class="style-card">
                <div>
                    <div class="card-icon purple">
                        <i data-lucide="gem"></i>
                    </div>
                    <h3>
                        <span>Glass Dark Premium</span>
                        <span class="count-tag">21 Komponen All-in-One</span>
                    </h3>
                    <p>
                        Sistem desain kaca gelap modern: multi-layer blur, border asimetris, noise shader optik, spring physics dock, bottom sheet swirl, dan seluruh komponen dasar standalone bebas error dengan multi-file code modal.
                    </p>
                </div>
                <div class="style-card-footer">
                    <span>Buka Showroom Glass</span>
                    <i data-lucide="arrow-right"></i>
                </div>
            </a>

            <!-- Card 2: Raw Pure HTML -->
            <a href="ui/components/raw/showcase.html" class="style-card">
                <div>
                    <div class="card-icon blue">
                        <i data-lucide="code-2"></i>
                    </div>
                    <h3>
                        <span>Raw HTML Baku (Unstyled)</span>
                        <span class="count-tag">9 Komponen Baku</span>
                    </h3>
                    <p>
                        Implementasi semantik murni tanpa dekorasi visual (CSS dasar 0 rules). Digunakan sebagai baseline acuan fungsional sebelum menerapkan berbagai lapisan style sistem desain.
                    </p>
                </div>
                <div class="style-card-footer">
                    <span>Buka Showroom Raw</span>
                    <i data-lucide="arrow-right"></i>
                </div>
            </a>

        </div>

    </main>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""

with open(os.path.join(ROOT, "showcase.html"), "w", encoding="utf-8") as f:
    f.write(root_showcase_content)

print("showcase.html rebuilt successfully!")

# ----------------------------------------------------------------------
# 4. BUILD RAW SHOWCASE (ui/components/raw/showcase.html)
# ----------------------------------------------------------------------
print("4/4. Building Raw Showcase (ui/components/raw/showcase.html)...")
raw_components = [
    ("button", "Buttons & Actions", "<button>", False),
    ("input", "Form Input Fields", "<input type=\"...\">", False),
    ("checkbox-radio", "Checkboxes & Radios", "<input type=\"checkbox|radio\">", False),
    ("select-dropdown", "Select Dropdown", "<select> & <option>", False),
    ("toggle-switch", "Toggle Switch (Raw)", "<input type=\"checkbox\" role=\"switch\">", False),
    ("details-accordion", "Disclosure / Accordion", "<details> & <summary>", False),
    ("modal-dialog", "Native Modal Dialog", "<dialog>", False),
    ("progress-meter", "Progress & Meter", "<progress> & <meter>", False),
    ("table", "Tabular Data Grid", "<table>, <thead>, <tbody>", False),
]

raw_files_db = {}
for folder, title, tag, is_tall in raw_components:
    folder_path = os.path.join(RAW_DIR, folder)
    raw_files_db[folder] = {}
    
    aio_file = f"{folder}.html"
    for fn in [aio_file, "index.html", "index.css"]:
        p = os.path.join(folder_path, fn)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                raw_files_db[folder][fn] = f.read()

raw_cards_html = ""
for folder, title, tag, is_tall in raw_components:
    aio_file = f"{folder}.html"
    raw_cards_html += f"""
            <!-- Component: {title} -->
            <article class="comp-card">
                <div class="comp-card-head">
                    <span class="comp-card-title">{title}</span>
                    <span class="comp-card-tag">{tag}</span>
                </div>
                <div class="comp-preview-zone">
                    <iframe src="{folder}/{aio_file}" title="{title} Preview"></iframe>
                </div>
                <div class="comp-card-foot">
                    <span class="path-label">ui/components/raw/{folder}/</span>
                    <div class="foot-actions">
                        <button class="btn-act" onclick="openRawModal('{folder}', '{title}')">Kode</button>
                        <button class="btn-act" onclick="copyRawAio('{folder}')">Salin</button>
                        <a href="{folder}/{aio_file}" target="_blank" class="btn-act">Solo</a>
                    </div>
                </div>
            </article>
"""

raw_escaped_json = safe_json_embed(raw_files_db)

raw_showcase_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raw Unstyled HTML Components Showcase</title>
    <meta name="description" content="Katalog komponen web murni tanpa styling CSS untuk acuan taksonomi dan struktur anatomi HTML5 baku.">
    <link rel="icon" type="image/svg+xml" href="../../../favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --bg-page: #0C0D12;
            --card-bg: #141620;
            --border-color: #242838;
            --text-primary: #F1F5F9;
            --text-secondary: #94A3B8;
            --accent-blue: #3B82F6;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            background-color: var(--bg-page);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .raw-header {{
            padding: 16px 32px; background: #10121A; border-bottom: 1px solid var(--border-color);
            display: flex; align-items: center; justify-content: space-between;
        }}
        .brand-cluster {{ display: flex; align-items: center; gap: 12px; }}
        .brand-icon {{
            width: 38px; height: 38px; border-radius: 10px; background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.3); display: flex; align-items: center; justify-content: center;
            color: #60A5FA;
        }}
        .brand-text h1 {{ font-size: 17px; font-weight: 700; }}
        .brand-text p {{ font-size: 12px; color: var(--text-secondary); }}

        .header-actions {{ display: flex; align-items: center; gap: 10px; }}
        .nav-link {{
            padding: 7px 14px; border-radius: 8px; font-size: 12.5px; text-decoration: none;
            color: var(--text-secondary); background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color); transition: all 0.2s;
        }}
        .nav-link:hover {{ color: #FFFFFF; background: rgba(255, 255, 255, 0.08); }}

        .raw-grid {{
            padding: 24px 32px 64px; display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 20px;
        }}

        .comp-card {{
            background: var(--card-bg); border-radius: 14px; border: 1px solid var(--border-color);
            display: flex; flex-direction: column; overflow: hidden;
        }}

        .comp-card-head {{
            padding: 12px 16px; display: flex; align-items: center; justify-content: space-between;
            background: rgba(0, 0, 0, 0.2); border-bottom: 1px solid var(--border-color);
        }}
        .comp-card-title {{ font-size: 14px; font-weight: 600; }}
        .comp-card-tag {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 2px 6px;
            border-radius: 4px; background: rgba(255, 255, 255, 0.06); color: #93C5FD;
        }}

        .comp-preview-zone {{
            height: 240px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;
            padding: 12px;
        }}
        .comp-preview-zone iframe {{ width: 100%; height: 100%; border: none; }}

        .comp-card-foot {{
            padding: 10px 16px; display: flex; align-items: center; justify-content: space-between;
            background: rgba(0, 0, 0, 0.3); border-top: 1px solid var(--border-color); font-size: 12px;
        }}
        .path-label {{ font-family: 'JetBrains Mono', monospace; color: var(--text-secondary); }}

        .foot-actions {{ display: flex; align-items: center; gap: 6px; }}
        .btn-act {{
            padding: 4px 10px; border-radius: 6px; font-size: 11.5px;
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color);
            color: var(--text-primary); cursor: pointer; text-decoration: none;
            transition: all 0.2s;
        }}
        .btn-act:hover {{ background: rgba(255, 255, 255, 0.12); }}

        /* Modal */
        .modal-overlay {{
            position: fixed; inset: 0; z-index: 1000; background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; padding: 24px;
        }}
        .modal-overlay.active {{ display: flex; }}

        .modal-card {{
            width: 100%; max-width: 800px; height: 75vh; background: #0F1118; border-radius: 16px;
            border: 1px solid var(--border-color); display: flex; flex-direction: column; overflow: hidden;
        }}
        .modal-header {{
            padding: 14px 20px; display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid var(--border-color); background: #141722;
        }}
        .modal-body {{ flex: 1; overflow: auto; padding: 18px 20px; background: #0B0D13; }}
        .code-pre {{ margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 1.6; color: #CBD5E1; }}

        .toast {{
            position: fixed; bottom: 24px; right: 24px; z-index: 2000; padding: 10px 18px;
            border-radius: 8px; background: #1E293B; border: 1px solid var(--border-color);
            color: #FFFFFF; font-size: 13px; transform: translateY(60px); opacity: 0;
            transition: all 0.25s; pointer-events: none;
        }}
        .toast.active {{ transform: translateY(0); opacity: 1; }}
    </style>
</head>
<body>

    <header class="raw-header">
        <div class="brand-cluster">
            <div class="brand-icon"><i data-lucide="code-2"></i></div>
            <div class="brand-text">
                <h1>Raw Unstyled HTML Showcase</h1>
                <p>9 Komponen Anatomi Dasar Web Semantic</p>
            </div>
        </div>

        <div class="header-actions">
            <a href="../../../index.html" class="nav-link"><i data-lucide="home"></i> Gateway</a>
            <a href="../../../showcase.html" class="nav-link"><i data-lucide="layers"></i> Master Hub</a>
            <a href="../../../web-apps.html" class="nav-link"><i data-lucide="folder-kanban"></i> Web Apps Studio</a>
            <a href="../glass/showcase.html" class="nav-link"><i data-lucide="gem"></i> Glass Dark (21)</a>
        </div>
    </header>

    <main class="raw-grid">
{raw_cards_html}
    </main>

    <div class="modal-overlay" id="rawModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3 id="modalTitle">Kode Komponen Raw</h3>
                <button class="btn-act" onclick="closeRawModal()">Tutup</button>
            </div>
            <div class="modal-body">
                <pre class="code-pre"><code id="modalCode">Memuat...</code></pre>
            </div>
        </div>
    </div>

    <div class="toast" id="toastMsg">Kode disalin!</div>

    <script type="application/json" id="rawDb">
{raw_escaped_json}
    </script>

    <script>
        let RAW_DB = {{}};
        try {{
            RAW_DB = JSON.parse(document.getElementById('rawDb').textContent);
        }} catch(e) {{
            console.error('Failed to parse raw db:', e);
        }}

        lucide.createIcons();

        function openRawModal(folder, title) {{
            document.getElementById('modalTitle').innerText = `${{title}} (${{folder}}.html)`;
            const code = (RAW_DB[folder] && RAW_DB[folder][`${{folder}}.html`]) || "";
            document.getElementById('modalCode').innerText = code;
            document.getElementById('rawModal').classList.add('active');
        }}

        function closeRawModal() {{
            document.getElementById('rawModal').classList.remove('active');
        }}

        async function copyRawAio(folder) {{
            const code = (RAW_DB[folder] && RAW_DB[folder][`${{folder}}.html`]) || "";
            if (code) {{
                await navigator.clipboard.writeText(code);
                showToast(`Kode raw ${{folder}} disalin!`);
            }}
        }}

        function showToast(msg) {{
            const t = document.getElementById('toastMsg');
            t.innerText = msg;
            t.classList.add('active');
            setTimeout(() => t.classList.remove('active'), 2000);
        }}

        document.getElementById('rawModal').addEventListener('click', (e) => {{
            if (e.target.id === 'rawModal') closeRawModal();
        }});
    </script>
</body>
</html>
"""

with open(os.path.join(RAW_DIR, "showcase.html"), "w", encoding="utf-8") as f:
    f.write(raw_showcase_content)

print("Raw showcase built successfully!")
print("ALL SHOWCASE FILES REBUILT CLEANLY!")
