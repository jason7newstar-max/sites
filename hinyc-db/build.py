#!/usr/bin/env python3
"""HI NYC — Static restaurant database generator.

Merges:
  - publisher/queue.json + jobs/{id}.json (full restaurants with YT video)
  - lead-gen/leads.json (candidates, less data)

Outputs:
  - api/restaurants.json    machine feed
  - restaurants/{slug}/index.html  per-restaurant SEO page
  - index.html              listing + filter
  - sitemap.xml             SEO
  - robots.txt
"""
import json, re, html, sys
from pathlib import Path
from datetime import datetime, timezone

SITE = Path(__file__).parent
PUB_DIR = Path.home() / "projects" / "foodbrand" / "tools" / "publisher"
LEAD_DIR = Path.home() / "projects" / "foodbrand" / "tools" / "lead-gen"

BASE_URL = "https://hinyc-db.vercel.app"  # tentative; user may change to custom domain


def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60]


def load_pub_jobs():
    """Read publisher queue + per-job specs. Each entry has YT video, photos, captions."""
    out = []
    queue = json.loads((PUB_DIR / "queue.json").read_text())
    for entry in queue:
        if not entry.get("youtube_id"):
            continue
        spec_path = Path(entry.get("spec_file", ""))
        if not spec_path.exists():
            continue
        spec = json.loads(spec_path.read_text())
        r = spec.get("restaurant", {})
        # Caption: queue.json has older captions baked, but we use what's in queue entry if present
        cap = entry.get("caption", {}) if isinstance(entry.get("caption"), dict) else {}
        out.append({
            "id": entry["id"],
            "slug": slugify(r.get("name_en", entry["id"])),
            "source": "featured",
            "name_en": r.get("name_en", ""),
            "name_cn": r.get("name_cn", ""),
            "tagline_cn": (r.get("hook_title_cn") or "").replace("<br/>", " · "),
            "tagline_kr": r.get("hook_title_kr", ""),
            "address_line": r.get("address_line", ""),
            "address_city": r.get("address_city", ""),
            "neighborhood": (r.get("address_city") or "").split("·")[0].strip().title(),
            "rating_tag": r.get("name_tag", ""),
            "accent_color": r.get("accent_color", "#1a1410"),
            "dishes": r.get("dishes", []),
            "youtube_id": entry["youtube_id"].split("/")[-1] if entry["youtube_id"] else "",
            "youtube_url": entry["youtube_id"],
            "scheduled_at": entry.get("scheduled_at", ""),
            "yt_title": cap.get("title", ""),
            "yt_description": cap.get("description", "")[:600],
            "yt_tags": cap.get("tags", []),
        })
    return out


def load_leads():
    """Read lead-gen leads. Less rich but covers more restaurants."""
    p = LEAD_DIR / "leads.json"
    if not p.exists():
        return []
    db = json.loads(p.read_text())
    out = []
    for l in db.get("leads", []):
        name = l.get("name", "")
        if not name:
            continue
        out.append({
            "id": l.get("id", slugify(name)),
            "slug": slugify(name),
            "source": "lead",
            "name_en": name,
            "name_cn": "",
            "tagline_cn": "",
            "tagline_kr": "",
            "address_line": l.get("address", ""),
            "address_city": "NEW YORK CITY",
            "neighborhood": "",
            "rating_tag": l.get("source_label", ""),
            "accent_color": "#5a5a5a",
            "dishes": [],
            "youtube_id": "",
            "youtube_url": "",
            "scheduled_at": "",
            "yt_title": "",
            "yt_description": l.get("blurb", ""),
            "yt_tags": [],
            "tier": l.get("tier", "B"),
        })
    return out


def merge():
    """Merge featured + leads, dedup by slug."""
    featured = load_pub_jobs()
    leads = load_leads()
    seen = {f["slug"] for f in featured}
    out = list(featured)
    for l in leads:
        if l["slug"] not in seen:
            out.append(l)
            seen.add(l["slug"])
    return out


# ---------- HTML helpers ----------

def esc(s):
    return html.escape(str(s or ""), quote=True)


def head_block(title, description, slug=None, image=None):
    canonical = f"{BASE_URL}/restaurants/{slug}/" if slug else BASE_URL + "/"
    img = image or f"{BASE_URL}/og-default.png"
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{'../../styles/style.css' if slug else 'styles/style.css'}">"""


CSS = """
:root {
  --bg: #faf6ee; --bg-elev: #fffdf7; --bg-card: #fff;
  --ink: #1a1410; --ink-mute: #4a3d33; --ink-dim: #8a7a6a;
  --line: rgba(26,20,16,0.12); --accent: #c2410c;
  --display: 'Noto Serif SC', 'Songti SC', serif;
  --body: 'Inter', 'PingFang SC', sans-serif;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { background: var(--bg); color: var(--ink); font-family: var(--body); line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Header */
header { position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px); background: rgba(250,246,238,0.85); border-bottom: 1px solid var(--line); }
.nav { max-width: 1100px; margin: 0 auto; padding: 18px 24px; display: flex; align-items: center; justify-content: space-between; }
.logo { font-family: var(--display); font-weight: 900; font-size: 22px; letter-spacing: -0.5px; }
.logo span { color: var(--accent); }
.nav-links { display: flex; gap: 24px; align-items: center; }
.nav-links a { color: var(--ink); font-size: 14px; }
.btn { display: inline-block; padding: 10px 20px; background: var(--ink); color: var(--bg-elev); border-radius: 999px; font-size: 14px; font-weight: 500; }
.btn:hover { background: var(--accent); text-decoration: none; }

/* Index */
.hero { max-width: 1100px; margin: 0 auto; padding: 80px 24px 40px; }
.hero h1 { font-family: var(--display); font-size: clamp(38px, 6vw, 64px); line-height: 1.05; font-weight: 900; letter-spacing: -1px; margin-bottom: 16px; }
.hero h1 em { font-style: italic; color: var(--accent); }
.hero p { color: var(--ink-mute); font-size: 18px; max-width: 600px; }
.search-box { margin: 30px 0; display: flex; gap: 12px; flex-wrap: wrap; }
.search-box input { flex: 1; min-width: 240px; padding: 14px 18px; border: 1.5px solid var(--line); border-radius: 12px; font-size: 16px; font-family: var(--body); background: var(--bg-elev); }
.search-box input:focus { outline: none; border-color: var(--accent); }
.filter-pill { padding: 10px 16px; border: 1.5px solid var(--line); border-radius: 999px; background: var(--bg-elev); cursor: pointer; font-size: 13px; font-family: var(--body); }
.filter-pill.active { background: var(--ink); color: var(--bg-elev); border-color: var(--ink); }

.grid { max-width: 1100px; margin: 0 auto 80px; padding: 0 24px; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.card { background: var(--bg-card); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; transition: transform 0.15s, border 0.15s; display: flex; flex-direction: column; }
.card:hover { transform: translateY(-3px); border-color: var(--accent); text-decoration: none; }
.card-cover { aspect-ratio: 16/10; background: var(--ink); position: relative; display: flex; align-items: center; justify-content: center; color: rgba(255,255,255,0.85); font-family: var(--display); font-size: 28px; font-weight: 700; padding: 20px; text-align: center; }
.card-cover.has-yt::after { content: '▶'; position: absolute; top: 12px; right: 12px; background: rgba(0,0,0,0.7); color: white; padding: 4px 10px; border-radius: 999px; font-size: 11px; }
.card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; }
.card h3 { font-family: var(--display); font-size: 18px; font-weight: 700; margin-bottom: 4px; line-height: 1.2; color: var(--ink); }
.card .meta { font-size: 12px; color: var(--ink-dim); margin-bottom: 8px; }
.card .blurb { font-size: 13px; color: var(--ink-mute); line-height: 1.5; flex: 1; }
.card .tag { display: inline-block; font-size: 10px; padding: 3px 8px; background: rgba(194,65,12,0.12); color: var(--accent); border-radius: 999px; margin-top: 10px; letter-spacing: 1px; font-weight: 600; }

/* Restaurant page */
.r-hero { max-width: 900px; margin: 0 auto; padding: 60px 24px 30px; }
.r-back { display: inline-block; margin-bottom: 24px; color: var(--ink-dim); font-size: 13px; }
.r-back:hover { color: var(--accent); }
.r-hero h1 { font-family: var(--display); font-size: clamp(36px, 5vw, 56px); font-weight: 900; line-height: 1.05; letter-spacing: -0.5px; margin-bottom: 8px; }
.r-hero .name-cn { font-family: var(--display); font-size: 22px; color: var(--ink-mute); margin-bottom: 16px; font-weight: 400; }
.r-hero .meta { font-size: 14px; color: var(--ink-dim); display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 24px; }
.r-hero .meta strong { color: var(--ink); }

.r-video { max-width: 900px; margin: 0 auto 40px; padding: 0 24px; }
.r-video-wrap { aspect-ratio: 9/16; max-width: 380px; margin: 0 auto; background: var(--ink); border-radius: 14px; overflow: hidden; }
.r-video-wrap iframe { width: 100%; height: 100%; border: 0; }

.r-section { max-width: 900px; margin: 0 auto 40px; padding: 0 24px; }
.r-section h2 { font-family: var(--display); font-size: 24px; font-weight: 700; margin-bottom: 14px; }
.r-section p { color: var(--ink-mute); font-size: 15px; line-height: 1.7; }

.r-dishes { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.r-dish { background: var(--bg-elev); border: 1px solid var(--line); border-radius: 12px; padding: 18px; }
.r-dish .dish-cn { font-family: var(--display); font-size: 18px; font-weight: 700; }
.r-dish .dish-en { font-size: 12px; color: var(--ink-dim); letter-spacing: 1px; margin-top: 4px; }

.r-tags { margin-top: 14px; display: flex; flex-wrap: wrap; gap: 6px; }
.r-tag { font-size: 11px; padding: 4px 10px; background: var(--bg-elev); border: 1px solid var(--line); border-radius: 999px; color: var(--ink-mute); }

.r-actions { max-width: 900px; margin: 0 auto 30px; padding: 0 24px; display: flex; gap: 10px; flex-wrap: wrap; }
.r-action { display: inline-flex; align-items: center; gap: 6px; padding: 10px 16px; background: var(--ink); color: var(--bg-elev); border-radius: 999px; font-size: 13px; font-weight: 600; text-decoration: none; transition: transform 0.15s, background 0.15s; }
.r-action:hover { transform: translateY(-1px); background: var(--accent); text-decoration: none; }

footer { padding: 40px 24px; text-align: center; color: var(--ink-dim); font-size: 13px; border-top: 1px solid var(--line); }
footer .links { margin-bottom: 12px; }
footer .links a { color: var(--ink-mute); margin: 0 10px; font-size: 13px; }

@media (max-width: 720px) { .nav-links a:not(.btn) { display: none; } }
"""


# ---------- Index page ----------

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
{head}
</head>
<body>
<header>
  <nav class="nav">
    <div class="logo">HI <span>NYC</span></div>
    <div class="nav-links">
      <a href="#about">关于</a>
      <a href="https://www.instagram.com/newhinyc/">Instagram</a>
      <a href="https://www.youtube.com/@Jason2-f5y" class="btn">YouTube</a>
    </div>
  </nav>
</header>

<section class="hero">
  <h1>纽约 / 新泽西<br/><em>{n_featured}</em> 家精选餐厅<br/><em>+ {n_leads}</em> 家正在挖掘</h1>
  <p>每家附 22 秒短视频 + 真菜照 + 中英双语介绍。一周更新 5 家。</p>
  <div class="search-box">
    <input type="search" id="search" placeholder="搜餐厅名 / 街区 / 菜系…" autocomplete="off">
    <button class="filter-pill active" data-filter="all">全部</button>
    <button class="filter-pill" data-filter="featured">精选(有视频)</button>
    <button class="filter-pill" data-filter="lead">候选</button>
  </div>
</section>

<main class="grid" id="grid">
{cards}
</main>

<footer id="about">
  <div class="links">
    <a href="https://www.instagram.com/newhinyc/">@newhinyc</a>
    <a href="https://www.youtube.com/@Jason2-f5y">YouTube</a>
    <a href="/api/restaurants.json">JSON Feed</a>
  </div>
  <div>HI NYC · 纽约 / NJ / LI / CT 餐厅数据库</div>
  <div style="margin-top:6px; color: var(--ink-dim);">© 2026 HI NYC · {total} restaurants indexed</div>
</footer>

<script>
const grid = document.getElementById('grid');
const search = document.getElementById('search');
let activeFilter = 'all';

function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  for (const card of grid.children) {{
    const matchesText = !q || card.dataset.search.includes(q);
    const matchesFilter = activeFilter === 'all' || card.dataset.source === activeFilter;
    card.style.display = (matchesText && matchesFilter) ? '' : 'none';
  }}
}}
search.addEventListener('input', applyFilters);
document.querySelectorAll('.filter-pill').forEach(b => {{
  b.addEventListener('click', () => {{
    document.querySelectorAll('.filter-pill').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    activeFilter = b.dataset.filter;
    applyFilters();
  }});
}});
</script>

</body>
</html>
"""


def render_card(r):
    cover_class = "card-cover has-yt" if r["youtube_id"] else "card-cover"
    cover_text = esc(r["name_en"]) or esc(r["name_cn"])
    blurb = esc((r["yt_description"] or r["tagline_cn"])[:140])
    source_tag = "FEATURED" if r["source"] == "featured" else "CANDIDATE"
    search_kv = " ".join([
        r.get("name_en", ""), r.get("name_cn", ""),
        r.get("address_line", ""), r.get("address_city", ""),
        r.get("neighborhood", ""), source_tag,
    ]).lower()
    return f"""<a class="card" href="restaurants/{esc(r['slug'])}/" data-source="{r['source']}" data-search="{esc(search_kv)}">
  <div class="{cover_class}" style="background: {esc(r['accent_color'])};">{cover_text}</div>
  <div class="card-body">
    <h3>{esc(r['name_en'] or r['name_cn'])}</h3>
    <div class="meta">{esc(r['address_line'])}{' · ' if r['address_line'] else ''}{esc(r['neighborhood'])}</div>
    <div class="blurb">{blurb}</div>
    <span class="tag">{source_tag}</span>
  </div>
</a>"""


# ---------- Restaurant page ----------

REST_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
{head}
{schema}
</head>
<body>
<header>
  <nav class="nav">
    <div class="logo"><a href="../../" style="color:inherit;">HI <span>NYC</span></a></div>
    <div class="nav-links">
      <a href="../../">所有餐厅</a>
      <a href="https://www.instagram.com/newhinyc/" class="btn">关注</a>
    </div>
  </nav>
</header>

<section class="r-hero">
  <a class="r-back" href="../../">← 所有餐厅</a>
  <h1>{name_en}</h1>
  {name_cn_block}
  <div class="meta">
    {addr_block}
    {rating_block}
    {yt_block}
  </div>
</section>

{video_block}

{actions_block}

{tagline_block}

{dishes_block}

{description_block}

{tags_block}

<footer>
  <div class="links">
    <a href="../../">所有餐厅</a>
    <a href="https://www.instagram.com/newhinyc/">@newhinyc</a>
    <a href="https://www.youtube.com/@Jason2-f5y">YouTube</a>
  </div>
  <div>HI NYC · 纽约餐厅数据库</div>
</footer>
</body>
</html>
"""


def render_restaurant(r):
    title = f"{r['name_en']} · {r['neighborhood'] or 'NYC'} · HI NYC 评测"
    if r["name_cn"]:
        title = f"{r['name_en']} {r['name_cn']} · {r['neighborhood'] or 'NYC'} · HI NYC"
    desc = r["yt_description"][:155] or r["tagline_cn"] or f"NYC restaurant: {r['name_en']}"

    schema = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": r["name_en"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": r["address_line"],
            "addressLocality": r["neighborhood"] or "New York",
            "addressRegion": "NY",
            "addressCountry": "US",
        },
    }
    if r["youtube_url"]:
        schema["video"] = {
            "@type": "VideoObject",
            "name": r["yt_title"] or r["name_en"],
            "embedUrl": f"https://www.youtube.com/embed/{r['youtube_id']}",
            "thumbnailUrl": f"https://img.youtube.com/vi/{r['youtube_id']}/maxresdefault.jpg",
            "uploadDate": r.get("scheduled_at", "2026-01-01T00:00:00Z")[:19] + "Z" if r.get("scheduled_at") else "2026-01-01T00:00:00Z",
            "description": r["yt_description"][:300],
        }

    schema_block = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

    # Action buttons (reserve / delivery / directions). Pre-positioned for affiliate swap-in.
    # OpenTable affiliate ID will go in `?refid=YOUR_ID` once user signs up via Impact.
    import urllib.parse as _up
    full_addr = f"{r['address_line']}, {r['address_city']}".strip(" ,")
    name_q = _up.quote(r["name_en"] or r["name_cn"])
    addr_q = _up.quote(full_addr) if full_addr else name_q
    actions_block = ""
    if full_addr or r["name_en"]:
        actions_block = f'''<section class="r-actions">
  <a class="r-action" target="_blank" rel="noopener" href="https://www.opentable.com/s?term={name_q}+New+York&datetime=&covers=2">📅 Reserve</a>
  <a class="r-action" target="_blank" rel="noopener" href="https://www.ubereats.com/feed?diningMode=DELIVERY&pl=%7B%22type%22%3A%22query%22%2C%22query%22%3A%22{name_q}%22%7D">🛵 Delivery</a>
  <a class="r-action" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query={addr_q}">🗺️ Directions</a>
</section>'''

    name_cn_block = f'<div class="name-cn">{esc(r["name_cn"])}</div>' if r["name_cn"] else ""

    addr_block = f'<span><strong>📍</strong> {esc(r["address_line"])}, {esc(r["address_city"])}</span>' if r["address_line"] else ""
    rating_block = f'<span><strong>⭐</strong> {esc(r["rating_tag"])}</span>' if r["rating_tag"] else ""
    yt_block = f'<span><strong>▶</strong> <a href="{esc(r["youtube_url"])}">看视频</a></span>' if r["youtube_url"] else ""

    if r["youtube_id"]:
        video_block = f'''<section class="r-video"><div class="r-video-wrap"><iframe src="https://www.youtube.com/embed/{esc(r["youtube_id"])}" title="{esc(r["name_en"])}" allowfullscreen></iframe></div></section>'''
    else:
        video_block = ""

    tagline_block = ""
    if r["tagline_cn"]:
        tagline_block = f'''<section class="r-section"><h2>看点</h2><p>{esc(r["tagline_cn"])}</p></section>'''

    dishes_block = ""
    if r["dishes"]:
        dish_html = "".join(
            f'<div class="r-dish"><div class="dish-cn">{esc(d.get("cn",""))} {esc(d.get("emoji",""))}</div><div class="dish-en">{esc(d.get("en",""))}</div></div>'
            for d in r["dishes"]
        )
        dishes_block = f'<section class="r-section"><h2>招牌菜</h2><div class="r-dishes">{dish_html}</div></section>'

    description_block = ""
    if r["yt_description"]:
        description_block = f'''<section class="r-section"><h2>介绍</h2><p>{esc(r["yt_description"])}</p></section>'''

    tags_block = ""
    if r["yt_tags"]:
        tag_html = "".join(f'<span class="r-tag">{esc(t)}</span>' for t in r["yt_tags"])
        tags_block = f'<section class="r-section"><h2>标签</h2><div class="r-tags">{tag_html}</div></section>'

    head = head_block(title, desc, slug=r["slug"], image=f"https://img.youtube.com/vi/{r['youtube_id']}/maxresdefault.jpg" if r["youtube_id"] else None)

    return REST_TEMPLATE.format(
        head=head,
        schema=schema_block,
        name_en=esc(r["name_en"]),
        name_cn_block=name_cn_block,
        addr_block=addr_block,
        rating_block=rating_block,
        yt_block=yt_block,
        video_block=video_block,
        actions_block=actions_block,
        tagline_block=tagline_block,
        dishes_block=dishes_block,
        description_block=description_block,
        tags_block=tags_block,
    )


# ---------- Sitemap & robots ----------

def build_sitemap(records):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f'<url><loc>{BASE_URL}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>']
    for r in records:
        urls.append(f'<url><loc>{BASE_URL}/restaurants/{esc(r["slug"])}/</loc><lastmod>{today}</lastmod><priority>0.7</priority></url>')
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"


ROBOTS = """User-agent: *
Allow: /
Sitemap: """ + BASE_URL + "/sitemap.xml\n"


# ---------- Main ----------

def main():
    records = merge()
    n_featured = sum(1 for r in records if r["source"] == "featured")
    n_leads = sum(1 for r in records if r["source"] == "lead")
    print(f"merged: {n_featured} featured + {n_leads} leads = {len(records)} total")

    # Sort: featured first, then leads
    records.sort(key=lambda r: (r["source"] != "featured", r["name_en"].lower()))

    # CSS
    (SITE / "styles" / "style.css").write_text(CSS)

    # Per-restaurant pages
    SITE.joinpath("restaurants").mkdir(exist_ok=True)
    for r in records:
        d = SITE / "restaurants" / r["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render_restaurant(r))

    # Index
    cards = "\n".join(render_card(r) for r in records)
    head = head_block(
        "HI NYC — 183 家纽约餐厅数据库 · 中英双语",
        "纽约 · 新泽西 · 长岛 · 康州 餐厅指南。每家附短视频 + 真菜照 + 中英双语介绍。",
    )
    (SITE / "index.html").write_text(INDEX_TEMPLATE.format(
        head=head, n_featured=n_featured, n_leads=n_leads, total=len(records), cards=cards,
    ))

    # API
    SITE.joinpath("api").mkdir(exist_ok=True)
    (SITE / "api" / "restaurants.json").write_text(json.dumps(records, indent=2, ensure_ascii=False))

    # SEO
    (SITE / "sitemap.xml").write_text(build_sitemap(records))
    (SITE / "robots.txt").write_text(ROBOTS)

    print(f"  generated {len(records)} pages + index + sitemap + robots + api/restaurants.json")
    print(f"  preview: open {SITE / 'index.html'}")


if __name__ == "__main__":
    main()
