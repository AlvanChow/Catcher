"""Writes the lander's secondary pages (confirmation, privacy, terms) from one shared shell.

Run from the repo root: python3 tools/build-lander-pages.py
The output is plain static HTML in apps/lander/, committed as is (no build step on Vercel).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "apps" / "lander"
ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2032%2032%27%3E%3Crect%20width%3D%2732%27%20height%3D%2732%27%20rx%3D%278%27%20fill%3D%27%230a8582%27/%3E%3Cpath%20transform%3D%27rotate(20%2016%2016)%27%20d%3D%27M10%206V26M16%206V26M22%206V26M6%2010H26M6%2016H26M6%2022H26%27%20stroke%3D%27white%27%20stroke-width%3D%272.6%27%20stroke-linecap%3D%27round%27/%3E%3C/svg%3E">'
MARK = '<svg width="{s}" height="{s}" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round"><path transform="rotate(20 16 16)" d="M10 6V26M16 6V26M22 6V26M6 10H26M6 16H26M6 22H26"/></svg>'

CSS = """
:root { --ink:#1b1f2e; --muted:#596078; --rule:#cde0e4; --paper:#fff; --ground:#f7fbfc; --teal:#0a8582; --teal-soft:#e0f7f7; --teal-ink:#076b69;
  --font:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Helvetica,Arial,sans-serif; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; position: relative; min-height: 100vh; display: flex; flex-direction: column; background: var(--ground); color: var(--ink); font: 16px/1.5 var(--font); }
main { flex: 1; }
.canopy { position: absolute; inset: 0 0 auto 0; height: 560px; z-index: -1; background: linear-gradient(105deg, #ecfbfb, #bdeff0 38%, #c3e6fb 70%, #f1f8ff); -webkit-mask-image: linear-gradient(#000 35%, transparent); mask-image: linear-gradient(#000 35%, transparent); }
.wrap { width: min(1120px, 100% - 40px); margin: 0 auto; }
nav { display: flex; justify-content: center; padding: 22px 0; }
.brand { display: inline-flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none; font-weight: 600; font-size: 18px; }
.hero { padding: 56px 0 40px; text-align: center; }
h1 { margin: 0; font-size: clamp(36px, 5.4vw, 60px); line-height: 1.04; letter-spacing: -0.035em; font-weight: 700; text-wrap: balance; }
h1 em { display: block; font-style: normal; color: var(--teal); }
.ty-hero { position: relative; }
.ty-icon { position: absolute; left: -80px; top: 10px; width: 300px; height: 275px; pointer-events: none; animation: ty-pop .7s cubic-bezier(.2,.9,.3,1.3) both; }
.ty-icon svg { width: 100%; height: 100%; }
@media (max-width: 1180px) { .ty-icon { width: 200px; height: 183px; left: 0; top: 40px; } }
@media (max-width: 960px) { .ty-icon { position: static; width: 170px; height: 156px; margin: 0 auto 10px; } }
@keyframes ty-pop { from { transform: scale(.6); opacity: 0; } to { transform: none; opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .ty-icon { animation: none; } }
#confetti { position: fixed; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 40; }
.sub-lead { margin-top: 18px !important; color: var(--ink) !important; font-size: 21px !important; font-weight: 600; }
.sub-lead + .sub { margin-top: 8px; }
.sub { margin: 20px auto 0; max-width: 44ch; color: var(--muted); font-size: 18px; }
.band { padding: 56px 0 24px; }
.steps { position: relative; width: min(600px, 100%); margin: 0 auto; padding: 0; list-style: none; display: grid; gap: 16px; }
.steps > li:not(:last-child)::after { content: ""; position: absolute; left: 17px; top: 64px; bottom: -14px; width: 2px; background: var(--rule); }
.steps > li { position: relative; display: grid; grid-template-columns: 36px 1fr; gap: 18px; align-items: start; }
.num { position: relative; z-index: 1; width: 36px; height: 36px; margin-top: 20px; border-radius: 50%; display: grid; place-items: center; background: var(--teal); color: #fff; font-weight: 700; font-size: 15px; }
.card { padding: 22px 24px; border-radius: 18px; background: var(--paper); border: 1px solid var(--rule); box-shadow: 0 10px 28px -22px rgb(10 40 50 / .45); }
.card h2 { margin: 0; font-size: 20px; font-weight: 650; letter-spacing: -0.01em; }
.card p { margin: 6px 0 0; color: var(--muted); }
.tips { margin-top: 0; }
.tips h2 { margin: 0 0 12px; font-size: 20px; }
.tips ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; }
.tips li { display: flex; gap: 12px; align-items: flex-start; }
.ck { flex: none; width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; background: #e6f6ee; color: #12805c; }
.doc { width: min(720px, 100%); margin: 0 auto; padding: 8px 0 24px; }
.doc h1 { font-size: clamp(32px, 4.4vw, 44px); text-align: left; }
.doc .upd { margin: 10px 0 28px; color: var(--muted); font-size: 14px; }
.doc h2 { margin: 32px 0 8px; font-size: 20px; letter-spacing: -0.01em; scroll-margin-top: 24px; }
.doc p, .doc li { color: #2f3546; }
.doc a { color: var(--teal-ink); }
.faq { padding: 48px 0 0; }
.faq h2 { box-sizing: border-box; width: min(600px, 100%); padding-left: 54px; margin: 0 auto 16px; font-size: 28px; letter-spacing: -0.02em; }
.faq-list { box-sizing: border-box; width: min(600px, 100%); padding-left: 54px; margin: 0 auto; display: grid; gap: 10px; }
.faq details { border-radius: 16px; background: var(--paper); border: 1px solid var(--rule); }
.faq summary { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 18px 24px; cursor: pointer; list-style: none; font-size: 17px; font-weight: 600; }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: ""; flex: none; width: 28px; height: 28px; border-radius: 50%; background: var(--teal-soft) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 6v12M6 12h12' stroke='%23076b69' stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E") center/16px no-repeat; }
.faq details[open] summary::after { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12h12' stroke='%23076b69' stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E"); }
.faq details p { margin: 0; padding: 0 24px 20px; color: var(--muted); }
.faq summary:focus-visible { outline: 3px solid rgb(10 133 130 / .45); outline-offset: 2px; border-radius: 16px; }
.ft2 { margin-top: 96px; padding: 56px 0 48px; background: #0c1d1f; color: rgb(255 255 255 / .62); text-align: center; }
.ft2-brand { display: inline-flex; align-items: center; gap: 10px; color: #fff; text-decoration: none; font-size: 22px; font-weight: 600; }
.ft2-note { margin: 22px auto 0; max-width: 64ch; font-size: 12px; line-height: 1.6; }
.ft2-links { margin-top: 18px; display: flex; flex-wrap: wrap; justify-content: center; gap: 8px 22px; }
.ft2-links a { color: rgb(255 255 255 / .78); font-size: 12px; text-decoration: none; }
.ft2-links a:hover { color: #fff; text-decoration: underline; text-underline-offset: 3px; }
.ft2-upd { margin: 18px 0 0; font-size: 12px; }
.ft2-copy { margin: 8px 0 0; font-size: 12px; font-weight: 700; color: rgb(255 255 255 / .85); }
@media (max-width: 520px) { .hero { padding: 24px 0 8px; } .band { padding-top: 28px; } .card { padding: 18px; } .steps > li { gap: 12px; } .num { margin-top: 16px; } .steps > li:not(:last-child)::after { top: 60px; } .faq h2, .faq-list { padding-left: 48px; } .faq { padding-top: 40px; } .faq h2 { font-size: 24px; } .faq summary { padding: 16px 18px; font-size: 16px; } .faq details p { padding: 0 18px 18px; } .ft2 { margin-top: 56px; padding: 40px 0 36px; } .ft2-links { gap: 0 4px; } .ft2-links a { display: inline-flex; align-items: center; min-height: 44px; padding: 0 10px; } }
"""

FOOTER = f"""<footer class="ft2">
  <div class="wrap">
    <a class="ft2-brand" href="/">{MARK.format(s=30, c="#4fd0cc")}Catcher</a>
    <p class="ft2-note">Disclaimer: Catcher is not a law firm and does not give legal advice, recommend lawyers or refer clients for a fee. Filevine, CASEpeer, Clio and Lead Docket are trademarks of their respective owners and are not affiliated with Catcher.</p>
    <nav class="ft2-links" aria-label="Legal" style="padding:0"><a href="/terms">Terms of Service</a><a href="/privacy">Privacy Policy</a><a href="/privacy#recording">Call Recording Notice</a><a href="/privacy#accessibility">Accessibility</a></nav>
    <p class="ft2-upd">Last updated: November 11, 2026</p>
    <p class="ft2-copy">© 2026 Catcher. All rights reserved.</p>
  </div>
</footer>"""


def page(title, body, robots="index,follow"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="{robots}">
<title>{title}</title>
{ICON}
<style>{CSS}</style>
</head>
<body>
<div class="canopy" aria-hidden="true"></div>
<div class="wrap"><nav aria-label="Main"><a class="brand" href="/">{MARK.format(s=26, c="#0a8582")}Catcher</a></nav></div>
<main>
{body}
</main>
{FOOTER}
</body>
</html>
"""


CHECK = '<span class="ck"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg></span>'

steps = [
    ("Step 1: Watch your phone", "We'll call or text you to set up your call."),
    ("Step 2: Check your email", "We'll send you the time and the link for your call. Check spam too."),
    ("Step 3: Say yes", "Open the invite and click Yes. Now the call is on your calendar."),
]
# Shown instead when the visitor booked a time in Calendly on the last form step.
booked_steps = [
    ("Step 1: Check your email", "We sent you the time and the link for your call. Look in your inbox. Check spam too."),
    ("Step 2: Say yes", "Open the invite and click Yes. Now the call is on your calendar."),
    ("Step 3: Reply YES to our text", "We'll text you before your call. Reply YES so we know you're coming."),
]
tips = [
    "Join 5 minutes early.",
    "Find a quiet place.",
    "Have your intake questions close by.",
    "Know which case types you take.",
]


def items(rows, kind):
    return "".join(
        f'<li data-show="{kind}"><span class="num">{n}</span><div class="card"><h2>{t}</h2><p>{d}</p></div></li>'
        for n, (t, d) in enumerate(rows, 1)
    )


step_items = items(steps, "open") + items(booked_steps, "booked")

faqs = [
    ("Will callers know they're talking to AI?",
     "That's your call. On our setup call we decide together how Catcher introduces itself and when a caller is handed to your team."),
    ("Won't it sound robotic to someone who was just in an accident?",
     "You'll hear Catcher on real practice calls before anything goes live, and you approve the script and tone. Nothing answers your phone until you're happy with it."),
    ("Does it replace our intake team?",
     "No. Catcher picks up the calls your team can't get to: nights, weekends and overflow. Your team gets the full intake and takes it from there."),
    ("What if a caller needs a real person?",
     "You set the rules. Callers who meet them go to your team; everyone else is screened and booked, so no one hits voicemail."),
    ("What if it gets a detail wrong?",
     "Every call is recorded and transcribed, so your team can check any intake against what the caller actually said."),
    ("Who decides which cases we take?",
     "You do. Catcher screens callers against the criteria you set, and your attorneys make every decision about taking a case."),
    ("Does it work with our case management software?",
     "Each intake is sent to your case management software, such as Filevine, CASEpeer, Clio or Lead Docket. Using something else? Bring it up on the call."),
    ("Is Catcher a referral or lead service?",
     "No. Catcher answers calls to your own number. We don't sell leads, refer cases or take any share of your fees."),
    ("What happens to calls you don't take?",
     "Catcher screens every caller against your case criteria. The ones that don't fit are logged with their details, so your team can see every call."),
    ("Are calls recorded?",
     "Yes. Each call is recorded and transcribed so your team gets an accurate intake. Callers are told when a call is recorded, as the law where they are requires."),
    ("What does it cost?",
     "We go over pricing on the call, once we know your call volume and what you want Catcher to handle."),
]
faq_items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
tip_items = "".join(f"<li>{CHECK}{t}</li>" for t in tips)
confirmation = f"""<section class="wrap hero ty-hero">
  <div class="ty-icon" aria-hidden="true"><svg viewBox="0 0 240 220">
<g fill="none" stroke-linecap="round" stroke-linejoin="round">
<path d="M21.3 152.4 L25.3 159.6 L29.2 166.8 L33.2 174.0 L37.2 181.2 L41.1 188.4 L45.1 195.6 M23.5 116.4 L27.5 123.6 L31.4 130.8 L35.4 138.0 L39.4 145.2 L43.3 152.4 L47.3 159.6 L51.2 166.8 L55.2 174.0 L59.2 181.2 L63.1 188.4 L67.1 195.6 M21.8 73.2 L25.7 80.4 L29.7 87.6 L33.6 94.8 L37.6 102.0 L41.6 109.2 L45.5 116.4 L49.5 123.6 L53.4 130.8 L57.4 138.0 L61.4 145.2 L65.3 152.4 L69.3 159.6 L73.2 166.8 L77.2 174.0 L81.2 181.2 L85.1 188.4 M20.0 30.0 L24.0 37.2 L27.9 44.4 L31.9 51.6 L35.8 58.8 L39.8 66.0 L43.8 73.2 L47.7 80.4 L51.7 87.6 L55.6 94.8 L59.6 102.0 L63.6 109.2 L67.5 116.4 L71.5 123.6 L75.4 130.8 L79.4 138.0 L83.4 145.2 L87.3 152.4 L91.3 159.6 L95.2 166.8 L99.2 174.0 L103.2 181.2 M46.0 37.2 L49.9 44.4 L53.9 51.6 L57.8 58.8 L61.8 66.0 L65.8 73.2 L69.7 80.4 L73.7 87.6 L77.6 94.8 L81.6 102.0 L85.6 109.2 L89.5 116.4 L93.5 123.6 L97.4 130.8 L101.4 138.0 L105.4 145.2 L109.3 152.4 L113.3 159.6 L117.2 166.8 L121.2 174.0 M38.0 37.2 L34.1 44.4 L30.1 51.6 L26.2 58.8 L22.2 66.0 M71.9 44.4 L75.9 51.6 L79.8 58.8 L83.8 66.0 L87.8 73.2 L91.7 80.4 L95.7 87.6 L99.6 94.8 L103.6 102.0 L107.6 109.2 L111.5 116.4 L115.5 123.6 L119.4 130.8 L123.4 138.0 L127.4 145.2 L131.3 152.4 L135.3 159.6 L139.2 166.8 L143.2 174.0 L147.2 181.2 L151.1 188.4 M56.1 44.4 L52.1 51.6 L48.2 58.8 L44.2 66.0 L40.2 73.2 L36.3 80.4 L32.3 87.6 L28.4 94.8 L24.4 102.0 L20.4 109.2 M97.9 51.6 L101.8 58.8 L105.8 66.0 L109.8 73.2 L113.7 80.4 L117.7 87.6 L121.6 94.8 L125.6 102.0 L129.6 109.2 L133.5 116.4 L137.5 123.6 L141.4 130.8 L145.4 138.0 L149.4 145.2 L153.3 152.4 L157.3 159.6 L161.2 166.8 L165.2 174.0 L169.2 181.2 L173.1 188.4 L177.1 195.6 M78.1 44.4 L74.1 51.6 L70.2 58.8 L66.2 66.0 L62.2 73.2 L58.3 80.4 L54.3 87.6 L50.4 94.8 L46.4 102.0 L42.4 109.2 L38.5 116.4 L34.5 123.6 L30.6 130.8 L26.6 138.0 L22.6 145.2 M119.9 51.6 L123.8 58.8 L127.8 66.0 L131.8 73.2 L135.7 80.4 L139.7 87.6 L143.6 94.8 L147.6 102.0 L151.6 109.2 L155.5 116.4 L159.5 123.6 L163.4 130.8 L167.4 138.0 L171.4 145.2 L175.3 152.4 L179.3 159.6 L183.2 166.8 L187.2 174.0 L191.2 181.2 L195.1 188.4 L199.1 195.6 M96.1 51.6 L92.2 58.8 L88.2 66.0 L84.2 73.2 L80.3 80.4 L76.3 87.6 L72.4 94.8 L68.4 102.0 L64.4 109.2 L60.5 116.4 L56.5 123.6 L52.6 130.8 L48.6 138.0 L44.6 145.2 L40.7 152.4 L36.7 159.6 L32.8 166.8 L28.8 174.0 L24.8 181.2 L20.9 188.4 M141.9 51.6 L145.8 58.8 L149.8 66.0 L153.8 73.2 L157.7 80.4 L161.7 87.6 L165.6 94.8 L169.6 102.0 L173.6 109.2 L177.5 116.4 L181.5 123.6 L185.4 130.8 L189.4 138.0 L193.4 145.2 L197.3 152.4 L201.3 159.6 L205.2 166.8 L209.2 174.0 L213.2 181.2 L217.1 188.4 M118.1 51.6 L114.2 58.8 L110.2 66.0 L106.2 73.2 L102.3 80.4 L98.3 87.6 L94.4 94.8 L90.4 102.0 L86.4 109.2 L82.5 116.4 L78.5 123.6 L74.6 130.8 L70.6 138.0 L66.6 145.2 L62.7 152.4 L58.7 159.6 L54.8 166.8 L50.8 174.0 L46.8 181.2 L42.9 188.4 L38.9 195.6 M163.9 51.6 L167.8 58.8 L171.8 66.0 L175.8 73.2 L179.7 80.4 L183.7 87.6 L187.6 94.8 L191.6 102.0 L195.6 109.2 L199.5 116.4 L203.5 123.6 L207.4 130.8 L211.4 138.0 L215.4 145.2 L219.3 152.4 M140.1 51.6 L136.2 58.8 L132.2 66.0 L128.2 73.2 L124.3 80.4 L120.3 87.6 L116.4 94.8 L112.4 102.0 L108.4 109.2 L104.5 116.4 L100.5 123.6 L96.6 130.8 L92.6 138.0 L88.6 145.2 L84.7 152.4 L80.7 159.6 L76.8 166.8 L72.8 174.0 L68.8 181.2 L64.9 188.4 L60.9 195.6 M181.9 44.4 L185.9 51.6 L189.8 58.8 L193.8 66.0 L197.8 73.2 L201.7 80.4 L205.7 87.6 L209.6 94.8 L213.6 102.0 L217.6 109.2 M166.1 44.4 L162.1 51.6 L158.2 58.8 L154.2 66.0 L150.2 73.2 L146.3 80.4 L142.3 87.6 L138.4 94.8 L134.4 102.0 L130.4 109.2 L126.5 116.4 L122.5 123.6 L118.6 130.8 L114.6 138.0 L110.6 145.2 L106.7 152.4 L102.7 159.6 L98.8 166.8 L94.8 174.0 L90.8 181.2 L86.9 188.4 M200.0 37.2 L203.9 44.4 L207.9 51.6 L211.8 58.8 L215.8 66.0 L219.8 73.2 M188.1 44.4 L184.1 51.6 L180.2 58.8 L176.2 66.0 L172.2 73.2 L168.3 80.4 L164.3 87.6 L160.4 94.8 L156.4 102.0 L152.4 109.2 L148.5 116.4 L144.5 123.6 L140.6 130.8 L136.6 138.0 L132.6 145.2 L128.7 152.4 L124.7 159.6 L120.8 166.8 L116.8 174.0 M214.0 37.2 L210.1 44.4 L206.1 51.6 L202.2 58.8 L198.2 66.0 L194.2 73.2 L190.3 80.4 L186.3 87.6 L182.4 94.8 L178.4 102.0 L174.4 109.2 L170.5 116.4 L166.5 123.6 L162.6 130.8 L158.6 138.0 L154.6 145.2 L150.7 152.4 L146.7 159.6 L142.8 166.8 L138.8 174.0 L134.8 181.2 M216.2 73.2 L212.3 80.4 L208.3 87.6 L204.4 94.8 L200.4 102.0 L196.4 109.2 L192.5 116.4 L188.5 123.6 L184.6 130.8 L180.6 138.0 L176.6 145.2 L172.7 152.4 L168.7 159.6 L164.8 166.8 L160.8 174.0 L156.8 181.2 L152.9 188.4 M218.4 109.2 L214.5 116.4 L210.5 123.6 L206.6 130.8 L202.6 138.0 L198.6 145.2 L194.7 152.4 L190.7 159.6 L186.8 166.8 L182.8 174.0 L178.8 181.2 L174.9 188.4 L170.9 195.6 M216.7 152.4 L212.7 159.6 L208.8 166.8 L204.8 174.0 L200.8 181.2 L196.9 188.4 L192.9 195.6" stroke="#4fd0cc" stroke-width="2.2"/>
<path d="M20 190.0 L25 192.3 L30 194.5 L35 196.5 L40 198.1 L45 199.2 L50 199.9 L55 200.0 L60 199.5 L65 198.5 L70 197.1 L75 195.2 L80 193.1 L85 190.8 L90 188.4 L95 186.2 L100 184.1 L105 182.4 L110 181.1 L115 180.3 L120 180.0 L125 180.3 L130 181.1 L135 182.4 L140 184.1 L145 186.2 L150 188.4 L155 190.8 L160 193.1 L165 195.2 L170 197.1 L175 198.5 L180 199.5 L185 200.0 L190 199.9 L195 199.2 L200 198.1 L205 196.5 L210 194.5 L215 192.3 L220 190.0" stroke="#0a8582" stroke-width="3"/>
<path d="M20 30.0 L25 31.4 L30 32.8 L35 34.2 L40 35.6 L45 36.9 L50 38.2 L55 39.4 L60 40.6 L65 41.7 L70 42.7 L75 43.7 L80 44.6 L85 45.3 L90 46.0 L95 46.6 L100 47.1 L105 47.5 L110 47.8 L115 47.9 L120 48.0 L125 47.9 L130 47.8 L135 47.5 L140 47.1 L145 46.6 L150 46.0 L155 45.3 L160 44.6 L165 43.7 L170 42.7 L175 41.7 L180 40.6 L185 39.4 L190 38.2 L195 36.9 L200 35.6 L205 34.2 L210 32.8 L215 31.4 L220 30.0" stroke="#0a8582" stroke-width="4.5"/>
</g>
<ellipse cx="30" cy="32.8" rx="7" ry="5.5" fill="#f5b83d"/><ellipse cx="68" cy="42.3" rx="7" ry="5.5" fill="#f5b83d"/><ellipse cx="106" cy="47.6" rx="7" ry="5.5" fill="#f5b83d"/><ellipse cx="144" cy="46.7" rx="7" ry="5.5" fill="#f5b83d"/><ellipse cx="182" cy="40.1" rx="7" ry="5.5" fill="#f5b83d"/><ellipse cx="220" cy="30.0" rx="7" ry="5.5" fill="#f5b83d"/>
</svg></div>
  <h1>Thank you<span data-name></span> <em>for choosing Catcher</em></h1>
  <p class="sub sub-lead" data-show="booked">Your call is booked, but not confirmed yet</p>
  <p class="sub sub-lead" data-show="open">We got your answers, here's what happens next</p>
  <p class="sub">Do these 3 steps to lock in your call</p>
</section>
<section class="band">
  <div class="wrap">
    <ol class="steps">{step_items}<li><span class="num" aria-hidden="true">✓</span><div class="card tips"><h2>Tips for your call</h2><ul>{tip_items}</ul></div></li></ol>
  </div>
</section>
<section class="faq" aria-labelledby="faq-title">
  <div class="wrap">
    <h2 id="faq-title">Frequently asked questions</h2>
    <div class="faq-list">{faq_items}</div>
  </div>
</section>
<canvas id="confetti" aria-hidden="true"></canvas>
<script>
(() => {{
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const c = document.getElementById('confetti'), x = c.getContext('2d'), dpr = devicePixelRatio || 1;
  const size = () => {{ c.width = innerWidth * dpr; c.height = innerHeight * dpr; }};
  size(); addEventListener('resize', size);
  const colors = ['#0a8582', '#14bfb5', '#4fd0cc', '#2f6fdb', '#f5b83d', '#12805c', '#7357d6'];
  const N = innerWidth < 600 ? 90 : 160, start = performance.now(), DUR = 6500;
  const p = Array.from({{ length: N }}, (_, i) => ({{
    x: innerWidth * (0.5 + (Math.random() - 0.5) * 0.3), y: innerHeight * 0.32,
    vx: (Math.random() - 0.5) * 8, vy: -Math.random() * 9 - 3, r: Math.random() * Math.PI,
    vr: (Math.random() - 0.5) * 0.12, w: 6 + Math.random() * 6, h: 8 + Math.random() * 8, c: colors[i % colors.length]
  }}));
  (function tick(t) {{
    const age = t - start; x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, innerWidth, innerHeight);
    x.globalAlpha = Math.max(0, 1 - Math.max(0, age - (DUR - 1500)) / 1500);
    for (const q of p) {{ q.vy = Math.min(q.vy + 0.12, 2.2); q.vx *= 0.985; q.x += q.vx; q.y += q.vy; q.r += q.vr;
      x.save(); x.translate(q.x, q.y); x.rotate(q.r); x.fillStyle = q.c; x.fillRect(-q.w / 2, -q.h / 2, q.w, q.h * Math.abs(Math.cos(q.r * 2)) + 2); x.restore(); }}
    if (age < DUR) requestAnimationFrame(tick); else c.remove();
  }})(start);
}})();
</script>
<script>
let booked = false;
try {{ booked = sessionStorage.getItem('catcher_booked') === '1'; }} catch (_) {{}}
document.querySelectorAll('[data-show]').forEach(el => {{ if (el.dataset.show !== (booked ? 'booked' : 'open')) el.remove(); }});
try {{ const n = sessionStorage.getItem('catcher_name'); const el = document.querySelector('[data-name]'); if (n && el) el.textContent = " " + n.replace(/[<>]/g, ''); }} catch (_) {{}}
</script>"""

privacy = """<article class="wrap doc">
  <h1>Privacy Policy</h1>
  <p class="upd">Last updated: November 11, 2026</p>
  <p>This policy explains what Catcher collects through this website and how we use it.</p>
  <h2>What we collect</h2>
  <p>When you fill out our form, we collect your name, phone number, email, firm website and your answers to our questions. We also record the page you came from and any campaign tags in the link (such as utm_source).</p>
  <h2>How we use it</h2>
  <p>We use it to contact you about a call with Catcher, to prepare for that call and to improve our marketing. We do not sell your information.</p>
  <h2>Calls and texts</h2>
  <p>If you agreed to it on our form, we may call or text the number you gave us about your call, including with automated messages. Msg &amp; data rates may apply. Reply STOP to opt out at any time.</p>
  <h2>Who processes it</h2>
  <p>Our website is hosted by Vercel, and form submissions are delivered to our team by email through Resend. These providers process the information only to provide their services to us.</p>
  <h2 id="recording">Call Recording Notice</h2>
  <p>Calls that Catcher answers for law firms may be recorded and transcribed so the firm receives an accurate intake. Callers are told at the start of the call when it is recorded, as the law where they are requires.</p>
  <h2 id="accessibility">Accessibility</h2>
  <p>We want this site to work for everyone, including people who use a keyboard or a screen reader. If something doesn't work for you, email us and we'll fix it.</p>
  <h2>Your choices</h2>
  <p>You can ask us to see, correct or delete the information you gave us, or to stop contacting you, by emailing <a href="mailto:hello@catchersolutions.com">hello@catchersolutions.com</a>.</p>
</article>"""

terms = """<article class="wrap doc">
  <h1>Terms of Service</h1>
  <p class="upd">Last updated: November 11, 2026</p>
  <p>These terms apply to your use of catchersolutions.com. By using the site or submitting our form, you agree to them.</p>
  <h2>What this site is</h2>
  <p>This site describes Catcher's call answering and intake service for law firms and lets you request a call with us. Submitting the form does not create a contract for services; any service is covered by a separate written agreement.</p>
  <h2>Not legal advice</h2>
  <p>Catcher is not a law firm and does not give legal advice, recommend lawyers or refer clients for a fee. Nothing on this site is legal advice.</p>
  <h2>Your information</h2>
  <p>You agree that the information you submit is accurate and that you are authorized to submit it. Our <a href="/privacy">Privacy Policy</a> explains how we use it.</p>
  <h2>Acceptable use</h2>
  <p>Don't misuse the site, including by submitting false information, attempting to disrupt it or accessing it by automated means.</p>
  <h2>No warranties</h2>
  <p>The site is provided as is. To the fullest extent the law allows, Catcher is not liable for any damages arising from your use of the site.</p>
  <h2>Changes</h2>
  <p>We may update these terms. The date above shows when they last changed.</p>
  <h2>Contact</h2>
  <p>Questions: <a href="mailto:hello@catchersolutions.com">hello@catchersolutions.com</a>.</p>
</article>"""

out = {
    "confirmation/index.html": page("Thank you · Catcher", confirmation, robots="noindex"),
    "privacy/index.html": page("Privacy Policy · Catcher", privacy),
    "terms/index.html": page("Terms of Service · Catcher", terms),
}
for rel, html in out.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    print("wrote", p.relative_to(ROOT.parent.parent))
