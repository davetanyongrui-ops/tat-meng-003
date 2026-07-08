"""Fix phone numbers across all HTML files to be clickable tel: links."""
import re
from pathlib import Path

root = Path("C:/Users/user/tat_meng_carpentry")
HTML_FILES = ["index.html", "carpentry.html", "services.html", "portfolio.html", "about.html"]

PHONE_SVG = '<svg class="w-4 h-4 inline-block mr-1.5 align-text-bottom fill-none stroke-current" viewBox="0 0 24 24" stroke-width="1.5"><path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>'

for fname in HTML_FILES:
    fpath = root / fname
    if not fpath.exists():
        continue
    
    content = fpath.read_text(encoding="utf-8")
    original = content
    
    if fname == "index.html":
        # Format: <li class="text-stone-400" style="font-family:Inter,sans-serif;"><span>&#128222; +65 9392 6778 (General)</span><br>...
        old_block = '<li class="text-stone-400" style="font-family:Inter,sans-serif;"><span>&#128222; +65 9392 6778 (General)</span><br><span>&#128222; +65 9187 1757 (Consultations)</span><br><span>&#128222; +65 9028 6373 (After-Sales)</span></li>'
        
        parts = []
        for num, label in [("+65 9392 6778", "(General)"), ("+65 9187 1757", "(Consultations)"), ("+65 9028 6373", "(After-Sales)")]:
            d = re.sub(r"[^\d]", "", num)
            line = '<li class="text-stone-400"><a href="tel:+{0}" class="hover:text-gold-300 transition-colors block" style="font-family:Inter,sans-serif;">{1}{2} {3}</a></li>'.format(d, PHONE_SVG, num, label)
            parts.append(line)
        
        content = content.replace(old_block, "\n".join(parts))

    elif fname == "carpentry.html":
        # Format: <li class="flex items-start gap-2"><svg...phone icon...><span class="text-slate-400">+65 9392 6778<br>+65 9187 1757<br>+65 9028 6373</span></li>
        ul_match = re.search(r'<ul class="space-y-3 text-sm">.*?</ul>', content, re.DOTALL)
        if ul_match:
            block = content[ul_match.start():ul_match.end()]
            # Find the phone li and replace it
            phone_li = re.search(r'<li class="flex items-start gap-2"><svg[^>]*phone[^>]*</svg><span class="text-slate-400">([^<]+)</span></li>', block, re.IGNORECASE)
            if phone_li:
                nums_str = phone_li.group(1)
                nums = ["+65 9392 6778", "+65 9187 1757", "+65 9028 6373"]
                new_parts = []
                for n in nums:
                    d = re.sub(r"[^\d]", "", n)
                    svg = '<svg class="w-4 h-4 text-gold-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>'
                    line = '<li class="flex items-start gap-2">{0}<span class="text-slate-400"><a href="tel:+{1}" class="hover:text-gold-300">{2}</a></span></li>'.format(svg, d, n)
                    new_parts.append(line)
                block = block[:phone_li.start()] + "\n".join(new_parts) + block[phone_li.end():]
                content = content[:ul_match.start()] + block + content[ul_match.end():]

    elif fname == "services.html":
        # Format: <li class="text-slate-400">+65 9392 6778<br>+65 9187 1757<br>+65 9028 6373</li>
        old_block = '<li class="text-slate-400">+65 9392 6778<br>+65 9187 1757<br>+65 9028 6373</li>'
        new_parts = []
        for n in ["+65 9392 6778", "+65 9187 1757", "+65 9028 6373"]:
            d = re.sub(r"[^\d]", "", n)
            new_parts.append('<li class="text-slate-400"><a href="tel:+{0}" class="hover:text-gold-300 transition-colors">{1}</a></li>'.format(d, n))
        content = content.replace(old_block, "\n".join(new_parts))

    elif fname == "portfolio.html":
        # Format: <li class="text-slate-400">+65 9392 6778 / +65 9187 1757<br>9003 Tampines St 9 #01-156, Singapore 528837</li>
        old_block = '<li class="text-slate-400">+65 9392 6778 / +65 9187 1757<br>9003 Tampines St 9 #01-156, Singapore 528837</li>'
        new_parts = [
            '<li class="text-slate-400"><a href="tel:+6593926778" class="hover:text-gold-300 transition-colors">+65 9392 6778</a> / <a href="tel:+6591871757" class="hover:text-gold-300 transition-colors">+65 9187 1757</a><br>' +
            '<li class="text-slate-400"><a href="tel:+6590286373" class="hover:text-gold-300 transition-colors">+65 9028 6373 (After-Sales)</a></li>',
            '<li class="text-slate-400"><svg class="w-4 h-4 inline-block mr-1.5 align-text-bottom" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg><a href="https://maps.google.com/?q=9003+Tampines+St+9+%2301-156+Singapore+528837" target="_blank" rel="noopener" class="hover:text-gold-300 transition-colors">9003 Tampines St 9 #01-156, Singapore 528837</a></li>'
        ]
        content = content.replace(old_block, "\n".join(new_parts))

    elif fname == "about.html":
        # Format: <li class="text-slate-400">+65 9392 6778 / +65 9187 1757 / +65 9028 6373</li>
        old_block = '<li class="text-slate-400">+65 9392 6778 / +65 9187 1757 / +65 9028 6373</li>'
        new_parts = []
        for n in ["+65 9392 6778", "+65 9187 1757", "+65 9028 6373"]:
            d = re.sub(r"[^\d]", "", n)
            new_parts.append('<li class="text-slate-400"><a href="tel:+{0}" class="hover:text-gold-300 transition-colors">{1}</a></li>'.format(d, n))
        content = content.replace(old_block, "\n".join(new_parts))

    if content != original:
        fpath.write_text(content, encoding="utf-8")
        print("MODIFIED: {0}".format(fname))
    else:
        print("UNCHANGED: {0}".format(fname))

print("Done!")
