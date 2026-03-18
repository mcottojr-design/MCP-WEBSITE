import os
import shutil

# Map directory to new file name
file_mapping = {
    'miguel_cotto_promotions_home_linked': 'index.html',
    'events_tickets': 'events.html',
    'boxer_roster_miguel_cotto_promotions': 'boxers.html',
    'latest_news_miguel_cotto_promotions': 'news.html',
    'about_us_miguel_cotto_promotions': 'about.html',
    'boxer_profile_with_social_links': 'profile.html'
}

# Link replacements
replacements = {
    "{{DATA:SCREEN:SCREEN_8}}": "events.html",
    "{{DATA:SCREEN:SCREEN_7}}": "boxers.html",
    "{{DATA:SCREEN:SCREEN_2}}": "news.html",
    "{{DATA:SCREEN:SCREEN_6}}": "profile.html", # Just in case
    # other screens mapping to index?
}

# 1. Copy files to root
for d, f in file_mapping.items():
    src = os.path.join(d, 'code.html')
    if os.path.exists(src):
        shutil.copy(src, f)
        print(f"Copied {src} to {f}")

# 2. Update links in all new html files
html_files = list(file_mapping.values())
for f in html_files:
    if os.path.exists(f):
        with open(f, 'r') as file:
            content = file.read()
        
        # Replace the known screen placeholders
        for k, v in replacements.items():
            content = content.replace(k, v)
            
        # Optional: Replace specific hash links by examining the text around them, but that's risky.
        # Let's replace simple instances like href="#" when text is About Us
        content = content.replace('href="#" style="">About Us', 'href="about.html" style="">About Us')
        
        # In the navbar, the brand links to home
        content = content.replace('href="#" style="">\n<div class="w-10 h-10 bg-primary', 'href="index.html" style="">\n<div class="w-10 h-10 bg-primary')
        content = content.replace('href="#" style="">\n<div class="w-12 h-12 bg-primary', 'href="index.html" style="">\n<div class="w-12 h-12 bg-primary')

        with open(f, 'w') as file:
            file.write(content)
        print(f"Updated links in {f}")

print("Done building website.")
