import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pages_to_check = [
    os.path.join(ROOT, "index.html"),
    os.path.join(ROOT, "showcase.html"),
    os.path.join(ROOT, "web-apps.html"),
    os.path.join(ROOT, "404.html"),
    os.path.join(ROOT, "projects", "file-manager", "index.html"),
    os.path.join(ROOT, "projects", "ai-studio", "index.html"),
    os.path.join(ROOT, "ui", "components", "glass", "showcase.html"),
    os.path.join(ROOT, "ui", "components", "raw", "showcase.html"),
]

link_patterns = [
    re.compile(r'href=["\'](.*?)["\']', re.IGNORECASE),
    re.compile(r'src=["\'](.*?)["\']', re.IGNORECASE),
]

broken = []
verified_count = 0

print("Verifying link integrity across all core HTML pages...")

for p in pages_to_check:
    if not os.path.exists(p):
        broken.append((p, "FILE DOES NOT EXIST ON DISK", p))
        continue
    
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()

    p_dir = os.path.dirname(p)
    rel_page = os.path.relpath(p, ROOT)

    found_links = set()
    for pattern in link_patterns:
        for match in pattern.findall(content):
            found_links.add(match)

    for link in sorted(found_links):
        # Skip external, inline anchors, data URIs, javascript, and JS template variables
        if link.startswith(('http://', 'https://', '#', 'data:', 'javascript:', 'mailto:')) or '${' in link:
            continue
        
        # Strip query parameters and anchors
        clean_target = link.split('?')[0].split('#')[0]
        if not clean_target:
            continue

        resolved_target = os.path.normpath(os.path.join(p_dir, clean_target))
        verified_count += 1

        if not os.path.exists(resolved_target):
            broken.append((rel_page, link, resolved_target))

print(f"Total internal links, iframes, and assets tested: {verified_count}")

if broken:
    print(f"\n[FAILED] Found {len(broken)} broken link(s):")
    for page, link, target in broken:
        print(f"  - In [{page}]: link '{link}' -> NOT FOUND at: {target}")
    exit(1)
else:
    print("\n[PASSED] 100% of internal links, iframes, and assets exist and resolve perfectly!")
