#!/usr/bin/env python3
"""
Refresh all 13 skyzai.com product HTML pages from canonical copy decks.
Preserves per-page CSS; regenerates content from copy deck source.
"""

import re
from pathlib import Path

BASE = Path("/Users/Yves/Magnum Opus")
DECK_DIR = BASE / "02_SKYZAI/01_NOOSPHERE/03_PRODUCTS/skyzai_marketplace/copy_decks"
HTML_DIR = BASE / "02_SKYZAI/01_NOOSPHERE/07_PWAs/skyzai_com/products"
ASSET_VERSION = "v8"

# Mapping: copy deck filename -> product directory name
PRODUCTS = {
    "B2B_01_API_PAY.md": "api-pay",
    "B2B_02_OFN_RECEIPTS.md": "ofn-receipts",
    "B2B_03_KYC_KYB_HOOKS.md": "kyc-kyb-hooks",
    "B2B_04_WALLET_BOUNDARIES.md": "wallet-boundaries",
    "B2B_05_AGENTZ_ENTITLEMENTS.md": "agentz-entitlements",
    "B2B_06_DEX_SETTLEMENT_BADGES.md": "dex-settlement-badges",
    "B2B_07_MARKETPLACE.md": "marketplace",
    "B2C_01_NEXUS.md": "nexus",
    "B2C_02_PAY_POS.md": "pay-pos",
    "B2C_03_EVENTS.md": "events",
    "B2C_04_PERSONAL_RECEIPTS.md": "personal-receipts",
    "B2C_05_PERSONAL_WALLET.md": "personal-wallet",
    "B2C_06_APU_ADVISOR.md": "apu-advisor",
}

PRODUCT_META = {
    "api-pay": {
        "wordmark": "API Pay",
        "glyph": "⟩⟨",
        "glyph_class": "product-glyph--wide",
        "docs": "https://skyzai.org/docs/wiki/P0-api-pay",
        "route": "api-pay.skyzai.com",
        "surface": "B2B-1",
        "proof": "Paid endpoint wrapper, OFN receipt, control event, statement row.",
    },
    "ofn-receipts": {
        "wordmark": "OFN Receipts",
        "glyph": "◇",
        "glyph_class": "",
        "docs": "https://skyzai.org/docs/wiki/P1-ofn-receipts",
        "route": "ofn.skyzai.com",
        "surface": "B2B-2",
        "proof": "Receipt emit, receipt verify, replay packet, export hook.",
    },
    "kyc-kyb-hooks": {
        "wordmark": "KYC/KYB Hooks",
        "glyph": "◦|",
        "glyph_class": "product-glyph--wide",
        "docs": "https://skyzai.org/docs/wiki/P2-kyc-kyb-hooks",
        "route": "kyc.skyzai.com",
        "surface": "B2B-3",
        "proof": "Provider pass-through, policy status, K2 exception queue.",
    },
    "wallet-boundaries": {
        "wordmark": "Wallet Boundaries",
        "glyph": "⬡-⬡-⬡-⬡-⬡",
        "glyph_class": "product-glyph--wide",
        "docs": "https://skyzai.org/docs/wiki/P3-wallet-boundaries",
        "route": "wallet.skyzai.com",
        "surface": "B2B-4",
        "proof": "W1-W5 map, signer boundary, recovery receipt, Grace Exit path.",
    },
    "agentz-entitlements": {
        "wordmark": "Agentz Entitlements",
        "glyph": "decagram",
        "glyph_class": "product-glyph--decagram",
        "docs": "https://skyzai.org/docs/wiki/P4-agentz-entitlements",
        "route": "agentz.skyzai.com",
        "surface": "B2B-5",
        "proof": "Capability scope, caste entitlement, usage receipt, audit rail.",
    },
    "dex-settlement-badges": {
        "wordmark": "DEX Badges",
        "glyph": "⬡",
        "glyph_class": "",
        "docs": "https://skyzai.org/docs/wiki/P5-dex-settlement-badges",
        "route": "dex.skyzai.com",
        "surface": "B2B-6",
        "proof": "Settlement reference, replay evidence, no outcome badge without receipt.",
    },
    "marketplace": {
        "wordmark": "Marketplace",
        "glyph": "⊞",
        "glyph_class": "",
        "docs": "https://skyzai.org/docs/wiki/P6-marketplace",
        "route": "marketplace.skyzai.com",
        "surface": "B2B-M",
        "proof": "Listed service, declared evidence tier, active boundary, buyer route.",
    },
    "nexus": {
        "wordmark": "Nexus",
        "glyph": "✺",
        "glyph_class": "",
        "docs": "https://skyzai.org/docs/wiki/P7-nexus",
        "route": "nexus.skyzai.com",
        "surface": "B2C-1",
        "proof": "Personal API, K2 inbox, portable state, user-controlled export.",
    },
    "pay-pos": {
        "wordmark": "Pay POS",
        "glyph": ")))",
        "glyph_class": "product-glyph--wide",
        "docs": "https://skyzai.org/docs/wiki/P8-pay-pos",
        "route": "pay.skyzai.com",
        "surface": "B2C-2",
        "proof": "Payment intent, receipt, merchant settlement state, refund boundary.",
    },
    "events": {
        "wordmark": "Events",
        "glyph": "[•┊•]",
        "glyph_class": "product-glyph--wide",
        "docs": "https://skyzai.org/docs/wiki/P9-events",
        "route": "events.skyzai.com",
        "surface": "B2C-3",
        "proof": "Ticket state, organizer payout, attendee receipt, cancellation path.",
    },
    "personal-receipts": {
        "wordmark": "Personal Receipts",
        "glyph": "◇─",
        "glyph_class": "product-glyph--wide",
        "docs": "https://skyzai.org/docs/wiki/P10-personal-receipts",
        "route": "receipts.skyzai.com",
        "surface": "B2C-4",
        "proof": "Life receipt, private ledger row, export packet, deletion boundary.",
    },
    "personal-wallet": {
        "wordmark": "Personal Wallet",
        "glyph": "⬡-⬡-⬡",
        "glyph_class": "product-glyph--wide",
        "docs": "https://skyzai.org/docs/wiki/P11-personal-wallet",
        "route": "personal-wallet.skyzai.com",
        "surface": "B2C-5",
        "proof": "W1 wallet state, recovery path, signer receipt, K4 exit proof.",
    },
    "apu-advisor": {
        "wordmark": "APU Advisor",
        "glyph": "◐",
        "glyph_class": "",
        "docs": "https://skyzai.org/docs/wiki/P12-apu-advisor",
        "route": "advisor.skyzai.com",
        "surface": "B2C-6",
        "proof": "Recommendation packet, evidence tier, no-signature boundary, K2 handoff.",
    },
}

PRODUCT_SCENES = {
    "api-pay": {
        "future": "A DLT API turns one endpoint into receipt-native revenue.",
        "user": "DLT banking API CTO",
        "environment": "engineering review with the finance lead present",
        "job": "Wrap one buyer-visible endpoint with a payment gate, then turn the paid call into a receipt, journal row, and control event.",
        "proof": "OFN receipt + journal row",
        "boundary": "K2 threshold appears before any above-limit action executes.",
        "evidence": "LOCAL_PROOF",
    },
    "ofn-receipts": {
        "future": "Every API action emits a replayable proof artifact.",
        "user": "Developer integrating a regulated workflow",
        "environment": "docs console and receipt verifier side by side",
        "job": "Emit, verify, replay, and export a machine-readable receipt without changing the customer's settlement rail.",
        "proof": "receipt verifier response",
        "boundary": "Evidence tier label stays visible on every receipt state.",
        "evidence": "LOCAL_PROOF",
    },
    "kyc-kyb-hooks": {
        "future": "Regulated buyers clear access before the API call fires.",
        "user": "Compliance operator",
        "environment": "endpoint policy screen during onboarding review",
        "job": "Route buyer identity and entity checks into access policy before a paid endpoint is opened.",
        "proof": "KYB status + policy log",
        "boundary": "No custody, approval, or regulatory finality claim is shown.",
        "evidence": "SPEC",
    },
    "wallet-boundaries": {
        "future": "A DAC wallet policy is legible before funds move.",
        "user": "DAC controller",
        "environment": "formal signer review before treasury movement",
        "job": "Map W1-W5 wallet classes, signatory thresholds, recovery routes, and Grace Exit before any transfer.",
        "proof": "signer table + control receipt",
        "boundary": "K4 export path and human signature stay visible.",
        "evidence": "SPEC→PROOF",
    },
    "agentz-entitlements": {
        "future": "A bounded agent capability becomes a subscribable service.",
        "user": "Operations lead",
        "environment": "marketplace subscription flow",
        "job": "Subscribe to a caste-bounded agent capability with limits, audit trace, and human override.",
        "proof": "entitlement card + limits",
        "boundary": "Human override remains visible next to the entitlement.",
        "evidence": "SPEC",
    },
    "dex-settlement-badges": {
        "future": "Settlement evidence can be replayed without trust theater.",
        "user": "Auditor",
        "environment": "settlement replay surface",
        "job": "Replay a settlement badge against source receipt, rail, timestamp, and evidence tier.",
        "proof": "badge result + source receipt",
        "boundary": "Finality follows the visible proof state, never the static glyph.",
        "evidence": "EVIDENCE_GATED",
    },
    "marketplace": {
        "future": "API services are listed with price, proof, and refusal boundaries.",
        "user": "API service buyer",
        "environment": "procurement comparison session",
        "job": "Compare services by job-to-be-done, evidence tier, price shape, and refusal path.",
        "proof": "listing cards with evidence tiers",
        "boundary": "Terms and refusal path are visible before purchase.",
        "evidence": "SPEC",
    },
    "nexus": {
        "future": "A person sees their sovereign API surface in one app.",
        "user": "Natural person",
        "environment": "quiet K2 inbox review",
        "job": "Inspect envelopes, receipts, wallet state, and export paths before signing or refusing.",
        "proof": "envelope preview + receipt trail",
        "boundary": "Sign and refuse are equally visible decisions.",
        "evidence": "SPEC",
    },
    "pay-pos": {
        "future": "A merchant payment becomes a receipt-backed record.",
        "user": "Merchant and customer",
        "environment": "counter payment moment",
        "job": "Capture a payment, issue a receipt, and make the merchant settlement state visible.",
        "proof": "POS receipt + ledger row",
        "boundary": "No custody claim appears in the flow.",
        "evidence": "SPEC",
    },
    "events": {
        "future": "Ticketing creates organizer records without lock-in.",
        "user": "Event organizer",
        "environment": "venue entrance and back-office payout screen",
        "job": "Issue tickets, check attendees in, and export organizer records without trapping the event data.",
        "proof": "ticket receipt + attendee state",
        "boundary": "K4 export path is visible for organizer and attendee data.",
        "evidence": "SPEC",
    },
    "personal-receipts": {
        "future": "Everyday transactions become a personal audit trail.",
        "user": "Tax-conscious individual",
        "environment": "home-office monthly review",
        "job": "Collect personal receipts, inspect categories, and export a private audit packet.",
        "proof": "receipt vault + export preview",
        "boundary": "No tax advice claim; only receipt-backed organization.",
        "evidence": "SPEC",
    },
    "personal-wallet": {
        "future": "A user sees key control and exit before balance.",
        "user": "Crypto-savvy individual",
        "environment": "phone and laptop recovery setup",
        "job": "Set wallet class, recovery route, and Grace Exit before presenting any balance emphasis.",
        "proof": "W1/W2 state + recovery receipt",
        "boundary": "K4 exit path remains visible before wallet lock-in can form.",
        "evidence": "SPEC",
    },
    "apu-advisor": {
        "future": "AI recommends; the person signs or refuses.",
        "user": "Active investor",
        "environment": "desk review before an allocation decision",
        "job": "Read an APU recommendation envelope with evidence, refusal option, and signature line.",
        "proof": "recommendation envelope",
        "boundary": "Human signature line is visible; AI never signs.",
        "evidence": "SPEC→PROOF",
    },
}


def parse_markdown_table(text):
    """Parse a markdown table into list of dicts."""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if not lines:
        return []
    # Skip separator line
    if len(lines) > 1 and lines[1].startswith("|---"):
        lines = [lines[0]] + lines[2:]
    headers = [h.strip() for h in lines[0].split("|") if h.strip()]
    rows = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if cells:
            row = dict(zip(headers, cells))
            # Skip annotation rows that aren't real data
            first_key = list(row.keys())[0] if row else ""
            first_val = row.get(first_key, "")
            if first_val in ("---", "", "—"):
                continue
            if "Constitutional rationale" in first_val or "Note:" in first_val:
                continue
            if "**" in first_val and "rationale" in first_val.lower():
                continue
            rows.append(row)
    return rows


def extract_section(text, heading):
    """Extract content between ## heading and next ## or end."""
    pattern = rf"## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else ""


def parse_copy_deck(path):
    """Parse a copy deck into structured sections."""
    text = path.read_text(encoding="utf-8")
    data = {}

    # Page metadata
    meta = extract_section(text, "Page metadata")
    m = re.search(r"\*\*Title:\*\* `(.*?)`", meta)
    data["title"] = m.group(1) if m else ""
    m = re.search(r'\*\*Meta description:\*\* `(.*?)`', meta)
    data["meta_desc"] = m.group(1) if m else ""

    # Hero
    hero = extract_section(text, "Hero")
    m = re.search(r"\*\*Eyebrow:\*\* `(.*?)`", hero)
    data["eyebrow"] = m.group(1) if m else ""
    m = re.search(r"\*\*Headline:\*\* `(.*?)`", hero)
    data["headline"] = m.group(1) if m else ""
    m = re.search(r"\*\*Lead:\*\* `(.*?)`", hero)
    data["lead"] = m.group(1) if m else ""
    m = re.search(r"\*\*Primary CTA:\*\* `(.*?)` → `(.*?)`", hero)
    data["primary_cta"] = {"text": m.group(1), "href": m.group(2)} if m else None
    m = re.search(r"\*\*Secondary CTA:\*\* `(.*?)` → `(.*?)`", hero)
    data["secondary_cta"] = {"text": m.group(1), "href": m.group(2)} if m else None
    m = re.search(r"\*\*Status badge:\*\* `(.*?)`", hero)
    data["status_badge"] = m.group(1) if m else ""

    # eta=0 Boundary panel
    boundary = extract_section(text, "η = 0 Boundary panel")
    m = re.search(r"\*\*Headline:\*\* `(.*?)`", boundary)
    data["boundary_headline"] = m.group(1) if m else ""
    m = re.search(r"\*\*Body:\*\* `(.*?)`", boundary)
    data["boundary_body"] = m.group(1) if m else ""
    # Status panel table
    m = re.search(r"\*\*Status panel:\*\*\n\n(.*?)(?=\n\n---|\Z)", boundary, re.DOTALL)
    if m:
        data["status_panel"] = parse_markdown_table(m.group(1))
    else:
        data["status_panel"] = []

    # Feature grid
    features = extract_section(text, "Feature grid")
    data["features"] = parse_markdown_table(features)

    # Pricing
    pricing = extract_section(text, "Pricing")
    data["pricing"] = parse_markdown_table(pricing)
    # Pricing note
    m = re.search(r"\*\*Note:\*\* (.*?)$", pricing, re.MULTILINE)
    data["pricing_note"] = m.group(1) if m else ""
    m = re.search(r"\*\*Constitutional rationale:\*\* (.*?)$", pricing, re.MULTILINE)
    data["pricing_note"] = m.group(1) if m else data["pricing_note"]

    # eta=0 Boundary table
    boundary_table = extract_section(text, "η = 0 Boundary table")
    data["boundary_table"] = parse_markdown_table(boundary_table)

    # Matrix
    matrix = extract_section(text, "Matrix")
    data["matrix"] = parse_markdown_table(matrix)

    # CTA band
    cta = extract_section(text, "CTA band")
    m = re.search(r"\*\*Headline:\*\* `(.*?)`", cta)
    data["cta_headline"] = m.group(1) if m else ""
    m = re.search(r"\*\*Subhead:\*\* `(.*?)`", cta)
    data["cta_subhead"] = m.group(1) if m else ""
    m = re.search(r"\*\*CTA:\*\* `(.*?)` → `(.*?)`", cta)
    data["cta"] = {"text": m.group(1), "href": m.group(2)} if m else None

    # Footer cross-links
    footer = extract_section(text, "Footer cross-links")
    data["footer_links"] = re.findall(r"- `(.*?)` → `(.*?)`", footer)

    # Status from header
    m = re.search(r"\*\*Status:\*\* (.*?)$", text, re.MULTILINE)
    data["status"] = m.group(1).strip() if m else ""
    m = re.search(r"\*\*Segment:\*\* (.*?)$", text, re.MULTILINE)
    data["segment"] = m.group(1).strip() if m else ""

    return data


def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_product_glyph(meta):
    """Build the product child glyph from the brand hierarchy specs."""
    glyph = meta.get("glyph", "")
    glyph_class = meta.get("glyph_class", "")
    if glyph == "decagram":
        return """<span class="product-glyph product-glyph--decagram" aria-hidden="true">
            <svg viewBox="0 0 50 50" focusable="false">
              <polygon class="pentagram" points="25 2 31.8 16.6 47.6 18.2 35.8 28.8 39.4 44.2 25 36.2 10.6 44.2 14.2 28.8 2.4 18.2 18.2 16.6" />
              <polygon class="pentagram" transform="rotate(180 25 25)" points="25 2 31.8 16.6 47.6 18.2 35.8 28.8 39.4 44.2 25 36.2 10.6 44.2 14.2 28.8 2.4 18.2 18.2 16.6" />
            </svg>
          </span>"""
    class_attr = f" product-glyph {glyph_class}".strip()
    return f'<span class="{class_attr}" aria-hidden="true">{html_escape(glyph)}</span>'


def build_theme_boot(default_theme="light"):
    """Set the preferred theme before CSS paints."""
    return f"""  <script>
    (function () {{
      var allowed = ["light", "true-tone", "dark"];
      var fallback = "{default_theme}";
      var stored = null;
      try {{
        stored = localStorage.getItem("skyzai-theme");
      }} catch (error) {{}}
      if (stored === "cream") stored = "true-tone";
      if (allowed.indexOf(stored) === -1) stored = fallback;
      document.documentElement.setAttribute("data-theme", stored);
    }}());
  </script>"""


def build_scene_section(product_name, meta, glyph_html):
    """Build the Amazon Working Backwards scene for a product page."""
    scene = PRODUCT_SCENES.get(product_name)
    if not scene:
        return ""
    fields = [
        ("User", scene["user"]),
        ("Environment", scene["environment"]),
        ("Job", scene["job"]),
        ("Visible proof", scene["proof"]),
        ("Boundary", scene["boundary"]),
    ]
    rows = "\n".join(
        f"""              <div>
                <span>{html_escape(label)}</span>
                <strong>{html_escape(value)}</strong>
              </div>"""
        for label, value in fields
    )
    return f"""    <section class="product-scene">
      <div class="shell scene-grid">
        <div class="scene-copy">
          <span class="kicker">Working Backwards scene</span>
          <h2>{html_escape(scene["future"])}</h2>
          <p>{html_escape(scene["job"])}</p>
        </div>
        <aside class="scene-proof">
          <div class="scene-proof-head">
            <div>
              <span>{html_escape(meta.get("surface", ""))}</span>
              <strong>{html_escape(meta.get("wordmark", ""))}</strong>
            </div>
            {glyph_html}
          </div>
          <div class="scene-proof-grid">
{rows}
          </div>
          <div class="scene-evidence">
            <span>Evidence tier</span>
            <strong>{html_escape(scene["evidence"])}</strong>
          </div>
        </aside>
      </div>
    </section>"""


def build_badges(segment, status_badge):
    """Build B2B/B2C badge HTML."""
    badges = []
    seg_lower = segment.lower()
    if "b2b" in seg_lower:
        badges.append('<span class="b2b-badge">B2B</span>')
    if "b2c" in seg_lower:
        badges.append('<span class="b2c-badge">B2C</span>')
    if status_badge and status_badge not in seg_lower:
        # Add explicit badge if different from segment
        pass  # Status badge is usually redundant with segment
    return "\n            ".join(badges)


def build_pricing_card(tier, price, what, featured=False):
    """Build a pricing card from copy deck tier data."""
    featured_class = ' featured' if featured else ''
    # Clean up price for display
    price_display = price
    price_span = ""
    if "Free" in price or "free" in price:
        price_display = "Free"
        price_span = ""
    elif "TBD" in price and "per K2" not in price.lower():
        price_display = "TBD"
        price_span = ""
    elif "Terms TBD" in price:
        price_display = "Terms"
        price_span = '<span>TBD</span>'
    elif "/mo" in price and "OR" not in price and "rec" not in price:
        # Simple monthly price
        m = re.search(r"(\$[\d,]+(?:\.\d+)?)/mo", price)
        if m:
            price_display = m.group(1)
            price_span = '<span>/mo</span>'
    elif "/mo" in price:
        # Complex price with OR or per-rec — show as-is but tag /mo
        price_display = price
        price_span = ""

    # Build bullet list from "What you get"
    bullets = ""
    if what and what != "—":
        items = [i.strip() for i in what.replace("+", ";").split(";") if i.strip()]
        if not items:
            items = [what]
        bullet_lines = "\n".join(f'              <li>{html_escape(i)}</li>' for i in items)
        bullets = f"""            <ul>
{bullet_lines}
            </ul>"""

    return f"""          <div class="pricing-card{featured_class}">
            <div class="tier">{html_escape(tier)}</div>
            <div class="price">{html_escape(price_display)}{price_span}</div>
{bullets}
          </div>"""


def choose_featured_index(pricing_rows):
    """Choose which pricing tier to mark as featured."""
    # Prefer middle tier, or first non-free tier
    for i, row in enumerate(pricing_rows):
        price = row.get("Price", "")
        if "Free" not in price and "free" not in price and "TBD" not in price:
            if i > 0:
                return i
    return min(1, len(pricing_rows) - 1) if len(pricing_rows) > 1 else -1


def generate_html(data, existing_html, product_name):
    """Generate updated HTML preserving CSS from existing file."""
    # Extract style block from existing HTML
    style_match = re.search(r"(<style>.*?</style>)", existing_html, re.DOTALL)
    style_block = style_match.group(1) if style_match else ""

    # Determine relative depth
    rel_prefix = "../../"
    meta = PRODUCT_META.get(product_name, {})
    wordmark = meta.get("wordmark", data.get("title", "Product").split("|")[0].strip())
    docs_href = meta.get("docs", "https://skyzai.org")
    product_route = meta.get("route", f"{product_name}.skyzai.com")
    surface_code = meta.get("surface", "")
    proof_object = meta.get("proof", "Receipt, evidence tier, K2 boundary, and exportable audit trail.")
    glyph_html = build_product_glyph(meta)
    scene_html = build_scene_section(product_name, meta, glyph_html)
    theme_boot = build_theme_boot("light")

    # Build hero CTAs
    hero_ctas = ""
    if data["primary_cta"]:
        hero_ctas += f'            <a class="button" href="{data["primary_cta"]["href"]}">{html_escape(data["primary_cta"]["text"])}</a>\n'
    badges = build_badges(data.get("segment", ""), data.get("status_badge", ""))
    if badges:
        hero_ctas += f'            {badges}\n'

    # Secondary CTA (doc link)
    secondary_cta_html = ""
    if data["secondary_cta"]:
        secondary_cta_html = f'''          <div style="margin-top:.75rem">
            <a class="doc-link" href="{docs_href}">{html_escape(data["secondary_cta"]["text"])} →</a>
          </div>'''

    # Build feature grid
    feature_cards = []
    for i, feat in enumerate(data.get("features", [])[:6]):
        headline = feat.get("Headline", feat.get("headline", ""))
        desc = feat.get("Description", feat.get("description", ""))
        feature_cards.append(f"""          <div class="feature-card">
            <div class="feature-index">{i + 1:02d}</div>
            <h3>{html_escape(headline)}</h3>
            <p>{html_escape(desc)}</p>
          </div>""")
    feature_grid = "\n".join(feature_cards)

    # Build pricing
    pricing_cards = []
    featured_idx = choose_featured_index(data.get("pricing", []))
    for i, row in enumerate(data.get("pricing", [])):
        tier = row.get("Tier", row.get("tier", ""))
        price = row.get("Price", row.get("price", ""))
        what = row.get("What you get", row.get("what you get", ""))
        pricing_cards.append(build_pricing_card(tier, price, what, featured=(i == featured_idx)))
    pricing_grid = "\n".join(pricing_cards)

    # Build status panel
    status_panel_html = ""
    for row in data.get("status_panel", []):
        field = row.get("Field", row.get("field", list(row.keys())[0] if row else ""))
        value = row.get("Value", row.get("value", list(row.values())[0] if row else ""))
        status_panel_html += f'            <div><span>{html_escape(field)}</span><strong>{html_escape(value)}</strong></div>\n'

    # Build matrix
    matrix_html = ""
    for row in data.get("matrix", []):
        field = row.get("Field", row.get("field", list(row.keys())[0] if row else ""))
        value = row.get("Value", row.get("value", list(row.values())[0] if row else ""))
        # Strip markdown bold from field
        field = re.sub(r'\*\*(.*?)\*\*', r'\1', field)
        matrix_html += f'        <dl><dt>{html_escape(field)}</dt><dd>{html_escape(value)}</dd></dl>\n'

    # Build footer links from public routes rather than source markdown paths.
    footer_links = (
        f'<a href="{rel_prefix}">Back to skyzai.com</a> · '
        f'<a href="{docs_href}">Normative docs</a> · '
        f'<a href="{rel_prefix}marketplace.html">Marketplace</a>'
    )

    product_route_html = f"""    <section class="product-route-strip">
      <div class="shell route-mini-grid">
        <article class="route-mini">
          <span>Declarative</span>
          <strong>{html_escape(product_route)}</strong>
          <p>Commercial product page for buyers and users.</p>
        </article>
        <article class="route-mini">
          <span>Normative</span>
          <strong>skyzai.org / {html_escape(surface_code)}</strong>
          <p>Doctrine, architecture, refusals, and evidence rules.</p>
        </article>
        <article class="route-mini">
          <span>Proof object</span>
          <strong>{html_escape(proof_object.split(',')[0])}</strong>
          <p>{html_escape(proof_object)}</p>
        </article>
      </div>
    </section>"""

    proof_gates = f"""    <section class="band product-gates">
      <div class="shell">
        <div class="section-head">
          <div>
            <span class="kicker">Launch discipline</span>
            <h2>Bounded by receipts, not promises.</h2>
          </div>
          <p class="section-copy">The product page can sell the job-to-be-done. Claims about outcomes stay gated until the product emits the right proof object.</p>
        </div>
        <div class="gate-grid">
          <article class="gate-card">
            <span>η = 0</span>
            <strong>Charge for delivered value.</strong>
            <p>Setup, software, support, verification, and replay are billable. Rent without value is not.</p>
          </article>
          <article class="gate-card">
            <span>K2 / PRISM</span>
            <strong>Consequential acts require signature.</strong>
            <p>The product may stage, verify, or route envelopes. It does not replace the signer.</p>
          </article>
          <article class="gate-card">
            <span>A7</span>
            <strong>Evidence tier is visible.</strong>
            <p>Static product glyphs never imply completion, settlement, approval, or advice before evidence exists.</p>
          </article>
        </div>
      </div>
    </section>"""

    # CTA band
    cta_band = ""
    if data.get("cta"):
        cta_band = f"""    <div class="cta-band">
      <div class="shell">
        <h2>{html_escape(data.get("cta_headline", ""))}</h2>
        <p>{html_escape(data.get("cta_subhead", ""))}</p>
        <a class="button" href="{data["cta"]["href"]}">{html_escape(data["cta"]["text"])}</a>
      </div>
    </div>"""

    # Build the HTML
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light" data-theme-default="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html_escape(data["title"])}</title>
  <meta name="description" content="{html_escape(data["meta_desc"])}" />
{theme_boot}
  <link rel="manifest" href="{rel_prefix}manifest.json" />
  <link rel="icon" href="{rel_prefix}favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="{rel_prefix}marketplace.css?{ASSET_VERSION}" />
  {style_block}
</head>
<body class="product-page product-{product_name}">
  <header class="topbar">
    <div class="shell nav">
      <a class="brand product-brand" href="{rel_prefix}" aria-label="Skyzai {html_escape(wordmark)}">
        <span class="mark">⊙</span>
        <span>Skyzai <span class="product-name">{html_escape(wordmark)}</span></span>
        {glyph_html}
      </a>
      <nav class="navlinks" aria-label="Primary navigation">
        <a href="{rel_prefix}#catalog">Products</a>
        <a href="{rel_prefix}marketplace.html">Marketplace</a>
        <a href="{docs_href}">Docs</a>
        <a href="{rel_prefix}pilot-intake.html">Pilot</a>
        <button class="theme-toggle" type="button" data-theme-toggle aria-label="Cycle theme">
          <span data-theme-label>Light</span>
        </button>
      </nav>
    </div>
  </header>

  <main>
    <section class="detail-hero">
      <div class="shell detail-grid">
        <div>
          <div class="eyebrow">{html_escape(data["eyebrow"])}</div>
          <h1>{html_escape(data["headline"])}</h1>
          <p class="lead">{html_escape(data["lead"])}</p>
          <div class="dual-lane">
{hero_ctas.rstrip()}
          </div>
{secondary_cta_html}
        </div>
        <aside class="detail-panel">
          <h2>{html_escape(data.get("boundary_headline", "η = 0 Boundary"))}</h2>
          <p>{html_escape(data.get("boundary_body", ""))}</p>
          <div class="detail-meta">
{status_panel_html.rstrip()}
          </div>
        </aside>
      </div>
    </section>

{product_route_html}

{scene_html}

    <section>
      <div class="shell">
        <h2>Workflow modules</h2>
        <div class="feature-grid">
{feature_grid}
        </div>
      </div>
    </section>

    <section>
      <div class="shell">
        <h2>Pricing</h2>
        <div class="pricing-grid">
{pricing_grid}
        </div>
      </div>
    </section>

    <section>
      <div class="shell matrix">
{matrix_html.rstrip()}
      </div>
    </section>

{proof_gates}

{cta_band}
  </main>

  <footer class="footer"><div class="shell footer-row"><div>⊙ = • x ○</div><div>{footer_links}</div></div></footer>
  <script src="{rel_prefix}app.js?{ASSET_VERSION}"></script>
</body>
</html>
"""
    return html


def main():
    for deck_name, product_dir in PRODUCTS.items():
        deck_path = DECK_DIR / deck_name
        html_path = HTML_DIR / product_dir / "index.html"

        if not deck_path.exists():
            print(f"SKIP: copy deck not found: {deck_path}")
            continue
        if not html_path.exists():
            print(f"SKIP: HTML not found: {html_path}")
            continue

        data = parse_copy_deck(deck_path)
        existing_html = html_path.read_text(encoding="utf-8")
        new_html = generate_html(data, existing_html, product_dir)

        html_path.write_text(new_html, encoding="utf-8")
        print(f"UPDATED: {product_dir}/index.html ({len(new_html)} bytes)")


if __name__ == "__main__":
    main()
