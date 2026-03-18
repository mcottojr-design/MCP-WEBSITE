import os
import re

header_regex = re.compile(
    r'<a class="flex items-center gap-3 text-white" href="index\.html".*?>\s*'
    r'<div class="w-10 h-10 bg-primary.*?>\s*'
    r'<span class="material-symbols-outlined.*?sports_martial_arts</span>\s*'
    r'</div>\s*'
    r'<span class="text-xl font-bold.*?>Miguel Cotto.*?Promotions</span></span>\s*'
    r'</a>', re.DOTALL
)

footer_regex = re.compile(
    r'<div class="flex items-center gap-3 text-white mb-10">\s*'
    r'<div class="w-12 h-12 bg-primary.*?>\s*'
    r'<span class="material-symbols-outlined.*?sports_martial_arts</span>\s*'
    r'</div>\s*'
    r'<span class="text-3xl font-black.*?>Miguel Cotto.*?Promotions</span></span>\s*'
    r'</div>', re.DOTALL
)

header_new = '''<a class="flex items-center" href="index.html">
<img src="assets/logo.png" alt="Miguel Cotto Promotions Logo" class="h-12 w-auto object-contain" />
</a>'''

footer_new = '''<div class="flex items-center justify-center mb-10">
<img src="assets/logo.png" alt="Miguel Cotto Promotions Logo" class="h-16 w-auto object-contain" />
</div>'''

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    new_content = header_regex.sub(header_new, content)
    new_content = footer_regex.sub(footer_new, new_content)

    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated logos in {f}")
    else:
        print(f"No changes matched in {f}")
