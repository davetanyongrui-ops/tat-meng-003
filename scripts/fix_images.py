import re, sys
from pathlib import Path

root = Path("C:/Users/user/tat_meng_carpentry")
HTML_FILES = ["index.html","carpentry.html","services.html","portfolio.html","about.html","contact.html"]

URLS = {
    "kitchen": "https://lamaisoncarpentry.com/wp-content/uploads/2026/04/Kitchen-Storage-Solutions-Singapore.jpg",
    "wardrobe_closet": "https://www.theheritagewardrobecompany.com/wp-content/uploads/2023/06/hayes-buckinghamshire-4.jpg",
    "cornice_lighting": "https://cdn.shopify.com/s/files/1/0206/8076/files/629b8493-b498-40e6-9c53-61b33f2e2d56.jpg",
    "space_living": "https://media.designcafe.com/wp-content/uploads/2021/05/28195456/space-saving-living-room-furniture.jpg",
}

class Counter:
    def __init__(self):
        self.value = 0

counter = Counter()

def classify(tag_text, seed):
    lower = tag_text.lower() + " " + seed.lower()
    
    # Kitchen first (highest priority matches)
    if any(k in lower for k in ["kitchen","cabinet","island-counter","dining","pantry","kitchens-cabinets"]):
        return URLS["kitchen"], "KITCHEN"
    # Wardrobe/closet
    if any(k in lower for k in ["wardrobe", "closet", "hidden-storage"]):
        # But kitchen context overrides
        if "kitchen" in lower or "cabinet" in lower:
            return URLS["kitchen"], "KITCHEN (was wardrobe seed)"
        return URLS["wardrobe_closet"], "WARDROBE"
    # Cornice/lighting
    if any(k in lower for k in ["cornice", "ledge", "ambient", "zero-glare", "warm-dimming", 
                                 "perimeter-lighting", "lighting-hallway", "hallway-warm"]):
        return URLS["cornice_lighting"], "CORNICED"
    # Space planning/living room
    if any(k in lower for k in ["space-plan", "sparing", "workflow-design", "living-room", 
                                 "floor-plan", "workflow-space-planning"]):
        return URLS["space_living"], "SPACING"
    
    # Portfolio-specific classification by seed names
    portfolio_map = {
        "hdb-kitchen-cabinet-tampines-project": (URLS["kitchen"], "KITCHEN"),
        "hidden-storage-closet-wardrobe": (URLS["wardrobe_closet"], "WARDROBE"),
        "kitchen-counter-wood-detail-workshop": (URLS["kitchen"], "KITCHEN"),
        "condo-dining-unit-marina-bay-project": (URLS["kitchen"], "KITCHEN"),
        "magic-corner-rotating-system": (URLS["wardrobe_closet"], "WARDROBE"),  # rotating corner system
        "waste-sorting-cabinet-softclose": (URLS["kitchen"], "KITCHEN"),
        "tatmeng-showroom-interior-wide-angle": (URLS["space_living"], "SPACE/LIVING fallback"),
        "tatmeng-workshop-exterior-aerial-tampines": (URLS["space_living"], "EXT/FALLBACK"),
        "tatmeng-street-view-tampines-front": (URLS["kitchen"], "STREET FALLBACK"),
        "tatmeng-kitchen-pantry-full-extension": (URLS["kitchen"], "KITCHEN"),
    }
    
    for seed_k, val in portfolio_map.items():
        if seed_k.startswith(seed) or seed.lower().startswith(seed_k) or seed_k in lower:
            return val
    
    # Fallback: use cornice/ambient lighting as default interior shot
    return URLS["cornice_lighting"], "FALLBACK CORNICED"

def do_replace(m, content):
    prefix = m.group(1)  # <img...src=\"
    suffix = m.group(2)  # \"...> (rest of tag after URL)
    full_src = re.search(r'(https://picsum\.photos/[^"]+)', prefix + suffix)
    if not full_src:
        return m.group(0)
    
    src_url = full_src.group(1)
    seed_match = re.search(r'seed/([^/"\?]+)', src_url)
    seed = (seed_match.group(1).lower() if seed_match else "")
    
    # Get surrounding context (the <a> or section this img is in)
    start_srch = max(0, m.start() - 800)
    end_srch = min(len(content), m.end() + 200)
    surrounding = content[start_srch:end_srch]
    
    url, label = classify(surrounding, seed)
    new_tag = prefix + url + suffix
    counter.value += 1
    return new_tag

for fname in HTML_FILES:
    fpath = root / fname
    if not fpath.exists():
        print(f"SKIP: {fname}")
        continue
    
    content = fpath.read_text(encoding="utf-8")
    original = content
    
    pattern = re.compile(r'(<img[^>]*src=")(https://picsum\.photos/[^"]+)("[^>]*/?>)')
    # Use a wrapper that captures content
    def make_repl(content):
        def repl(m):
            return do_replace(m, content)
        return repl
    
    content = pattern.sub(make_repl(original), content)
    
    if content != original:
        fpath.write_text(content, encoding="utf-8")
        print(f"MODIFIED: {fname}")
    else:
        print(f"UNCHANGED: {fname}")

print(f"\nTotal replaced: {counter.value}")
