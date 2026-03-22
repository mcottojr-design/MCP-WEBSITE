import re
import os
import unicodedata

roster_data = [
    {"name": "Oscar Collazo", "alias": "El Pupilo", "is_champion": True, "division": "Mini-Flyweight", "weight": "105LBS", "record": "14-0-0", "kos": "11"},
    {"name": "Belisa López De Jesús", "alias": "", "division": "Mini-Flyweight", "weight": "105LBS", "record": "2-0-1", "kos": "0"},
    {"name": "Jerryanis Morales", "alias": "La Yeya", "division": "Jr. Flyweight", "weight": "108LBS", "record": "0-0-0", "kos": "0"},
    {"name": "Kenny Romero", "alias": "", "division": "Jr. Flyweight", "weight": "108LBS", "record": "4-1-0", "kos": "3"},
    {"name": "Angel Acosta", "alias": "Tito", "division": "Flyweight", "weight": "112LBS", "record": "25-5-0", "kos": "23"},
    {"name": "Billy Rodríguez", "alias": "The Kid", "division": "Flyweight", "weight": "112LBS", "record": "6-0-0", "kos": "3"},
    {"name": "Arely Muciño", "alias": "La Ametralladora", "division": "Flyweight", "weight": "112LBS", "record": "32-5-2", "kos": "11"},
    {"name": "Juan Carlos Camacho Jr.", "alias": "El Indio", "division": "Flyweight", "weight": "112LBS", "record": "19-2-0", "kos": "8"},
    {"name": "Malik Quiñones", "alias": "", "division": "Jr. Bantamweight", "weight": "115LBS", "record": "4-1-0", "kos": "3"},
    {"name": "Yadriel Cabán", "alias": "El Electrico", "division": "Jr. Bantamweight", "weight": "115LBS", "record": "3-0-0", "kos": "3"},
    {"name": "Jordy Cardona", "alias": "El Príncipe", "division": "Bantamweight", "weight": "118LBS", "record": "10-0-0", "kos": "9"},
    {"name": "José Sánchez", "alias": "Tito", "division": "Jr. Featherweight", "weight": "122LBS", "record": "15-0-0", "kos": "9"},
    {"name": "Yan Carlos Santana", "alias": "Dangerous", "division": "Featherweight", "weight": "126LBS", "record": "16-0-0", "kos": "13"},
    {"name": "Yadiel Alomar", "alias": "", "division": "Featherweight", "weight": "126LBS", "record": "6-0-0", "kos": "4"},
    {"name": "Bryan Chevalier", "alias": "Chary", "division": "Jr. Lightweight", "weight": "130LBS", "record": "23-3-1", "kos": "16"},
    {"name": "Christian Barreto", "alias": "El Capitán", "division": "Lightweight", "weight": "135LBS", "record": "15-0-0", "kos": "9"},
    {"name": "Willjay De la Paz", "alias": "", "division": "Lightweight", "weight": "135LBS", "record": "1-0-0", "kos": "1"},
    {"name": "Leonardo Sánchez", "alias": "Bazooka", "division": "Lightweight", "weight": "135LBS", "record": "10-0-0", "kos": "8"},
    {"name": "Yariel Santiago", "alias": "", "division": "Lightweight", "weight": "135LBS", "record": "8-2-1", "kos": "2"},
    {"name": "Harold Laguna", "alias": "", "division": "Lightweight", "weight": "135LBS", "record": "7-2-1", "kos": "4"},
    {"name": "Danielito Zorrilla", "alias": "El Zorro", "division": "Jr. Welterweight", "weight": "140LBS", "record": "18-2-0", "kos": "14"},
    {"name": "Alberto Machado", "alias": "El Explosivo", "division": "Jr. Welterweight", "weight": "140LBS", "record": "24-4-0", "kos": "20"},
    {"name": "Ryan Enoch Rodríguez", "alias": "", "division": "Jr. Welterweight", "weight": "140LBS", "record": "7-0-0", "kos": "2"},
    {"name": "Yair Gallardo", "alias": "Manotas", "division": "Light Heavyweight", "weight": "175LBS", "record": "10-0-0", "kos": "8"}
]

placeholder_img = "https://images.unsplash.com/photo-1549719386-74dbba40f4ce?auto=format&fit=crop&q=80"
boxer_assets_dir = 'src/assets/boxers/'
available_images = os.listdir(boxer_assets_dir) if os.path.exists(boxer_assets_dir) else []

def slugify(text):
    text = text.replace(' ', '-').lower()
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    return f'{text}.png'

def find_best_image(name):
    slug_name = slugify(name)
    if "ryan-enoch" in slug_name: slug_name = "ryan-rodriguez.png"
    if slug_name in available_images: return slug_name
    for img in available_images:
        if slug_name.replace('.png', '') in img: return img
    return None

def get_boxer_card_boxers_page(boxer):
    parts = boxer['name'].split(' ')
    name_display = f"{parts[0]} \"{boxer['alias']}\" {' '.join(parts[1:])}" if boxer['alias'] and len(parts) > 1 else (f"{boxer['name']} \"{boxer['alias']}\"" if boxer['alias'] else boxer['name'])
    img_file = find_best_image(boxer['name'])
    final_img = f"/assets/boxers/{img_file}" if img_file else placeholder_img
    img_classes = "absolute inset-0 bg-cover bg-center group-hover:scale-110 transition-transform duration-500"
    if img_file and "yadiel-alomar" in img_file: img_classes = "absolute inset-0 bg-cover bg-top scale-90 group-hover:scale-95 transition-transform duration-500"
    
    champion_badge = '<div class="absolute top-4 left-4 z-20 bg-yellow-500 text-black text-[10px] font-black py-1 px-3 rounded uppercase tracking-widest shadow-lg">Champion</div>' if boxer.get('is_champion') else ""
    
    return f"""<div class="boxer-card group flex flex-col bg-primary/5 border border-primary/10 rounded-xl overflow-hidden hover:border-primary/50 transition-all duration-300 shadow-xl" data-division="{boxer['division']}"><div class="relative w-full aspect-[3/4] overflow-hidden">{champion_badge}<div class="{img_classes}" data-alt="Image for {name_display}" style='background-image: url("{final_img}");'></div><div class="absolute inset-0 bg-gradient-to-t from-background-dark via-transparent to-transparent opacity-80 pointer-events-none"></div></div><div class="p-5 flex flex-col gap-1"><h3 class="text-slate-100 text-xl font-bold uppercase italic tracking-tight group-hover:text-primary transition-colors">{name_display}</h3><p class="text-primary text-xs font-bold uppercase tracking-widest">{boxer['division']} / {boxer['weight']}</p><div class="flex items-center justify-between mt-2 border-t border-primary/10 pt-3"><div class="flex flex-col"><span class="text-slate-400 text-[10px] uppercase font-bold tracking-tighter">Record</span><span class="text-slate-100 font-bold">{boxer['record']}</span></div><div class="flex flex-col items-end"><span class="text-slate-400 text-[10px] uppercase font-bold tracking-tighter">KOs</span><span class="text-slate-100 font-bold">{boxer['kos']}</span></div></div><a class="mt-4 flex items-center justify-center w-full bg-primary/20 hover:bg-primary text-slate-100 font-bold py-3 rounded text-xs uppercase tracking-widest transition-all" href="boxers.html">View Profile</a></div></div>"""

def get_boxer_card_index_page(boxer):
    name_display = boxer['name']
    alias_display = f'"{boxer["alias"]}"' if boxer['alias'] else ""
    img_file = find_best_image(boxer['name'])
    final_img = f"/assets/boxers/{img_file}" if img_file else placeholder_img
    object_fit_class = "object-center"
    scale_class = ""
    if img_file and "yadiel-alomar" in img_file: 
        object_fit_class = "object-top"
        scale_class = "scale-90"
        
    champion_badge = '<div class="absolute top-4 left-4 z-20 bg-yellow-500 text-black text-[10px] font-black py-1 px-3 rounded uppercase tracking-widest shadow-lg">Champion</div>' if boxer.get('is_champion') else ""

    return f"""<div class="group relative aspect-[3/4] overflow-hidden rounded-lg bg-background-dark border border-border-muted snap-center shrink-0 w-[280px] md:w-auto">{champion_badge}<img class="w-full h-full object-cover grayscale {object_fit_class} {scale_class} transition-all duration-500 group-hover:scale-105 group-hover:grayscale-0" data-alt="Image for {name_display}" src="{final_img}" style=""/><div class="absolute inset-0 bg-gradient-to-t from-background-dark via-transparent to-transparent opacity-90 pointer-events-none"></div><div class="absolute bottom-0 left-0 right-0 p-6"><p class="text-primary text-[10px] font-bold tracking-widest uppercase mb-1" style="">{boxer['division']}</p><h5 class="text-xl font-black text-white uppercase tracking-tighter leading-none group-hover:text-primary transition-colors" style="">{name_display}</h5><p class="text-slate-400 text-xs mt-2 italic" style="">{alias_display}</p></div></div>"""

def update_file(path):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f: content = f.read()
    if 'boxers.html' in path:
        unique_divisions = sorted(list(set([b['division'] for b in roster_data])))
        filter_buttons = ['<button class="filter-btn flex h-10 shrink-0 items-center justify-center gap-x-2 rounded bg-primary px-5 text-white text-sm font-bold uppercase tracking-wider" data-division="all">All Weights</button>']
        for div in unique_divisions:
            filter_buttons.append(f'<button class="filter-btn flex h-10 shrink-0 items-center justify-center gap-x-2 rounded bg-primary/10 border border-primary/20 px-5 text-slate-100 text-sm font-medium hover:bg-primary/20 transition-colors uppercase tracking-wider" data-division="{div}">{div}</button>')
        
        filter_html = f'<div class="flex items-center gap-3 overflow-x-auto pb-4 scrollbar-hide no-scrollbar">{"".join(filter_buttons)}</div>'
        content = re.sub(r'<!-- Filters & Search Mobile -->.*?<div class="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-hide no-scrollbar">.*?</div>', f'<!-- Filters & Search Mobile -->\n<div class="px-6 md:px-10 py-6 flex flex-col gap-6">\n{filter_html}', content, flags=re.DOTALL)
        
        new_boxers_grid = "\n".join([get_boxer_card_boxers_page(b) for b in roster_data])
        content = re.sub(r'<!-- Fighter Grid -->.*?<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 px-6 md:px-10 pb-20">.*?</main>', f'<!-- Fighter Grid -->\n<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 px-6 md:px-10 pb-20">\n{new_boxers_grid}\n</div>\n\n<script>\nconst filterBtns = document.querySelectorAll(".filter-btn");\nconst searchInputs = document.querySelectorAll(\'input[placeholder*="Search for a fighter"]\');\nconst cards = document.querySelectorAll(".boxer-card");\n\nfunction filterFighters() {{\n    const activeBtn = document.querySelector(".filter-btn.bg-primary");\n    const division = activeBtn ? activeBtn.getAttribute("data-division") : "all";\n    const searchTerm = searchInputs[0]?.value.toLowerCase() || "";\n\n    cards.forEach(card => {{\n        const cardDivision = card.getAttribute("data-division");\n        const cardName = card.querySelector("h3").innerText.toLowerCase();\n        \n        const matchesDivision = division === "all" || cardDivision === division;\n        const matchesSearch = cardName.includes(searchTerm);\n        \n        if (matchesDivision && matchesSearch) {{\n            card.style.display = "flex";\n        }} else {{\n            card.style.display = "none";\n        }}\n    }});\n}}\n\nfilterBtns.forEach(btn => {{\n    btn.addEventListener("click", () => {{\n        filterBtns.forEach(b => {{\n            b.classList.remove("bg-primary", "text-white");\n            b.classList.add("bg-primary/10", "border-primary/20", "text-slate-100");\n        }});\n        btn.classList.add("bg-primary", "text-white");\n        btn.classList.remove("bg-primary/10", "border-primary/20", "text-slate-100");\n        filterFighters();\n    }});\n}});\n\nsearchInputs.forEach(input => {{\n    input.addEventListener("input", (e) => {{\n        searchInputs.forEach(si => {{ if(si !== input) si.value = e.target.value; }});\n        filterFighters();\n    }});\n}});\n</script>\n</main>', content, flags=re.DOTALL)
    if 'index.html' in path:
        featured_boxers_grid = "\n".join([get_boxer_card_index_page(b) for b in roster_data[:6]])
        content = re.sub(r'<!-- Boxers Directory -->.*?<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">.*?</div>\s*<div class="mt-16 text-center">', f'<!-- Boxers Directory -->\n<section class="py-24 bg-surface">\n<div class="max-w-7xl mx-auto px-6 md:px-12">\n<h2 class="text-center text-primary text-sm font-bold tracking-[0.4em] uppercase mb-2">Roster</h2>\n<h3 class="text-center text-4xl md:text-5xl font-black text-white uppercase tracking-tighter mb-16">Our Boxers</h3>\n<div class="flex flex-nowrap md:grid overflow-x-auto md:overflow-visible snap-x snap-mandatory no-scrollbar md:grid-cols-2 lg:grid-cols-3 gap-8 pb-8 md:pb-0">\n{featured_boxers_grid}\n</div>\n<div class="mt-16 text-center">', content, flags=re.DOTALL)
        if 'no-scrollbar::-webkit-scrollbar' not in content:
            style_tag = "<style>.no-scrollbar::-webkit-scrollbar { display: none; } .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }</style>"
            content = content.replace('</head>', f'{style_tag}\n</head>')
    with open(path, 'w', encoding='utf-8') as f: f.write(content)
    print(f"Updated {path}")

update_file('src/boxers.html')
update_file('src/index.html')
