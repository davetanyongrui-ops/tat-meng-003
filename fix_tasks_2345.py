import os, re, json

BASE = r'C:\Users\user\tat_meng_carpentry'

# ============================================================
# TASK 2: Emoji → Inline SVG replacement map (emoji_char → SVG)
# ============================================================
EMOJI_SVG = {
    '\U0001F3ED': '<svg class="w-10 h-10 mx-auto mb-5 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M19 21V5a2 2 0 00-2-2H7l-3 3v11a2 2 0 002 2z"/><path d="M9 18a1 1 0 112 0H9zM15 18a1 1 0 112 0h-2z"/></svg>',
    '\U0001F91D': '<svg class="w-10 h-10 mx-auto mb-5 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M7 21a4 4 0 01-4-4V9a4 4 0 018 0v1a1 1 0 01-2 0V9a2 2 0 10-4 0v8a2 2 0 002 2"/><path d="M17 21a4 4 0 004-4V9a4 4 0 00-8 0v1a1 1 0 002 0V9a2 2 0 114 0v8a2 2 0 01-2 2"/></svg>',
    '\U0001F527': '<svg class="w-10 h-10 mx-auto mb-5 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>',
    '\u26A1':     '<svg class="w-5 h-5 inline-block mr-1 text-gold-500 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    '\U0001F4AC': '<svg class="w-5 h-5 inline-block mr-1 flex-shrink-0 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
    '\u2709\uFE0F': '<svg class="w-4 h-4 text-gold-400 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>',
    '\uD83D\uDCCC': '<svg class="w-4 h-4 text-gold-400 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
    '\U0001F538': '<svg class="w-4 h-4 text-gold-400 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>',
}

def replace_emojis(content):
    for emj, svg in EMOJI_SVG.items():
        cnt = content.count(emj)
        if cnt > 0:
            content = content.replace(emj, svg)
    return content


# ============================================================
# TASK 3+4: Unsplash → picsum.photos seeded replacement map
# Each unique photo ID gets a descriptive seed.
# Full-width hero images get 1920/1080, cards get 600/450 etc.
# ============================================================

# Build a master mapping of (photo_id, params) → new picsum URL
def build_picsum_replacements():
    replacements = []
    
    # Helper to create a replace dict entry: old_url_fragment → new_url_fragment
    def repl(photo_id, seed, w, h, fit='crop', q=80):
        return (photo_id, f'w={w}', f'h={h}' if h else '', fit, q, seed)
    
    # INDEX.HTML replacements
    idx_picsum = {
        ('1632890471155', 'tatmeng-hero-living'):      ('https://picsum.photos/seed/tatmeng-hero-living/1920/1080', 1920, 1080),  # hero bg (unpic already uses id/328 which is fine)
        ('1556909114', 'tatmeng-kitchen-pantry'):       ('https://picsum.photos/seed/tatmeng-kitchen-pantry/600/450'),  
        ('1600566753086', 'tatmeng-magic-corner'):      ('https://picsum.photos/seed/tatmeng-magic-corner/600/450'),
        ('1600585154526', 'tatmeng-waste-sorting'):     ('https://picsum.photos/seed/tatmeng-waste-sorting/600/450'),  
        ('1600607687939', 'tatmeng-gas-stove-cabinet'): ('https://picsum.photos/seed/tatmeng-gas-stove/600/450'),
        ('1600607687920', 'tatmeng-workflow-design'):   ('https://picsum.photos/seed/tatmeng-workflow/600/400'),
        ('1600607687644', 'tatmeng-zero-glare-living'): ('https://picsum.photos/seed/tatmeng-zero-glare/500/350'),
        ('1600566752355', 'tatmeng-kitchen-island'):    ('https://picsum.photos/seed/tatmeng-kitchen-island/500/350'),
        # LED cornices cards:
        ('1507146426996', 'tatmeng-led-perimeter'):     ('https://picsum.photos/seed/tatmeng-led-perimeter/500/350'),
        ('1524758631624', 'tatmeng-lighting-hallway'):  ('https://picsum.photos/seed/tatmeng-lighting-hallway/500/350'),
        # Portfolio cards:
        ('1600585154340', 'tatmeng-hdb-living-room'):   ('https://picsum.photos/seed/tatmeng-hdb-living-room/600/800'),
        ('1600566752355', 'tatmeng-condo-bedroom'):     ('https://picsum.photos/seed/tatmeng-condo-bedroom/600/800'),  
        # Services cards:
        ('1600566753190', 'tatmeng-hidden-storage'):    ('https://picsum.photos/seed/tatmeng-hidden-storage/600/400'),
        ('1600585154340', 'tatmeng-wet-works-basement'):('https://picsum.photos/seed/tatmeng-wet-works/600/400'),
        # CTA bg:
        ('1616486338812', 'tatmeng-showroom-interior'): ('https://picsum.photos/seed/tatmeng-showroom-int/1920/600', 1920, 600),
    }
    
    return idx_picsum

# Build a simple mapping: photo_id (just the numeric ID) → picsum seed name
PHOTO_SEEDS = {
    # INDEX unique seeds
    '1556909114':    'tatmeng-kitchen-pantry',
    '1600566753086':  'tatmeng-magic-corner',
    '1600585154526':  'tatmeng-waste-sorting-cabinet',
    '1600607687939':  'tatmeng-gas-stove-cabinet',
    '1600607687920':  'tatmeng-workflow-space-design',
    '1600607687644':  'tatmeng-zero-glare-living-room',
    '1600566752355':  'tatmeng-kitchen-island',
    '1507146426996':  'tatmeng-led-perimeter-lighting',  
    '1524758631624':  'tatmeng-lighting-hallway-warm',
    '1600585154340':  'tatmeng-hdb-living-room-furniture',
    '1616486338812':  'tatmeng-showroom-interior-wide',
    
    # CARPENTRY unique seeds  
    '1507089947368':  'tatmeng-hdb-kitchen-cabinet-tampines',
    '1523413651479':  'tatmeng-condo-dining-unit-marinabay',
    '1560448204':     'tatmeng-kitchen-counter-detail-wood',
    '1600573472591':  'tatmeng-storage-wardrobe-interior-gold',
    
    # SERVICES unique seeds
    '1504307651254':  'tatmeng-wet-works-concrete-flooring',
    '1581094794329':  'tatmeng-plumbing-coordination-pipe',
    '1581783898382':  'tatmeng-tile-laying-hd-bathroom',  
    '1585704032916':  'tatmeng-demolition-wall-removal',
    
    # ABOUT unique seeds
    '1504208434309':  'tatmeng-team-workshop-photo',
    '1594633313593':  'tatmeng-quality-inspection-materials',
    '1600596542815':  'tatmeng-craftsman-hand-tools-detailed',
    '1604871000606':  'tatmeng-installation-measurements-on-site',
    
    # CONTACT unique seeds  
    '1600566753190':  'tatmeng-workshop-exterior-aerial',
    '1600607687939':  'tatmeng-street-front-view-tampines',
    
    # PORTFOLIO unique seeds
    '1600585154340':  'tatmeng-project-bishan-hdb-living',   
    '1600585154526':  'tatmeng-project-westcoast-condo-bedroom',
}

def replace_unsplash_with_picsum(content, filename):
    """Replace all Unsplash photo URLs with picsum.photos seeded URLs."""
    
    for photo_id, seed in PHOTO_SEEDS.items():
        if photo_id not in content:
            continue
            
        # Find the full URL pattern for this photo ID
        pattern = re.compile(r'(https?://(?:images\.unsplash\.com|unpic\.fra1\.cdn\.picsum\.photos/id/\d+)'
                             r'/photo-' + photo_id + r'[^"\s<>]*)', re.IGNORECASE)
        
        matches = pattern.findall(content)
        if not matches:
            # Try alternate unpic pattern: id/PHOTO_ID  
            pattern2 = re.compile(r'https://unpic\.fra1\.cdn\.picsum\.photos/id/' + photo_id + r'[^"\s<>]*')
            for m in pattern2.findall(content):
                # Extract the ID and params
                pass
        
        for match in matches:
            # Preserve query params from original URL (w, h, fit, q)
            url_parts = re.split(r'/photo-' + photo_id, match)
            prefix = url_parts[0]  # base URL up to photo-
            
            # Extract size params 
            rest_params = ''
            if len(url_parts) > 1:
                rest_params = url_parts[1]
            
            # Parse w,h from original
            w_match = re.search(r'w=(\d+)', rest_params)
            h_match = re.search(r'h=(\d+)', rest_params)
            fit_match = re.search(r'fit=crop', rest_params)
            q_match = re.search(r'q=(\d+)', rest_params)
            
            w = int(w_match.group(1)) if w_match else 600
            h = int(h_match.group(1)) if h_match else (450 if 'w=1920' in rest_params else (800 if h > 600 else 400) if f'photo-{seed}' in content else 350)
            
            # Override sizes based on context detection
            is_hero = False
            if w >= 1920 or 'w=1920' in rest_params:
                is_hero = True
                h = 1080
            
            # Build new picsum URL  
            new_url = f'https://picsum.photos/seed/{seed}/{w}/{h}'
            
            # Check for other image service domains and route appropriately
            if 'unpic' in prefix:
                # For unpic URLs, still use picsum.photos since that's the requirement
                pass
            
            new_full = f'{prefix}https://picsum.photos/seed/{seed}/{w}/{h}'
            
    return content

# Actually let me take a much simpler approach - just do direct string replacements
def do_all_replacements():
    files_processed = []
    
    files_to_process = sorted([f for f in os.listdir(BASE) if f.endswith('.html')])
    
    for fname in files_to_process:
        path = os.path.join(BASE, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_len = len(content)
        
        # TASK 2: Replace emojis  
        content = replace_emojis(content)
        
        # TASK 3+4: Replace Unsplash URLs with picsum.photos seeded URLs
        for photo_id, seed in PHOTO_SEEDS.items():
            if photo_id not in content:
                continue
            
            # Build pattern matching the full unsplash URL with this photo ID
            pattern = re.compile(r'https?://(?:images\.unsplash\.com/photo-' + photo_id+r'|unpic\.fra1\.cdn\.picsum\.photos/id/' 
                                 + photo_id + r')[^"\'\s<>,]*')
            
            matches = pattern.findall(content)
            if not matches:
                # Try alternate unpic format
                pattern2 = re.compile(r'https://unpic\.fra1\.cdn\.picsum\.photos/id/' + photo_id + r'/\d+/[^"\'\s<>,]*')
                matches = pattern2.findall(content)
            
            if not matches:
                continue
                
            for old_url in set(matches):
                # Extract the query params from original URL
                w_match = re.search(r'w=(\d+)', old_url)
                h_match = re.search(r'h=(\d+)', old_url)
                
                w = int(w_match.group(1)) if w_match else 600
                h = int(h_match.group(1)) if (h_match and len(old_url) > 50) else None
                
                # Determine appropriate height
                if not h:
                    if w >= 1920:
                        h = 1080  
                    elif 'aspect-3/4' in old_url or 'w=600&h=800' in old_url or 'h=800' in old_url:
                        h = 800
                    else:
                        h = 450
                
                new_url = f'https://picsum.photos/seed/{seed}/{w}/{h}'
                content = content.replace(old_url, new_url)
        
        # Write back if changed
        if len(content) != orig_len:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_processed.append(fname)
    
    # Final verification
    print('=== POST-FIX VERIFICATION ===\n')
    
    for fname in sorted(os.listdir(BASE)):
        if not fname.endswith('.html'):
            continue
        path = os.path.join(BASE, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check remaining Unsplash images
        unsplash_count = len(re.findall(r'images\.unsplash\.com', content))  
        unpic_count = len(re.findall(r'unpic\.fra1\.cdn\.picsum\.photos/id/', content))
        
        if unsplash_count > 0:
            issues.append(f'{unsplash_count} remaining Unsplash URLs')
        
        # Check remaining emojis
        for emj in EMOJI_SVG:
            c = content.count(emj)  
            if c > 0:
                issues.append(f'emoji {emj}: {c}x remaining')
        
        status = f'BROKEN: {issues}' if issues else 'ALL CLEAR'
        print(f'  {fname}: {status}')
    
    print(f'\n=== FILES PROCESSED ===')
    for fname in files_processed:
        print(f'  ✓ {fname}')


if __name__ == '__main__':
    do_all_replacements()
