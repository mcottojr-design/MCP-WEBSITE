import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Header replacement
    new_content = content.replace('class="h-20 md:h-24 w-auto object-contain"', 'class="h-[72px] md:h-[86px] w-auto object-contain"')
    
    # Footer replacement 
    new_content = new_content.replace('class="h-24 md:h-32 w-auto object-contain"', 'class="h-[86px] md:h-[115px] w-auto object-contain"')
    
    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Scaled down logo by 10% in {f}")
    else:
        print(f"No changes matched in {f}")
