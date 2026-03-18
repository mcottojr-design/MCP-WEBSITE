import re
import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    if f == 'index.html': continue
    with open(f, 'r') as file:
        content = file.read()
    
    # Extract header logo block loosely (something containing an icon and Cotto)
    # usually inside header: <div class="flex items-center gap... text-white">...</div>
    match = re.search(r'(<div[^>]*flex items-center gap-[^>]*>.*?Cotto.*?</div>)', content, flags=re.DOTALL)
    if match:
        print(f"--- {f} Header Logo ---")
        print(match.group(1)[:200] + "...")
        print()
