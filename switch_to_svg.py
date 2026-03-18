import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    new_content = content.replace('assets/logo.png', 'assets/logo.svg')
    
    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f} to use logo.svg")
    else:
        print(f"No changes in {f}")
