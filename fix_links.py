import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

link_map = {
    'Events': 'events.html',
    'Fighters': 'boxers.html',
    'Boxers': 'boxers.html',
    'News': 'news.html',
    'About Us': 'about.html',
    'Home': 'index.html',
    'Tickets': 'events.html',
    'Our Roster': 'boxers.html',
    'Upcoming Events': 'events.html',
    'News Archive': 'news.html'
}

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # regex to find <a href="#">Text</a> or <a href="#" class="...">Text</a>
    # we can use a more generic substitution: change href="#" to href="target.html" if >Text< is matched
    
    # We'll parse the file and use a simple regex replacing href="#" with href="correct" based on text
    for link_text, target in link_map.items():
        # Match <a ... href="#" ...>LinkText</a>
        # Pattern: (<a[^>]*href=")#[^"]*("[^>]*>\s*)(.*?)\s*</a>
        # Actually it's simpler to use re.sub with a function
        
        def replacer(match):
            prefix = match.group(1) # <a ... href="
            suffix = match.group(2) # " ...>
            text = match.group(3)   # link text
            if link_text.lower() in text.lower():
                return f'{prefix}{target}{suffix}{text}</a>'
            return match.group(0) # return original if no match
            
        content = re.sub(r'(<a[^>]*href=")#[^"]*("[^>]*>)\s*([^<]*?)\s*</a>', replacer, content)

    # Specific logo link to index (the one with sports_martial_arts)
    content = content.replace('href="#"', 'href="index.html"') # fallback for any remaining # that are likely home or safe, but wait!
    # A generic fallback is risky, let's target the brand logo
    content = re.sub(r'(<a[^>]*href=")#[^"]*("[^>]*>\s*<div[^>]*bg-primary.*?</a\s*>)', r'\g<1>index.html\2', content, flags=re.DOTALL)
    
    with open(f, 'w') as file:
        file.write(content)
    
    print(f"Fixed links in {f}")

