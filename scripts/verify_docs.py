import os
import re
import urllib.parse

ROOT = os.path.abspath(r"d:\PROJECT\prototype")

print("Verifying link integrity across all Markdown documentation...")

md_files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    # Skip .git, node_modules, and hidden directories
    if ".git" in dirpath or "node_modules" in dirpath:
        continue
    for fname in filenames:
        if fname.endswith(".md"):
            md_files.append(os.path.join(dirpath, fname))

md_files.sort()

link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

broken = []
total_links = 0

for md_path in md_files:
    rel_md = os.path.relpath(md_path, ROOT)
    with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    matches = link_pattern.findall(content)
    for text, link in matches:
        link = link.strip()
        # Skip external web links, anchors, mailto
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        
        total_links += 1
        
        # Handle file:/// URIs
        if link.startswith("file:///"):
            raw_path = link[8:]
            # On Windows, e.g. d:/PROJECT/... or d:\PROJECT\...
            raw_path = urllib.parse.unquote(raw_path)
            clean_path = raw_path.split("#")[0].split("?")[0]
            norm_target = os.path.normpath(clean_path)
        else:
            clean_path = link.split("#")[0].split("?")[0]
            if not clean_path:
                continue
            norm_target = os.path.normpath(os.path.join(os.path.dirname(md_path), clean_path))
        
        if not os.path.exists(norm_target):
            broken.append((rel_md, link, norm_target))

print(f"Scanned {len(md_files)} Markdown files.")
print(f"Total internal Markdown links checked: {total_links}")

if broken:
    print(f"\n[FAILED] Found {len(broken)} broken link(s) in Markdown files:")
    for doc, link, target in broken:
        print(f"  - In [{doc}]: link '{link}' -> NOT FOUND: {target}")
    exit(1)
else:
    print("\n[PASSED] 100% of internal Markdown links resolve successfully to real files!")
