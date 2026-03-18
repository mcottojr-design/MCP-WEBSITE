import os
import shutil
import re

# 1. Restore originals
shutil.copyfile("latest_news_miguel_cotto_promotions/code.html", "news.html")
shutil.copyfile("boxer_roster_miguel_cotto_promotions/code.html", "boxers.html")
shutil.copyfile("about_us_miguel_cotto_promotions/code.html", "about.html")
shutil.copyfile("boxer_profile_with_social_links/code.html", "profile.html")

# 2. Extract Header and Footer from index.html
with open("index.html", "r") as f:
    idx_content = f.read()

header_match = re.search(r'(<!-- Top Navigation -->\s*<header.*?</header>)', idx_content, flags=re.DOTALL)
header_str = header_match.group(1) if header_match else ""

footer_match = re.search(r'(<!-- Footer -->\s*<footer.*?</footer>)', idx_content, flags=re.DOTALL)
footer_str = footer_match.group(1) if footer_match else ""

# 3. Patch the restored files
files_to_patch = ["news.html", "boxers.html", "about.html", "profile.html"]

for f in files_to_patch:
    with open(f, "r") as html_f:
        content = html_f.read()
    
    # 3a. Fix Links (mimicking fix_links.py logic safely)
    content = re.sub(r'\{\{DATA:SCREEN:SCREEN_.*?boxers\}\}', 'boxers.html', content)
    content = re.sub(r'\{\{DATA:SCREEN:SCREEN_.*?events\}\}', 'events.html', content)
    content = re.sub(r'\{\{DATA:SCREEN:SCREEN_.*?news\}\}', 'news.html', content)
    content = re.sub(r'\{\{DATA:SCREEN:SCREEN_.*?home\}\}', 'index.html', content)
    content = re.sub(r'\{\{DATA:SCREEN:SCREEN_.*?roster\}\}', 'boxers.html', content)
    content = re.sub(r'href="#"', 'href="index.html"', content)
    
    # 3b. Replace Header
    if header_str:
        content = re.sub(r'<!-- Top Navigation -->\s*<header.*?</header>', header_str, content, flags=re.DOTALL)
    
    # 3c. Replace Footer
    if footer_str:
        content = re.sub(r'<!-- Footer -->\s*<footer.*?</footer>', footer_str, content, flags=re.DOTALL)
        
    with open(f, "w") as html_f:
        html_f.write(content)
        
print("Successfully restored files and unified headers/footers!")
