import os

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # We accidentally deleted the wrapper <div class="flex items-center gap-8"> that groups the logo and nav
    # We can restore it by replacing:
    # <header ...>
    # <a class="flex items-center" href="index.html">
    # With:
    # <header ...>
    # <div class="flex items-center gap-8">
    # <a class="flex items-center" href="index.html">
    
    # We will simply find "<header" block end ">", and right after it, ensure we have the div wrapped if it's missing.
    # A safer string replacement:
    search_str = '<a class="flex items-center" href="index.html">\n<img src="assets/logo.svg" alt="Miguel Cotto Promotions Logo"'
    
    # Check if the line before search_str is the header or div.
    # In events.html, the header tag is closed, then immediately <a class="flex...
    # Let's just do a specific replace.
    if search_str in content:
        # Check if it already has the wrapper
        if '<div class="flex items-center gap-8">\n<a class="flex items-center" href="index.html">' not in content:
            new_content = content.replace(
                search_str, 
                '<div class="flex items-center gap-8">\n' + search_str
            )
            with open(f, 'w') as file:
                file.write(new_content)
            print(f"Fixed missing header div in {f}")
        else:
            print(f"Already fixed or different in {f}")
