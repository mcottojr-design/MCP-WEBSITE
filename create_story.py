import os
import re
import argparse
from datetime import datetime
import subprocess
import unicodedata

def slugify(text):
    # Normalize to decompose combined characters like ú into u + accent
    text = unicodedata.normalize('NFD', text)
    # Remove accents and non-ascii
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def create_news_post(title, author, category, excerpt, content, image=None):
    slug = slugify(title)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join("src", "news", filename)
    
    # Default image if none provided
    if not image:
        image = "/assets/hero_banner.jpg"
    
    front_matter = f"""---
layout: layouts/post.njk
tags: post
title: "{title}"
date: {date_str}
author: "{author}"
image: "{image}"
category: "{category}"
excerpt: "{excerpt}"
---
{content}
"""

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(front_matter)
    
    print(f"✅ Success! Story created: {filepath}")
    return filepath

def push_to_github(filepath, title):
    print("🚀 Pushing to GitHub...")
    try:
        subprocess.run(["git", "add", filepath], check=True)
        # Also add any new assets just in case
        subprocess.run(["git", "add", "src/assets/news"], check=True)
        subprocess.run(["git", "commit", "-m", f"Add news post: {title} (Safe Filename)"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🌍 Deployed! Vercel should have the update live in < 1 min.")
    except Exception as e:
        print(f"❌ Push failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP News Post Builder")
    parser.add_argument("--title", required=True, help="Title of the news post")
    parser.add_argument("--author", default="Miguel Cotto", help="Author name")
    parser.add_argument("--category", default="Announcement", help="Category (e.g., Fight Results, Interview)")
    parser.add_argument("--excerpt", required=True, help="Short summary")
    parser.add_argument("--content", required=True, help="Full article content (Markdown supported)")
    parser.add_argument("--image", help="URL to image or local path like /assets/boxers/oscar-collazo.png")
    parser.add_argument("--publish", action="store_true", help="Automatically commit and push to GitHub")

    args = parser.parse_args()
    
    path = create_news_post(
        args.title, 
        args.author, 
        args.category, 
        args.excerpt, 
        args.content, 
        args.image
    )
    
    if args.publish:
        push_to_github(path, args.title)
