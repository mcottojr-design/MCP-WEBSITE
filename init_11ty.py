import os
import shutil
import re
import glob

# 1. Setup directories
os.makedirs("src/_includes/layouts", exist_ok=True)
os.makedirs("src/news", exist_ok=True)

# 2. Copy assets
if not os.path.exists("src/assets"):
    shutil.copytree("assets", "src/assets")

# 3. Create .eleventy.js
eleventy_config = """
module.exports = function(eleventyConfig) {
    // Pass through normal files
    eleventyConfig.addPassthroughCopy("src/assets");
    
    return {
        dir: {
            input: "src",
            output: "_site",
            includes: "_includes"
        }
    };
};
"""
with open(".eleventy.js", "w") as f:
    f.write(eleventy_config)

# 4. Generate the post.njk layout from story.html
with open("story.html", "r") as f:
    post_content = f.read()

# Replace hardcoded parts with Nunjucks variables
post_content = post_content.replace('Inside The Camp: The Final Preparation', '{{ title }}')
post_content = post_content.replace('October 24, 2026', '{{ page.date }}')
post_content = post_content.replace('MCP Editorial', '{{ author }}')
post_content = post_content.replace('https://images.unsplash.com/photo-1549719386-74dbba40f4ce?auto=format&fit=crop&q=80', '{{ image }}')

# For the content, since it's an article wrapper, we replace the whole <article>...</article> text
# We just find the article tag
article_regex = r'<article class="w-full max-w-3xl">.*?</article>'
replacement = '<article class="w-full max-w-3xl prose prose-invert lg:prose-xl mx-auto">\n{{ content | safe }}\n</article>'
post_content = re.sub(article_regex, replacement, post_content, flags=re.DOTALL)

with open("src/_includes/layouts/post.njk", "w") as f:
    f.write(post_content)

# 5. Move all other html files to src
html_files = [f for f in glob.glob("*.html") if f != "story.html"]
for f in html_files:
    shutil.copy(f, f"src/{f}")

# 6. Transform news.html to dynamic loop
with open("src/news.html", "r") as f:
    news_content = f.read()

# Find the grid: `<div class="lg:col-span-3 grid grid-cols-1 md:grid-cols-2 gap-8">`
# We will inject the nunjucks loop
import string
nunjucks_loop = """
<div class="lg:col-span-3 grid grid-cols-1 md:grid-cols-2 gap-8">
{% for post in collections.post | reverse %}
<article class="group cursor-pointer" onclick="window.location.href='{{ post.url }}'">
<div class="relative overflow-hidden aspect-video rounded-lg mb-4 border border-border-muted shadow-lg">
<img class="object-cover w-full h-full transition-transform duration-500 group-hover:scale-110" src="{{ post.data.image }}"/>
<span class="absolute top-3 left-3 bg-primary text-white text-[10px] font-bold px-2 py-1 uppercase rounded-sm">{{ post.data.category }}</span>
</div>
<div class="space-y-2">
<time class="text-xs text-primary font-medium">{{ post.date }}</time>
<h3 class="text-lg font-bold leading-tight group-hover:text-primary transition-colors text-white uppercase">{{ post.data.title }}</h3>
<p class="text-slate-400 text-sm line-clamp-2 font-light">{{ post.data.excerpt }}</p>
<a class="inline-flex items-center gap-1 text-xs font-bold uppercase tracking-wider text-slate-200 hover:text-primary transition-colors pt-2" href="{{ post.url }}">
Read Story <span class="material-symbols-outlined text-sm">open_in_new</span>
</a>
</div>
</article>
{% endfor %}
</div>
"""
# Remove the old hardcoded grid and pagination
news_content = re.sub(
    r'<div class="lg:col-span-3 grid grid-cols-1 md:grid-cols-2 gap-8">.*?<!-- Pagination -->', 
    nunjucks_loop + '\n<!-- Pagination -->', 
    news_content, 
    flags=re.DOTALL
)

with open("src/news.html", "w") as f:
    f.write(news_content)

# 7. Create a sample markdown post
sample_post = """---
layout: layouts/post.njk
tags: post
title: Welcome to the New Automated Portal
date: 2026-03-18
author: Miguel Cotto
image: ../assets/hero_banner.jpg
category: Announcement
excerpt: This is a fully automated test post.
---
## A New Era of Automation

This article is generated completely automatically from a simple markdown file. Make.com will drop files just like this one directly into your codebase, and Eleventy will instantly turn them into gorgeous, masterfully styled HTML pages!

### Why is this powerful?

You never have to touch a single line of code again. Just type your newsletter, hit send, and this exact beautiful page materializes on your website automatically.
"""
with open("src/news/sample-post.md", "w") as f:
    f.write(sample_post)

print("11ty structure generated automatically!")
