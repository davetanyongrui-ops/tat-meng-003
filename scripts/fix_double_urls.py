"""Fix the double-URL issue from previous script."""
import re
from pathlib import Path

root = Path("C:/Users/user/tat_meng_carpentry")
HTML_FILES = ["index.html","carpentry.html","services.html","portfolio.html","about.html","contact.html"]

for fname in HTML_FILES:
    fpath = root / fname
    if not fpath.exists():
        continue
    
    content = fpath.read_text(encoding="utf-8")
    original = content
    
    # Pattern: target_url followed (no space) by picsum/url -> remove the picsum part
    # The real URLs all end with .jpg before the broken appendage
    pattern = r'(https://[^\""\s]*\.jpg)(https://picsum\.photos/[^\""\s]*)'
    
    def clean(m):
        return m.group(1)  # keep only the target URL
    
    content = re.sub(pattern, clean, content)
    
    if content != original:
        fpath.write_text(content, encoding="utf-8")
        print(f"FIXED: {fname}")

print("Done cleaning double URLs")
