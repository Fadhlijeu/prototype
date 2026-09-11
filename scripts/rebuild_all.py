import os
import json
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLASS_DIR = os.path.join(ROOT, "ui", "web", "components", "glass")
RAW_DIR = os.path.join(ROOT, "ui", "web", "components", "raw")
APPS_DIR = os.path.join(ROOT, "ui", "web", "apps")

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
    ("button-glass", "Glass Buttons Collection", "Action / Buttons", "Molecule", "inputs", ""),
    ("chat-input-bar", "Glass Chat Input Bar", "Form Input / AI Prompt", "Molecule", "inputs", ""),
    ("input-field-glass", "Glass Form Input Fields", "Form / Inputs", "Molecule", "inputs", ""),
    ("prompt-pills-row", "Prompt Pills Quick Scroller", "Chips / Action Pills", "Molecule", "inputs", ""),
    ("thinking-effort-selector", "Thinking Effort Selector", "Segmented Stepper", "Atomic", "inputs", ""),
    ("toggle-switch-glass", "Glass Toggle Switch", "Control / Switch", "Atomic", "inputs", ""),
    ("checkbox-glass", "Glass Checkbox & Radio", "Control / Checkbox", "Atomic", "inputs", ""),
    ("dropdown-select-glass", "Glass Floating Dropdown", "Control / Select", "Molecule", "inputs", ""),
    ("ai-model-selector", "AI Model Selector Card", "Selection Control", "Molecule", "cards", ""),
    ("frosted-folder-card", "Frosted Folder Card", "File System / Card", "Molecule", "cards", ""),
    ("aurora-storage-card", "Aurora Storage Card", "Data Display / Gauge", "Molecule", "cards", ""),
    ("progress-bar-glass", "Glass Glowing Progress Bar", "Display / Progress", "Atomic", "cards", ""),
    ("avatar-badge-glass", "Glass Avatar with Status", "Display / Avatar", "Atomic", "cards", ""),
    ("glass-dock-navigation", "Floating Glass Dock", "Navigation / Spring Dock", "Molecule", "navigation", ""),
    ("glass-sidepanel", "Productivity Glass Sidepanel", "Navigation / Desktop Drawer", "Organism", "navigation", "span-tall"),
    ("swirl-bottom-sheet", "Swirl Refraction Bottom Sheet", "Overlay / Canvas 2D Refraction", "Organism", "overlays", ""),
    ("modal-dialog-glass", "Glass Modal Dialog", "Overlay / Centered Dialog", "Molecule", "overlays", ""),
    ("toast-notification-glass", "Glass Toast Notification", "Feedback / Toast Alert", "Molecule", "overlays", ""),
    ("tooltip-glass", "Glass Micro Tooltip", "Feedback / Tooltip", "Atomic", "overlays", ""),
    ("telemetry-activity-chart", "Telemetry Activity Chart", "Analytics / Bar Histogram", "Molecule", "telemetry", ""),
    ("ai-agent-scenery", "AI Agent Studio Scenery", "Complete Workspace Scenery", "Scenery", "scenery", "span-tall"),
    ("lockscreen-pin-glass", "Phone Lockscreen PIN Keypad", "Security / PIN Keypad", "Organism", "overlays", "span-tall"),
    ("elastic-clock-glass", "Elastic Lockscreen Glass Clock", "Widget / Clock & Gestures", "Organism", "overlays", "span-tall"),
    ("mobile-control-center-glass", "Mobile Control Center Shade", "System / Quick Settings", "Organism", "overlays", "span-tall")
]

glass_files_db = {"css.css": shared_css_code}
glass_cards_html = ""

for folder, title, cat, badge, filter_cat, span_class in glass_components_metadata:
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
    card_classes = f"component-card {span_class}".strip()
    
    # Map aspect ratio for optimal SVG Blob matching
    if span_class == "span-tall":
        ratio_attr = "9:16"
        ratio_class = "ratio-9-16"
        ratio_label = "9:16"
    elif folder in ["button-glass", "toggle-switch-glass", "checkbox-glass", "dropdown-select-glass", "avatar-badge-glass", "thinking-effort-selector", "progress-bar-glass", "prompt-pills-row", "toast-notification-glass", "tooltip-glass", "glass-dock-navigation"]:
        ratio_attr = "1:1"
        ratio_class = "ratio-1-1"
        ratio_label = "1:1"
    else:
        ratio_attr = "4:5"
        ratio_class = "ratio-4-5"
        ratio_label = "4:5"

    glass_cards_html += f"""
            <!-- Component: {title} -->
            <article class="{card_classes}" data-cat="{filter_cat}" id="{card_id}">
                <div class="card-top">
                    <div class="card-meta-left">
                        <div class="card-name">{title}</div>
                        <div class="card-category">{cat}</div>
                    </div>
                    <span class="{badge_class}">{badge}</span>
                </div>
                <div class="card-actions-bar">
                    <button class="btn-card-full" onclick="openComponentStudio('{folder}', '{title}', 'preview')" title="Buka Component Studio Pop-up Full Screen">
                        <i data-lucide="maximize-2"></i> Full
                    </button>
                    <!-- Per-Component Background Switcher (Dark | Blob SVG Ratio: {ratio_label}) -->
                    <div class="comp-bg-switcher" id="bg-switcher-{folder}" title="Ganti latar khusus komponen ini ({ratio_label})">
                        <span class="comp-bg-text">BG:</span>
                        <button type="button" class="btn-comp-bg active" data-bg="dark" onclick="setComponentBg('{folder}', 'dark', this)" title="Latar Hitam Default">
                            <span class="swatch-dot dot-black"></span>
                        </button>
                        <button type="button" class="btn-comp-bg" data-bg="blob" onclick="setComponentBg('{folder}', 'blob', this)" title="Latar Blob SVG ({ratio_label})">
                            <span class="swatch-dot dot-blob"></span>
                        </button>
                    </div>
                    <div class="card-actions-tools">
                        <button class="btn-card-tool highlight" onclick="quickCopyAllInOne('{folder}')" title="Salin Kode All-in-One Langsung">
                            <i data-lucide="copy"></i> Salin
                        </button>
                        <button class="btn-card-tool download" onclick="quickDownloadAllInOne('{folder}')" title="Unduh File HTML All-in-One Langsung">
                            <i data-lucide="download"></i> Unduh
                        </button>
                    </div>
                </div>
                <div class="card-preview-zone {ratio_class}" id="preview-zone-{folder}" data-blob-ratio="{ratio_attr}" data-comp-bg="dark">
                    <div class="preview-resizer-wrapper">
                        <iframe src="{folder}/{aio_file}" id="iframe-{folder}" title="{title} Preview"></iframe>
                    </div>
                </div>
            </article>
"""

glass_escaped_json = safe_json_embed(glass_files_db)

glass_showcase_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glass Dark Premium Showroom — 24 All-in-One Components</title>
    <meta name="description" content="Koleksi 24 Komponen UI/UX Glass Dark Premium all-in-one mandiri dengan resize preview, multi-file code tabs, dan copy instant.">
    <link rel="icon" type="image/svg+xml" href="../../../../favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Shared Design System Tokens (Single Source of Truth) -->
    <link rel="stylesheet" href="css.css">
    <style>

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


        /* Dedicated Grid Background Switcher */
        .grid-bg-selector {{
            display: flex; align-items: center; gap: 4px; padding: 4px;
            background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
        }}
        .grid-bg-label {{
            font-size: 11.5px; font-weight: 600; color: var(--text-muted); padding: 0 8px;
            display: flex; align-items: center; gap: 5px;
        }}
        .grid-bg-label svg {{ width: 14px; height: 14px; }}
        .btn-grid-bg {{
            padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;
            background: transparent; border: none; color: var(--text-muted); cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-grid-bg:hover {{ color: var(--text-primary); }}
        .btn-grid-bg.active {{
            background: rgba(56, 189, 248, 0.18); color: #38BDF8; font-weight: 600;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }}

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

        /* Grid - Dense Bento Layout (Zero Holes / Gaps) */
        .showcase-grid {{
            margin: 12px 24px 48px;
            padding: 24px !important;
            width: calc(100% - 48px);
            box-sizing: border-box;
            display: grid;
            gap: 18px;
            grid-auto-flow: dense;
            grid-auto-rows: minmax(460px, auto);
            z-index: 5;
            transition: all 0.3s ease;
        }}
        .showcase-grid.cols-auto {{ grid-template-columns: repeat(auto-fill, minmax(min(100%, 360px), 1fr)); }}
        .showcase-grid.cols-1 {{ grid-template-columns: 1fr; max-width: 900px; margin: 12px auto 48px; width: 100%; }}
        .showcase-grid.cols-2 {{ grid-template-columns: repeat(2, 1fr); }}
        .showcase-grid.cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
        .showcase-grid.cols-4 {{ grid-template-columns: repeat(4, 1fr); }}

        /* Bento Grid Geometry: Vertical Rectangle & Horizontal Rectangle */
        @media (min-width: 800px) {{
            /* Horizontal Rectangle (AI Agent Studio Scenery): Spans 2 Columns */
            .showcase-grid.cols-auto .component-card.span-wide,
            .showcase-grid.cols-2 .component-card.span-wide,
            .showcase-grid.cols-3 .component-card.span-wide,
            .showcase-grid.cols-4 .component-card.span-wide {{
                grid-column: span 2;
                grid-row: span 1;
            }}

            /* Vertical Rectangle (Productivity Glass Sidepanel): Spans 2 Rows */
            .showcase-grid.cols-auto .component-card.span-tall,
            .showcase-grid.cols-2 .component-card.span-tall,
            .showcase-grid.cols-3 .component-card.span-tall,
            .showcase-grid.cols-4 .component-card.span-tall {{
                grid-row: span 2;
                min-height: 938px;
            }}
        }}

        @media (max-width: 799px) {{
            .component-card.span-wide,
            .component-card.span-tall {{
                grid-column: span 1 !important;
                grid-row: span 1 !important;
                min-height: 460px !important;
            }}
        }}

        /* Component Card - Unified Seamless Flex (No Blank Stretched Space) */
        .component-card {{
            position: relative; background: var(--glass-card); border-radius: 20px;
            border: 1px solid transparent; border-top-color: var(--glass-border-top);
            border-left-color: var(--glass-border-side); border-right-color: var(--glass-border-side);
            border-bottom-color: var(--glass-border-bottom);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.08);
            display: flex; flex-direction: column; overflow: hidden;
            height: 100%; min-height: 460px;
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

        /* Card Action Bar (Clean & Spacious) */
        .card-actions-bar {{
            padding: 8px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0, 0, 0, 0.28);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            flex-shrink: 0;
            gap: 8px;
        }}
        .btn-card-full {{
            padding: 6px 14px;
            border-radius: 9px;
            font-size: 12px;
            font-weight: 600;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.22), rgba(139, 92, 246, 0.25));
            border: 1px solid rgba(56, 189, 248, 0.45);
            color: #FFFFFF;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s var(--ease-spring);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
        }}
        .btn-card-full svg {{ width: 13px; height: 13px; color: #38BDF8; }}
        .btn-card-full:hover {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.38), rgba(139, 92, 246, 0.42));
            border-color: rgba(56, 189, 248, 0.8);
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
            transform: translateY(-1px);
        }}

        .card-actions-tools {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-card-tool {{
            padding: 5px 10px;
            border-radius: 7px;
            font-size: 11.5px;
            font-weight: 500;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-secondary);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            text-decoration: none;
            transition: all 0.18s;
        }}
        .btn-card-tool svg {{ width: 12px; height: 12px; }}
        .btn-card-tool:hover {{
            background: rgba(255, 255, 255, 0.12);
            color: #FFFFFF;
            border-color: rgba(255, 255, 255, 0.2);
        }}
        .btn-card-tool.highlight {{
            background: rgba(56, 189, 248, 0.1);
            border-color: rgba(56, 189, 248, 0.25);
            color: #93C5FD;
        }}
        .btn-card-tool.highlight:hover {{
            background: rgba(56, 189, 248, 0.22);
            color: #FFFFFF;
        }}
        .btn-card-tool.download {{
            background: rgba(56, 189, 248, 0.08);
            border-color: rgba(56, 189, 248, 0.2);
            color: #7DD3FC;
        }}
        .btn-card-tool.download:hover {{
            background: rgba(56, 189, 248, 0.2);
            border-color: rgba(56, 189, 248, 0.5);
            color: #FFFFFF;
        }}
        .btn-card-tool.new-tab,
        .btn-card-tool.solo {{
            color: var(--text-muted);
        }}
        .btn-card-tool.new-tab:hover,
        .btn-card-tool.solo:hover {{
            color: #C084FC;
        }}

        /* Preview Zone - Direct Interactive Component Viewport */
        .card-preview-zone {{
            flex: 1; width: 100%; min-height: 400px;
            display: flex; align-items: stretch; justify-content: center;
            background: transparent; position: relative;
            overflow: hidden;
            padding: 0;
        }}
        .card-preview-zone .preview-resizer-wrapper {{
            width: 100%; height: 100%; min-height: 100%;
            display: flex; align-items: stretch; justify-content: center;
            margin: 0 auto; flex-shrink: 0;
            background: transparent;
        }}
        .card-preview-zone iframe {{
            width: 100%; height: 100%; min-height: 100%; border: none; background: transparent;
            display: block; pointer-events: auto;
        }}

        /* ============================================================ */
        /* COMPONENT STUDIO POPUP MODAL (Fullscreen Interactive Studio) */
        /* ============================================================ */
        .modal-overlay {{
            position: fixed; inset: 0; z-index: 1000;
            background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            display: flex; align-items: center; justify-content: center;
            opacity: 0; pointer-events: none; transition: opacity 0.25s ease;
            padding: 24px;
        }}
        .modal-overlay.active {{
            opacity: 1; pointer-events: auto;
        }}

        .studio-modal-card {{
            width: 96vw; max-width: 1560px; height: 92vh; max-height: 1020px;
            background: #08080C; border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 28px 90px rgba(0, 0, 0, 0.85), inset 0 1px 0 rgba(255, 255, 255, 0.15);
            display: flex; flex-direction: column; overflow: hidden;
            transform: scale(0.97); transition: transform 0.25s var(--ease-spring);
        }}
        .modal-overlay.active .studio-modal-card {{
            transform: scale(1);
        }}

        /* Studio Header */
        .studio-header {{
            padding: 12px 24px; background: #0C0D14;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            display: flex; align-items: center; justify-content: space-between;
            gap: 16px; flex-shrink: 0;
        }}
        .studio-title-block {{ display: flex; flex-direction: column; gap: 2px; }}
        .studio-badge-row {{ display: flex; align-items: center; gap: 8px; }}
        .studio-type-badge {{
            font-size: 10px; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.06em; padding: 2px 6px; border-radius: 4px;
            background: rgba(56, 189, 248, 0.15); color: #38BDF8;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}
        .studio-path-tag {{
            font-family: 'JetBrains Mono', monospace; font-size: 11px;
            color: var(--text-muted);
        }}
        .studio-title {{
            font-size: 16px; font-weight: 700; color: #FFFFFF;
            letter-spacing: -0.01em; margin: 0;
        }}

        /* Mode Switcher Tabs */
        .studio-mode-switcher {{
            display: inline-flex; padding: 4px; border-radius: 12px;
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08);
            gap: 4px;
        }}
        .btn-mode-tab {{
            padding: 6px 16px; border-radius: 8px; border: 1px solid transparent;
            background: transparent; color: var(--text-muted); font-size: 12.5px;
            font-weight: 600; cursor: pointer; display: inline-flex; align-items: center;
            gap: 7px; transition: all 0.2s;
        }}
        .btn-mode-tab svg {{ width: 14px; height: 14px; }}
        .btn-mode-tab:hover {{ color: var(--text-primary); }}
        .btn-mode-tab.active {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.22), rgba(139, 92, 246, 0.25));
            border-color: rgba(56, 189, 248, 0.4);
            color: #FFFFFF; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }}

        /* Studio Header Right */
        .studio-header-right {{ display: flex; align-items: center; gap: 8px; }}
        .btn-studio-action {{
            padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;
            background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-secondary); cursor: pointer; display: inline-flex;
            align-items: center; gap: 6px; text-decoration: none; transition: all 0.2s;
        }}
        .btn-studio-action svg {{ width: 13px; height: 13px; }}
        .btn-studio-action:hover {{ background: rgba(255, 255, 255, 0.12); color: #FFFFFF; }}
        .btn-studio-action.highlight {{
            background: rgba(56, 189, 248, 0.15); border-color: rgba(56, 189, 248, 0.4);
            color: #38BDF8; font-weight: 600;
        }}
        .btn-studio-action.highlight:hover {{
            background: rgba(56, 189, 248, 0.25); color: #FFFFFF;
        }}
        .studio-close-btn {{
            width: 32px; height: 32px; border-radius: 8px;
            background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted); cursor: pointer; display: flex;
            align-items: center; justify-content: center; transition: all 0.2s;
        }}
        .studio-close-btn:hover {{
            background: rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.4);
            color: #EF4444;
        }}
        .studio-close-btn svg {{ width: 16px; height: 16px; }}

        /* Studio Panels */
        .studio-panel {{
            display: none; flex: 1; min-height: 0; flex-direction: column; overflow: hidden;
        }}
        .studio-panel.active {{
            display: flex;
        }}

        /* Studio Toolbar (Preset Pixel & Slider Rasio Ukuran) */
        .studio-toolbar {{
            padding: 10px 24px; background: #11121B;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            display: flex; align-items: center; justify-content: space-between;
            flex-wrap: wrap; gap: 14px; flex-shrink: 0;
        }}
        .studio-toolbar-section {{ display: flex; align-items: center; gap: 8px; }}
        .toolbar-label {{
            font-size: 12px; font-weight: 600; color: var(--text-muted);
            display: inline-flex; align-items: center; gap: 5px; text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        .toolbar-label svg {{ width: 13px; height: 13px; color: #38BDF8; }}

        .presets-group {{ display: flex; align-items: center; gap: 5px; flex-wrap: wrap; }}
        .btn-studio-preset {{
            padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;
            background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-secondary); cursor: pointer; display: inline-flex;
            align-items: center; gap: 6px; transition: all 0.15s;
        }}
        .btn-studio-preset svg {{ width: 12px; height: 12px; }}
        .btn-studio-preset:hover {{
            background: rgba(255, 255, 255, 0.08); color: #FFFFFF; border-color: rgba(255, 255, 255, 0.18);
        }}
        .btn-studio-preset.active {{
            background: rgba(56, 189, 248, 0.18); border-color: rgba(56, 189, 248, 0.45);
            color: #38BDF8; font-weight: 600; box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        }}

        .studio-toolbar-divider {{
            width: 1px; height: 24px; background: rgba(255, 255, 255, 0.08);
        }}

        .studio-slider-box {{
            display: inline-flex; align-items: center; gap: 10px;
            padding: 4px 12px; border-radius: 10px;
            background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .studio-slider-range {{
            -webkit-appearance: none; appearance: none;
            width: 130px; height: 5px; border-radius: 3px;
            background: rgba(255, 255, 255, 0.15); outline: none; cursor: pointer;
            transition: background 0.2s;
        }}
        .studio-slider-range::-webkit-slider-thumb {{
            -webkit-appearance: none; appearance: none;
            width: 14px; height: 14px; border-radius: 50%;
            background: #38BDF8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.8);
            cursor: pointer; transition: transform 0.15s;
        }}
        .studio-slider-range::-webkit-slider-thumb:hover {{
            transform: scale(1.25);
        }}
        .studio-slider-badge {{
            font-size: 11.5px; font-family: 'JetBrains Mono', monospace;
            color: #38BDF8; min-width: 75px; text-align: center; font-weight: 600;
        }}
        .btn-reset-studio-slider {{
            background: transparent; border: none; color: var(--text-muted);
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            padding: 3px; border-radius: 4px; transition: color 0.15s;
        }}
        .btn-reset-studio-slider:hover {{ color: #FFFFFF; }}
        .btn-reset-studio-slider svg {{ width: 13px; height: 13px; }}

        .btn-studio-tool {{
            padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 500;
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-secondary); cursor: pointer; display: inline-flex;
            align-items: center; gap: 6px; transition: all 0.2s;
        }}
        .btn-studio-tool svg {{ width: 13px; height: 13px; }}
        .btn-studio-tool:hover {{ background: rgba(255, 255, 255, 0.1); color: #FFFFFF; }}

        /* Viewport Canvas Stage */
        .studio-canvas-stage {{
            flex: 1; width: 100%; min-height: 0;
            background: radial-gradient(circle at center, #13141F 0%, #06070B 100%);
            overflow: auto; display: flex; align-items: stretch; justify-content: center;
            padding: 20px; position: relative;
        }}
        .studio-viewport-wrapper {{
            width: 100%; max-width: 100%; height: 100%; min-height: 100%;
            border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 16px 50px rgba(0, 0, 0, 0.7); overflow: hidden;
            background: #07070A;
            transition: max-width 0.25s var(--ease-spring), width 0.25s var(--ease-spring);
            position: relative; display: flex; flex-direction: column;
            margin: 0 auto;
        }}
        .studio-viewport-wrapper iframe {{
            width: 100%; height: 100%; flex: 1; border: none; display: block;
        }}
        .viewport-meta-floating {{
            position: absolute; bottom: 10px; right: 14px;
            padding: 3px 10px; border-radius: 6px;
            background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(6px);
            font-size: 11px; font-family: 'JetBrains Mono', monospace;
            color: #94A3B8; border: 1px solid rgba(255, 255, 255, 0.08);
            pointer-events: none; z-index: 10;
        }}

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
            .showcase-header {{
                padding: 10px 14px;
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            .header-actions {{
                width: 100%;
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 4px;
            }}
            .app-highlight-banner {{
                margin: 12px 14px 0;
                padding: 14px 16px;
                flex-direction: column;
                align-items: stretch;
                gap: 12px;
            }}
            .btn-banner-cta {{
                width: 100%;
                justify-content: center;
            }}
            .controls-bar {{
                padding: 12px 14px 6px;
                flex-direction: column;
                align-items: stretch;
                gap: 10px;
            }}
            .filter-tabs {{
                width: 100%;
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
            }}
            .controls-right {{
                width: 100%;
                justify-content: space-between;
            }}
            .search-box {{
                width: 100%;
            }}
            .showcase-grid,
            .showcase-grid.cols-auto,
            .showcase-grid.cols-1,
            .showcase-grid.cols-2,
            .showcase-grid.cols-3,
            .showcase-grid.cols-4 {{
                grid-template-columns: 1fr !important;
                padding: 10px 14px 48px !important;
                gap: 16px !important;
            }}
            .component-card {{
                min-height: 440px;
                border-radius: 16px;
            }}
            .card-preview-zone {{
                min-height: 320px;
            }}
            .studio-modal-card {{
                width: 100vw;
                height: 100vh;
                max-height: 100vh;
                margin: 0;
                border-radius: 0;
            }}
            .modal-overlay {{
                padding: 0;
            }}
            .studio-header {{
                padding: 10px 14px;
                flex-wrap: wrap;
                gap: 10px;
            }}
            .studio-mode-switcher {{
                order: 3;
                width: 100%;
                justify-content: center;
            }}
            .btn-mode-tab {{
                flex: 1;
                justify-content: center;
            }}
            .studio-toolbar {{
                padding: 8px 12px;
                gap: 8px;
            }}
            .presets-group {{
                overflow-x: auto;
                width: 100%;
                padding-bottom: 2px;
                scrollbar-width: none;
            }}
            .presets-group::-webkit-scrollbar {{ display: none; }}
            .studio-slider-box {{
                width: 100%;
                justify-content: space-between;
            }}
            .studio-slider-range {{
                flex: 1;
                width: auto;
            }}
        }}

        @media (max-width: 600px) {{
            .card-actions-bar {{
                padding: 6px 10px;
            }}
            .btn-card-tool.solo {{
                display: none !important;
            }}
            .layout-selector .btn-layout:nth-child(4),
            .layout-selector .btn-layout:nth-child(5) {{
                display: none !important;
            }}
        }}

                
                /* Per-Component Background Switcher */
        .comp-bg-switcher {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 6px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.2s;
        }}
        .comp-bg-text {{
            font-size: 10px;
            font-weight: 600;
            color: var(--text-muted);
            letter-spacing: 0.04em;
            margin-right: 2px;
        }}
        .btn-comp-bg {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            padding: 0;
            border-radius: 6px;
            background: transparent;
            border: 1px solid transparent;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-comp-bg:hover {{
            background: rgba(255, 255, 255, 0.12);
        }}
        .btn-comp-bg.active {{
            background: rgba(56, 189, 248, 0.22);
            border-color: #38BDF8;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
        }}
        .swatch-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            pointer-events: none;
        }}
        .dot-black {{
            background: #08080C;
            border: 1px solid rgba(255, 255, 255, 0.4);
        }}
        .dot-blob {{
            background: radial-gradient(circle at 70% 30%, #38BDF8 0%, #111F38 60%, #F59E0B 100%);
            border: 1px solid #38BDF8;
        }}

        /* Aspect Ratio Adaptive SVG Blob Backgrounds for Component Cards */
        .card-preview-zone.ratio-1-1[data-comp-bg="blob"],
        .card-preview-zone[data-blob-ratio="1:1"][data-comp-bg="blob"] {{
            background-color: #0D0D0D !important;
            background-image: url('blob_1-1.svg') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
        }}

        .card-preview-zone.ratio-4-5[data-comp-bg="blob"],
        .card-preview-zone[data-blob-ratio="4:5"][data-comp-bg="blob"] {{
            background-color: #0D0D0D !important;
            background-image: url('blob_4-5.svg') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
        }}

        .card-preview-zone.ratio-9-16[data-comp-bg="blob"],
        .card-preview-zone[data-blob-ratio="9:16"][data-comp-bg="blob"] {{
            background-color: #0D0D0D !important;
            background-image: url('blob_9-16.svg') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
        }}

        /* Default Dark Preview */
        .card-preview-zone[data-comp-bg="dark"],
        .card-preview-zone[data-comp-bg="black"] {{
            background-color: #08080C !important;
            background-image: none !important;
        }}

        /* Phone Viewport Preview Zones (Lockscreen PIN & Control Center) stay dark obsidian outside phone */
        #preview-zone-lockscreen-pin-glass,
        #preview-zone-lockscreen-pin-glass[data-comp-bg="blob"],
        #preview-zone-lockscreen-pin-glass[data-comp-bg="dark"],
        #preview-zone-mobile-control-center-glass,
        #preview-zone-mobile-control-center-glass[data-comp-bg="blob"],
        #preview-zone-mobile-control-center-glass[data-comp-bg="dark"] {{
            background-color: #08080C !important;
            background-image: none !important;
        }}

        /* Full-Width Showcase Grid Container (Clean solid dark obsidian, never wrapped with blob) */
        .showcase-grid,
        .showcase-grid[data-grid-bg="blob"],
        .showcase-grid[data-grid-bg="dark"] {{
            background: transparent !important;
            background-image: none !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            margin: 12px 24px 48px !important;
            padding: 24px !important;
            width: calc(100% - 48px) !important;
        }}

        /* Studio Modal Stage Backgrounds */
        .studio-canvas-stage[data-stage-bg="blob"] {{
            background-color: #0D0D0D !important;
            background-image: url('blob_2048x1156px.svg') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        .studio-canvas-stage[data-stage-bg="dark"] {{
            background: #08080C !important;
            background-image: none !important;
        }}
</style>
</head>
<body>

    <header class="showcase-header">
        <div class="brand-cluster">
            <div class="brand-badge">
                <i data-lucide="gem"></i>
            </div>
            <div class="brand-text">
                <h1>Proto<span>type</span> Glass Showcase</h1>
                <p>24 Komponen Glass Dark Premium All-in-One Mandiri</p>
            </div>
        </div>

        <div class="header-actions">

            <a href="../../../../index.html" class="btn-top-link" title="Master Gateway Portal">
                <i data-lucide="home"></i> Gateway
            </a>
            <a href="../../../../ui/web/apps.html" class="btn-top-link btn-highlight-webapp" title="Buka Halaman Khusus Web Applications">
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
                <p>Seluruh aplikasi web utuh berada di dalam folder <code>apps/</code> dan ditampilkan pada halaman studio tersendiri.</p>
            </div>
        </div>
        <a href="../../../../ui/web/apps.html" class="btn-banner-cta">
            <i data-lucide="folder-kanban"></i> Buka Web Applications Studio <i data-lucide="arrow-right"></i>
        </a>
    </div>

    <!-- Controls Bar with Filter and Layout Grid Switcher -->
    <div class="controls-bar">
        <div class="filter-tabs">
            <button class="filter-tab active" onclick="filterCategory('all', this)">Semua (24)</button>
            <button class="filter-tab" onclick="filterCategory('inputs', this)">Inputs</button>
            <button class="filter-tab" onclick="filterCategory('cards', this)">Cards</button>
            <button class="filter-tab" onclick="filterCategory('navigation', this)">Navigation</button>
            <button class="filter-tab" onclick="filterCategory('overlays', this)">Overlays</button>
            <button class="filter-tab" onclick="filterCategory('scenery', this)">Scenery</button>
        </div>

        <div class="controls-right">
            <!-- Grid Background Switcher (Dark | Blob Grid) -->
            <div class="grid-bg-selector">
                <span class="grid-bg-label"><i data-lucide="palette"></i> Grid BG:</span>
                <button type="button" class="btn-grid-bg active" data-bg="dark" onclick="setGridBg('dark')" title="Latar Grid Standar Obsidian">Dark</button>
                <button type="button" class="btn-grid-bg" data-bg="blob" onclick="setGridBg('blob')" title="Latar Grid Wallpaper Blob (Landscape 2048x1156)">Blob Grid</button>
            </div>

            <!-- Grid Layout Selector -->
            <div class="layout-selector">
                <span class="layout-label"><i data-lucide="grid"></i> Kolom:</span>
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

    <!-- Component Studio Modal (Fullscreen Interactive Popup) -->
    <div class="modal-overlay" id="componentStudioModal">
        <div class="studio-modal-card">
            <!-- Studio Header -->
            <header class="studio-header">
                <div class="studio-header-left">
                    <div class="studio-title-block">
                        <div class="studio-badge-row">
                            <span class="studio-type-badge" id="studioTypeBadge">Glass Component</span>
                            <span class="studio-path-tag" id="studioPathTag">ui/web/components/glass/...</span>
                        </div>
                        <h2 class="studio-title" id="studioComponentTitle">Glass Component Title</h2>
                    </div>
                </div>

                <!-- Mode Switcher Tabs: Live Preview vs Lihat Code -->
                <div class="studio-mode-switcher">
                    <button class="btn-mode-tab active" id="modePreviewBtn" onclick="switchStudioMode('preview')">
                        <i data-lucide="eye"></i> <span>Live Preview</span>
                    </button>
                    <button class="btn-mode-tab" id="modeCodeBtn" onclick="switchStudioMode('code')">
                        <i data-lucide="code-2"></i> <span>Lihat Code</span>
                    </button>
                </div>

                <!-- Header Quick Actions -->
                <div class="studio-header-right">
                    <button class="btn-studio-action highlight" id="studioCopyBtn" onclick="copyCurrentStudioCode()" title="Salin Kode ke Clipboard">
                        <i data-lucide="copy"></i> <span>Salin</span>
                    </button>
                    <button class="btn-studio-action" id="studioDownloadBtn" onclick="downloadCurrentStudioCode()" title="Unduh File Kode">
                        <i data-lucide="download"></i> <span>Unduh</span>
                    </button>
                    <a href="#" target="_blank" class="btn-studio-action solo-link" id="studioSoloLink" title="Buka Standalone File di Tab Baru">
                        <i data-lucide="external-link"></i> <span>Tab Baru</span>
                    </a>
                    <button class="studio-close-btn" onclick="closeComponentStudio()" title="Tutup Modal (Esc)">
                        <i data-lucide="x"></i>
                    </button>
                </div>
            </header>

            <!-- Mode 1: Live Interactive Viewport Studio -->
            <div class="studio-panel active" id="studioPreviewPanel">
                <!-- Studio Toolbar: Presets Pixel & Slider Rasio Ukuran -->
                <div class="studio-toolbar">
                    <div class="studio-toolbar-section">
                        <span class="toolbar-label"><i data-lucide="palette"></i> BG:</span>
                        <div class="presets-group">
                            <button type="button" class="btn-studio-preset btn-studio-bg active" data-bg="dark" onclick="setStudioBg('dark')">Dark</button>
                            <button type="button" class="btn-studio-preset btn-studio-bg" data-bg="blob" onclick="setStudioBg('blob')">Blob Wide</button>
                        </div>
                    </div>

                    <div class="studio-toolbar-divider"></div>

                    <div class="studio-toolbar-section presets-group">
                        <span class="toolbar-label"><i data-lucide="monitor"></i> Preset:</span>
                        <button class="btn-studio-preset active" data-preset="100%" onclick="setStudioPreset('100%', this)" title="Full Viewport (100%)">
                            <i data-lucide="maximize-2"></i> Full
                        </button>
                        <button class="btn-studio-preset" data-preset="1440px" onclick="setStudioPreset('1440px', this)" title="Desktop Ultra (1440px)">
                            <i data-lucide="monitor"></i> 1440px
                        </button>
                        <button class="btn-studio-preset" data-preset="1024px" onclick="setStudioPreset('1024px', this)" title="Laptop (1024px)">
                            <i data-lucide="laptop"></i> 1024px
                        </button>
                        <button class="btn-studio-preset" data-preset="768px" onclick="setStudioPreset('768px', this)" title="Tablet (768px)">
                            <i data-lucide="tablet"></i> 768px
                        </button>
                        <button class="btn-studio-preset" data-preset="375px" onclick="setStudioPreset('375px', this)" title="Mobile (375px)">
                            <i data-lucide="smartphone"></i> 375px
                        </button>
                    </div>

                    <div class="studio-toolbar-divider"></div>

                    <!-- Slider Rasio Ukuran -->
                    <div class="studio-toolbar-section slider-group">
                        <span class="toolbar-label"><i data-lucide="sliders-horizontal"></i> Slider Rasio:</span>
                        <div class="studio-slider-box" title="Geser untuk mengatur lebar preview secara fluid">
                            <input type="range" class="studio-slider-range" id="studioWidthSlider"
                                   min="320" max="1440" step="10" value="1440"
                                   oninput="setStudioSliderWidth(this.value)"
                                   aria-label="Atur lebar viewport komponen">
                            <span class="studio-slider-badge" id="studioSliderBadge">Full (100%)</span>
                            <button class="btn-reset-studio-slider" onclick="resetStudioWidth()" title="Reset ke Full (100%)">
                                <i data-lucide="rotate-ccw"></i>
                            </button>
                        </div>
                    </div>

                    <div class="studio-toolbar-right">
                        <button class="btn-studio-tool" onclick="reloadStudioIframe()" title="Muat Ulang Iframe Preview">
                            <i data-lucide="refresh-cw"></i> <span>Reload</span>
                        </button>
                    </div>
                </div>

                <!-- Live Viewport Canvas Stage -->
                <div class="studio-canvas-stage">
                    <div class="studio-viewport-wrapper" id="studioViewportWrapper">
                        <div class="viewport-meta-floating">
                            <span id="viewportDimensionIndicator">100% (Full Width)</span>
                        </div>
                        <iframe src="" id="studioIframe" title="Component Live Preview"></iframe>
                    </div>
                </div>
            </div>

            <!-- Mode 2: Multi-file Code Studio -->
            <div class="studio-panel" id="studioCodePanel">
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

        let activeFolder = "";
        let activeTitle = "";
        let activeFile = "";
        let currentMode = "preview";

        function openComponentStudio(folder, title, initialMode = 'preview') {{
            activeFolder = folder;
            activeTitle = title;
            
            document.getElementById('studioComponentTitle').innerText = title;
            document.getElementById('studioPathTag').innerText = `ui/web/components/glass/${{folder}}/`;
            document.getElementById('studioSoloLink').href = `${{folder}}/${{folder}}.html`;
            
            const iframe = document.getElementById('studioIframe');
            iframe.src = `${{folder}}/${{folder}}.html`;
            
            const curBg = localStorage.getItem(`comp-bg-${{folder}}`) || currentGridBg || 'dark';
            setStudioBg(curBg);
            iframe.onload = () => {{
                try {{
                    const doc = iframe.contentDocument;
                    if (doc && doc.body) {{
                        if (folder === 'lockscreen-pin-glass') {{
                            doc.body.style.backgroundColor = '#08080C';
                            const phoneViewport = doc.getElementById('phoneViewport');
                            if (phoneViewport) {{
                                phoneViewport.setAttribute('data-phone-bg', curBg === 'blob' ? 'blob' : 'black');
                            }}
                            if (iframe.contentWindow && typeof iframe.contentWindow.setPhoneWallpaper === 'function') {{
                                iframe.contentWindow.setPhoneWallpaper(curBg === 'blob' ? 'blob' : 'black');
                            }}
                        }} else if (curBg === 'blob') {{
                            doc.body.style.backgroundColor = 'transparent';
                        }}
                    }}
                }} catch(e) {{}}
            }};
            
            populateCodeTabs(folder);
            resetStudioWidth();
            switchStudioMode(initialMode);
            
            const modal = document.getElementById('componentStudioModal');
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            if (window.lucide) lucide.createIcons();
        }}

        function populateCodeTabs(folder) {{
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

            if (firstFile) {{
                switchCodeTab(firstFile);
            }}
        }}

        function switchStudioMode(mode) {{
            currentMode = mode;
            const previewBtn = document.getElementById('modePreviewBtn');
            const codeBtn = document.getElementById('modeCodeBtn');
            const previewPanel = document.getElementById('studioPreviewPanel');
            const codePanel = document.getElementById('studioCodePanel');
            const copyBtnText = document.querySelector('#studioCopyBtn span');

            if (mode === 'preview') {{
                previewBtn.classList.add('active');
                codeBtn.classList.remove('active');
                previewPanel.classList.add('active');
                codePanel.classList.remove('active');
                if (copyBtnText) copyBtnText.innerText = "Salin";
            }} else {{
                codeBtn.classList.add('active');
                previewBtn.classList.remove('active');
                codePanel.classList.add('active');
                previewPanel.classList.remove('active');
                if (copyBtnText) copyBtnText.innerText = "Salin File";
            }}
            if (window.lucide) lucide.createIcons();
        }}

        function setStudioPreset(width, btn) {{
            document.querySelectorAll('.btn-studio-preset[data-preset]').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');

            const wrapper = document.getElementById('studioViewportWrapper');
            const slider = document.getElementById('studioWidthSlider');
            const badge = document.getElementById('studioSliderBadge');
            const dimIndicator = document.getElementById('viewportDimensionIndicator');

            if (width === '100%') {{
                wrapper.style.maxWidth = '100%';
                wrapper.style.width = '100%';
                if (slider) slider.value = 1440;
                if (badge) badge.innerText = 'Full (100%)';
                if (dimIndicator) dimIndicator.innerText = '100% (Full Width)';
            }} else {{
                wrapper.style.maxWidth = width;
                wrapper.style.width = width;
                const num = parseInt(width);
                if (slider) slider.value = num;
                if (badge) badge.innerText = width;
                if (dimIndicator) dimIndicator.innerText = `${{width}} × auto`;
            }}
        }}

        function setStudioSliderWidth(val) {{
            document.querySelectorAll('.btn-studio-preset[data-preset]').forEach(b => b.classList.remove('active'));

            const wrapper = document.getElementById('studioViewportWrapper');
            const badge = document.getElementById('studioSliderBadge');
            const dimIndicator = document.getElementById('viewportDimensionIndicator');

            if (val >= 1440) {{
                wrapper.style.maxWidth = '100%';
                wrapper.style.width = '100%';
                badge.innerText = 'Full (100%)';
                dimIndicator.innerText = '100% (Full Width)';
                const fullBtn = document.querySelector('.btn-studio-preset[data-preset="100%"]');
                if (fullBtn) fullBtn.classList.add('active');
            }} else {{
                const w = `${{val}}px`;
                wrapper.style.maxWidth = w;
                wrapper.style.width = w;
                badge.innerText = w;
                dimIndicator.innerText = `${{w}} × auto`;
                const matchBtn = document.querySelector(`.btn-studio-preset[data-preset="${{w}}"]`);
                if (matchBtn) matchBtn.classList.add('active');
            }}
        }}

        function resetStudioWidth() {{
            const slider = document.getElementById('studioWidthSlider');
            if (slider) slider.value = 1440;
            const fullBtn = document.querySelector('.btn-studio-preset[data-preset="100%"]');
            setStudioPreset('100%', fullBtn);
        }}

        function reloadStudioIframe() {{
            const iframe = document.getElementById('studioIframe');
            if (iframe && iframe.src) {{
                const cur = iframe.src;
                iframe.src = 'about:blank';
                setTimeout(() => {{ iframe.src = cur; }}, 50);
            }}
        }}

        function closeComponentStudio() {{
            const modal = document.getElementById('componentStudioModal');
            modal.classList.remove('active');
            document.body.style.overflow = '';
            const iframe = document.getElementById('studioIframe');
            if (iframe) iframe.src = 'about:blank';
        }}

        // Backward compatibility alias
        function openComponentModal(folder, title) {{
            openComponentStudio(folder, title, 'code');
        }}
        function closeCodeModal() {{
            closeComponentStudio();
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
                document.getElementById('modalSubbarFilePath').innerText = `ui/web/components/glass/css.css (Master Shared Tokens)`;
            }} else {{
                code = (COMP_DB[activeFolder] && COMP_DB[activeFolder][filename]) || "";
                document.getElementById('modalSubbarFilePath').innerText = `ui/web/components/glass/${{activeFolder}}/${{filename}}`;
            }}

            const lines = code ? code.split('\\n').length : 0;
            const kb = (new Blob([code]).size / 1024).toFixed(1);
            document.getElementById('modalSubbarStats').innerText = `${{lines}} baris (${{kb}} KB)`;

            document.getElementById('modalCodeSnippet').innerText = code;
        }}

        async function copyCurrentStudioCode() {{
            let code = "";
            let label = "";

            if (currentMode === 'code') {{
                if (activeFile === "css.css") {{
                    code = COMP_DB["css.css"] || "";
                    label = "Shared Tokens (css.css)";
                }} else {{
                    code = (COMP_DB[activeFolder] && COMP_DB[activeFolder][activeFile]) || "";
                    label = activeFile;
                }}
            }} else {{
                const aioFile = `${{activeFolder}}.html`;
                code = (COMP_DB[activeFolder] && COMP_DB[activeFolder][aioFile]) || "";
                label = `All-in-One (${{activeFolder}})`;
            }}

            if (code) {{
                await navigator.clipboard.writeText(code);
                showToast(`Kode ${{label}} berhasil disalin ke clipboard!`);
            }} else {{
                showToast(`Kode tidak tersedia untuk disalin.`);
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

        function downloadFile(filename, content) {{
            const mime = filename.endsWith('.html') ? 'text/html;charset=utf-8' :
                         filename.endsWith('.css') ? 'text/css;charset=utf-8' :
                         filename.endsWith('.js') ? 'text/javascript;charset=utf-8' : 'text/plain;charset=utf-8';
            const blob = new Blob([content], {{ type: mime }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast(`File ${{filename}} berhasil diunduh!`);
        }}

        function quickDownloadAllInOne(folder) {{
            const aioFile = `${{folder}}.html`;
            const code = (COMP_DB[folder] && COMP_DB[folder][aioFile]) || "";
            if (code) {{
                downloadFile(aioFile, code);
            }} else {{
                showToast("File tidak ditemukan untuk diunduh.");
            }}
        }}

        function downloadCurrentStudioCode() {{
            if (currentMode === 'code') {{
                let code = "";
                let fn = activeFile;
                if (activeFile === "css.css") {{
                    code = COMP_DB["css.css"] || "";
                    fn = "glass-tokens.css";
                }} else {{
                    code = (COMP_DB[activeFolder] && COMP_DB[activeFolder][activeFile]) || "";
                }}
                if (code && fn) {{
                    downloadFile(fn, code);
                }} else {{
                    showToast("Kode tidak tersedia untuk diunduh.");
                }}
            }} else {{
                const aioFile = `${{activeFolder}}.html`;
                const code = (COMP_DB[activeFolder] && COMP_DB[activeFolder][aioFile]) || "";
                if (code) {{
                    downloadFile(aioFile, code);
                }} else {{
                    showToast("Kode tidak tersedia untuk diunduh.");
                }}
            }}
        }}

        function showToast(msg) {{
            const toast = document.getElementById('toast');
            document.getElementById('toastMsg').innerText = msg;
            toast.classList.add('active');
            setTimeout(() => toast.classList.remove('active'), 2500);
        }}

        document.getElementById('componentStudioModal').addEventListener('click', (e) => {{
            if (e.target.id === 'componentStudioModal') closeComponentStudio();
        }});

        window.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                const modal = document.getElementById('componentStudioModal');
                if (modal && modal.classList.contains('active')) {{
                    closeComponentStudio();
                }}
            }}
        }});

        // ============================================================
        // COMPONENT & GRID BACKGROUND CONTROLLER (DARK | BLOB SVG)
        // ============================================================
                // Per-Component & Grid Background Management
        let currentGridBg = localStorage.getItem('prototype-grid-bg') || 'dark';

        function isPhoneComponent(f) {{
            return f === 'lockscreen-pin-glass' || f === 'mobile-control-center-glass';
        }}

        function setComponentBg(folder, bg, btnEl) {{
            const previewZone = document.getElementById(`preview-zone-${{folder}}`);
            if (previewZone) {{
                if (isPhoneComponent(folder)) {{
                    previewZone.setAttribute('data-comp-bg', 'dark');
                }} else {{
                    previewZone.setAttribute('data-comp-bg', bg);
                }}
            }}
            const switcher = document.getElementById(`bg-switcher-${{folder}}`);
            if (switcher) {{
                switcher.querySelectorAll('.btn-comp-bg').forEach(b => {{
                    b.classList.toggle('active', b.getAttribute('data-bg') === bg);
                }});
            }}
            const iframe = document.getElementById(`iframe-${{folder}}`);
            if (iframe) {{
                try {{
                    const doc = iframe.contentDocument;
                    if (doc && doc.body) {{
                        if (isPhoneComponent(folder)) {{
                            doc.body.style.backgroundColor = '#08080C';
                            const phoneViewport = doc.getElementById('phoneViewport');
                            if (phoneViewport) {{
                                phoneViewport.setAttribute('data-phone-bg', bg === 'blob' ? 'blob' : 'black');
                            }}
                            if (iframe.contentWindow) {{
                                if (typeof iframe.contentWindow.setPhoneWallpaper === 'function') {{
                                    iframe.contentWindow.setPhoneWallpaper(bg === 'blob' ? 'blob' : 'black');
                                }}
                                if (typeof iframe.contentWindow.setControlCenterBg === 'function') {{
                                    iframe.contentWindow.setControlCenterBg(bg === 'blob' ? 'blob' : 'black');
                                }}
                            }}
                        }} else if (folder === 'elastic-clock-glass') {{
                            if (iframe.contentWindow && typeof iframe.contentWindow.setClockBg === 'function') {{
                                iframe.contentWindow.setClockBg(bg === 'blob' ? 'blob' : 'black');
                            }}
                            doc.body.style.backgroundColor = 'transparent';
                        }} else {{
                            if (bg === 'blob') {{
                                doc.body.style.backgroundColor = 'transparent';
                            }} else {{
                                doc.body.style.backgroundColor = '';
                            }}
                        }}
                    }}
                }} catch (e) {{}}
            }}
            localStorage.setItem(`comp-bg-${{folder}}`, bg);
        }}

        function setStudioBg(bg) {{
            const stage = document.getElementById('studioCanvasStage');
            if (stage) {{
                if (isPhoneComponent(activeFolder)) {{
                    stage.setAttribute('data-stage-bg', 'dark');
                }} else {{
                    stage.setAttribute('data-stage-bg', bg);
                }}
            }}
            document.querySelectorAll('.btn-studio-bg').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-bg') === bg);
            }});
            const iframe = document.getElementById('studioIframe');
            if (iframe) {{
                try {{
                    const doc = iframe.contentDocument;
                    if (doc && doc.body) {{
                        if (isPhoneComponent(activeFolder)) {{
                            doc.body.style.backgroundColor = '#08080C';
                            const phoneViewport = doc.getElementById('phoneViewport');
                            if (phoneViewport) {{
                                phoneViewport.setAttribute('data-phone-bg', bg === 'blob' ? 'blob' : 'black');
                            }}
                            if (iframe.contentWindow) {{
                                if (typeof iframe.contentWindow.setPhoneWallpaper === 'function') {{
                                    iframe.contentWindow.setPhoneWallpaper(bg === 'blob' ? 'blob' : 'black');
                                }}
                                if (typeof iframe.contentWindow.setControlCenterBg === 'function') {{
                                    iframe.contentWindow.setControlCenterBg(bg === 'blob' ? 'blob' : 'black');
                                }}
                            }}
                        }} else if (activeFolder === 'elastic-clock-glass') {{
                            if (iframe.contentWindow && typeof iframe.contentWindow.setClockBg === 'function') {{
                                iframe.contentWindow.setClockBg(bg === 'blob' ? 'blob' : 'black');
                            }}
                            doc.body.style.backgroundColor = 'transparent';
                        }} else {{
                            if (bg === 'blob') {{
                                doc.body.style.backgroundColor = 'transparent';
                            }} else {{
                                doc.body.style.backgroundColor = '';
                            }}
                        }}
                    }}
                }} catch (e) {{}}
            }}
        }}

        function setGridBg(bg) {{
            currentGridBg = bg;
            const grid = document.getElementById('componentsGrid');
            if (grid) {{
                grid.setAttribute('data-grid-bg', bg);
            }}
            document.querySelectorAll('.btn-grid-bg').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-bg') === bg);
            }});
            localStorage.setItem('prototype-grid-bg', bg);

            // Update all individual component backgrounds to match
            document.querySelectorAll('.component-card').forEach(card => {{
                const folder = card.id.replace('card-', '');
                setComponentBg(folder, bg);
            }});
            showToast(`Latar Grid diatur ke: ${{bg === 'blob' ? 'BLOB (2048x1156)' : 'DARK OBSIDIAN'}}`);
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            // Restore Grid BG
            const grid = document.getElementById('componentsGrid');
            if (grid) {{
                grid.setAttribute('data-grid-bg', currentGridBg);
            }}
            document.querySelectorAll('.btn-grid-bg').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-bg') === currentGridBg);
            }});

            // Restore individual component background preferences
            document.querySelectorAll('.component-card').forEach(card => {{
                const folder = card.id.replace('card-', '');
                const savedBg = localStorage.getItem(`comp-bg-${{folder}}`) || currentGridBg || 'dark';
                setComponentBg(folder, savedBg);
            }});
        }});

        document.querySelectorAll('iframe').forEach(iframe => {{
            iframe.addEventListener('load', () => {{
                const folder = iframe.id ? iframe.id.replace('iframe-', '') : '';
                const bg = (folder && localStorage.getItem(`comp-bg-${{folder}}`)) || currentGridBg || 'dark';
                try {{
                    const doc = iframe.contentDocument;
                    if (doc && doc.body) {{
                        if (folder === 'lockscreen-pin-glass') {{
                            doc.body.style.backgroundColor = '#08080C';
                            const phoneViewport = doc.getElementById('phoneViewport');
                            if (phoneViewport) {{
                                phoneViewport.setAttribute('data-phone-bg', bg === 'blob' ? 'blob' : 'black');
                            }}
                            if (iframe.contentWindow && typeof iframe.contentWindow.setPhoneWallpaper === 'function') {{
                                iframe.contentWindow.setPhoneWallpaper(bg === 'blob' ? 'blob' : 'black');
                            }}
                        }} else if (bg === 'blob') {{
                            doc.body.style.backgroundColor = 'transparent';
                        }}
                    }}
                }} catch(e) {{}}
            }});
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
            <article class="comp-card" id="raw-card-{folder}">
                <div class="comp-card-head">
                    <span class="comp-card-title">{title}</span>
                    <span class="comp-card-tag">{escaped_tag}</span>
                </div>
                <div class="card-actions-bar">
                    <button class="btn-card-full" onclick="openRawStudio('{folder}', '{title}', 'preview')" title="Buka Raw Studio Pop-up Full Screen">
                        <i data-lucide="maximize-2"></i> Full
                    </button>
                    <div class="card-actions-tools">
                        <button class="btn-card-tool" onclick="openRawStudio('{folder}', '{title}', 'code')" title="Lihat Source HTML Baku">
                            <i data-lucide="code"></i> Kode
                        </button>
                        <button class="btn-card-tool highlight" onclick="copyRawAio('{folder}')" title="Salin Kode HTML Murni">
                            <i data-lucide="copy"></i> Salin
                        </button>
                        <button class="btn-card-tool" onclick="quickDownloadRawAio('{folder}')" title="Unduh File HTML Baku">
                            <i data-lucide="download"></i> Unduh
                        </button>
                        <a href="{folder}/{aio_file}" target="_blank" class="btn-card-tool new-tab" title="Buka di Tab Baru">
                            <i data-lucide="external-link"></i> Tab Baru
                        </a>
                    </div>
                </div>
                <div class="comp-preview-zone">
                    <div class="preview-resizer-wrapper" id="raw-wrapper-{folder}">
                        <iframe src="{folder}/{aio_file}" title="{title} Preview"></iframe>
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
    <link rel="icon" type="image/svg+xml" href="../../../../favicon.svg">
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
        .raw-grid.cols-auto {{ grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr)); }}
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

        /* Card Action Bar */
        .card-actions-bar {{
            padding: 8px 14px; display: flex; align-items: center; justify-content: space-between;
            background: rgba(0, 0, 0, 0.35); border-bottom: 1px solid var(--border-color);
            flex-shrink: 0; gap: 8px;
        }}
        .btn-card-full {{
            padding: 5px 12px; border-radius: 6px; font-size: 11.5px; font-weight: 600;
            background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.45);
            color: #60A5FA; cursor: pointer; display: inline-flex; align-items: center; gap: 5px;
            transition: all 0.2s;
        }}
        .btn-card-full svg {{ width: 12px; height: 12px; }}
        .btn-card-full:hover {{
            background: rgba(59, 130, 246, 0.35); border-color: rgba(59, 130, 246, 0.8);
            color: #FFFFFF;
        }}
        .card-actions-tools {{ display: flex; align-items: center; gap: 6px; }}
        .btn-card-tool {{
            padding: 4px 10px; border-radius: 6px; font-size: 11.5px;
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color);
            color: var(--text-primary); cursor: pointer; text-decoration: none;
            display: inline-flex; align-items: center; gap: 5px; transition: all 0.2s;
        }}
        .btn-card-tool svg {{ width: 12px; height: 12px; }}
        .btn-card-tool:hover {{ background: rgba(255, 255, 255, 0.12); }}
        .btn-card-tool.highlight {{
            background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.35);
            color: #93C5FD;
        }}
        .btn-card-tool.highlight:hover {{
            background: rgba(59, 130, 246, 0.25); color: #FFFFFF;
        }}
        .btn-card-tool.new-tab,
        .btn-card-tool.solo {{ color: var(--text-secondary); }}
        .btn-card-tool.new-tab:hover,
        .btn-card-tool.solo:hover {{ color: #FFFFFF; }}

        .comp-preview-zone {{
            flex: 1; min-height: 320px; background: #FFFFFF;
            display: flex; align-items: stretch; justify-content: center;
            padding: 0; overflow: hidden; position: relative;
        }}
        .comp-preview-zone .preview-resizer-wrapper {{
            width: 100%; height: 100%; min-height: 100%;
            display: flex; align-items: stretch; justify-content: center;
            margin: 0 auto; flex-shrink: 0;
        }}
        .comp-preview-zone iframe {{ width: 100%; height: 100%; min-height: 100%; border: none; display: block; pointer-events: auto; }}

        /* Raw Studio Modal */
        .modal-overlay {{
            position: fixed; inset: 0; z-index: 1000; background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px); display: flex; align-items: center; justify-content: center;
            opacity: 0; pointer-events: none; transition: opacity 0.25s ease; padding: 24px;
        }}
        .modal-overlay.active {{ opacity: 1; pointer-events: auto; }}

        .studio-modal-card {{
            width: 96vw; max-width: 1500px; height: 90vh; max-height: 980px;
            background: #0E1017; border-radius: 16px; border: 1px solid var(--border-color);
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.8); display: flex; flex-direction: column;
            overflow: hidden; transform: scale(0.97); transition: transform 0.25s var(--ease-spring);
        }}
        .modal-overlay.active .studio-modal-card {{ transform: scale(1); }}

        .studio-header {{
            padding: 12px 20px; background: #141722; border-bottom: 1px solid var(--border-color);
            display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-shrink: 0;
        }}
        .studio-title-block {{ display: flex; flex-direction: column; gap: 2px; }}
        .studio-badge-row {{ display: flex; align-items: center; gap: 8px; }}
        .studio-type-badge {{
            font-size: 10px; font-weight: 700; text-transform: uppercase;
            padding: 2px 6px; border-radius: 4px; background: rgba(59, 130, 246, 0.15);
            color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3);
        }}
        .studio-path-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-secondary); }}
        .studio-title {{ font-size: 15px; font-weight: 700; color: #FFFFFF; margin: 0; }}

        .studio-mode-switcher {{
            display: inline-flex; padding: 3px; border-radius: 10px;
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color); gap: 3px;
        }}
        .btn-mode-tab {{
            padding: 5px 14px; border-radius: 7px; border: 1px solid transparent;
            background: transparent; color: var(--text-secondary); font-size: 12px;
            font-weight: 600; cursor: pointer; display: inline-flex; align-items: center;
            gap: 6px; transition: all 0.2s;
        }}
        .btn-mode-tab svg {{ width: 13px; height: 13px; }}
        .btn-mode-tab:hover {{ color: var(--text-primary); }}
        .btn-mode-tab.active {{
            background: rgba(59, 130, 246, 0.25); border-color: rgba(59, 130, 246, 0.45);
            color: #FFFFFF;
        }}

        .studio-header-right {{ display: flex; align-items: center; gap: 8px; }}
        .btn-studio-action {{
            padding: 5px 12px; border-radius: 7px; font-size: 11.5px; font-weight: 500;
            background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border-color);
            color: var(--text-primary); cursor: pointer; display: inline-flex;
            align-items: center; gap: 5px; text-decoration: none; transition: all 0.2s;
        }}
        .btn-studio-action svg {{ width: 12px; height: 12px; }}
        .btn-studio-action:hover {{ background: rgba(255, 255, 255, 0.12); }}
        .btn-studio-action.highlight {{
            background: rgba(59, 130, 246, 0.2); border-color: rgba(59, 130, 246, 0.45);
            color: #60A5FA; font-weight: 600;
        }}
        .studio-close-btn {{
            width: 30px; height: 30px; border-radius: 6px;
            background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border-color);
            color: var(--text-secondary); cursor: pointer; display: flex;
            align-items: center; justify-content: center; transition: all 0.2s;
        }}
        .studio-close-btn:hover {{ background: rgba(239, 68, 68, 0.2); color: #EF4444; border-color: rgba(239, 68, 68, 0.4); }}
        .studio-close-btn svg {{ width: 15px; height: 15px; }}

        .studio-panel {{ display: none; flex: 1; min-height: 0; flex-direction: column; overflow: hidden; }}
        .studio-panel.active {{ display: flex; }}

        .studio-toolbar {{
            padding: 9px 20px; background: #12141D; border-bottom: 1px solid var(--border-color);
            display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; flex-shrink: 0;
        }}
        .studio-toolbar-section {{ display: flex; align-items: center; gap: 8px; }}
        .toolbar-label {{
            font-size: 11.5px; font-weight: 600; color: var(--text-secondary);
            display: inline-flex; align-items: center; gap: 5px; text-transform: uppercase;
        }}
        .toolbar-label svg {{ width: 12px; height: 12px; color: #60A5FA; }}

        .presets-group {{ display: flex; align-items: center; gap: 4px; flex-wrap: wrap; }}
        .btn-studio-preset {{
            padding: 4px 10px; border-radius: 6px; font-size: 11.5px; font-weight: 500;
            background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border-color);
            color: var(--text-secondary); cursor: pointer; display: inline-flex;
            align-items: center; gap: 5px; transition: all 0.15s;
        }}
        .btn-studio-preset svg {{ width: 11px; height: 11px; }}
        .btn-studio-preset:hover {{ background: rgba(255, 255, 255, 0.08); color: #FFFFFF; }}
        .btn-studio-preset.active {{
            background: rgba(59, 130, 246, 0.2); border-color: rgba(59, 130, 246, 0.5);
            color: #60A5FA; font-weight: 600;
        }}

        .studio-toolbar-divider {{ width: 1px; height: 20px; background: var(--border-color); }}

        .studio-slider-box {{
            display: inline-flex; align-items: center; gap: 8px; padding: 3px 10px;
            border-radius: 8px; background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border-color);
        }}
        .studio-slider-range {{
            -webkit-appearance: none; appearance: none;
            width: 120px; height: 4px; border-radius: 2px;
            background: rgba(255, 255, 255, 0.2); outline: none; cursor: pointer;
        }}
        .studio-slider-range::-webkit-slider-thumb {{
            -webkit-appearance: none; appearance: none;
            width: 12px; height: 12px; border-radius: 50%;
            background: #60A5FA; cursor: pointer;
        }}
        .studio-slider-badge {{
            font-size: 11px; font-family: 'JetBrains Mono', monospace;
            color: #60A5FA; min-width: 65px; text-align: center; font-weight: 600;
        }}
        .btn-reset-studio-slider {{
            background: transparent; border: none; color: var(--text-secondary);
            cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 2px;
        }}
        .btn-reset-studio-slider:hover {{ color: #FFFFFF; }}
        .btn-reset-studio-slider svg {{ width: 12px; height: 12px; }}

        .btn-studio-tool {{
            padding: 4px 10px; border-radius: 6px; font-size: 11.5px;
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color);
            color: var(--text-secondary); cursor: pointer; display: inline-flex;
            align-items: center; gap: 5px; transition: all 0.2s;
        }}
        .btn-studio-tool svg {{ width: 12px; height: 12px; }}
        .btn-studio-tool:hover {{ background: rgba(255, 255, 255, 0.1); color: #FFFFFF; }}

        .studio-canvas-stage {{
            flex: 1; width: 100%; min-height: 0; background: #0B0D13;
            overflow: auto; display: flex; align-items: stretch; justify-content: center;
            padding: 20px; position: relative;
        }}
        .studio-viewport-wrapper {{
            width: 100%; max-width: 100%; height: 100%; min-height: 100%;
            border-radius: 10px; border: 1px solid var(--border-color);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7); overflow: hidden; background: #FFFFFF;
            transition: max-width 0.25s var(--ease-spring), width 0.25s var(--ease-spring);
            position: relative; display: flex; flex-direction: column; margin: 0 auto;
        }}
        .studio-viewport-wrapper iframe {{ width: 100%; height: 100%; flex: 1; border: none; display: block; }}
        .viewport-meta-floating {{
            position: absolute; bottom: 8px; right: 12px; padding: 2px 8px; border-radius: 4px;
            background: rgba(0, 0, 0, 0.75); font-size: 10px; font-family: 'JetBrains Mono', monospace;
            color: #94A3B8; pointer-events: none; z-index: 10;
        }}

        .modal-tabs-bar {{
            display: flex; align-items: center; gap: 4px; padding: 8px 16px 0;
            background: #11141E; border-bottom: 1px solid var(--border-color);
            overflow-x: auto; scrollbar-width: none;
        }}
        .modal-tabs-bar::-webkit-scrollbar {{ display: none; }}
        .code-tab-btn {{
            padding: 7px 14px; border-radius: 8px 8px 0 0; background: transparent;
            border: 1px solid transparent; border-bottom: none; color: var(--text-secondary);
            font-size: 12px; font-family: 'JetBrains Mono', monospace; cursor: pointer;
            display: flex; align-items: center; gap: 7px; transition: all 0.2s; white-space: nowrap;
        }}
        .code-tab-btn:hover {{ color: var(--text-primary); background: rgba(255, 255, 255, 0.04); }}
        .code-tab-btn.active {{
            background: #0B0D13; border-color: var(--border-color); color: #FFFFFF; font-weight: 600;
        }}
        .modal-tab-subbar {{
            padding: 7px 20px; background: #0B0D13; border-bottom: 1px solid var(--border-color);
            display: flex; align-items: center; justify-content: space-between; font-size: 11.5px;
            color: var(--text-secondary);
        }}
        .subbar-file-path {{ font-family: 'JetBrains Mono', monospace; color: #60A5FA; }}
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
            .raw-header {{
                padding: 10px 14px;
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            .raw-header .header-actions {{
                width: 100%;
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 4px;
            }}
            .controls-bar {{
                padding: 10px 14px;
                flex-direction: column;
                align-items: stretch;
                gap: 10px;
            }}
            .filter-tabs {{
                width: 100%;
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
            }}
            .raw-grid,
            .raw-grid.cols-auto,
            .raw-grid.cols-1,
            .raw-grid.cols-2,
            .raw-grid.cols-3,
            .raw-grid.cols-4 {{
                grid-template-columns: 1fr !important;
                padding: 10px 14px 40px !important;
                gap: 16px !important;
            }}
            .studio-modal-card {{
                width: 100vw;
                height: 100vh;
                max-height: 100vh;
                margin: 0;
                border-radius: 0;
            }}
            .modal-overlay {{
                padding: 0;
            }}
            .studio-header {{
                padding: 10px 14px;
                flex-wrap: wrap;
                gap: 10px;
            }}
            .studio-mode-switcher {{
                order: 3;
                width: 100%;
                justify-content: center;
            }}
            .btn-mode-tab {{
                flex: 1;
                justify-content: center;
            }}
            .studio-toolbar {{
                padding: 8px 12px;
                gap: 8px;
            }}
            .presets-group {{
                overflow-x: auto;
                width: 100%;
                padding-bottom: 2px;
                scrollbar-width: none;
            }}
            .presets-group::-webkit-scrollbar {{ display: none; }}
            .studio-slider-box {{
                width: 100%;
                justify-content: space-between;
            }}
            .studio-slider-range {{
                flex: 1;
                width: auto;
            }}
        }}

        @media (max-width: 600px) {{
            .card-actions-bar {{
                padding: 6px 10px;
            }}
            .btn-card-tool.solo {{
                display: none !important;
            }}
            .layout-selector .btn-layout:nth-child(4),
            .layout-selector .btn-layout:nth-child(5) {{
                display: none !important;
            }}
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
            <a href="../../../../index.html" class="nav-link"><i data-lucide="home"></i> Gateway</a>
            <a href="../../../../ui/web/apps.html" class="nav-link"><i data-lucide="folder-kanban"></i> Web Apps</a>
            <a href="../glass/showcase.html" class="nav-link"><i data-lucide="gem"></i> Glass Dark (24)</a>
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

    <!-- Raw Component Studio Modal (Fullscreen Interactive Popup) -->
    <div class="modal-overlay" id="rawStudioModal">
        <div class="studio-modal-card">
            <header class="studio-header">
                <div class="studio-title-block">
                    <div class="studio-badge-row">
                        <span class="studio-type-badge" id="rawStudioTypeBadge">Raw HTML5</span>
                        <span class="studio-path-tag" id="rawStudioPathTag">ui/components/raw/...</span>
                    </div>
                    <h2 class="studio-title" id="rawStudioComponentTitle">Raw Component Title</h2>
                </div>

                <div class="studio-mode-switcher">
                    <button class="btn-mode-tab active" id="rawModePreviewBtn" onclick="switchRawStudioMode('preview')">
                        <i data-lucide="eye"></i> <span>Live Preview</span>
                    </button>
                    <button class="btn-mode-tab" id="rawModeCodeBtn" onclick="switchRawStudioMode('code')">
                        <i data-lucide="code-2"></i> <span>Lihat Code</span>
                    </button>
                </div>

                <div class="studio-header-right">
                    <button class="btn-studio-action highlight" id="rawStudioCopyBtn" onclick="copyCurrentRawStudioCode()" title="Salin Kode ke Clipboard">
                        <i data-lucide="copy"></i> <span>Salin</span>
                    </button>
                    <button class="btn-studio-action" id="rawStudioDownloadBtn" onclick="downloadCurrentRawStudioCode()" title="Unduh File HTML">
                        <i data-lucide="download"></i> <span>Unduh</span>
                    </button>
                    <a href="#" target="_blank" class="btn-studio-action solo-link" id="rawStudioSoloLink" title="Buka Standalone File di Tab Baru">
                        <i data-lucide="external-link"></i> <span>Tab Baru</span>
                    </a>
                    <button class="studio-close-btn" onclick="closeRawStudio()" title="Tutup Modal (Esc)">
                        <i data-lucide="x"></i>
                    </button>
                </div>
            </header>

            <!-- Mode 1: Live Interactive Viewport Studio -->
            <div class="studio-panel active" id="rawStudioPreviewPanel">
                <div class="studio-toolbar">
                    <div class="studio-toolbar-section presets-group">
                        <span class="toolbar-label"><i data-lucide="monitor"></i> Preset:</span>
                        <button class="btn-studio-preset active" data-preset="100%" onclick="setRawStudioPreset('100%', this)" title="Full Viewport (100%)">
                            <i data-lucide="maximize-2"></i> Full
                        </button>
                        <button class="btn-studio-preset" data-preset="1440px" onclick="setRawStudioPreset('1440px', this)" title="Desktop Ultra (1440px)">
                            <i data-lucide="monitor"></i> 1440px
                        </button>
                        <button class="btn-studio-preset" data-preset="1024px" onclick="setRawStudioPreset('1024px', this)" title="Laptop (1024px)">
                            <i data-lucide="laptop"></i> 1024px
                        </button>
                        <button class="btn-studio-preset" data-preset="768px" onclick="setRawStudioPreset('768px', this)" title="Tablet (768px)">
                            <i data-lucide="tablet"></i> 768px
                        </button>
                        <button class="btn-studio-preset" data-preset="375px" onclick="setRawStudioPreset('375px', this)" title="Mobile (375px)">
                            <i data-lucide="smartphone"></i> 375px
                        </button>
                    </div>

                    <div class="studio-toolbar-divider"></div>

                    <!-- Slider Rasio Ukuran -->
                    <div class="studio-toolbar-section slider-group">
                        <span class="toolbar-label"><i data-lucide="sliders-horizontal"></i> Slider Rasio:</span>
                        <div class="studio-slider-box" title="Geser untuk mengatur lebar preview secara fluid">
                            <input type="range" class="studio-slider-range" id="rawStudioWidthSlider"
                                   min="320" max="1440" step="10" value="1440"
                                   oninput="setRawStudioSliderWidth(this.value)"
                                   aria-label="Atur lebar viewport komponen">
                            <span class="studio-slider-badge" id="rawStudioSliderBadge">Full (100%)</span>
                            <button class="btn-reset-studio-slider" onclick="resetRawStudioWidth()" title="Reset ke Full (100%)">
                                <i data-lucide="rotate-ccw"></i>
                            </button>
                        </div>
                    </div>

                    <div class="studio-toolbar-right">
                        <button class="btn-studio-tool" onclick="reloadRawStudioIframe()" title="Muat Ulang Iframe Preview">
                            <i data-lucide="refresh-cw"></i> <span>Reload</span>
                        </button>
                    </div>
                </div>

                <div class="studio-canvas-stage">
                    <div class="studio-viewport-wrapper" id="rawStudioViewportWrapper">
                        <div class="viewport-meta-floating">
                            <span id="rawViewportDimensionIndicator">100% (Full Width)</span>
                        </div>
                        <iframe src="" id="rawStudioIframe" title="Raw Component Live Preview"></iframe>
                    </div>
                </div>
            </div>

            <!-- Mode 2: Multi-file Code Studio -->
            <div class="studio-panel" id="rawStudioCodePanel">
                <div class="modal-tabs-bar" id="rawModalTabsBar"></div>
                <div class="modal-tab-subbar">
                    <span class="subbar-file-path" id="rawModalSubbarFilePath">...</span>
                    <span id="rawModalSubbarStats">0 baris</span>
                </div>
                <div class="modal-body">
                    <pre class="code-pre"><code id="rawModalCodeSnippet">Memuat kode...</code></pre>
                </div>
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

        let rawActiveFolder = "";
        let rawActiveTitle = "";
        let rawActiveFile = "";
        let rawCurrentMode = "preview";

        function openRawStudio(folder, title, initialMode = 'preview') {{
            rawActiveFolder = folder;
            rawActiveTitle = title;
            
            document.getElementById('rawStudioComponentTitle').innerText = title;
            document.getElementById('rawStudioPathTag').innerText = `ui/components/raw/${{folder}}/`;
            document.getElementById('rawStudioSoloLink').href = `${{folder}}/${{folder}}.html`;
            
            const iframe = document.getElementById('rawStudioIframe');
            iframe.src = `${{folder}}/${{folder}}.html`;
            
            populateRawCodeTabs(folder);
            resetRawStudioWidth();
            switchRawStudioMode(initialMode);
            
            const modal = document.getElementById('rawStudioModal');
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            if (window.lucide) lucide.createIcons();
        }}

        function populateRawCodeTabs(folder) {{
            const tabsBar = document.getElementById('rawModalTabsBar');
            tabsBar.innerHTML = '';

            const compFiles = RAW_DB[folder] || {{}};
            const aioFile = `${{folder}}.html`;
            const fileOrder = [aioFile, "index.html", "index.css"];

            let firstFile = null;

            fileOrder.forEach(fn => {{
                if (compFiles[fn] !== undefined) {{
                    if (!firstFile) firstFile = fn;
                    const btn = document.createElement('button');
                    btn.className = "code-tab-btn";
                    btn.setAttribute('data-filename', fn);
                    btn.innerHTML = `<i data-lucide="${{fn.endsWith('.css') ? 'palette' : 'file-code'}}"></i> ${{fn}}`;
                    btn.onclick = () => switchRawCodeTab(fn);
                    tabsBar.appendChild(btn);
                }}
            }});

            if (firstFile) {{
                switchRawCodeTab(firstFile);
            }}
        }}

        function switchRawStudioMode(mode) {{
            rawCurrentMode = mode;
            const previewBtn = document.getElementById('rawModePreviewBtn');
            const codeBtn = document.getElementById('rawModeCodeBtn');
            const previewPanel = document.getElementById('rawStudioPreviewPanel');
            const codePanel = document.getElementById('rawStudioCodePanel');
            const copyBtnText = document.querySelector('#rawStudioCopyBtn span');

            if (mode === 'preview') {{
                previewBtn.classList.add('active');
                codeBtn.classList.remove('active');
                previewPanel.classList.add('active');
                codePanel.classList.remove('active');
                if (copyBtnText) copyBtnText.innerText = "Salin";
            }} else {{
                codeBtn.classList.add('active');
                previewBtn.classList.remove('active');
                codePanel.classList.add('active');
                previewPanel.classList.remove('active');
                if (copyBtnText) copyBtnText.innerText = "Salin File";
            }}
            if (window.lucide) lucide.createIcons();
        }}

        function setRawStudioPreset(width, btn) {{
            document.querySelectorAll('#rawStudioModal .btn-studio-preset').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');

            const wrapper = document.getElementById('rawStudioViewportWrapper');
            const slider = document.getElementById('rawStudioWidthSlider');
            const badge = document.getElementById('rawStudioSliderBadge');
            const dimIndicator = document.getElementById('rawViewportDimensionIndicator');

            if (width === '100%') {{
                wrapper.style.maxWidth = '100%';
                wrapper.style.width = '100%';
                if (slider) slider.value = 1440;
                if (badge) badge.innerText = 'Full (100%)';
                if (dimIndicator) dimIndicator.innerText = '100% (Full Width)';
            }} else {{
                wrapper.style.maxWidth = width;
                wrapper.style.width = width;
                const num = parseInt(width);
                if (slider) slider.value = num;
                if (badge) badge.innerText = width;
                if (dimIndicator) dimIndicator.innerText = `${{width}} × auto`;
            }}
        }}

        function setRawStudioSliderWidth(val) {{
            document.querySelectorAll('#rawStudioModal .btn-studio-preset').forEach(b => b.classList.remove('active'));

            const wrapper = document.getElementById('rawStudioViewportWrapper');
            const badge = document.getElementById('rawStudioSliderBadge');
            const dimIndicator = document.getElementById('rawViewportDimensionIndicator');

            if (val >= 1440) {{
                wrapper.style.maxWidth = '100%';
                wrapper.style.width = '100%';
                badge.innerText = 'Full (100%)';
                dimIndicator.innerText = '100% (Full Width)';
                const fullBtn = document.querySelector('#rawStudioModal .btn-studio-preset[data-preset="100%"]');
                if (fullBtn) fullBtn.classList.add('active');
            }} else {{
                const w = `${{val}}px`;
                wrapper.style.maxWidth = w;
                wrapper.style.width = w;
                badge.innerText = w;
                dimIndicator.innerText = `${{w}} × auto`;
                const matchBtn = document.querySelector(`#rawStudioModal .btn-studio-preset[data-preset="${{w}}"]`);
                if (matchBtn) matchBtn.classList.add('active');
            }}
        }}

        function resetRawStudioWidth() {{
            const slider = document.getElementById('rawStudioWidthSlider');
            if (slider) slider.value = 1440;
            const fullBtn = document.querySelector('#rawStudioModal .btn-studio-preset[data-preset="100%"]');
            setRawStudioPreset('100%', fullBtn);
        }}

        function reloadRawStudioIframe() {{
            const iframe = document.getElementById('rawStudioIframe');
            if (iframe && iframe.src) {{
                const cur = iframe.src;
                iframe.src = 'about:blank';
                setTimeout(() => {{ iframe.src = cur; }}, 50);
            }}
        }}

        function closeRawStudio() {{
            const modal = document.getElementById('rawStudioModal');
            modal.classList.remove('active');
            document.body.style.overflow = '';
            const iframe = document.getElementById('rawStudioIframe');
            if (iframe) iframe.src = 'about:blank';
        }}

        // Backward compatibility
        function openRawModal(folder, title) {{
            openRawStudio(folder, title, 'code');
        }}
        function closeRawModal() {{
            closeRawStudio();
        }}

        function switchRawCodeTab(filename) {{
            rawActiveFile = filename;
            document.querySelectorAll('#rawModalTabsBar .code-tab-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-filename') === filename);
            }});

            const code = (RAW_DB[rawActiveFolder] && RAW_DB[rawActiveFolder][filename]) || "";
            document.getElementById('rawModalSubbarFilePath').innerText = `ui/components/raw/${{rawActiveFolder}}/${{filename}}`;
            const lines = code ? code.split('\\n').length : 0;
            const kb = (new Blob([code]).size / 1024).toFixed(1);
            document.getElementById('rawModalSubbarStats').innerText = `${{lines}} baris (${{kb}} KB)`;
            document.getElementById('rawModalCodeSnippet').innerText = code;
        }}

        async function copyCurrentRawStudioCode() {{
            let code = "";
            let label = "";

            if (rawCurrentMode === 'code') {{
                code = (RAW_DB[rawActiveFolder] && RAW_DB[rawActiveFolder][rawActiveFile]) || "";
                label = rawActiveFile;
            }} else {{
                const aioFile = `${{rawActiveFolder}}.html`;
                code = (RAW_DB[rawActiveFolder] && RAW_DB[rawActiveFolder][aioFile]) || "";
                label = `All-in-One (${{rawActiveFolder}})`;
            }}

            if (code) {{
                await navigator.clipboard.writeText(code);
                showToast(`Kode ${{label}} disalin ke clipboard!`);
            }} else {{
                showToast(`Kode tidak tersedia.`);
            }}
        }}

        async function copyRawAio(folder) {{
            const code = (RAW_DB[folder] && RAW_DB[folder][`${{folder}}.html`]) || "";
            if (code) {{
                await navigator.clipboard.writeText(code);
                showToast(`Kode raw ${{folder}} disalin!`);
            }}
        }}

        function downloadFile(filename, content) {{
            const mime = filename.endsWith('.html') ? 'text/html;charset=utf-8' :
                         filename.endsWith('.css') ? 'text/css;charset=utf-8' : 'text/plain;charset=utf-8';
            const blob = new Blob([content], {{ type: mime }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast(`File ${{filename}} berhasil diunduh!`);
        }}

        function quickDownloadRawAio(folder) {{
            const aioFile = `${{folder}}.html`;
            const code = (RAW_DB[folder] && RAW_DB[folder][aioFile]) || "";
            if (code) {{
                downloadFile(aioFile, code);
            }} else {{
                showToast(`File raw tidak ditemukan.`);
            }}
        }}

        function downloadCurrentRawStudioCode() {{
            if (rawCurrentMode === 'code') {{
                const code = (RAW_DB[rawActiveFolder] && RAW_DB[rawActiveFolder][rawActiveFile]) || "";
                if (code && rawActiveFile) {{
                    downloadFile(rawActiveFile, code);
                }} else {{
                    showToast(`Kode tidak tersedia untuk diunduh.`);
                }}
            }} else {{
                const aioFile = `${{rawActiveFolder}}.html`;
                const code = (RAW_DB[rawActiveFolder] && RAW_DB[rawActiveFolder][aioFile]) || "";
                if (code) {{
                    downloadFile(aioFile, code);
                }} else {{
                    showToast(`Kode tidak tersedia untuk diunduh.`);
                }}
            }}
        }}

        function showToast(msg) {{
            const t = document.getElementById('toastMsg');
            t.innerText = msg;
            t.classList.add('active');
            setTimeout(() => t.classList.remove('active'), 2500);
        }}

        document.getElementById('rawStudioModal').addEventListener('click', (e) => {{
            if (e.target.id === 'rawStudioModal') closeRawStudio();
        }});

        window.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                const modal = document.getElementById('rawStudioModal');
                if (modal && modal.classList.contains('active')) {{
                    closeRawStudio();
                }}
            }}
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

# Discover all projects in apps/
projects_registry = [
    {
        "id": "file-manager",
        "title": "Cloud File Manager",
        "version": "v2.4",
        "status": "Production Ready",
        "desc": "Sistem Operasi Manajemen Berkas Awan & Produktivitas AI Berbasis Glass Dark Premium dengan Web Audio synthesizer procedur, Canvas 2D swirl refraction, dan spring dock navigasi.",
        "icon": "cloud",
        "folder": "apps/file-manager",
        "components": [
            ("Floating Glass Dock", "compass", "components/glass/showcase.html#card-glass-dock-navigation"),
            ("Swirl Refraction Bottom Sheet", "layers", "components/glass/showcase.html#card-swirl-bottom-sheet"),
            ("Aurora Storage Card", "gauge", "components/glass/showcase.html#card-aurora-storage-card"),
            ("Frosted Folder Card", "folder", "components/glass/showcase.html#card-frosted-folder-card"),
            ("Telemetry Activity Chart", "bar-chart-2", "components/glass/showcase.html#card-telemetry-activity-chart"),
            ("Glass Buttons Collection", "sparkles", "components/glass/showcase.html#card-button-glass"),
            ("Form Input Fields", "text-cursor-input", "components/glass/showcase.html#card-input-field-glass"),
            ("Glass Toggle Switch", "toggle-left", "components/glass/showcase.html#card-toggle-switch-glass"),
            ("Glass Chat Input Bar", "message-square", "components/glass/showcase.html#card-chat-input-bar"),
            ("Prompt Pills Quick Scroller", "tag", "components/glass/showcase.html#card-prompt-pills-row"),
            ("AI Model Selector Card", "cpu", "components/glass/showcase.html#card-ai-model-selector"),
            ("Thinking Effort Selector", "sliders", "components/glass/showcase.html#card-thinking-effort-selector"),
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
        "title": "AI Agent Studio",
        "version": "v1.0",
        "status": "Interactive Prototype",
        "desc": "Ruang kerja agentik AI otonom interaktif dengan pemilihan model reaktif (K3-Pro Ultra, Swarm Agent, Flash Instant), pengatur penalaran bergradasi, respon streaming interaktif, dan sound haptik.",
        "icon": "sparkles",
        "folder": "apps/ai-studio",
        "components": [
            ("AI Model Selector Card", "cpu", "components/glass/showcase.html#card-ai-model-selector"),
            ("Thinking Effort Selector", "brain", "components/glass/showcase.html#card-thinking-effort-selector"),
            ("Prompt Pills Quick Scroller", "tag", "components/glass/showcase.html#card-prompt-pills-row"),
            ("Glass Chat Input Bar", "send", "components/glass/showcase.html#card-chat-input-bar"),
            ("Status Badge & Sound Synthesizer", "volume-2", "components/glass/showcase.html#card-avatar-badge-glass"),
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
    pdir = os.path.join(APPS_DIR, pid)
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
                    Semua folder di bawah direktori <code>apps/</code> akan otomatis menjadi bagian dari koleksi Web Applications ini.
                </p>
                <div class="add-instructions">
                    <div class="code-line">mkdir apps/nama-aplikasi</div>
                    <div class="code-line">cp apps/TEMPLATE.md apps/nama-aplikasi/PROJECT_SPEC.md</div>
                </div>
                <a href="apps/TEMPLATE.md" target="_blank" class="btn-blueprint">
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
    <title>Web Applications Studio — Production Projects</title>
    <meta name="description" content="Showroom & Workbench sekumpulan Aplikasi Web Utuh dari folder apps/ berbasis tema Glass Dark Premium.">
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Shared Design System Tokens (Single Source of Truth) -->
    <link rel="stylesheet" href="components/glass/css.css">
    <style>

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

        .card-slider-wrap {{
            display: inline-flex; align-items: center; gap: 6px;
            padding: 3px 8px; border-radius: 8px;
            background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
            margin-left: 4px;
        }}
        .slider-icon {{ width: 12px; height: 12px; color: var(--accent-cyan); opacity: 0.85; flex-shrink: 0; }}
        .card-slider-range {{
            -webkit-appearance: none; appearance: none;
            width: 80px; height: 4px; border-radius: 2px;
            background: rgba(255, 255, 255, 0.15); outline: none; cursor: pointer;
            transition: background 0.2s;
        }}
        .card-slider-range::-webkit-slider-thumb {{
            -webkit-appearance: none; appearance: none;
            width: 12px; height: 12px; border-radius: 50%;
            background: #38BDF8; box-shadow: 0 0 8px rgba(56, 189, 248, 0.7);
            cursor: pointer; transition: transform 0.15s;
        }}
        .card-slider-range::-webkit-slider-thumb:hover {{
            transform: scale(1.25);
        }}
        .slider-val-badge {{
            font-size: 10.5px; font-family: 'JetBrains Mono', monospace;
            color: #38BDF8; min-width: 36px; text-align: center;
        }}

        /* Live Preview Stage with Horizontal Slider Scrollbar */
        .app-live-stage {{
            position: relative; width: 100%; height: 750px; background: #040407;
            border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.08);
            display: flex; align-items: stretch; justify-content: center;
            overflow-x: auto; overflow-y: hidden;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6);
            scrollbar-width: thin;
            scrollbar-color: rgba(56, 189, 248, 0.45) rgba(0, 0, 0, 0.5);
        }}
        .app-live-stage::-webkit-scrollbar {{
            height: 8px;
        }}
        .app-live-stage::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.5);
            border-radius: 4px;
        }}
        .app-live-stage::-webkit-scrollbar-thumb {{
            background: linear-gradient(90deg, rgba(56, 189, 248, 0.45), rgba(139, 92, 246, 0.45));
            border-radius: 4px;
        }}
        .app-live-stage::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(90deg, rgba(56, 189, 248, 0.8), rgba(139, 92, 246, 0.8));
        }}

        .app-frame-wrapper {{
            width: 100%; height: 100%; transition: max-width 0.25s var(--ease-spring), width 0.25s var(--ease-spring);
            margin: 0 auto; display: flex; align-items: stretch; justify-content: center;
            flex-shrink: 0;
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
            display: none; grid-template-columns: repeat(auto-fit, minmax(min(100%, 380px), 1fr));
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
            .hub-header {{
                padding: 10px 14px;
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            .hub-header .header-actions {{
                width: 100%;
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 4px;
            }}
            .hub-main {{
                padding: 14px 14px 48px;
            }}
            .hero-banner {{
                margin-bottom: 16px;
            }}
            .hero-title {{
                font-size: 22px;
            }}
            .hero-desc {{
                font-size: 13px;
            }}
            .projects-selection-bar {{
                padding: 8px 10px;
                flex-direction: column;
                align-items: stretch;
                gap: 10px;
            }}
            .project-tabs-cluster {{
                width: 100%;
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
            }}
            .app-showcase-box {{
                padding: 14px;
                border-radius: 18px;
                margin-bottom: 20px;
            }}
            .app-card-topbar {{
                flex-direction: column;
                align-items: stretch;
                gap: 14px;
                padding-bottom: 12px;
            }}
            .app-controls-cluster {{
                width: 100%;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
            }}
            .viewport-selector,
            .card-slider-wrap {{
                display: none !important;
            }}
            .app-frame-wrapper {{
                width: 100% !important;
                max-width: 100% !important;
            }}
            .app-live-stage {{
                height: 500px;
                border-radius: 14px;
            }}
            .btn-launch-primary {{
                flex: 1;
                justify-content: center;
            }}
            .app-architecture-grid {{
                grid-template-columns: 1fr;
                gap: 16px;
            }}
            .projects-gallery-grid,
            .projects-gallery-grid.active {{
                grid-template-columns: 1fr !important;
                gap: 16px;
            }}
            .gallery-card {{
                padding: 14px;
                border-radius: 16px;
            }}
            .gallery-preview-frame {{
                height: 260px;
            }}
            .gallery-card-bottom {{
                flex-direction: column;
                align-items: stretch;
                gap: 8px;
            }}
            .gallery-card-bottom .btn-card-action {{
                width: 100%;
                justify-content: center;
            }}
            .modal-card {{
                width: 100%;
                height: 95vh;
                margin: 0;
                border-radius: 18px 18px 0 0;
            }}
            .modal-overlay {{
                padding: 0;
                align-items: flex-end;
            }}
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
                <h1>Proto<span>type</span> Web Applications</h1>
                <p>Portofolio & Workbench Seluruh Proyek di <code>apps/</code></p>
            </div>
        </div>

        <div class="header-actions">
            <a href="../../index.html" class="action-link-btn" title="Master Gateway Portal">
                <i data-lucide="home"></i> Gateway
            </a>
            <a href="components/glass/showcase.html" class="action-link-btn" title="Koleksi Komponen Kaca">
                <i data-lucide="gem"></i> Glass Components (24)
            </a>
            <a href="components/raw/showcase.html" class="action-link-btn" title="Koleksi Komponen Baku">
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
                Ruang kerja terpusat untuk menguji dan mengeksplorasi seluruh aplikasi web utuh yang berada di dalam folder <code>apps/</code>. Setiap proyek siap dijalankan dalam simulator multi-viewport atau diluncurkan penuh ke tab browser baru.
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
                            <span id="stageTitle">Cloud File Manager</span>
                            <span class="app-version-badge" id="stageVersionBadge">v2.4 Production Ready</span>
                        </h2>
                        <p id="stageDesc">Sistem Operasi Manajemen Berkas Awan & Produktivitas AI Berbasis Glass Dark Premium</p>
                    </div>
                </div>

                <div class="app-controls-cluster">
                    <div class="viewport-selector">
                        <button class="vp-btn active" onclick="setAppViewport('100%', this)" title="Desktop (100%)">
                            <i data-lucide="monitor"></i> Desktop
                        </button>
                        <button class="vp-btn" onclick="setAppViewport('768px', this)" title="Tablet (768px)">
                            <i data-lucide="tablet"></i> 768px
                        </button>
                        <button class="vp-btn" onclick="setAppViewport('375px', this)" title="Mobile (375px)">
                            <i data-lucide="smartphone"></i> 375px
                        </button>
                        <div class="card-slider-wrap" title="Slider Lebar Horizontal: Geser simulator viewport secara fluid">
                            <i data-lucide="sliders-horizontal" class="slider-icon"></i>
                            <input type="range" id="stageWidthSlider" min="360" max="1440" step="10" value="1440"
                                   oninput="setStageSliderWidth(this.value)" class="card-slider-range" aria-label="Slider lebar viewport">
                            <span class="slider-val-badge" id="stageWidthBadge">100%</span>
                        </div>
                    </div>

                    <button class="btn-tool-secondary" onclick="openActiveAppModal('PROJECT_SPEC.md')">
                        <i data-lucide="book-open"></i> Spesifikasi
                    </button>
                    <button class="btn-tool-secondary" onclick="openActiveAppModal('index.html')">
                        <i data-lucide="code"></i> Kode Sumber
                    </button>
                    <a href="apps/file-manager/index.html" target="_blank" class="btn-launch-primary" id="stageLaunchBtn">
                        <i data-lucide="external-link"></i> Jalankan Layar Penuh
                    </a>
                </div>
            </div>

            <!-- Live Interactive Stage -->
            <div class="app-live-stage">
                <div class="app-frame-wrapper" id="appFrameWrapper">
                    <iframe id="stageIframe" src="apps/file-manager/index.html" title="Live Preview"></iframe>
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
                    <p id="modalProjectPath">apps/...</p>
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
                <span class="subbar-file-path" id="modalActiveFilePath">apps/.../index.html</span>
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
            if (btn) btn.classList.add('active');
            const wrapper = document.getElementById('appFrameWrapper');
            const slider = document.getElementById('stageWidthSlider');
            const badge = document.getElementById('stageWidthBadge');

            if (width === '100%') {{
                if (wrapper) {{
                    wrapper.style.maxWidth = '100%';
                    wrapper.style.width = '100%';
                }}
                if (slider) slider.value = 1440;
                if (badge) badge.innerText = '100%';
            }} else {{
                if (wrapper) {{
                    wrapper.style.maxWidth = width;
                    wrapper.style.width = width;
                }}
                const num = parseInt(width);
                if (slider) slider.value = num;
                if (badge) badge.innerText = width;
            }}
        }}

        function setStageSliderWidth(val) {{
            const wrapper = document.getElementById('appFrameWrapper');
            const badge = document.getElementById('stageWidthBadge');
            document.querySelectorAll('.vp-btn').forEach(b => b.classList.remove('active'));

            if (val >= 1440) {{
                if (wrapper) {{
                    wrapper.style.maxWidth = '100%';
                    wrapper.style.width = '100%';
                }}
                if (badge) badge.innerText = '100%';
                const dBtn = document.querySelector('.vp-btn:first-child');
                if (dBtn) dBtn.classList.add('active');
            }} else {{
                const w = `${{val}}px`;
                if (wrapper) {{
                    wrapper.style.maxWidth = w;
                    wrapper.style.width = w;
                }}
                if (badge) badge.innerText = w;
                document.querySelectorAll('.vp-btn').forEach(b => {{
                    if (b.textContent.includes(w)) b.classList.add('active');
                }});
            }}
        }}

        function openActiveAppModal(filename) {{
            openAppModal(activeProjectId, filename);
        }}

        function openAppModal(pid, filename) {{
            modalProjectId = pid;
            const p = PROJECTS_META.find(x => x.id === pid) || {{}};
            document.getElementById('modalProjectTitle').innerText = `${{p.title || pid}} Source & Specs`;
            document.getElementById('modalProjectPath').innerText = `apps/${{pid}}/`;
            document.getElementById('appModal').classList.add('active');
            switchAppTab(filename || 'index.html');
        }}

        function switchAppTab(filename) {{
            currentTab = filename;
            document.getElementById('tab-btn-index').classList.toggle('active', filename === 'index.html');
            document.getElementById('tab-btn-spec').classList.toggle('active', filename === 'PROJECT_SPEC.md');

            const projFiles = APPS_DB[modalProjectId] || {{}};
            const code = projFiles[filename] || "";
            document.getElementById('modalActiveFilePath').innerText = `apps/${{modalProjectId}}/${{filename}}`;
            
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

with open(os.path.join(ROOT, "ui", "web", "apps.html"), "w", encoding="utf-8") as f:
    f.write(web_apps_html_content)

print("web-apps.html rebuilt as multi-project collection successfully!")
print("ALL CORE PAGES REBUILT AND OPTIMIZED!")
