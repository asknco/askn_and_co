"""
Build the ASKN & Co. LLP articles section from Markdown.

    py tools/build_articles.py

Reads every content/articles/*.md file and writes:
  - articles/<file-name>/index.html   one page per article
  - articles/index.html               the list of all articles
  - the latest 4 article cards on the homepage (between the ARTICLES markers in index.html)
  - sitemap.xml                       homepage, service pages and every article

Each Markdown file starts with a header block, for example:

    ---
    title: GST Compliance: Common Errors in ITC Claims
    description: One or two sentences shown in Google results (under 160 characters).
    date: 2026-03-01
    updated: 2026-11-03          (optional)
    category: GST
    author: CA Naveen Kumar      (optional, defaults to ASKN & Co. LLP)
    ---

The body supports ## and ### headings, paragraphs, - bullet lists, 1. numbered lists,
> quotes, **bold**, *italics* and [links](/services/gst-consultant-hyderabad/).
"""
import html
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "articles"
OUT = ROOT / "articles"
BASE = "https://asknandco.com"
FIRM = "ASKN & Co. LLP"

SERVICES = [
    ("income-tax-notice-reply-hyderabad", "Income Tax Notices"),
    ("income-tax-appeals-litigation-hyderabad", "Income Tax Appeals"),
    ("gst-consultant-hyderabad", "GST Services"),
    ("statutory-audit-hyderabad", "Audit &amp; Assurance"),
    ("itr-filing-tax-planning-hyderabad", "ITR Filing &amp; Tax Planning"),
    ("company-registration-roc-compliance-hyderabad", "Company Incorporation &amp; ROC"),
    ("accounting-bookkeeping-virtual-cfo-hyderabad", "Accounting &amp; Virtual CFO"),
    ("international-tax-transfer-pricing-hyderabad", "International Tax"),
    ("bank-loan-project-finance-hyderabad", "Bank Loans &amp; Project Finance"),
    ("government-subsidies-incentives-hyderabad", "Subsidies &amp; Incentives"),
]

ICON_BOOK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" aria-hidden="true"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>'
ICON_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
WA_FLOAT_PATH = "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


# ─── Markdown ───────────────────────────────────────────────

def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
    return t


def markdown_to_html(md):
    out, para, items, list_tag = [], [], [], None

    def flush():
        nonlocal para, items, list_tag
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []
        if items:
            out.append(f"<{list_tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{list_tag}>")
            items, list_tag = [], None

    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            flush()
            continue
        heading = re.match(r"^(#{2,4})\s+(.*)", line)
        bullet = re.match(r"^[-*]\s+(.*)", line)
        number = re.match(r"^\d+[.)]\s+(.*)", line)
        if heading:
            flush()
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
        elif bullet or number:
            tag = "ul" if bullet else "ol"
            if para or (list_tag and list_tag != tag):
                flush()
            list_tag = tag
            items.append((bullet or number).group(1))
        elif line.startswith(">"):
            flush()
            out.append(f"<blockquote><p>{inline(line.lstrip('> '))}</p></blockquote>")
        elif items and raw.startswith((" ", "\t")):
            items[-1] += " " + line  # continuation of a list item
        else:
            if items:
                flush()
            para.append(line)
    flush()
    return "\n".join(out)


def read_article(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path.name}: missing the --- header block at the top")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip().lower()] = value.strip()
    for key in ("title", "description", "date", "category"):
        if not meta.get(key):
            sys.exit(f"{path.name}: the header needs a '{key}:' line")
    try:
        meta["date_obj"] = date.fromisoformat(meta["date"])
        meta["updated_obj"] = date.fromisoformat(meta["updated"]) if meta.get("updated") else None
    except ValueError as e:
        sys.exit(f"{path.name}: dates must look like 2026-03-01 ({e})")
    meta["slug"] = path.stem
    meta["author"] = meta.get("author") or FIRM
    meta["page_title"] = meta.get("seo_title") or f"{meta['title']} | {FIRM}"
    meta["body_md"] = m.group(2)
    meta["body"] = markdown_to_html(m.group(2))
    meta["faq"] = read_faq(m.group(2))
    meta["services"] = set(re.findall(r"\]\(/services/([a-z0-9-]+)/\)", m.group(2)))
    words = len(re.findall(r"\w+", m.group(2)))
    meta["minutes"] = max(1, math.ceil(words / 200))
    meta["url"] = f"{BASE}/articles/{path.stem}/"
    # Google cuts titles at about 60 characters and descriptions at about 155
    if len(meta["page_title"]) > 65:
        print(f"note     {path.name}: search title is {len(meta['page_title'])} characters; add a shorter 'seo_title:' (under 60)")
    if len(meta["description"]) > 160:
        print(f"note     {path.name}: description is {len(meta['description'])} characters; Google shows about 155")
    return meta


def read_faq(md):
    """Questions under a '## Frequently asked questions' heading, written as '### Question' + answer paragraphs."""
    m = re.search(r"^##\s+Frequently asked questions\s*$(.*?)(?=^##\s|\Z)", md, re.M | re.S | re.I)
    if not m:
        return []
    faq = []
    for block in re.split(r"^###\s+", m.group(1), flags=re.M)[1:]:
        question, _, answer = block.partition("\n")
        answer = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", answer)      # links -> text
        answer = re.sub(r"\*\*?(.+?)\*\*?", r"\1", answer)              # bold / italics -> text
        answer = " ".join(answer.split())
        if question.strip() and answer:
            faq.append((question.strip(), answer))
    return faq


def long_date(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def esc(s):
    return html.escape(s, quote=True)


# ─── Shared page parts ──────────────────────────────────────

def head(title, description, canonical, og_type, schema):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#1e4078">
  <link rel="canonical" href="{canonical}">

  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="en_IN">
  <meta property="og:site_name" content="ASKN &amp; Co. LLP">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{BASE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{BASE}/og-image.png">

  <!-- Google Analytics (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-3B6NZ2B776"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-3B6NZ2B776');
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" href="/icon-192.png" sizes="192x192">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="/src/styles.css">

  <script type="application/ld+json">
{json.dumps(schema, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>

  <nav id="navbar">
    <div class="nav-inner container">
      <a href="/" class="nav-logo" aria-label="ASKN and Co LLP - Home">ASKN &amp; Co. LLP</a>
      <ul class="nav-links" id="navLinks">
        <li><a href="/#about">About</a></li>
        <li><a href="/#services">Services</a></li>
        <li><a href="/#litigation">Litigation</a></li>
        <li><a href="/articles/">Journal</a></li>
        <li><a href="/#team">Team</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
      <a href="/#contact" class="btn nav-cta">Book Free Consultation</a>
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
"""


def foot():
    links = "".join(f'<li><a href="/services/{slug}/">{name}</a></li>' for slug, name in SERVICES)
    return f"""
  <footer class="footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="/" class="nav-logo">ASKN &amp; Co.</a>
        <p class="footer-sub-logo">CHARTERED ACCOUNTANTS LLP</p>
        <p class="footer-tagline">Precision. Perspective. Performance.</p>
        <address class="footer-nap">C1, Spaces &amp; More Business Park @ Madhapur # 2, Plot # 27, Shilpi Enclave, Durgam Cheruvu, Inorbit Mall Rd, Madhapur, Hyderabad, Telangana 500081<br><a href="tel:+919849541701">+91 98495 41701</a> &middot; <a href="mailto:office@asknca.com">office@asknca.com</a></address>
      </div>
      <div class="footer-col footer-col--wide">
        <h4>SERVICES</h4>
        <ul>{links}</ul>
      </div>
      <div class="footer-col">
        <h4>COMPANY</h4>
        <ul><li><a href="/#about">About Us</a></li><li><a href="/#team">Our Team</a></li><li><a href="/articles/">Articles</a></li><li><a href="/#simulator">Tax Calculator</a></li><li><a href="/#contact">Contact</a></li></ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>&copy; <span id="copyrightYear">{date.today().year}</span> ASKN &amp; Co. LLP. All rights reserved.</p>
      <p class="footer-disclaimer">This website is for informational purposes only and does not constitute professional advice.</p>
    </div>
  </footer>

  <a href="https://wa.me/919177638662?text=Hello%20ASKN%20%26%20Co.%20LLP%2C%20I%20would%20like%20to%20enquire%20about%20your%20services." target="_blank" rel="noopener" class="wa-float" aria-label="Chat on WhatsApp">
    <span class="wa-tooltip">Chat with us</span>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="white"><path d="{WA_FLOAT_PATH}"/></svg>
  </a>

  <script src="/src/app.js"></script>
</body>
</html>
"""


def card(a, tag="article"):
    """Journal card linking to an article; used on the homepage and the articles list."""
    return (f'<a class="j-card" href="/articles/{a["slug"]}/">'
            f'<div class="j-cat">{ICON_BOOK} {esc(a["category"].upper())} <span class="arrow-icon">↗</span></div>'
            f'<h3>{esc(a["title"])}</h3>'
            f'<p>{esc(a["description"])}</p>'
            f'<span class="j-date">{ICON_CAL} {MONTHS[a["date_obj"].month - 1]} {a["date_obj"].year}</span></a>')


# ─── Pages ──────────────────────────────────────────────────

def article_page(a, others):
    firm_ref = {"@type": "Organization", "@id": f"{BASE}/#firm", "name": FIRM, "url": f"{BASE}/",
                "logo": {"@type": "ImageObject", "url": f"{BASE}/icon-512.png"}}
    author = firm_ref if a["author"] == FIRM else {"@type": "Person", "name": a["author"], "worksFor": firm_ref}
    schema = {"@context": "https://schema.org", "@graph": [
        {
            "@type": "BlogPosting",
            "@id": f"{a['url']}#article",
            "headline": a["title"],
            "description": a["description"],
            "articleSection": a["category"],
            "datePublished": a["date"],
            "dateModified": a.get("updated") or a["date"],
            "author": author,
            "publisher": firm_ref,
            "image": f"{BASE}/og-image.png",
            "mainEntityOfPage": a["url"],
            "inLanguage": "en-IN",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Articles", "item": f"{BASE}/articles/"},
                {"@type": "ListItem", "position": 3, "name": a["title"], "item": a["url"]},
            ],
        },
    ]}
    if a["faq"]:
        schema["@graph"].append({
            "@type": "FAQPage",
            "@id": f"{a['url']}#faq",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
                           for q, ans in a["faq"]],
        })
    updated = f' &middot; Updated {long_date(a["updated_obj"])}' if a["updated_obj"] else ""
    # Prefer articles on the same subject, so readers and Google move through a topic
    others = sorted(others, key=lambda o: (o["category"] != a["category"], not (o["services"] & a["services"])))
    related = "\n".join(f"        {card(o)}" for o in others[:3])
    return head(a["page_title"], a["description"], a["url"], "article", schema) + f"""
  <header class="page-hero">
    <div class="hero-grid"></div>
    <div class="container page-hero-body">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/articles/">Articles</a> <span aria-hidden="true">/</span> <span aria-current="page">{esc(a["category"])}</span></nav>
      <h1 class="page-hero-title">{esc(a["title"])}</h1>
      <p class="article-meta">By {esc(a["author"])} &middot; <time datetime="{a["date"]}">{long_date(a["date_obj"])}</time>{updated} &middot; {a["minutes"]} min read</p>
    </div>
  </header>

  <section class="section section--white">
    <div class="container">
      <article class="article-body">
{a["body"]}
        <aside class="article-cta">
          <h2>Need advice on this?</h2>
          <p>Speak to a partner at ASKN &amp; Co. LLP, Chartered Accountants in Madhapur, Hyderabad.</p>
          <div class="article-cta-actions">
            <a href="tel:+919849541701" class="btn btn-brand btn-icon">{ICON_PHONE} +91 98495 41701</a>
            <a href="https://wa.me/919177638662?text=Hello%20ASKN%20%26%20Co.%20LLP%2C%20I%20read%20your%20article%20and%20would%20like%20advice." target="_blank" rel="noopener" class="btn btn-outline-brand btn-icon">{ICON_WA} WhatsApp Us</a>
          </div>
        </aside>
        <p class="article-disclaimer">This article is general information based on the law as at the date shown and is not professional advice. Please consult us before acting on it.</p>
      </article>
    </div>
  </section>

  <section class="section section--light">
    <div class="container">
      <div class="section-head center">
        <h2 class="section-title">More from the ASKN Journal</h2>
        <div class="brand-rule brand-rule--center"></div>
      </div>
      <div class="journal-grid journal-grid--3">
{related}
      </div>
      <div class="center" style="margin-top:2.5rem"><a href="/articles/" class="btn btn-outline-brand">View all articles</a></div>
    </div>
  </section>
""" + foot()


def index_page(articles):
    url = f"{BASE}/articles/"
    schema = {"@context": "https://schema.org", "@graph": [
        {
            "@type": "Blog",
            "@id": f"{url}#blog",
            "name": "The ASKN Journal",
            "url": url,
            "publisher": {"@id": f"{BASE}/#firm"},
            "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": a["url"], "datePublished": a["date"]} for a in articles],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Articles", "item": url},
            ],
        },
    ]}
    cards = "\n".join(f"        {card(a)}" for a in articles)
    return head("Income Tax, GST & Company Law Articles | ASKN & Co. LLP, Hyderabad",
                "Practical articles on income tax, GST, audit, company law and international tax by ASKN & Co. LLP, Chartered Accountants in Madhapur, Hyderabad.",
                url, "website", schema) + f"""
  <header class="page-hero">
    <div class="hero-grid"></div>
    <div class="container page-hero-body">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span aria-current="page">Articles</span></nav>
      <h1 class="page-hero-title">The ASKN Journal</h1>
      <p class="hero-sub">Practical insights on income tax, GST, audit, company law and international tax from the Chartered Accountants at ASKN &amp; Co. LLP, Hyderabad.</p>
    </div>
  </header>

  <section class="section section--white">
    <div class="container">
      <div class="journal-grid">
{cards}
      </div>
    </div>
  </section>
""" + foot()


def update_homepage(articles):
    path = ROOT / "index.html"
    s = path.read_text(encoding="utf-8")
    start, end = "<!-- ARTICLES:START -->", "<!-- ARTICLES:END -->"
    if start not in s or end not in s:
        sys.exit("index.html: could not find the ARTICLES:START / ARTICLES:END markers in the Journal section")
    cards = "\n".join(f"        {card(a)}" for a in articles[:4])
    s = re.sub(re.escape(start) + r".*?" + re.escape(end), f"{start}\n{cards}\n        {end}", s, flags=re.S)
    path.write_text(s, encoding="utf-8", newline="")


def update_service_pages(articles):
    """Fill each service page's related-articles block with the articles that link to that service."""
    start, end = "<!-- RELATED-ARTICLES:START -->", "<!-- RELATED-ARTICLES:END -->"
    for path in sorted((ROOT / "services").glob("*/index.html")):
        s = path.read_text(encoding="utf-8")
        if start not in s:
            print(f"note     {path.parent.name}: no related-articles markers; run tools/build_service_pages.py first")
            continue
        linked = [a for a in articles if path.parent.name in a["services"]][:6]
        block = ""
        if linked:
            cards = "\n".join(f"        {card(a)}" for a in linked)
            block = f"""
  <section class="section section--white">
    <div class="container">
      <div class="section-head center">
        <p class="section-overline">INSIGHTS</p>
        <h2 class="section-title">Related articles</h2>
        <div class="brand-rule brand-rule--center"></div>
      </div>
      <div class="journal-grid journal-grid--3">
{cards}
      </div>
    </div>
  </section>
  """
        s = re.sub(re.escape(start) + r".*?" + re.escape(end), f"{start}{block}{end}", s, flags=re.S)
        path.write_text(s, encoding="utf-8", newline="\n")


def write_sitemap(articles):
    today = date.today().isoformat()
    urls = [(f"{BASE}/", today)]
    for p in sorted((ROOT / "services").glob("*/index.html")):
        urls.append((f"{BASE}/services/{p.parent.name}/", today))
    urls.append((f"{BASE}/articles/", articles[0]["date"] if articles else today))
    for a in articles:
        urls.append((a["url"], a.get("updated") or a["date"]))
    body = "\n".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n',
        encoding="utf-8", newline="\n")


def main():
    files = sorted(SRC.glob("*.md"))
    if not files:
        sys.exit(f"No articles found in {SRC}")
    articles = sorted((read_article(f) for f in files), key=lambda a: a["date_obj"], reverse=True)

    keep = {a["slug"] for a in articles}
    for old in OUT.glob("*/index.html"):
        if old.parent.name not in keep:  # article file was deleted or renamed
            old.unlink()
            try:
                old.parent.rmdir()
            except OSError:
                pass  # folder locked (e.g. by OneDrive); an empty folder is not published
            print("removed  articles/" + old.parent.name + "/")

    for a in articles:
        target = OUT / a["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        others = [o for o in articles if o is not a]
        target.write_text(article_page(a, others), encoding="utf-8", newline="\n")
        print("built    articles/" + a["slug"] + "/")
    (OUT / "index.html").write_text(index_page(articles), encoding="utf-8", newline="\n")
    update_homepage(articles)
    update_service_pages(articles)
    write_sitemap(articles)
    print(f"\nDone: {len(articles)} articles. Homepage Journal, service pages and sitemap.xml updated.")


if __name__ == "__main__":
    main()
