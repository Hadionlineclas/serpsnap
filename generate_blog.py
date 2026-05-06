import os
import re
import json
import random
import requests
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

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
    "linear-gradient(135deg,#ff9a9e,#fecfef)",
    "linear-gradient(135deg,#a1c4fd,#c2e9fb)",
    "linear-gradient(135deg,#fd7043,#ff8a65)",
]

EMOJIS = ["📊","🔍","🚀","💡","🎯","📈","🔑","⚡","🛠️","📝","🌐","🔗"]

def get_used_topics():
    try:
        with open("blog.html","r",encoding="utf-8") as f:
            content = f.read()
        titles = re.findall(r"title:\s*'([^']+)'", content)
        return [t.lower() for t in titles]
    except:
        return []

def pick_topic(used_topics):
    used_words = " ".join(used_topics[-10:])
    available = [t for t in TOPICS if t.split()[0] not in used_words]
    if not available:
        available = TOPICS
    return random.choice(available)

def generate_blog_post(topic):
    current_year = datetime.now().year

    prompt = f"""Write a detailed, humanized SEO blog post about: "{topic}"

STRICT REQUIREMENTS:
- Length: 800-1000 words
- Tone: Conversational, like explaining to a friend. Not corporate.
- Use first person sometimes ("I've found", "In my experience", "When I tried")
- Short paragraphs (2-3 sentences max)
- Include practical examples
- Mention year {current_year} where relevant
- DO NOT use: "In today's digital landscape", "Let's dive in", "Game-changer", "In conclusion"
- Naturally mention SERPSnap tools where relevant
- Link: https://tools.serpsnap.abrdns.com/

Return ONLY a valid JSON object. No markdown. No backticks. No extra text before or after.
{{
  "title": "blog post title here",
  "category": "SEO Basics",
  "excerpt": "2 sentence teaser",
  "readTime": "5 min read",
  "content": "full HTML using only p, h2, h3, ul, ol, li, strong, em tags"
}}"""
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 2500,
        }
    }

    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    raw = data["candidates"][0]["content"]["parts"][0]["text"]

    # Clean markdown if present
    raw = re.sub(r'```json\s*', '', raw)
    raw = re.sub(r'```\s*', '', raw)
    raw = raw.strip()

    # Find JSON object
    start = raw.find('{')
    end = raw.rfind('}') + 1
    if start >= 0 and end > start:
        raw = raw[start:end]

    return json.loads(raw)

def inject_post(post_data):
    with open("blog.html","r",encoding="utf-8") as f:
        html = f.read()

    now = datetime.now()
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    date_str = f"{months[now.month-1]} {now.day}, {now.year}"

    gradient = random.choice(GRADIENTS)
    emoji = random.choice(EMOJIS)
    cat = post_data.get("category","SEO Tips")
    title = post_data["title"]
    excerpt = post_data["excerpt"]
    read_time = post_data.get("readTime","5 min read")
    content = post_data["content"]

    # Escape for JS template literal
    def js_escape(s):
        return s.replace('\\','\\\\').replace('`','\\`').replace('${','\\${').replace("'","\\'")

    title_js = js_escape(title)
    excerpt_js = js_escape(excerpt)
    content_js = js_escape(content)

    # Count existing posts
    existing = len(re.findall(r'\bcat:', html))
    new_index = existing  # 0-based index of new post

    # NEW POST CARD — inject before closing of post-list
    new_card = f"""
    <div class="post-card" onclick="showPost({new_index})">
      <div class="post-img" style="background:{gradient}">{emoji}</div>
      <div class="post-body">
        <div class="post-cat">{cat}</div>
        <div class="post-title">{title}</div>
        <div class="post-excerpt">{excerpt}</div>
        <div class="post-meta"><span>📅 {date_str}</span><span>·</span><span>⏱ {read_time}</span></div>
        <div class="read-more">Read Article →</div>
      </div>
    </div>"""

    # NEW POST JS OBJECT — inject before closing ];
    new_post_js = f"""
,{{
  cat: '{cat}',
  title: '{title_js}',
  date: '{date_str}',
  readTime: '{read_time}',
  emoji: '{emoji}',
  gradient: '{gradient}',
  content: `{content_js}`,
  related: [0, 1]
}}"""

    # Inject card into post-list
    html = html.replace(
        '  <!-- SINGLE POST VIEW -->',
        new_card + '\n\n  <!-- SINGLE POST VIEW -->'
    )

    # Inject JS object before ]; at end of posts array
    html = html.replace(
        '];\n\nfunction showPost',
        new_post_js + '\n];\n\nfunction showPost'
    )

    with open("blog.html","w",encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Post added: {title}")

def main():
    print("🚀 SERPSnap Blog Generator Starting...")

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY missing!")
        return

    # 30% skip for natural variation
    if random.random() < 0.3:
        print("⏭️ Skipping this run — natural variation")
        return

    used = get_used_topics()
    print(f"📚 Existing posts: {len(used)}")

    topic = pick_topic(used)
    print(f"📝 Topic: {topic}")

    try:
        post = generate_blog_post(topic)
        print(f"✅ Generated: {post['title']}")
        inject_post(post)
        print("✅ blog.html updated!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
