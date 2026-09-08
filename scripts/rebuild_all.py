import os
import json
import html

ROOT = r"d:\PROJECT\prototype"
GLASS_DIR = os.path.join(ROOT, "ui", "components", "glass")
RAW_DIR = os.path.join(ROOT, "ui", "components", "raw")
PROJECTS_DIR = os.path.join(ROOT, "projects")

def safe_json_embed(data):
    s = json.dumps(data, ensure_ascii=False)
    # Valid RFC 8259 JSON escape for solidus: prevents any </script from breaking HTML parser
    return s.replace("</", "<\\/")

# ======================================================================
# 1. BUILD GLASS SHOWCASE (ui/components/glass/showcase.html)
# ======================================================================
print("1/3. Building Glass Showcase (Fixed Card Stretches & Added Grid Selector)...")
with open(os.path.join(GLASS_DIR, "css.css"), "r", encoding="utf-8") as f:
    shared_css_code = f.read()

glass_components_metadata = [
    ("button-glass", "Glass Buttons Collection", "Action / Buttons", "Molecule", "inputs"),
    ("chat-input-bar", "Glass Chat Input Bar", "Form Input / AI Prompt", "Molecule", "inputs"),
    ("input-field-glass", "Glass Form Input Fields", "Form / Inputs", "Molecule", "inputs"),
    ("prompt-pills-row", "Prompt Pills Quick Scroller", "Chips / Action Pills", "Molecule", "inputs"),
    ("thinking-effort-selector", "Thinking Effort Selector", "Segmented Stepper", "Atomic", "inputs"),
    ("toggle-switch-glass", "Glass Toggle Switch", "Control / Switch", "Atomic", "inputs"),
    ("checkbox-glass", "Glass Checkbox & Radio", "Control / Checkbox", "Atomic", "inputs"),
    ("dropdown-select-glass", "Glass Floating Dropdown", "Control / Select", "Molecule", "inputs"),
    ("ai-model-selector", "AI Model Selector Card", "Selection Control", "Molecule", "cards"),
    ("frosted-folder-card", "Frosted Folder Card", "File System / Card", "Molecule", "cards"),
    ("aurora-storage-card", "Aurora Storage Card", "Data Display / Gauge", "Molecule", "cards"),
    ("progress-bar-glass", "Glass Glowing Progress Bar", "Display / Progress", "Atomic", "cards"),
    ("avatar-badge-glass", "Glass Avatar with Status", "Display / Avatar", "Atomic", "cards"),
    ("glass-dock-navigation", "Floating Glass Dock", "Navigation / Spring Dock", "Molecule", "navigation"),
    ("glass-sidepanel", "Productivity Glass Sidepanel", "Navigation / Desktop Drawer", "Organism", "navigation"),
    ("swirl-bottom-sheet", "Swirl Refraction Bottom Sheet", "Overlay / Canvas 2D Refraction", "Organism", "overlays"),
    ("modal-dialog-glass", "Glass Modal Dialog", "Overlay / Centered Dialog", "Molecule", "overlays"),
    ("toast-notification-glass", "Glass Toast Notification", "Feedback / Toast Alert", "Molecule", "overlays"),
    ("tooltip-glass", "Glass Micro Tooltip", "Feedback / Tooltip", "Atomic", "overlays"),
    ("telemetry-activity-chart", "Telemetry Activity Chart", "Analytics / Bar Histogram", "Molecule", "telemetry"),
    ("ai-agent-scenery", "AI Agent Studio Scenery", "Complete Workspace Scenery", "Scenery", "scenery")
]

glass_files_db = {"css.css": shared_css_code}
glass_cards_html = ""

for folder, title, cat, badge, filter_cat in glass_components_metadata:
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
                            <i data-lucide="code"></i> Kode
                        </button>
                        <button class="btn-action-tool highlight" onclick="quickCopyAllInOne('{folder}')" title="Salin kode file mandiri">
                            <i data-lucide="copy"></i> Salin
                        </button>
                    </div>
                </div>
                <div class="card-preview-zone">
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
            background: rgba(8, 8, 12, 0.78); display: flex; align-items: center; justify-content: space-between;
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
            margin: 20px 32px 0; padding: 16px 24px; border-radius: 16px;
            background: linear-gradient(90deg, rgba(6, 182, 212, 0.10), rgba(59, 130, 246, 0.10));
            border: 1px solid rgba(6, 182, 212, 0.25);
            display: flex; align-items: center; justify-content: space-between; gap: 16px;
        }}
        .banner-info {{ display: flex; align-items: center; gap: 14px; }}
        .banner-icon-badge {{
            width: 40px; height: 40px; border-radius: 12px; background: rgba(6, 182, 212, 0.2);
            border: 1px solid rgba(6, 182, 212, 0.35); display: flex; align-items: center; justify-content: center;
            color: #22D3EE; flex-shrink: 0;
        }}
        .banner-text h3 {{ font-size: 14.5px; font-weight: 600; color: #FFFFFF; }}
        .banner-text p {{ font-size: 12px; color: var(--text-secondary); margin-top: 2px; }}

        .btn-banner-cta {{
            display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px;
            border-radius: 10px; font-size: 12.5px; font-weight: 600; text-decoration: none;
            background: linear-gradient(135deg, #06B6D4, #3B82F6); color: #FFFFFF;
            box-shadow: 0 4px 14px rgba(6, 182, 212, 0.35); transition: transform 0.2s; white-space: nowrap;
        }}
        .btn-banner-cta:hover {{ transform: scale(1.02); }}

        /* Controls Bar with Layout Switcher */
        .controls-bar {{
            padding: 18px 32px 10px; display: flex; align-items: center; justify-content: space-between;
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

        .controls-right {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}

        /* Layout Switcher (1, 2, 3, 4, Auto Kolom) */
        .layout-selector {{
            display: flex; align-items: center; gap: 4px; padding: 4px;
            background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
        }}
        .layout-label {{
            font-size: 11.5px; font-weight: 600; color: var(--text-muted); padding: 0 8px;
            display: flex; align-items: center; gap: 5px;
        }}
        .layout-label svg {{ width: 14px; height: 14px; }}
        .btn-layout {{
            padding: 5px 10px; border-radius: 8px; font-size: 12px; font-weight: 500;
            background: transparent; border: none; color: var(--text-muted); cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-layout:hover {{ color: var(--text-primary); }}
        .btn-layout.active {{
            background: rgba(56, 189, 248, 0.18); color: #38BDF8; font-weight: 600;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }}

        .search-box {{
            display: flex; align-items: center; gap: 10px; padding: 7px 14px;
            border-radius: 12px; background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08); width: 220px;
        }}
        .search-box svg {{ color: var(--text-muted); width: 15px; height: 15px; }}
        .search-box input {{
            background: transparent; border: none; outline: none; font-size: 13px;
            color: #FFFFFF; width: 100%; font-family: inherit;
        }}

        /* Grid */
        .showcase-grid {{
            padding: 16px 32px 64px; display: grid; gap: 24px; z-index: 5;
            transition: all 0.3s ease;
        }}
        .showcase-grid.cols-auto {{ grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); }}
        .showcase-grid.cols-1 {{ grid-template-columns: 1fr; max-width: 900px; margin: 0 auto; width: 100%; }}
        .showcase-grid.cols-2 {{ grid-template-columns: repeat(2, 1fr); }}
        .showcase-grid.cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
        .showcase-grid.cols-4 {{ grid-template-columns: repeat(4, 1fr); }}

        /* Component Card - Unified Seamless Flex (No Blank Stretched Space) */
        .component-card {{
            position: relative; background: var(--glass-card); border-radius: 20px;
            border: 1px solid transparent; border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side); border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            display: flex; flex-direction: column; overflow: hidden;
            height: 100%; min-height: 520px;
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
            flex-shrink: 0;
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
            flex-shrink: 0;
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

        /* Preview Zone - Seamless Flex Fill without detached gap */
        .card-preview-zone {{
            flex: 1; width: 100%; min-height: 400px;
            display: flex; align-items: center; justify-content: center;
            background: #050508; position: relative; overflow: hidden; padding: 0;
        }}

        .preview-resizer-wrapper {{
            width: 100%; height: 100%; min-height: 100%; transition: max-width 0.35s var(--ease-spring);
            display: flex; align-items: center; justify-content: center; margin: 0 auto;
        }}

        .preview-resizer-wrapper iframe {{
            width: 100%; height: 100%; min-height: 100%; border: none; background: #07070A;
            display: block;
        }}

        .card-bottom {{
            padding: 10px 18px; display: flex; align-items: center; justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.05); background: rgba(255, 255, 255, 0.02);
            font-size: 11.5px; flex-shrink: 0;
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
            .showcase-grid {{ padding: 12px 18px 48px; }}
            .showcase-grid.cols-2, .showcase-grid.cols-3, .showcase-grid.cols-4 {{ grid-template-columns: 1fr; }}
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
            <a href="../../../web-apps.html" class="btn-top-link btn-highlight-webapp" title="Buka Halaman Khusus Web Applications">
                <i data-lucide="folder-kanban"></i> Web Applications
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
                <i data-lucide="folder-kanban"></i>
            </div>
            <div class="banner-text">
                <h3>Koleksi Aplikasi Web Utuh (Projects Workspace)</h3>
                <p>Seluruh aplikasi web utuh berada di dalam folder <code>projects/</code> dan ditampilkan pada halaman studio tersendiri.</p>
            </div>
        </div>
        <a href="../../../web-apps.html" class="btn-banner-cta">
            <i data-lucide="folder-kanban"></i> Buka Web Applications Studio <i data-lucide="arrow-right"></i>
        </a>
    </div>

    <!-- Controls Bar with Filter and Layout Grid Switcher -->
    <div class="controls-bar">
        <div class="filter-tabs">
            <button class="filter-tab active" onclick="filterCategory('all', this)">Semua (21)</button>
            <button class="filter-tab" onclick="filterCategory('inputs', this)">Inputs</button>
            <button class="filter-tab" onclick="filterCategory('cards', this)">Cards</button>
            <button class="filter-tab" onclick="filterCategory('navigation', this)">Navigation</button>
            <button class="filter-tab" onclick="filterCategory('overlays', this)">Overlays</button>
            <button class="filter-tab" onclick="filterCategory('scenery', this)">Scenery</button>
        </div>

        <div class="controls-right">
            <!-- Grid Layout Selector -->
            <div class="layout-selector">
                <span class="layout-label"><i data-lucide="grid"></i> Tampilan:</span>
                <button class="btn-layout" data-cols="1" onclick="setGridLayout('1', this)" title="1 Kolom">1</button>
                <button class="btn-layout" data-cols="2" onclick="setGridLayout('2', this)" title="2 Kolom">2</button>
                <button class="btn-layout" data-cols="3" onclick="setGridLayout('3', this)" title="3 Kolom">3</button>
                <button class="btn-layout" data-cols="4" onclick="setGridLayout('4', this)" title="4 Kolom">4</button>
                <button class="btn-layout active" data-cols="auto" onclick="setGridLayout('auto', this)" title="Auto Kolom">Auto</button>
            </div>

            <div class="search-box">
                <i data-lucide="search"></i>
                <input type="text" id="searchInput" placeholder="Cari komponen..." oninput="handleSearch(this.value)">
            </div>
        </div>
    </div>

    <!-- Main Grid -->
    <main class="showcase-grid cols-auto" id="componentsGrid">
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
            <div class="modal-tabs-bar" id="modalTabsBar"></div>

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

        // Restore layout preference
        const savedCols = localStorage.getItem('glass-grid-layout') || 'auto';
        const savedBtn = document.querySelector(`.btn-layout[data-cols="${{savedCols}}"]`);
        if (savedBtn) setGridLayout(savedCols, savedBtn);

        function setGridLayout(cols, btn) {{
            document.querySelectorAll('.btn-layout').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            const grid = document.getElementById('componentsGrid');
            if (!grid) return;
            grid.classList.remove('cols-1', 'cols-2', 'cols-3', 'cols-4', 'cols-auto');
            grid.classList.add(`cols-${{cols}}`);
            localStorage.setItem('glass-grid-layout', cols);
        }}

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

# ======================================================================
# 2. BUILD RAW SHOWCASE (ui/components/raw/showcase.html)
# ======================================================================
print("2/3. Building Raw Showcase (Fixed HTML Entity Bugs & Added Grid Selector)...")
raw_components = [
    ("button", "Buttons & Actions", "<button>"),
    ("input", "Form Input Fields", "<input type=\"...\">"),
    ("checkbox-radio", "Checkboxes & Radios", "<input type=\"checkbox|radio\">"),
    ("select-dropdown", "Select Dropdown", "<select> & <option>"),
    ("toggle-switch", "Toggle Switch (Raw)", "<input type=\"checkbox\" role=\"switch\">"),
    ("details-accordion", "Disclosure / Accordion", "<details> & <summary>"),
    ("modal-dialog", "Native Modal Dialog", "<dialog>"),
    ("progress-meter", "Progress & Meter", "<progress> & <meter>"),
    ("table", "Tabular Data Grid", "<table>, <thead>, <tbody>"),
]

raw_files_db = {}
for folder, title, tag in raw_components:
    folder_path = os.path.join(RAW_DIR, folder)
    raw_files_db[folder] = {}
    
    aio_file = f"{folder}.html"
    for fn in [aio_file, "index.html", "index.css"]:
        p = os.path.join(folder_path, fn)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                raw_files_db[folder][fn] = f.read()

raw_cards_html = ""
for folder, title, tag in raw_components:
    aio_file = f"{folder}.html"
    # CRITICAL FIX: Escape HTML tags so they don't break the DOM parser!
    escaped_tag = html.escape(tag)
    
    raw_cards_html += f"""
            <!-- Component: {title} -->
            <article class="comp-card">
                <div class="comp-card-head">
                    <span class="comp-card-title">{title}</span>
                    <span class="comp-card-tag">{escaped_tag}</span>
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

        /* Controls Bar */
        .controls-bar {{
            padding: 18px 32px 6px; display: flex; align-items: center; justify-content: space-between;
        }}
        .layout-selector {{
            display: flex; align-items: center; gap: 4px; padding: 4px;
            background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-color);
            border-radius: 12px;
        }}
        .layout-label {{
            font-size: 11.5px; font-weight: 600; color: var(--text-secondary); padding: 0 8px;
            display: flex; align-items: center; gap: 5px;
        }}
        .btn-layout {{
            padding: 5px 10px; border-radius: 8px; font-size: 12px; font-weight: 500;
            background: transparent; border: none; color: var(--text-secondary); cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-layout:hover {{ color: #FFFFFF; }}
        .btn-layout.active {{
            background: rgba(59, 130, 246, 0.2); color: #60A5FA; font-weight: 600;
        }}

        .raw-grid {{
            padding: 16px 32px 64px; display: grid; gap: 20px;
            transition: all 0.3s ease;
        }}
        .raw-grid.cols-auto {{ grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); }}
        .raw-grid.cols-1 {{ grid-template-columns: 1fr; max-width: 800px; margin: 0 auto; width: 100%; }}
        .raw-grid.cols-2 {{ grid-template-columns: repeat(2, 1fr); }}
        .raw-grid.cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
        .raw-grid.cols-4 {{ grid-template-columns: repeat(4, 1fr); }}

        .comp-card {{
            background: var(--card-bg); border-radius: 14px; border: 1px solid var(--border-color);
            display: flex; flex-direction: column; overflow: hidden; height: 100%; min-height: 380px;
        }}

        .comp-card-head {{
            padding: 12px 16px; display: flex; align-items: center; justify-content: space-between;
            background: rgba(0, 0, 0, 0.2); border-bottom: 1px solid var(--border-color);
            flex-shrink: 0;
        }}
        .comp-card-title {{ font-size: 14px; font-weight: 600; }}
        .comp-card-tag {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 2px 6px;
            border-radius: 4px; background: rgba(255, 255, 255, 0.06); color: #93C5FD;
        }}

        .comp-preview-zone {{
            flex: 1; min-height: 280px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;
            padding: 0; overflow: hidden;
        }}
        .comp-preview-zone iframe {{ width: 100%; height: 100%; min-height: 100%; border: none; display: block; }}

        .comp-card-foot {{
            padding: 10px 16px; display: flex; align-items: center; justify-content: space-between;
            background: rgba(0, 0, 0, 0.3); border-top: 1px solid var(--border-color); font-size: 12px;
            flex-shrink: 0;
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

        @media (max-width: 768px) {{
            .raw-header {{ padding: 12px 18px; }}
            .controls-bar {{ padding: 12px 18px; }}
            .raw-grid {{ padding: 12px 18px; }}
            .raw-grid.cols-2, .raw-grid.cols-3, .raw-grid.cols-4 {{ grid-template-columns: 1fr; }}
        }}
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
            <a href="../../../web-apps.html" class="nav-link"><i data-lucide="folder-kanban"></i> Web Apps</a>
            <a href="../glass/showcase.html" class="nav-link"><i data-lucide="gem"></i> Glass Dark (21)</a>
        </div>
    </header>

    <div class="controls-bar">
        <div></div>
        <div class="layout-selector">
            <span class="layout-label"><i data-lucide="grid"></i> Tampilan:</span>
            <button class="btn-layout" data-cols="1" onclick="setRawGridLayout('1', this)" title="1 Kolom">1</button>
            <button class="btn-layout" data-cols="2" onclick="setRawGridLayout('2', this)" title="2 Kolom">2</button>
            <button class="btn-layout" data-cols="3" onclick="setRawGridLayout('3', this)" title="3 Kolom">3</button>
            <button class="btn-layout" data-cols="4" onclick="setRawGridLayout('4', this)" title="4 Kolom">4</button>
            <button class="btn-layout active" data-cols="auto" onclick="setRawGridLayout('auto', this)" title="Auto Kolom">Auto</button>
        </div>
    </div>

    <main class="raw-grid cols-auto" id="rawGrid">
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

        // Restore layout preference
        const savedRawCols = localStorage.getItem('raw-grid-layout') || 'auto';
        const savedRawBtn = document.querySelector(`.btn-layout[data-cols="${{savedRawCols}}"]`);
        if (savedRawBtn) setRawGridLayout(savedRawCols, savedRawBtn);

        function setRawGridLayout(cols, btn) {{
            document.querySelectorAll('.btn-layout').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            const grid = document.getElementById('rawGrid');
            if (!grid) return;
            grid.classList.remove('cols-1', 'cols-2', 'cols-3', 'cols-4', 'cols-auto');
            grid.classList.add(`cols-${{cols}}`);
            localStorage.setItem('raw-grid-layout', cols);
        }}

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

# ======================================================================
# 3. BUILD WEB APPLICATIONS STUDIO (web-apps.html)
# ======================================================================
print("3/3. Building Dynamic Web Applications Portfolio Studio (web-apps.html)...")

# Discover all projects in projects/
projects_registry = [
    {
        "id": "file-manager",
        "title": "GlassOS Cloud File Manager",
        "version": "v2.4",
        "status": "Production Ready",
        "desc": "Sistem Operasi Manajemen Berkas Awan & Produktivitas AI Berbasis Glass Dark Premium dengan Web Audio synthesizer procedur, Canvas 2D swirl refraction, dan spring dock navigasi.",
        "icon": "cloud",
        "folder": "projects/file-manager",
        "components": [
            ("Floating Glass Dock", "compass", "ui/components/glass/showcase.html#card-glass-dock-navigation"),
            ("Swirl Refraction Bottom Sheet", "layers", "ui/components/glass/showcase.html#card-swirl-bottom-sheet"),
            ("Aurora Storage Card", "gauge", "ui/components/glass/showcase.html#card-aurora-storage-card"),
            ("Frosted Folder Card", "folder", "ui/components/glass/showcase.html#card-frosted-folder-card"),
            ("Telemetry Activity Chart", "bar-chart-2", "ui/components/glass/showcase.html#card-telemetry-activity-chart"),
            ("Glass Buttons Collection", "sparkles", "ui/components/glass/showcase.html#card-button-glass"),
            ("Form Input Fields", "text-cursor-input", "ui/components/glass/showcase.html#card-input-field-glass"),
            ("Glass Toggle Switch", "toggle-left", "ui/components/glass/showcase.html#card-toggle-switch-glass"),
            ("Glass Chat Input Bar", "message-square", "ui/components/glass/showcase.html#card-chat-input-bar"),
            ("Prompt Pills Quick Scroller", "tag", "ui/components/glass/showcase.html#card-prompt-pills-row"),
            ("AI Model Selector Card", "cpu", "ui/components/glass/showcase.html#card-ai-model-selector"),
            ("Thinking Effort Selector", "sliders", "ui/components/glass/showcase.html#card-thinking-effort-selector"),
        ],
        "features": [
            "Native Web Audio Procedural Sound (AudioContext)",
            "Asymmetric Physical Light Simulation (border 0.35 / 0.06)",
            "Canvas 2D Swirl Refraction Mathematics",
            "Zero-Dependency Vanilla Architecture"
        ]
    },
    {
        "id": "ai-studio",
        "title": "GlassOS AI Agent Studio",
        "version": "v1.0",
        "status": "Production Ready",
        "desc": "Ruang kerja agentik AI otonom interaktif dengan pemilihan model reaktif (K3-Pro Ultra, Swarm Agent, Flash Instant), pengatur penalaran bergradasi, respon streaming interaktif, dan sound haptik.",
        "icon": "sparkles",
        "folder": "projects/ai-studio",
        "components": [
            ("AI Model Selector Card", "cpu", "ui/components/glass/showcase.html#card-ai-model-selector"),
            ("Thinking Effort Selector", "brain", "ui/components/glass/showcase.html#card-thinking-effort-selector"),
            ("Prompt Pills Quick Scroller", "tag", "ui/components/glass/showcase.html#card-prompt-pills-row"),
            ("Glass Chat Input Bar", "send", "ui/components/glass/showcase.html#card-chat-input-bar"),
            ("Status Badge & Sound Synthesizer", "volume-2", "ui/components/glass/showcase.html#card-avatar-badge-glass"),
        ],
        "features": [
            "Reactive Model Context & State Switcher",
            "Discrete Reasoning Effort Stepper",
            "Synthesizer Sine Wave Haptic Audio Feedback",
            "Adaptive Fluid Viewport for Mobile & Desktop"
        ]
    }
]

# Read code for all registered projects
web_apps_db = {}
for p in projects_registry:
    pid = p["id"]
    pdir = os.path.join(ROOT, "projects", pid)
    web_apps_db[pid] = {}
    
    idx_p = os.path.join(pdir, "index.html")
    if os.path.exists(idx_p):
        with open(idx_p, "r", encoding="utf-8") as f:
            web_apps_db[pid]["index.html"] = f.read()
            
    spec_p = os.path.join(pdir, "PROJECT_SPEC.md")
    if os.path.exists(spec_p):
        with open(spec_p, "r", encoding="utf-8") as f:
            web_apps_db[pid]["PROJECT_SPEC.md"] = f.read()

apps_escaped_json = safe_json_embed(web_apps_db)
projects_meta_json = safe_json_embed(projects_registry)

# Generate Gallery Cards HTML
gallery_cards_html = ""
for p in projects_registry:
    pid = p["id"]
    gallery_cards_html += f"""
        <article class="gallery-card" id="gallery-{pid}">
            <div class="gallery-card-top">
                <div class="gallery-icon-box">
                    <i data-lucide="{p['icon']}"></i>
                </div>
                <div class="gallery-title-wrap">
                    <h3>{p['title']}</h3>
                    <div class="gallery-meta-tags">
                        <span class="tag-version">{p['version']}</span>
                        <span class="tag-status">{p['status']}</span>
                        <span class="tag-folder">{p['folder']}/</span>
                    </div>
                </div>
            </div>
            <p class="gallery-card-desc">{p['desc']}</p>
            
            <div class="gallery-preview-frame">
                <iframe src="{p['folder']}/index.html" title="{p['title']} Preview"></iframe>
            </div>

            <div class="gallery-card-bottom">
                <button class="btn-card-action" onclick="switchToProject('{pid}')">
                    <i data-lucide="play"></i> Buka di Stage Simulator
                </button>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-card-icon" onclick="openAppModal('{pid}', 'PROJECT_SPEC.md')" title="Spesifikasi Proyek">
                        <i data-lucide="book-open"></i>
                    </button>
                    <button class="btn-card-icon" onclick="openAppModal('{pid}', 'index.html')" title="Kode Sumber">
                        <i data-lucide="code"></i>
                    </button>
                    <a href="{p['folder']}/index.html" target="_blank" class="btn-card-launch" title="Buka Layar Penuh">
                        <i data-lucide="external-link"></i>
                    </a>
                </div>
            </div>
        </article>
"""

# Add "Add New Project Blueprint Card"
gallery_cards_html += """
        <article class="gallery-card add-project-card">
            <div class="add-card-inner">
                <div class="add-icon-box">
                    <i data-lucide="plus"></i>
                </div>
                <h3>Tambah Proyek Web App Baru</h3>
                <p>
                    Semua folder di bawah direktori <code>projects/</code> akan otomatis menjadi bagian dari koleksi Web Applications ini.
                </p>
                <div class="add-instructions">
                    <div class="code-line">mkdir projects/nama-aplikasi</div>
                    <div class="code-line">cp projects/TEMPLATE.md projects/nama-aplikasi/PROJECT_SPEC.md</div>
                </div>
                <a href="projects/TEMPLATE.md" target="_blank" class="btn-blueprint">
                    <i data-lucide="file-text"></i> Baca Blueprint TEMPLATE.md
                </a>
            </div>
        </article>
"""

web_apps_html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GlassOS Web Applications Studio — Production Projects</title>
    <meta name="description" content="Showroom & Workbench sekumpulan Aplikasi Web Utuh dari folder projects/ berbasis tema Glass Dark Premium.">
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
            position: sticky; top: 0; z-index: 50; padding: 14px 32px;
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(7, 7, 11, 0.82); display: flex; align-items: center; justify-content: space-between;
        }}

        .brand-cluster {{ display: flex; align-items: center; gap: 12px; }}

        .brand-badge {{
            width: 40px; height: 40px; border-radius: 12px;
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
            display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px;
            border-radius: 10px; font-size: 12.5px; font-weight: 500; text-decoration: none;
            color: var(--text-secondary); background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08); transition: all 0.2s;
        }}
        .action-link-btn:hover {{
            background: rgba(255, 255, 255, 0.09); color: #FFFFFF; border-color: rgba(255, 255, 255, 0.18);
        }}

        /* Main Hub */
        .hub-main {{
            flex: 1; padding: 24px 32px 64px; max-width: 1360px; margin: 0 auto; width: 100%; z-index: 5;
        }}

        /* Hero Banner */
        .hero-banner {{
            margin-bottom: 24px; text-align: center; max-width: 820px; margin-left: auto; margin-right: auto;
        }}
        .hero-tag {{
            display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px;
            border-radius: 20px; font-size: 11.5px; font-weight: 600; text-transform: uppercase;
            letter-spacing: 0.05em; background: rgba(6, 182, 212, 0.15); color: #22D3EE;
            border: 1px solid rgba(6, 182, 212, 0.3); margin-bottom: 10px;
        }}
        .hero-title {{
            font-size: 28px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 8px;
        }}
        .hero-desc {{
            font-size: 14px; line-height: 1.6; color: var(--text-secondary);
        }}

        /* Project Selection Bar */
        .projects-selection-bar {{
            display: flex; align-items: center; justify-content: space-between; gap: 16px;
            padding: 8px 12px; margin-bottom: 24px; border-radius: 16px;
            background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
            flex-wrap: wrap;
        }}

        .project-tabs-cluster {{
            display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
        }}

        .proj-tab-btn {{
            display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px;
            border-radius: 10px; border: 1px solid transparent; background: transparent;
            color: var(--text-secondary); font-size: 13px; font-weight: 500; cursor: pointer;
            transition: all 0.2s;
        }}
        .proj-tab-btn:hover {{ background: rgba(255, 255, 255, 0.05); color: #FFFFFF; }}
        .proj-tab-btn.active {{
            background: rgba(59, 130, 246, 0.18); border-color: rgba(59, 130, 246, 0.4);
            color: #93C5FD; font-weight: 600; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        }}
        .proj-tab-btn .badge-pill {{
            font-size: 10.5px; padding: 2px 6px; border-radius: 6px;
            background: rgba(16, 185, 129, 0.2); color: #34D399; font-weight: 600;
        }}

        /* View Mode Switcher */
        .mode-toggle-cluster {{
            display: flex; align-items: center; gap: 4px; padding: 4px;
            background: rgba(0, 0, 0, 0.3); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .btn-mode {{
            padding: 6px 12px; border-radius: 7px; font-size: 12px; font-weight: 500;
            background: transparent; border: none; color: var(--text-muted); cursor: pointer;
            display: flex; align-items: center; gap: 6px; transition: all 0.2s;
        }}
        .btn-mode.active {{
            background: rgba(255, 255, 255, 0.14); color: #FFFFFF; font-weight: 600;
        }}

        /* Stage View Mode */
        .app-showcase-box {{
            background: var(--glass-card); border-radius: 24px;
            border: 1px solid transparent; border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side); border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            padding: 24px; margin-bottom: 32px;
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

        /* Gallery Grid View */
        .projects-gallery-grid {{
            display: none; grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
            gap: 24px; margin-bottom: 32px;
        }}
        .projects-gallery-grid.active {{ display: grid; }}

        .gallery-card {{
            background: var(--glass-card); border-radius: 20px;
            border: 1px solid transparent; border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side); border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            display: flex; flex-direction: column; overflow: hidden; padding: 20px;
            transition: all 0.25s;
        }}
        .gallery-card:hover {{
            background: var(--glass-card-hover); border-top-color: rgba(255, 255, 255, 0.35);
            transform: translateY(-2px); box-shadow: 0 18px 42px rgba(0, 0, 0, 0.55);
        }}

        .gallery-card-top {{ display: flex; align-items: center; gap: 14px; margin-bottom: 12px; }}
        .gallery-icon-box {{
            width: 44px; height: 44px; border-radius: 12px;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(59, 130, 246, 0.25));
            border: 1px solid rgba(56, 189, 248, 0.3); display: flex; align-items: center; justify-content: center;
            color: #38BDF8; flex-shrink: 0;
        }}
        .gallery-title-wrap h3 {{ font-size: 16px; font-weight: 700; }}
        .gallery-meta-tags {{ display: flex; align-items: center; gap: 6px; margin-top: 4px; flex-wrap: wrap; }}
        .tag-version {{ font-size: 10.5px; font-weight: 600; padding: 2px 6px; border-radius: 5px; background: rgba(59, 130, 246, 0.15); color: #60A5FA; }}
        .tag-status {{ font-size: 10.5px; font-weight: 600; padding: 2px 6px; border-radius: 5px; background: rgba(16, 185, 129, 0.15); color: #34D399; }}
        .tag-folder {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: var(--text-muted); }}

        .gallery-card-desc {{ font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 16px; }}

        .gallery-preview-frame {{
            width: 100%; height: 340px; border-radius: 12px; overflow: hidden; background: #050508;
            border: 1px solid rgba(255, 255, 255, 0.06); margin-bottom: 16px;
        }}
        .gallery-preview-frame iframe {{ width: 100%; height: 100%; border: none; }}

        .gallery-card-bottom {{
            display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: auto;
        }}
        .btn-card-action {{
            display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px;
            border-radius: 8px; font-size: 12px; font-weight: 600;
            background: linear-gradient(135deg, #06B6D4, #3B82F6); color: #FFFFFF;
            border: none; cursor: pointer; transition: transform 0.2s;
        }}
        .btn-card-action:hover {{ transform: scale(1.02); }}
        .btn-card-icon {{
            width: 32px; height: 32px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.05); color: var(--text-secondary); cursor: pointer;
            display: flex; align-items: center; justify-content: center; transition: all 0.2s;
        }}
        .btn-card-icon:hover {{ background: rgba(255, 255, 255, 0.12); color: #FFFFFF; }}
        .btn-card-launch {{
            width: 32px; height: 32px; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.4);
            background: rgba(59, 130, 246, 0.2); color: #93C5FD; text-decoration: none;
            display: flex; align-items: center; justify-content: center; transition: all 0.2s;
        }}
        .btn-card-launch:hover {{ background: rgba(59, 130, 246, 0.35); color: #FFFFFF; }}

        /* Add Project Card */
        .add-project-card {{
            border-style: dashed; border-color: rgba(255, 255, 255, 0.15);
            background: rgba(255, 255, 255, 0.015); display: flex; align-items: center; justify-content: center;
            text-align: center; min-height: 480px;
        }}
        .add-card-inner {{ max-width: 360px; display: flex; flex-direction: column; align-items: center; }}
        .add-icon-box {{
            width: 54px; height: 54px; border-radius: 16px; background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12); display: flex; align-items: center; justify-content: center;
            color: var(--accent-cyan); margin-bottom: 14px;
        }}
        .add-card-inner h3 {{ font-size: 16px; font-weight: 700; margin-bottom: 6px; }}
        .add-card-inner p {{ font-size: 12.5px; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.5; }}
        .add-instructions {{
            background: #050508; border-radius: 10px; padding: 10px 14px; border: 1px solid rgba(255, 255, 255, 0.08);
            font-family: 'JetBrains Mono', monospace; font-size: 11px; text-align: left; width: 100%;
            margin-bottom: 16px; color: #93C5FD;
        }}
        .code-line {{ margin-bottom: 4px; }}
        .btn-blueprint {{
            display: inline-flex; align-items: center; gap: 7px; padding: 8px 16px; border-radius: 10px;
            font-size: 12.5px; font-weight: 600; text-decoration: none; color: #FFFFFF;
            background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.2s;
        }}
        .btn-blueprint:hover {{ background: rgba(255, 255, 255, 0.16); }}

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

        @media (max-width: 768px) {{
            .hub-header {{ padding: 12px 18px; }}
            .hub-main {{ padding: 16px 18px; }}
            .projects-gallery-grid {{ grid-template-columns: 1fr; }}
            .app-live-stage {{ height: 540px; }}
        }}
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
                <i data-lucide="folder-kanban"></i>
            </div>
            <div class="brand-text">
                <h1>Glass<span>OS</span> Web Applications Studio</h1>
                <p>Portofolio & Workbench Seluruh Proyek di <code>projects/</code></p>
            </div>
        </div>

        <div class="header-actions">
            <a href="index.html" class="action-link-btn" title="Master Gateway Portal">
                <i data-lucide="home"></i> Gateway
            </a>
            <a href="ui/components/glass/showcase.html" class="action-link-btn" title="Koleksi Komponen Kaca">
                <i data-lucide="gem"></i> Glass Components (21)
            </a>
            <a href="ui/components/raw/showcase.html" class="action-link-btn" title="Koleksi Komponen Baku">
                <i data-lucide="code-2"></i> Raw HTML (9)
            </a>
        </div>
    </header>

    <main class="hub-main">

        <!-- Hero Banner -->
        <section class="hero-banner">
            <span class="hero-tag"><i data-lucide="boxes"></i> Projects Collection Layer</span>
            <h2 class="hero-title">Koleksi Aplikasi Web Mandiri</h2>
            <p class="hero-desc">
                Ruang kerja terpusat untuk menguji dan mengeksplorasi seluruh aplikasi web utuh yang berada di dalam folder <code>projects/</code>. Setiap proyek siap dijalankan dalam simulator multi-viewport atau diluncurkan penuh ke tab browser baru.
            </p>
        </section>

        <!-- Project Selection & View Mode Bar -->
        <div class="projects-selection-bar">
            <div class="project-tabs-cluster">
                <button class="proj-tab-btn active" id="tab-file-manager" onclick="switchToProject('file-manager')">
                    <i data-lucide="cloud"></i> Cloud File Manager
                    <span class="badge-pill">v2.4</span>
                </button>
                <button class="proj-tab-btn" id="tab-ai-studio" onclick="switchToProject('ai-studio')">
                    <i data-lucide="sparkles"></i> AI Agent Studio
                    <span class="badge-pill">v1.0</span>
                </button>
            </div>

            <div class="mode-toggle-cluster">
                <button class="btn-mode active" id="mode-stage" onclick="setViewMode('stage')">
                    <i data-lucide="monitor"></i> Stage View
                </button>
                <button class="btn-mode" id="mode-gallery" onclick="setViewMode('gallery')">
                    <i data-lucide="layout-grid"></i> Gallery View
                </button>
            </div>
        </div>

        <!-- 1. STAGE VIEW (Active Selected Project Spotlight) -->
        <section class="app-showcase-box" id="stageSection">
            
            <div class="app-card-topbar">
                <div class="app-meta-header">
                    <div class="app-icon-badge" id="stageIconBox">
                        <i data-lucide="cloud"></i>
                    </div>
                    <div class="app-title-group">
                        <h2>
                            <span id="stageTitle">GlassOS Cloud File Manager</span>
                            <span class="app-version-badge" id="stageVersionBadge">v2.4 Production Ready</span>
                        </h2>
                        <p id="stageDesc">Sistem Operasi Manajemen Berkas Awan & Produktivitas AI Berbasis Glass Dark Premium</p>
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

                    <button class="btn-tool-secondary" onclick="openActiveAppModal('PROJECT_SPEC.md')">
                        <i data-lucide="book-open"></i> Spesifikasi
                    </button>
                    <button class="btn-tool-secondary" onclick="openActiveAppModal('index.html')">
                        <i data-lucide="code"></i> Kode Sumber
                    </button>
                    <a href="projects/file-manager/index.html" target="_blank" class="btn-launch-primary" id="stageLaunchBtn">
                        <i data-lucide="external-link"></i> Jalankan Layar Penuh
                    </a>
                </div>
            </div>

            <!-- Live Interactive Stage -->
            <div class="app-live-stage">
                <div class="app-frame-wrapper" id="appFrameWrapper">
                    <iframe id="stageIframe" src="projects/file-manager/index.html" title="GlassOS Live Preview"></iframe>
                </div>
            </div>

            <!-- Architecture & Component Integration Map -->
            <div class="app-architecture-grid">
                <div>
                    <h3 class="arch-col-title">
                        <i data-lucide="boxes" style="color: var(--accent-cyan);"></i> Komponen Terintegrasi
                    </h3>
                    <p class="arch-desc" id="stageArchDesc">
                        Komponen Glass Dark Premium yang dirakit secara modular di dalam aplikasi ini:
                    </p>
                    <div class="components-pills-wrap" id="stageComponentsWrap">
                        <!-- Dynamically filled -->
                    </div>
                </div>

                <div>
                    <h3 class="arch-col-title">
                        <i data-lucide="cpu" style="color: #A78BFA;"></i> Fitur Rekayasa & Arsitektur
                    </h3>
                    <ul class="spec-list" id="stageFeaturesList">
                        <!-- Dynamically filled -->
                    </ul>
                </div>
            </div>

        </section>

        <!-- 2. GALLERY GRID VIEW (All Projects Side-by-Side) -->
        <section class="projects-gallery-grid" id="gallerySection">
{gallery_cards_html}
        </section>

    </main>

    <!-- Code & Spec Modal -->
    <div class="modal-overlay" id="appModal">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title-wrap">
                    <h3 id="modalProjectTitle">Project Source & Specs</h3>
                    <p id="modalProjectPath">projects/...</p>
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
                    <i data-lucide="file-code"></i> index.html (Aplikasi)
                </button>
                <button class="code-tab-btn" id="tab-btn-spec" onclick="switchAppTab('PROJECT_SPEC.md')">
                    <i data-lucide="book-open"></i> PROJECT_SPEC.md (Spesifikasi)
                </button>
            </div>

            <div class="modal-tab-subbar">
                <span class="subbar-file-path" id="modalActiveFilePath">projects/.../index.html</span>
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

    <script type="application/json" id="appsDbJson">
{apps_escaped_json}
    </script>
    <script type="application/json" id="projectsMetaJson">
{projects_meta_json}
    </script>

    <script>
        let APPS_DB = {{}};
        let PROJECTS_META = [];
        try {{
            APPS_DB = JSON.parse(document.getElementById('appsDbJson').textContent);
            PROJECTS_META = JSON.parse(document.getElementById('projectsMetaJson').textContent);
        }} catch(e) {{
            console.error('Failed to parse apps database:', e);
        }}

        let activeProjectId = "file-manager";
        let modalProjectId = "file-manager";
        let currentTab = "index.html";

        lucide.createIcons();
        renderActiveProjectData();

        function setViewMode(mode) {{
            const stageSec = document.getElementById('stageSection');
            const gallerySec = document.getElementById('gallerySection');
            const btnStage = document.getElementById('mode-stage');
            const btnGallery = document.getElementById('mode-gallery');

            if (mode === 'stage') {{
                stageSec.style.display = 'block';
                gallerySec.classList.remove('active');
                btnStage.classList.add('active');
                btnGallery.classList.remove('active');
            }} else {{
                stageSec.style.display = 'none';
                gallerySec.classList.add('active');
                btnStage.classList.remove('active');
                btnGallery.classList.add('active');
            }}
        }}

        function switchToProject(pid) {{
            activeProjectId = pid;
            modalProjectId = pid;

            document.querySelectorAll('.proj-tab-btn').forEach(b => {{
                b.classList.toggle('active', b.id === `tab-${{pid}}`);
            }});

            renderActiveProjectData();
            setViewMode('stage');
        }}

        function renderActiveProjectData() {{
            const p = PROJECTS_META.find(x => x.id === activeProjectId) || PROJECTS_META[0];
            if (!p) return;

            document.getElementById('stageTitle').innerText = p.title;
            document.getElementById('stageVersionBadge').innerText = `${{p.version}} ${{p.status}}`;
            document.getElementById('stageDesc').innerText = p.desc;
            document.getElementById('stageIframe').src = `${{p.folder}}/index.html`;
            document.getElementById('stageLaunchBtn').href = `${{p.folder}}/index.html`;

            const iconBox = document.getElementById('stageIconBox');
            iconBox.innerHTML = `<i data-lucide="${{p.icon}}"></i>`;

            // Render Components Pills
            const compWrap = document.getElementById('stageComponentsWrap');
            compWrap.innerHTML = (p.components || []).map(c => `
                <a href="${{c[2]}}" class="comp-link-pill">
                    <i data-lucide="${{c[1]}}"></i> ${{c[0]}}
                </a>
            `).join('');

            // Render Features
            const featList = document.getElementById('stageFeaturesList');
            featList.innerHTML = (p.features || []).map(f => `
                <li class="spec-item">
                    <i data-lucide="check"></i>
                    <div>${{f}}</div>
                </li>
            `).join('');

            if (window.lucide) lucide.createIcons();
        }}

        function setAppViewport(width, btn) {{
            document.querySelectorAll('.vp-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('appFrameWrapper').style.maxWidth = width;
        }}

        function openActiveAppModal(filename) {{
            openAppModal(activeProjectId, filename);
        }}

        function openAppModal(pid, filename) {{
            modalProjectId = pid;
            const p = PROJECTS_META.find(x => x.id === pid) || {{}};
            document.getElementById('modalProjectTitle').innerText = `${{p.title || pid}} Source & Specs`;
            document.getElementById('modalProjectPath').innerText = `projects/${{pid}}/`;
            document.getElementById('appModal').classList.add('active');
            switchAppTab(filename || 'index.html');
        }}

        function switchAppTab(filename) {{
            currentTab = filename;
            document.getElementById('tab-btn-index').classList.toggle('active', filename === 'index.html');
            document.getElementById('tab-btn-spec').classList.toggle('active', filename === 'PROJECT_SPEC.md');

            const projFiles = APPS_DB[modalProjectId] || {{}};
            const code = projFiles[filename] || "";
            document.getElementById('modalActiveFilePath').innerText = `projects/${{modalProjectId}}/${{filename}}`;
            
            const lines = code ? code.split('\\n').length : 0;
            const kb = (new Blob([code]).size / 1024).toFixed(1);
            document.getElementById('modalActiveFileStats').innerText = `${{lines}} baris (${{kb}} KB)`;

            document.getElementById('modalAppCodeSnippet').innerText = code;
        }}

        function closeAppModal() {{
            document.getElementById('appModal').classList.remove('active');
        }}

        async function copyAppCode() {{
            const projFiles = APPS_DB[modalProjectId] || {{}};
            const code = projFiles[currentTab] || "";
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

print("web-apps.html rebuilt as multi-project collection successfully!")
print("ALL CORE PAGES REBUILT AND OPTIMIZED!")
