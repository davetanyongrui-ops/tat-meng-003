import os, re

BASE = r'C:\Users\user\tat_meng_carpentry'
html_files = ['index.html', 'about.html', 'carpentry.html', 'services.html', 'portfolio.html', 'contact.html']

# Expected navigation links (should be consistent across all pages)
NAV_LINKS = [
    ('Home', '/'),
    ('Our Work', '/carpentry'),
    ('Services', '/services'),
    ('Portfolio', '/portfolio'),
    ('About Us', '/about'),
]

print('=== CROSS-FILE NAVIGATION LINK AUDIT ===')
print()

for fname in html_files:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'  {fname}: FILE NOT FOUND (X)')
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check internal nav links
    for link_text, expected_path in NAV_LINKS:
        if href := re.search(rf'href=["\'][\/]?{re.escape(expected_path)}[^"\'>]*', content):
            ok_line = f'LINK {link_text} -> {href.group(1)} -- OK'
        elif 'nav' in content.lower() or expected_path.replace('/', '') in content:
            # Text exists but href might use different format
            pass
        else:
            issues.append(f'missing nav link: {link_text}')
    
    # Check footer links 
    for term in ['Home', 'About Us', 'Portfolio', 'Contact']:
        if term.lower() not in content.lower():
            issues.append(f'missing footer ref: {term}')
    
    # Check contact info presence
    contact_checks = [
        ('email', r'tatmeng\.sg\@gmail\.com'),
        ('whatsapp/phone', r'\+65|\(24\/7\)'),  
        ('address/tampines', r'tampines.*st|tampines\s+\d+|workshop'),
    ]
    
    for name, pattern in contact_checks:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append(f'contact missing: {name}')
    
    status = 'ALL CLEAR' if not issues else 'ISSUES: ' + '; '.join(issues)
    print(f'  {fname}: {status}\n')

print('\n=== EXACT CONTACT INFO IN FOOTER ===')
for fname in html_files:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    footer_section = ''  
    # Find footer section (last ~10000 chars typically contains footer)
    footer_start = max(0, len(content) - 10000)
    footer_section = content[footer_start:]
    
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', footer_section)
    phone_pat = r'\+?65\s?\d[\d\s\-\(\)]{7,10}'
    phones = re.findall(phone_pat, content)  
    
    print(f'\n--- {fname} footer contact data ---')
    if emails:
        for e in set(emails):
            print(f'  email: {e}')
    if 'wa.me' in content or 'whatsapp' in content.lower():
        wa_links = re.findall(r'https?://(?:wa\.me|web\.whatsapp\.com)[^\s\"\']+', content)
        for w in set(wa_links):
            print(f'  whatsapp: {w}')
    if tamps := re.findall(r'(Tampines St \d+ .*)', content):
        for addr in set(tamps):
            print(f'  address: {addr}')
