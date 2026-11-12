"""One-time reskin of apps/lander-foundation (and its page generator) from Catcher teal to Sandrock.

Sandrock palette: rock slate for the brand, sand gold for accents, warm stone neutrals.
"""
import re, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [ROOT / "apps/lander-foundation/index.html", ROOT / "tools/build-foundation-pages.py",
         ROOT / "apps/lander-foundation/api/lead.js"]

HEX = {
    "#0a8582": "#2f4858", "#076b69": "#22363f", "#087572": "#263c48", "#14bfb5": "#4a6878",
    "#4fd0cc": "#d9a441", "#e0f7f7": "#e8edf0", "#e3f4f3": "#e8edf0", "#f3fbfb": "#f3f6f7",
    "#1b1f2e": "#1f2a30", "#596078": "#5d6670", "#cde0e4": "#ddd3c4", "#f7fbfc": "#fbf8f3",
    "#f6fafb": "#faf7f1", "#e6eef0": "#eee7dc", "#2f3546": "#333b41",
    "#ecfbfb": "#f8f1e4", "#bdeff0": "#efdcc0", "#c3e6fb": "#e4e2da", "#f1f8ff": "#f6f3ee",
    "#0c1d1f": "#1d2327", "#12805c": "#3f7a4a", "#e6f6ee": "#e8f1e6",
    "#2f6fdb": "#a4562f", "#e8f0fd": "#f6e7dc", "#7357d6": "#6b6458", "#efebfc": "#eeebe5",
    "#c2417f": "#b4541f", "#fbe9f2": "#f8e6da", "#f5b83d": "#d9a441",
}
RGB = {
    "rgb(10 133 130": "rgb(47 72 88", "rgb(20 191 181": "rgb(74 104 120", "rgb(10 40 50": "rgb(40 34 26",
    "rgb(12 29 31": "rgb(26 22 18", "rgb(205 224 228": "rgb(221 211 196", "rgb(18 184 134": "rgb(63 122 74",
}

def mark(top, mid, low):
    return (f'<rect x="6" y="6" width="20" height="5.5" rx="2.75" fill="{top}"/>'
            f'<rect x="3" y="13.25" width="26" height="5.5" rx="2.75" fill="{mid}"/>'
            f'<rect x="5" y="20.5" width="22" height="5.5" rx="2.75" fill="{low}"/>')

def run():
    for f in FILES:
        s = f.read_text()
        for a, b in HEX.items():
            s = re.sub(re.escape(a), b, s, flags=re.I)
        for a, b in RGB.items():
            s = s.replace(a, b)
        s = s.replace("Catcher", "Sandrock").replace("catcher_name", "sandrock_name").replace("catcher_booked", "sandrock_booked")
        f.write_text(s)

    # Logos: the tilted mesh becomes three stacked strata.
    idx = FILES[0]; s = idx.read_text()
    s = re.sub(r'<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="#2f4858"[^>]*>\s*<path transform="rotate\(20 16 16\)"[^/]*/>\s*</svg>',
               f'<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true">{mark("#d9a441", "#2f4858", "#4a6878")}</svg>', s)
    s = re.sub(r'<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="#d9a441"[^>]*>\s*<path transform="rotate\(20 16 16\)"[^/]*/>\s*</svg>',
               f'<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true">{mark("#d9a441", "#e8edf0", "#9fb0ba")}</svg>', s)
    fav = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='#2f4858'/>{mark('#d9a441', '#ffffff', '#9fb0ba').replace(chr(34), chr(39))}</svg>"
    s = re.sub(r'<link rel="icon" href="[^"]*">', '<link rel="icon" href="data:image/svg+xml,' + urllib.parse.quote(fav) + '">', s, count=1)
    s = s.replace("h1 em { font-style: normal; color: var(--teal); }", "h1 em { font-style: normal; color: #9a6a17; }")
    idx.write_text(s)
    print("rotate left in index:", s.count("rotate(20 16 16)"))

if __name__ == "__main__":
    run()
