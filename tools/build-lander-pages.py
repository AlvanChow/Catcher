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
.sub { margin: 20px auto 0; max-width: 44ch; color: var(--muted); font-size: 18px; }
.band { padding: 56px 0 24px; }
.steps { position: relative; width: min(600px, 100%); margin: 0 auto; padding: 0; list-style: none; display: grid; gap: 16px; }
.steps li:not(:last-child)::after { content: ""; position: absolute; left: 17px; top: 60px; bottom: -22px; width: 2px; background: var(--rule); }
.steps li { position: relative; display: grid; grid-template-columns: 36px 1fr; gap: 18px; align-items: start; }
.num { position: relative; z-index: 1; width: 36px; height: 36px; margin-top: 18px; border-radius: 50%; display: grid; place-items: center; background: var(--teal); color: #fff; font-weight: 700; font-size: 15px; box-shadow: 0 0 0 6px var(--ground); }
.card { padding: 22px 24px; border-radius: 18px; background: var(--paper); border: 1px solid var(--rule); box-shadow: 0 10px 28px -22px rgb(10 40 50 / .45); }
.card h2 { margin: 0; font-size: 20px; font-weight: 650; letter-spacing: -0.01em; }
.card p { margin: 6px 0 0; color: var(--muted); }
.tips { margin-top: 0; }
.tips h2 { margin: 0 0 12px; font-size: 20px; }
.tips ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; }
.tips li { display: flex; gap: 12px; align-items: center; }
.ck { flex: none; width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; background: #e6f6ee; color: #12805c; }
.doc { width: min(720px, 100%); margin: 0 auto; padding: 8px 0 24px; }
.doc h1 { font-size: clamp(32px, 4.4vw, 44px); text-align: left; }
.doc .upd { margin: 10px 0 28px; color: var(--muted); font-size: 14px; }
.doc h2 { margin: 32px 0 8px; font-size: 20px; letter-spacing: -0.01em; scroll-margin-top: 24px; }
.doc p, .doc li { color: #2f3546; }
.doc a { color: var(--teal-ink); }
.ft2 { margin-top: 96px; padding: 56px 0 48px; background: #0c1d1f; color: rgb(255 255 255 / .62); text-align: center; }
.ft2-brand { display: inline-flex; align-items: center; gap: 10px; color: #fff; text-decoration: none; font-size: 22px; font-weight: 600; }
.ft2-note { margin: 22px auto 0; max-width: 64ch; font-size: 12px; line-height: 1.6; }
.ft2-links { margin-top: 18px; display: flex; flex-wrap: wrap; justify-content: center; gap: 8px 22px; }
.ft2-links a { color: rgb(255 255 255 / .78); font-size: 12px; text-decoration: none; }
.ft2-links a:hover { color: #fff; text-decoration: underline; text-underline-offset: 3px; }
.ft2-upd { margin: 18px 0 0; font-size: 12px; }
.ft2-copy { margin: 8px 0 0; font-size: 12px; font-weight: 700; color: rgb(255 255 255 / .85); }
@media (max-width: 520px) { .hero { padding-top: 32px; } .card { padding: 18px; } .steps li { gap: 12px; } }
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
    ("Step 1: Watch your phone", "We'll call or text you from Catcher to pick a time for your call."),
    ("Step 2: Check your email", "We'll send the time and the link for your call. Check spam too."),
    ("Step 3: Say yes", "Open the invite and click Yes. Now the call is on your calendar."),
]
# Shown instead when the visitor booked a time in Calendly on the last form step.
booked_steps = [
    ("Step 1: Check your email", "We sent you the time and the link for your call. Look in your inbox. Check spam too."),
    ("Step 2: Say yes", "Open the invite and click Yes. Now the call is on your calendar."),
    ("Step 3: Reply YES to our text", "We'll text you before the call. Reply YES so we know you're coming."),
]
tips = [
    "Join 5 minutes early.",
    "Bring whoever runs intake at your firm.",
    "Have your current intake questions close by.",
    "Know which case types you take, and where.",
]
def items(rows, kind):
    return "".join(
        f'<li data-show="{kind}"><span class="num">{n}</span><div class="card"><h2>{t}</h2><p>{d}</p></div></li>'
        for n, (t, d) in enumerate(rows, 1)
    )


step_items = items(steps, "open") + items(booked_steps, "booked")
tip_items = "".join(f"<li>{CHECK}{t}</li>" for t in tips)
confirmation = f"""<section class="wrap hero">
  <h1 data-show="open"><span data-name>You're in,</span> <em>here's what happens next</em></h1>
  <h1 data-show="booked">Your call is booked, <em>but not confirmed yet</em></h1>
  <p class="sub">Do these 3 things to lock in your call</p>
</section>
<section class="band">
  <div class="wrap">
    <ol class="steps">{step_items}<li><span class="num" aria-hidden="true">✓</span><div class="card tips"><h2>Tips for your call</h2><ul>{tip_items}</ul></div></li></ol>
  </div>
</section>
<script>
let booked = false;
try {{ booked = sessionStorage.getItem('catcher_booked') === '1'; }} catch (_) {{}}
document.querySelectorAll('[data-show]').forEach(el => {{ if (el.dataset.show !== (booked ? 'booked' : 'open')) el.remove(); }});
try {{ const n = sessionStorage.getItem('catcher_name'); const el = document.querySelector('[data-name]'); if (n && el) el.textContent = "You're in, " + n.replace(/[<>]/g, '') + ","; }} catch (_) {{}}
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
    "confirmation/index.html": page("You're in · Catcher", confirmation, robots="noindex"),
    "privacy/index.html": page("Privacy Policy · Catcher", privacy),
    "terms/index.html": page("Terms of Service · Catcher", terms),
}
for rel, html in out.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    print("wrote", p.relative_to(ROOT.parent.parent))
