import re
import os
import unicodedata

roster_data = [
    {"name": "Oscar Collazo", "alias": "El Pupilo", "division": "Mini-Flyweight", "weight": "105LBS"},
    {"name": "Belisa López De Jesús", "alias": "", "division": "Mini-Flyweight", "weight": "105LBS"},
    {"name": "Jerryanis Morales", "alias": "La Yeya", "division": "Jr. Flyweight", "weight": "108LBS"},
    {"name": "Kenny Romero", "alias": "", "division": "Jr. Flyweight", "weight": "108LBS"},
    {"name": "Angel Acosta", "alias": "Tito", "division": "Flyweight", "weight": "112LBS"},
    {"name": "Billy Rodríguez", "alias": "The Kid", "division": "Flyweight", "weight": "112LBS"},
    {"name": "Arely Muciño", "alias": "La Ametralladora", "division": "Flyweight", "weight": "112LBS"},
    {"name": "Juan Carlos Camacho Jr.", "alias": "El Indio", "division": "Flyweight", "weight": "112LBS"},
    {"name": "Malik Quiñones", "alias": "", "division": "Jr. Bantamweight", "weight": "115LBS"},
    {"name": "Yadriel Cabán", "alias": "El Electrico", "division": "Jr. Bantamweight", "weight": "115LBS"},
    {"name": "Jordy Cardona", "alias": "El Príncipe", "division": "Bantamweight", "weight": "118LBS"},
    {"name": "José Sánchez", "alias": "Tito", "division": "Jr. Featherweight", "weight": "122LBS"},
    {"name": "Yan Carlos Santana", "alias": "Dangerous", "division": "Featherweight", "weight": "126LBS"},
    {"name": "Yadiel Alomar", "alias": "", "division": "Featherweight", "weight": "126LBS"},
    {"name": "Bryan Chevalier", "alias": "Chary", "division": "Jr. Lightweight", "weight": "130LBS"},
    {"name": "Christian Barreto", "alias": "El Capitán", "division": "Lightweight", "weight": "135LBS"},
    {"name": "Willjay De la Paz", "alias": "", "division": "Lightweight", "weight": "135LBS"},
    {"name": "Leonardo Sánchez", "alias": "Bazooka", "division": "Lightweight", "weight": "135LBS"},
    {"name": "Yariel Santiago", "alias": "", "division": "Lightweight", "weight": "135LBS"},
    {"name": "Harold Laguna", "alias": "", "division": "Lightweight", "weight": "135LBS"},
    {"name": "Danielito Zorrilla", "alias": "El Zorro", "division": "Jr. Welterweight", "weight": "140LBS"},
    {"name": "Alberto Machado", "alias": "El Explosivo", "division": "Jr. Welterweight", "weight": "140LBS"},
    {"name": "Ryan Enoch Rodríguez", "alias": "", "division": "Jr. Welterweight", "weight": "140LBS"},
    {"name": "Yair Gallardo", "alias": "Manotas", "division": "Light Heavyweight", "weight": "175LBS"}
]

placeholder_img = "https://images.unsplash.com/photo-1549719386-74dbba40f4ce?auto=format&fit=crop&q=80"

# Pre-list images for easier matching
boxer_assets_dir = 'src/assets/boxers/'
available_images = os.listdir(boxer_assets_dir) if os.path.exists(boxer_assets_dir) else []

def slugify(text):
    text = text.replace(' ', '-').lower()
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    return f'{text}.png'

def find_best_image(name):
    slug_name = slugify(name)
    if "ryan-enoch" in slug_name:
        slug_name = "ryan-rodriguez.png"
    if slug_name in available_images:
        return slug_name
    for img in available_images:
        if slug_name.replace('.png', '') in img:
            return img
    return None

def get_boxer_card_boxers_page(boxer):
    parts = boxer['name'].split(' ')
    name_display = f"{parts[0]} \"{boxer['alias']}\" {' '.join(parts[1:])}" if boxer['alias'] and len(parts) > 1 else (f"{boxer['name']} \"{boxer['alias']}\"" if boxer['alias'] else boxer['name'])
    img_file = find_best_image(boxer['name'])
    final_img = f"/assets/boxers/{img_file}" if img_file else placeholder_img
    img_classes = "absolute inset-0 bg-cover bg-center group-hover:scale-110 transition-transform duration-500"
    if img_file and "yadiel-alomar" in img_file:
        img_classes = "absolute inset-0 bg-cover bg-top scale-90 group-hover:scale-95 transition-transform duration-500"

    return f"""
<div class="group flex flex-col bg-primary/5 border border-primary/10 rounded-xl overflow-hidden hover:border-primary/50 transition-all duration-300 shadow-xl">
<div class="relative w-full aspect-[3/4] overflow-hidden">
<div class="{img_classes}" data-alt="Image for {name_display}" style='background-image: url("{final_img}");'></div>
<div class="absolute inset-0 bg-gradient-to-t from-background-dark via-transparent to-transparent opacity-80 pointer-events-none"></div>
</div>
<div class="p-5 flex flex-col gap-1">
<h3 class="text-slate-100 text-xl font-bold uppercase italic tracking-tight group-hover:text-primary transition-colors">{name_display}</h3>
<p class="text-primary text-xs font-bold uppercase tracking-widest">{boxer['division']} / {boxer['weight']}</p>
<div class="flex items-center justify-between mt-2 border-t border-primary/10 pt-3">
<div class="flex flex-col">
<span class="text-slate-400 text-[10px] uppercase font-bold tracking-tighter">Record</span>
<span class="text-slate-100 font-bold">-- - -- - --</span>
</div>
<div class="flex flex-col items-end">
<span class="text-slate-400 text-[10px] uppercase font-bold tracking-tighter">KOs</span>
<span class="text-slate-100 font-bold">--</span>
</div>
</div>
<a class="mt-4 flex items-center justify-center w-full bg-primary/20 hover:bg-primary text-slate-100 font-bold py-3 rounded text-xs uppercase tracking-widest transition-all" href="boxers.html">
                                View Profile
                            </a>
</div>
</div>"""

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

    # Added 'snap-center shrink-0 w-[280px] md:w-auto' for carousel behavior
    return f"""
<div class="group relative aspect-[3/4] overflow-hidden rounded-lg bg-background-dark border border-border-muted snap-center shrink-0 w-[280px] md:w-auto">
<img class="w-full h-full object-cover grayscale {object_fit_class} {scale_class} transition-all duration-500 group-hover:scale-105 group-hover:grayscale-0" data-alt="Image for {name_display}" src="{final_img}" style=""/>
<div class="absolute inset-0 bg-gradient-to-t from-background-dark via-transparent to-transparent opacity-90 pointer-events-none"></div>
<div class="absolute bottom-0 left-0 right-0 p-6">
<p class="text-primary text-[10px] font-bold tracking-widest uppercase mb-1" style="">{boxer['division']}</p>
<h5 class="text-xl font-black text-white uppercase tracking-tighter leading-none group-hover:text-primary transition-colors" style="">{name_display}</h5>
<p class="text-slate-400 text-xs mt-2 italic" style="">{alias_display}</p>
</div>
</div>"""

def update_file(path):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'boxers.html' in path:
        new_boxers_grid = "\n".join([get_boxer_card_boxers_page(b) for b in roster_data])
        content = re.sub(
            r'<!-- Fighter Grid -->.*?<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 px-6 md:px-10 pb-20">.*?</main>',
            f'<!-- Fighter Grid -->\n<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 px-6 md:px-10 pb-20">\n{new_boxers_grid}\n</div>\n</main>',
            content,
            flags=re.DOTALL
        )

    if 'index.html' in path:
        featured_boxers_grid = "\n".join([get_boxer_card_index_page(b) for b in roster_data[:6]]) # 6 for 3 columns x 2 rows or just 3 across
        # Update Container for Desktop Bigger Cards + Mobile Carousel
        content = re.sub(
            r'<!-- Boxers Directory -->.*?<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">.*?</div>\s*<div class="mt-16 text-center">',
            f'<!-- Boxers Directory -->\n<section class="py-24 bg-surface">\n<div class="max-w-7xl mx-auto px-6 md:px-12">\n<h2 class="text-center text-primary text-sm font-bold tracking-[0.4em] uppercase mb-2">Roster</h2>\n<h3 class="text-center text-4xl md:text-5xl font-black text-white uppercase tracking-tighter mb-16">Our Boxers</h3>\n<div class="flex flex-nowrap md:grid overflow-x-auto md:overflow-visible snap-x snap-mandatory no-scrollbar md:grid-cols-2 lg:grid-cols-3 gap-8 pb-8 md:pb-0">\n{featured_boxers_grid}\n</div>\n<div class="mt-16 text-center">',
            content,
            flags=re.DOTALL
        )
        
        # Add no-scrollbar CSS if not present
        if 'no-scrollbar::-webkit-scrollbar' not in content:
            style_tag = "<style>.no-scrollbar::-webkit-scrollbar { display: none; } .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }</style>"
            content = content.replace('</head>', f'{style_tag}\n</head>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Bigger Desktop Cards & Mobile Carousel Updated for {path}")

update_file('src/boxers.html')
update_file('src/index.html')
update_file('boxers.html')
update_file('index.html')
