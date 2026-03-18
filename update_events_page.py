import re

with open('events.html', 'r') as file:
    content = file.read()

# We will completely replace the <main class="flex-grow"> ... </main> in events.html
# with a single focused Aibonito Event section, removing all standard placeholders.

main_content = '''<main class="flex-grow">
<section class="py-24 bg-background-dark min-h-[70vh]">
<div class="max-w-7xl mx-auto px-6 md:px-12">
<div class="flex items-end justify-between mb-12">
<div>
<h2 class="text-primary text-sm font-bold tracking-[0.4em] uppercase mb-2">Next Fight Night</h2>
<h3 class="text-4xl md:text-5xl font-black text-white uppercase tracking-tighter">Upcoming Events</h3>
</div>
</div>
<div class="flex justify-center">
<div class="w-full max-w-5xl group relative overflow-hidden rounded-xl bg-surface border border-border-muted flex flex-col md:flex-row h-full shadow-2xl">
<div class="w-full md:w-1/2 overflow-hidden h-64 md:h-auto">
<img class="w-full h-full object-cover grayscale transition-all duration-700 group-hover:grayscale-0 group-hover:scale-105" src="assets/hero_banner.jpg" style=""/>
</div>
<div class="p-8 flex flex-col justify-between flex-1">
<div>
<div class="flex items-center gap-2 mb-4">
<span class="material-symbols-outlined text-primary" style="">calendar_today</span>
<span class="text-slate-400 font-bold uppercase tracking-widest text-xs" style="">April 18</span>
</div>
<h4 class="text-3xl font-black text-white uppercase leading-tight mb-4" style="">ITF ES LA PELEA: <br/> Aibonito</h4>
<p class="text-slate-400 text-sm mb-6 leading-relaxed" style="">Witness the raw intensity of ITF Boxing at Coliseo "Marrón" Aponte. An unforgettable night of professional boxing displaying the next generation of champions.</p>
<div class="flex items-center gap-4 text-xs font-bold text-slate-300">
<span class="bg-primary/20 text-primary px-3 py-1 rounded" style="">MAIN EVENT</span>
</div>
</div>
<div class="mt-8 flex items-center justify-between border-t border-border-muted pt-6">
<div class="flex flex-col">
<span class="text-[10px] text-slate-500 uppercase tracking-widest" style="">Venue</span>
<span class="text-white font-bold" style="">Coliseo "Marrón" Aponte</span>
</div>
<button class="bg-primary text-white text-xs font-bold px-6 py-3 rounded-lg uppercase tracking-widest hover:bg-red-700" onclick="window.open('https://boletos.prticket.com/events/en/itf-aibonito')" style="">Get Tickets</button>
</div>
</div>
</div>
</div>
</div>
</section>
</main>'''

new_content = re.sub(r'<main class="flex-grow">.*?</main>', main_content, content, flags=re.DOTALL)

with open('events.html', 'w') as file:
    file.write(new_content)
    
print("Updated events.html to display only Aibonito Event.")
