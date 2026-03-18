import re
import os

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

header_logo_replacement = '''<a class="flex items-center" href="index.html">
<img src="assets/logo.png" alt="Miguel Cotto Promotions Logo" class="h-12 w-auto object-contain" />
</a>'''

footer_logo_replacement = '''<div class="flex items-center gap-3 text-white mb-6">
<img src="assets/logo.png" alt="Miguel Cotto Promotions Logo" class="h-16 w-auto object-contain" />
</div>'''

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Header logo matches
    # Usually we have a container for the logo. In these files, it often starts with <div class="flex items-center gap-... text-...
    # and ends with Cotto Promotions</h2> or similar
    
    # 1. Header logo with SVG or material icon ending in </h2> or </div>
    # Let's match from <div class="flex items-center gap... down to Miguel Cotto Promotions...</div>
    
    # Let's target the exact blocks we see:
    
    # Pattern for about.html, boxers.html, profile.html:
    pattern_header1 = re.compile(
        r'<div class="flex items-center gap-[^>]+>.*?<svg.*?Miguel Cotto Promotions.*?</div>', re.DOTALL
    )
    # Pattern for events.html:
    pattern_header2 = re.compile(
        r'<div class="flex items-center gap-[^>]+ text-white">\s*<div class="size-8 text-primary">.*?sports_kabaddi.*?<h2[^>]+>Miguel Cotto Promotions</h2>\s*</div>', re.DOTALL
    )
    # Pattern for news.html:
    pattern_header3 = re.compile(
        r'<div class="flex items-center gap-[^>]+>.*?sports_martial_arts.*?<h2.*?Miguel Cotto Promotions.*?</h2>\s*</div>', re.DOTALL
    )
    
    # Footer logos:
    pattern_footer1 = re.compile(
        r'<div class="flex items-center gap-[^>]+ text-white mb-6">.*?(?:<svg|<span).*?Miguel Cotto Promotions.*?</div>', re.DOTALL
    )
    
    # Apply
    # Actually, a more flexible regex for header logo:
    # A div containing 'flex items-center' that contains 'Miguel Cotto Promotions' and an icon
    # Since these are the ONLY places where the logo sits in the header/footer, we can do:
    
    new_content = content
    
    # Find all top-level logo divs
    new_content = re.sub(r'<div class="flex items-center gap-\d+[^"]*">\s*(?:<div|<span|<svg)(?:.*?)(?:Miguel Cotto Promotions)(?:.*?)</div>\s*(?:</div>)?', header_logo_replacement, new_content, count=1, flags=re.DOTALL)
    
    # Footer logo usually has mb-6
    new_content = re.sub(r'<div class="flex items-center gap-\d+[^"]* mb-[^"]*">(?:.*?)(?:Miguel Cotto Promotions)(?:.*?)</div>', footer_logo_replacement, new_content, count=1, flags=re.DOTALL)
    
    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated logos in {f}")
    else:
        print(f"No changes matched in {f}")

