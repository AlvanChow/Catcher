"""Second Sandrock reskin (owner, 12 Nov 2026: slate looked cold): terracotta clay brand, sand accents, warm neutrals."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "apps/lander-foundation/index.html"
GEN = ROOT / "tools/build-foundation-pages.py"
LEAD = ROOT / "apps/lander-foundation/api/lead.js"

CLAY, CLAY_INK, CLAY_DEEP, CLAY_SOFT = "#b84c22", "#8f3a18", "#a8441b", "#fbe9dc"
SAND, BROWN = "#e3a857", "#5a3a28"

MAP = {
    "#2f4858": CLAY, "#22363f": CLAY_INK, "#263c48": CLAY_DEEP, "#536576": "#c45a28", "#3b5566": "#bf5426",
    "#e8edf0": CLAY_SOFT, "#f3f6f7": "#fdf3ec", "#9fb0ba": "#d9b48c",
    "#1f2a30": "#2b2420", "#5d6670": "#6f6257", "#ddd3c4": "#ecdcc8", "#fbf8f3": "#fdf8f1",
    "#faf7f1": "#fcf6ee", "#eee7dc": "#f3e6d6", "#333b41": "#3a302a", "#1d2327": "#2a211c",
    "#9a6a17": CLAY, "#d9a441": SAND, "#c99a3e": "#d9944a", "#e8c47a": "#ffe2b8",
    "#f8f1e4": "#fdf1e2", "#efdcc0": "#f8dcc0", "#e4e2da": "#f6e6d6", "#f6f3ee": "#fdf6ee",
    "#f3ead9": "#fbe9dc", "#f7f2e9": "#fdf3ec", "#cfdde4": "#f9e4c7", "#7b858d": "#8a7d72",
}
RGB = {
    "rgb(47 72 88": "rgb(184 76 34", "rgb(34 54 63": "rgb(143 58 24", "rgb(217 164 65": "rgb(227 168 87",
    "rgb(221 211 196": "rgb(236 220 200", "rgb(74 104 120": "rgb(196 90 40",
}

def remap(s):
    # Encoded SVG colours first (%23xxxxxx), then plain hex.
    for a, b in MAP.items():
        s = re.sub(re.escape("%23" + a[1:]), "%23" + b[1:], s, flags=re.I)
        s = re.sub(re.escape(a) + r"\b", b, s, flags=re.I)
    for a, b in RGB.items():
        s = s.replace(a, b)
    return s

def logo(s, top, mid, low):
    return re.sub(r'(<rect x="6" y="6"[^>]*fill=")[^"]*("/><rect x="3" y="13.25"[^>]*fill=")[^"]*("/><rect x="5" y="20.5"[^>]*fill=")[^"]*(")',
                  lambda m: f'{m.group(1)}{top}{m.group(2)}{mid}{m.group(3)}{low}{m.group(4)}', s)

def run():
    # House graphic keeps concrete and brown for structure, clay only on the roof.
    g = GEN.read_text()
    a = g.index('<div class="ty-icon"'); b = g.index("</svg></div>", a)
    house = g[a:b].replace("#2f4858", BROWN).replace("#d9a441", "#c8572a")
    g = g[:a] + house + g[b:]
    GEN.write_text(remap(g))

    s = remap(IDX.read_text())
    s = s.replace("u.searchParams.set('primary_color', '0a8582');", "u.searchParams.set('primary_color', 'b84c22');")
    # One coordinated tone for the What you get icons.
    s = re.sub(r"\.wg li:nth-child\(\d\) \{ --c: [^;]*; --c-bg: [^;]*; \}", "", s)
    s = s.replace("</head>", f"<style>.wg li {{ --c: {CLAY}; --c-bg: {CLAY_SOFT}; }} .wg-ic {{ border-color: rgb(184 76 34 / .22) !important; }}</style>\n</head>", 1)
    IDX.write_text(s)
    LEAD.write_text(remap(LEAD.read_text()))

if __name__ == "__main__":
    run()
