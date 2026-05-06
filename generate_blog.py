import os
import re
import json
import random
import requests
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# SEO topics pool - niche related
TOPICS = [
    "how to write the perfect title tag for google search",
    "what is crawl budget and why does it matter for small websites",
    "how to do keyword research without paying for tools",
    "why your website is not showing on google and how to fix it",
    "how to write meta descriptions that actually get clicks",
    "what are long tail keywords and how to find them free",
    "how to improve your website loading speed for better rankings",
    "what is domain authority and how to increase it",
    "how to use google search console to improve your seo",
    "internal linking strategy that boosts your google rankings",
    "how to optimize images for seo without losing quality",
    "what is bounce rate and how to reduce it",
    "how to write blog posts that rank on google first page",
    "what are featured snippets and how to get them",
    "how to do a free seo audit of your website",
    "why mobile optimization matters for google rankings in 2025",
    "how to use schema markup to get rich results on google",
    "what is page experience and how google uses it for ranking",
    "how to build backlinks for free as a new blogger",
    "what is technical seo and where to start as a beginner",
    "how to find broken links on your website and fix them",
    "what is duplicate content and how it hurts your seo",
    "how to rank for local seo without spending money",
    "what is anchor text and how to use it properly in seo",
    "how to write alt text for images to improve seo",
    "what are core web vitals and why google cares about them",
    "how to get your blog indexed by google faster",
    "what is the difference between on page and off page seo",
    "how to use free keyword tools to find low competition keywords",
    "why your competitors rank higher than you and what to do",
    "how to optimize your website for voice search",
    "what is a sitemap and why your website needs one",
    "how to write seo friendly urls that rank better",
    "what is e e a t and why it matters for google rankings",
    "how to use google analytics to improve your seo strategy",
]

GRADIENTS = [
    "linear-gradient(135deg,#667eea,#764ba2)",
    "linear-gradient(135deg,#f093fb,#f5576c)",
    "linear-gradient(135deg,#4facfe,#00f2fe)",
    "linear-gradient(135deg,#43e97b,#38f9d7)",
    "linear-gradient(135deg,#fa709a,#fee140)",
    "linear-gradient(135deg,#a18cd1,#fbc2eb)",
    "linear-gradient(135deg,#ffecd2,#fcb69f)",
    "linear-gradient(135deg,#ff9a9e,#fecfef)",
    "linear-gradient(135deg,#a1c4fd,#c2e9fb)",
    "linear-gradient(135deg,#fd7043,#ff8a65)",
]

EMOJIS = ["📊", "🔍", "🚀", "💡", "🎯", "📈", "🔑", "⚡", "🛠️", "📝", "🌐", "🔗"]

CATEGORIES = [
    "SEO Basics", "Content Strategy", "Technical SEO",
    "Link Building", "Keyword Research", "On-Page SEO",
    "Google Tools", "Blogging Tips"
]

def get_used_topics():
    """Read blog.html and extract already used topics"""
    try:
        with open("blog.html", "r", encoding="utf-8") as f:
            content = f.read()
        titles = re.findall(r'"title":\s*"([^"]+)"', content)
        return [t.lower() for t in titles]
    except:
        return []

def pick_topic(used_topics):
    """Pick a topic not used recently"""
    available = [t for t in TOPICS if not any(
        word in " ".join(used_topics[-10:]) 
        for word in t.split()[:3]
    )]
    if not available:
        available = TOPICS
    return random.choice(available)

def generate_blog_post(topic):
    """Call Gemini API to generate humanized blog post"""
    
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    
    prompt = f"""Write a detailed, humanized SEO blog post about: "{topic}"

STRICT REQUIREMENTS:
- Length: 900-1200 words
- Tone: Conversational, like a friend explaining to another friend. Not corporate. Not robotic.
- Write in first person sometimes ("I've found that...", "When I started...", "In my experience...")
- Include occasional mild uncertainty ("I think", "from what I've seen", "this might vary")
- Use short paragraphs (2-4 sentences max)
- Include 2-3 real, practical examples
- Mention current year {current_year} where relevant
- Add a personal anecdote or story in the introduction
- DO NOT use these overused AI phrases: "In today's digital landscape", "It's worth noting", "Let's dive in", "Game-changer", "In conclusion"
- Use simple words. Avoid jargon where possible.
- Use subheadings (H2 and H3)
- End with a practical takeaway, not a generic conclusion
- Naturally mention SERPSnap tools where genuinely relevant (SERP preview, keyword density checker, meta tag generator, word counter, URL slug generator)
- Link to tools page: https://tools.serpsnap.abrdns.com/

OUTPUT FORMAT - Return ONLY a JSON object, no markdown, no backticks:
{{
  "title": "exact blog post title here",
  "category": "one of: SEO Basics, Content Strategy, Technical SEO, Link Building, Keyword Research, On-Page SEO, Google Tools, Blogging Tips",
  "excerpt": "2 sentence description that makes people want to read",
  "readTime": "X min read",
  "content": "full HTML content using only <p>, <h2>, <h3>, <ul>, <ol>, <li>, <strong>, <em> tags. No divs. No classes."
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 3000,
        }
    }
    
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    
    data = response.json()
    raw = data["candidates"][0]["content"]["parts"][0]["text"]
    
    # Clean response - remove markdown backticks if present
    raw = re.sub(r'```json\s*', '', raw)
    raw = re.sub(r'```\s*', '', raw)
    raw = raw.strip()
    
    return json.loads(raw)

def add_post_to_blog(post_data):
    """Inject new post into blog.html"""
    
    with open("blog.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    now = datetime.now()
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    date_str = f"{months[now.month-1]} {now.day}, {now.year}"
    
    gradient = random.choice(GRADIENTS)
    emoji = random.choice(EMOJIS)
    
    # Clean title for JS string safety
    title_safe = post_data["title"].replace("'", "\\'").replace('"', '\\"')
    excerpt_safe = post_data["excerpt"].replace("'", "\\'").replace('"', '\\"')
    
    # Clean content for JS
    content_safe = post_data["content"].replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    
    # Build new post object for the posts array
    new_post_js = f"""{{
  cat: '{post_data["category"]}',
  title: '{title_safe}',
  date: '{date_str}',
  readTime: '{post_data["readTime"]}',
  emoji: '{emoji}',
  gradient: '{gradient}',
  content: `{content_safe}`,
  related: [0, 1]
}}"""
    
    # Build new card HTML for the post list
    new_card_html = f"""
    <div class="post-card" onclick="showPost(NEWINDEX)">
      <div class="post-img" style="background:{gradient}">{emoji}</div>
      <div class="post-body">
        <div class="post-cat">{post_data["category"]}</div>
        <div class="post-title">{post_data["title"]}</div>
        <div class="post-excerpt">{post_data["excerpt"]}</div>
        <div class="post-meta"><span>📅 {date_str}</span><span>·</span><span>⏱ {post_data["readTime"]}</span></div>
        <div class="read-more">Read Article →</div>
      </div>
    </div>"""

    # Find the posts array and add new post
    posts_pattern = r'(const posts = \[)(.*?)(\];)'
    
    def add_to_posts(match):
        before = match.group(1)
        existing = match.group(2).rstrip()
        after = match.group(3)
        # Count existing posts to set index
        existing_count = len(re.findall(r'cat:', existing))
        new_post_indexed = new_post_js.replace("related: [0, 1]", 
                                                f"related: [0, {min(1, existing_count-1)}]")
        return f"{before}{existing},\n{new_post_indexed}\n{after}"
    
    content = re.sub(posts_pattern, add_to_posts, content, flags=re.DOTALL)
    
    # Count total posts after adding
    total_posts = len(re.findall(r'cat:', content)) - 1  # -1 for the pattern itself
    
    # Fix onclick indices for new card
    new_card_html = new_card_html.replace("NEWINDEX", str(total_posts - 1))
    
    # Add new card before closing of post-list div
    content = content.replace(
        '</div>\n\n  <!-- SINGLE POST VIEW -->',
        f'{new_card_html}\n\n  </div>\n\n  <!-- SINGLE POST VIEW -->'
    )
    
    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Added: {post_data['title']}")
    return True

def main():
    print("🚀 SERPSnap Blog Generator Starting...")
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found!")
        return
    
    # How many posts today - random between 2-4
    # But check what time it is to spread them out
    hour = datetime.now().hour
    
    # Each cron run generates 1 post
    # 4 cron schedules = max 4 posts/day
    # Random skip to keep it between 2-4
    if random.random() < 0.3:  # 30% chance to skip this run
        print("⏭️ Skipping this run for natural variation")
        return
    
    used_topics = get_used_topics()
    print(f"📚 Found {len(used_topics)} existing posts")
    
    topic = pick_topic(used_topics)
    print(f"📝 Generating post about: {topic}")
    
    try:
        post_data = generate_blog_post(topic)
        print(f"✅ Generated: {post_data['title']}")
        
        add_post_to_blog(post_data)
        print("✅ Blog updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
