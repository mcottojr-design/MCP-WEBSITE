import re

# Read index.html to extract standard wrappers
with open('index.html', 'r') as f:
    idx_content = f.read()

# Extract segments
head_match = re.search(r'(<!DOCTYPE html>.*?<body[^>]*>)', idx_content, flags=re.DOTALL)
header_match = re.search(r'(<!-- Top Navigation -->\s*<header.*?</header>)', idx_content, flags=re.DOTALL)
footer_match = re.search(r'(<!-- Footer -->\s*<footer.*?</footer>\s*</body>\s*</html>)', idx_content, flags=re.DOTALL)

head_str = head_match.group(1).replace('<title>Miguel Cotto Promotions | Elite Boxing Events</title>', '<title>News Story | Miguel Cotto Promotions</title>')
header_str = header_match.group(1)
footer_str = footer_match.group(1)

main_content = """
<main class="flex-grow bg-background-light dark:bg-background-dark">
    <!-- Article Hero -->
    <section class="relative w-full h-[60vh] min-h-[400px] flex items-end justify-center overflow-hidden">
        <!-- Background Image -->
        <div class="absolute inset-0 bg-cover bg-center" style="background-image: linear-gradient(to top, rgba(18,9,9,1) 0%, rgba(18,9,9,0.4) 50%, rgba(18,9,9,0) 100%), url('https://images.unsplash.com/photo-1549719386-74dbba40f4ce?auto=format&fit=crop&q=80');"></div>
        
        <div class="relative z-10 w-full max-w-4xl px-6 pb-12 text-center md:text-left">
            <div class="flex flex-wrap items-center justify-center md:justify-start gap-3 mb-6">
                <span class="bg-primary text-white text-[10px] md:text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-sm">Featured Story</span>
                <span class="text-slate-300 text-xs md:text-sm font-medium tracking-wider flex items-center gap-1"><span class="material-symbols-outlined text-[16px]">calendar_today</span> October 24, 2026</span>
            </div>
            <h1 class="text-4xl md:text-5xl lg:text-7xl font-black text-white uppercase italic tracking-tighter leading-tight drop-shadow-lg mb-6">
                Inside The Camp: The Final Preparation
            </h1>
            <div class="flex items-center justify-center md:justify-start gap-4">
                <div class="w-10 h-10 rounded-full bg-border-muted overflow-hidden border-2 border-primary">
                    <img src="https://ui-avatars.com/api/?name=Admin+Author&background=d72323&color=fff" alt="Author">
                </div>
                <div class="text-left">
                    <p class="text-white text-sm font-bold uppercase tracking-widest leading-none">MCP Editorial</p>
                    <p class="text-slate-400 text-xs mt-1">5 Min Read</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Article Content Layout -->
    <section class="py-16 md:py-24 px-6 relative w-full flex justify-center">
        <!-- Left Social Sidebar (Desktop) -->
        <div class="hidden lg:flex flex-col gap-6 absolute left-[10%] xl:left-[15%] top-24 sticky-socials">
            <p class="text-[10px] text-slate-500 font-bold uppercase tracking-widest writing-vertical-rl mb-4">Share Story</p>
            <button class="w-10 h-10 rounded-full border border-border-muted flex items-center justify-center text-slate-400 hover:bg-primary hover:text-white hover:border-primary transition-all">
                <span class="material-symbols-outlined text-[18px]">share</span>
            </button>
            <button class="w-10 h-10 rounded-full border border-border-muted flex items-center justify-center text-slate-400 hover:bg-[#1DA1F2] hover:text-white hover:border-[#1DA1F2] transition-all">
                <span class="material-symbols-outlined text-[18px]">tag</span>
            </button>
            <button class="w-10 h-10 rounded-full border border-border-muted flex items-center justify-center text-slate-400 hover:bg-primary hover:text-white hover:border-primary transition-all">
                <span class="material-symbols-outlined text-[18px]">link</span>
            </button>
        </div>

        <!-- Typography / Main Body -->
        <article class="w-full max-w-3xl">
            <p class="text-xl md:text-2xl text-slate-300 font-light leading-relaxed mb-10 border-l-4 border-primary pl-6 py-2">
                "The gym is where the fight is won. The ring is just where you go to pick up the trophy." As the Aibonito mega-event draws closer, the intensity behind closed doors reaches an all-time high.
            </p>

            <div class="space-y-8 text-base md:text-lg text-slate-400 font-medium leading-relaxed">
                <p>
                    Preparation is the invisible foundation of every victory. For the upcoming ITF event taking place at Coliseo "Marrón" Aponte, athletes have been pushing their physical and mental limits to prepare for war. The training camps established throughout Puerto Rico have seen grueling 5 AM roadwork sessions, endless sparring rounds, and meticulous strategic planning.
                </p>
                
                <h2 class="text-2xl md:text-4xl text-white font-black uppercase tracking-tighter mt-12 mb-6 text-left">The Science of Sparring</h2>
                
                <p>
                    There is an art to bringing a fighter to their absolute peak. Too much sparring, and an athlete risks peaking early and leaving their best performance in the gym. Too little, and the timing isn't sharp enough to deal with the chaos under the bright lights of the stadium.
                </p>

                <div class="my-12 w-full aspect-video rounded-xl overflow-hidden shadow-2xl relative">
                    <img src="https://images.unsplash.com/photo-1590480922416-62181d9f8df5?auto=format&fit=crop&q=80" alt="Boxer practicing" class="w-full h-full object-cover">
                </div>

                <p>
                    Local contenders featured on the Aibonito card have focused heavily on situational preparation. Coaches simulate pressure-fighting scenarios, high altitude conditioning, and technical counter-punching sequences. The goal is to hardwire instinct so that when the bell rings, there is no hesitation—only execution.
                </p>

                <div class="bg-surface border border-border-muted p-8 md:p-12 rounded-xl mt-12 shadow-inner">
                    <span class="material-symbols-outlined text-4xl text-primary mb-4 opacity-50">format_quote</span>
                    <p class="text-2xl text-white font-bold italic tracking-tight leading-snug">
                        "The atmosphere in this camp has been electric. Every single fighter knows what is at stake on April 18th. They aren't just fighting for a win; they are fighting to cement their legacy on the island."
                    </p>
                    <p class="text-sm text-primary uppercase font-bold tracking-widest mt-6">- Head Coach, Cotto Promotions</p>
                </div>
            </div>
        </article>
    </section>

    <!-- More Stories Section -->
    <section class="py-20 bg-surface border-t border-border-muted">
        <div class="max-w-7xl mx-auto px-6 md:px-12">
            <h3 class="text-2xl md:text-3xl font-black text-white uppercase tracking-tighter mb-10 text-center">Read Next</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Card 1 -->
                <a href="#" class="group block overflow-hidden rounded-xl bg-background-dark border border-border-muted hover:border-primary/50 transition-all">
                    <div class="aspect-video w-full overflow-hidden">
                        <img src="assets/hero_banner.jpg" alt="Related Story" class="w-full h-full object-cover grayscale transition-all duration-500 group-hover:grayscale-0 group-hover:scale-105">
                    </div>
                    <div class="p-6">
                        <span class="text-primary text-[10px] font-bold uppercase tracking-widest mb-2 block">Events</span>
                        <h4 class="text-xl font-bold text-white uppercase leading-tight group-hover:text-primary transition-colors">Everything You Need to Know: ITF Aibonito</h4>
                    </div>
                </a>
                <!-- Card 2 -->
                <a href="#" class="group block overflow-hidden rounded-xl bg-background-dark border border-border-muted hover:border-primary/50 transition-all">
                    <div class="aspect-video w-full overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1549719386-74dbba40f4ce?auto=format&fit=crop&q=80" alt="Related Story" class="w-full h-full object-cover grayscale transition-all duration-500 group-hover:grayscale-0 group-hover:scale-105">
                    </div>
                    <div class="p-6">
                        <span class="text-primary text-[10px] font-bold uppercase tracking-widest mb-2 block">Fighters</span>
                        <h4 class="text-xl font-bold text-white uppercase leading-tight group-hover:text-primary transition-colors">Rising Stars to Watch This Season</h4>
                    </div>
                </a>
                <!-- Card 3 -->
                <a href="#" class="group block overflow-hidden rounded-xl bg-background-dark border border-border-muted hover:border-primary/50 transition-all">
                    <div class="aspect-video w-full overflow-hidden absolute lg:static invisible lg:visible hidden lg:block">
                        <img src="https://images.unsplash.com/photo-1590480922416-62181d9f8df5?auto=format&fit=crop&q=80" alt="Related Story" class="w-full h-full object-cover grayscale transition-all duration-500 group-hover:grayscale-0 group-hover:scale-105">
                    </div>
                    <div class="p-6">
                        <span class="text-primary text-[10px] font-bold uppercase tracking-widest mb-2 block">Training</span>
                        <h4 class="text-xl font-bold text-white uppercase leading-tight group-hover:text-primary transition-colors">The conditioning secrets of Champions</h4>
                    </div>
                </a>
            </div>
            
            <div class="mt-12 text-center">
                <button class="border border-primary text-primary hover:bg-primary hover:text-white transition-all text-xs font-bold uppercase tracking-widest px-8 py-4 rounded" onclick="window.location.href='news.html'">
                    View All News
                </button>
            </div>
        </div>
    </section>
</main>
"""

story_html = head_str + header_str + main_content + footer_str

with open('story.html', 'w') as f:
    f.write(story_html)
    
print("Created story.html successfully")
