"""Writes the lander's secondary pages (confirmation, privacy, terms) from one shared shell.

Run from the repo root: python3 tools/build-lander-pages.py
The output is plain static HTML in apps/lander/, committed as is (no build step on Vercel).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "apps" / "lander-foundation"
ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2032%2032%27%3E%3Crect%20width%3D%2732%27%20height%3D%2732%27%20rx%3D%278%27%20fill%3D%27%23b84c22%27/%3E%3Crect%20x%3D%276%27%20y%3D%276%27%20width%3D%2720%27%20height%3D%275.5%27%20rx%3D%272.75%27%20fill%3D%27%23e3a857%27/%3E%3Crect%20x%3D%273%27%20y%3D%2713.25%27%20width%3D%2726%27%20height%3D%275.5%27%20rx%3D%272.75%27%20fill%3D%27%23ffffff%27/%3E%3Crect%20x%3D%275%27%20y%3D%2720.5%27%20width%3D%2722%27%20height%3D%275.5%27%20rx%3D%272.75%27%20fill%3D%27%23d9b48c%27/%3E%3C/svg%3E">'
MARK = '<svg width="{s}" height="{s}" viewBox="0 0 32 32" aria-hidden="true"><rect x="6" y="6" width="20" height="5.5" rx="2.75" fill="#e3a857"/><rect x="3" y="13.25" width="26" height="5.5" rx="2.75" fill="{c}"/><rect x="5" y="20.5" width="22" height="5.5" rx="2.75" fill="{c2}"/></svg>'

CSS = """
:root { --ink:#2b2420; --muted:#6f6257; --rule:#ecdcc8; --paper:#fff; --ground:#fdf8f1; --teal:#b84c22; --teal-soft:#fbe9dc; --teal-ink:#8f3a18;
  --font:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Helvetica,Arial,sans-serif; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; position: relative; min-height: 100vh; display: flex; flex-direction: column; background: var(--ground); color: var(--ink); font: 16px/1.5 var(--font); }
main { flex: 1; }
.canopy { position: absolute; inset: 0 0 auto 0; height: 560px; z-index: -1; background: linear-gradient(105deg, #fdf1e2, #f8dcc0 38%, #f6e6d6 70%, #fdf6ee); -webkit-mask-image: linear-gradient(#000 35%, transparent); mask-image: linear-gradient(#000 35%, transparent); }
.wrap { width: min(1120px, 100% - 40px); margin: 0 auto; }
nav { display: flex; justify-content: center; padding: 22px 0; }
.brand { display: inline-flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none; font-weight: 600; font-size: 18px; }
.hero { padding: 56px 0 40px; text-align: center; }
h1 { margin: 0; font-size: clamp(36px, 5.4vw, 60px); line-height: 1.04; letter-spacing: -0.035em; font-weight: 700; text-wrap: balance; }
h1 em { display: block; font-style: normal; color: #b84c22; }
.ty-hero { position: relative; }
.ty-icon { position: absolute; left: -80px; top: 10px; width: 300px; height: 275px; pointer-events: none; }
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
.card { padding: 22px 24px; border-radius: 18px; background: var(--paper); border: 1px solid var(--rule); box-shadow: 0 10px 28px -22px rgb(40 34 26 / .45); }
.card h2 { margin: 0; font-size: 20px; font-weight: 650; letter-spacing: -0.01em; }
.card p { margin: 6px 0 0; color: var(--muted); }
.tips { margin-top: 0; }
.tips h2 { margin: 0 0 12px; font-size: 20px; }
.tips ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; }
.tips li { display: flex; gap: 12px; align-items: flex-start; }
.ck { flex: none; width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; background: #fbe9dc; color: #b84c22; }
.doc { width: min(720px, 100%); margin: 0 auto; padding: 8px 0 24px; }
.doc h1 { font-size: clamp(32px, 4.4vw, 44px); text-align: left; }
.doc .upd { margin: 10px 0 28px; color: var(--muted); font-size: 14px; }
.doc h2 { margin: 32px 0 8px; font-size: 20px; letter-spacing: -0.01em; scroll-margin-top: 24px; }
.doc p, .doc li { color: #3a302a; }
.doc a { color: var(--teal-ink); }
.faq { padding: 48px 0 0; }
.faq h2 { box-sizing: border-box; width: min(600px, 100%); padding-left: 54px; margin: 0 auto 16px; font-size: 28px; letter-spacing: -0.02em; }
.faq-list { box-sizing: border-box; width: min(600px, 100%); padding-left: 54px; margin: 0 auto; display: grid; gap: 10px; }
.faq details { border-radius: 16px; background: var(--paper); border: 1px solid var(--rule); }
.faq summary { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 18px 24px; cursor: pointer; list-style: none; font-size: 17px; font-weight: 600; }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: ""; flex: none; width: 28px; height: 28px; border-radius: 50%; background: var(--teal-soft) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 6v12M6 12h12' stroke='%23b84c22' stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E") center/16px no-repeat; }
.faq details[open] summary::after { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12h12' stroke='%23b84c22' stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E"); }
.faq details p { margin: 0; padding: 0 24px 20px; color: var(--muted); }
.faq summary:focus-visible { outline: 3px solid rgb(184 76 34 / .45); outline-offset: 2px; border-radius: 16px; }
.ft2 { margin-top: 96px; padding: 56px 0 48px; background: #2a211c; color: rgb(255 255 255 / .62); text-align: center; }
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
    <a class="ft2-brand" href="/">{MARK.format(s=30, c="#fbe9dc", c2="#d9b48c")}Sandrock</a>
    <p class="ft2-note">Disclaimer: Sandrock does not guarantee search rankings or a number of leads. Results depend on your local market and competition. Sandrock does not inspect homes or give engineering advice or quote prices.</p>
    <nav class="ft2-links" aria-label="Legal" style="padding:0"><a href="/terms">Terms of Service</a><a href="/privacy">Privacy Policy</a><a href="/privacy#recording">Call Recording Notice</a><a href="/privacy#accessibility">Accessibility</a></nav>
    <p class="ft2-upd">Last updated: 11 November 2026</p>
    <p class="ft2-copy">© 2026 Sandrock. All rights reserved.</p>
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
<div class="wrap"><nav aria-label="Main"><a class="brand" href="/">{MARK.format(s=26, c="#b84c22", c2="#5a3a28")}Sandrock</a></nav></div>
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
    "Know which jobs you want more of.",
    "Have your service area and lead sources close by.",
]


def items(rows, kind):
    return "".join(
        f'<li data-show="{kind}"><span class="num">{n}</span><div class="card"><h2>{t}</h2><p>{d}</p></div></li>'
        for n, (t, d) in enumerate(rows, 1)
    )


step_items = items(steps, "open") + items(booked_steps, "booked")

faqs = [
    ("What do I get in the free lead audit?",
     "We look up how many homeowners search for foundation work in your service area and show you which companies are getting those leads today. It is yours to keep whether you work with us or not."),
    ("How do I get the $100?",
     "Show up to your 15-minute audit call and we send you $100 for your time. One payment per company. We confirm how you want to be paid on the call."),
    ("Are the leads shared with other contractors?",
     "No. Leads come from your own website and Google Business Profile and phone number so they go to you and no one else."),
    ("Do you guarantee rankings or a number of leads?",
     "No and you should be wary of anyone who does. Results depend on your market and competition. We show you exactly what moved every month."),
    ("How long until we see leads?",
     "SEO builds over months not days. On the call we look at your market and your current site and tell you honestly what to expect."),
    ("What makes a lead qualified?",
     "You decide. We screen for the job types you want and addresses inside your service area so you only drive out to real jobs."),
    ("We already pay for Angi or HomeAdvisor. Do we stop?",
     "Not on day one. Most contractors keep them running while their own leads grow and cut back once the numbers show it is safe."),
    ("Do you work with new-construction foundation crews?",
     "Yes. For builders and GCs we focus on the searches and pages that bring in bid requests alongside homeowner repair work if you do both."),
    ("Does it work with our CRM?",
     "Each lead is sent to your team and we can send it into the CRM you already use like Jobber or ServiceTitan or Housecall Pro. Using something else? Bring it up on the call."),
    ("What does it cost?",
     "We go over pricing on the call once we know your market and how many leads you want."),
]
faq_items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
tip_items = "".join(f"<li>{CHECK}{t}</li>" for t in tips)
confirmation = f"""<section class="wrap hero ty-hero">
  <div class="ty-icon" aria-hidden="true"><svg viewBox="0 0 240 220">
  <!-- ground strata -->
  <path d="M8 128 Q120 118 232 128 L232 150 Q120 142 8 150 Z" fill="#c9a46a"/>
  <path d="M8 150 Q120 142 232 150 L232 172 Q120 166 8 172 Z" fill="#b38a52"/>
  <path d="M8 172 Q120 166 232 172 L232 196 Q120 192 8 196 Z" fill="#9c7a4a"/>
  <g fill="#e9dcc3" opacity=".7"><circle cx="40" cy="160" r="3"/><circle cx="182" cy="183" r="3.5"/><circle cx="96" cy="185" r="2.5"/><circle cx="150" cy="140" r="2.5"/><circle cx="210" cy="160" r="2.5"/></g>
  <!-- piers -->
  <g fill="#6f6257"><rect x="70" y="122" width="9" height="66" rx="3"/><rect x="116" y="122" width="9" height="70" rx="3"/><rect x="162" y="122" width="9" height="66" rx="3"/></g>
  <g fill="#8a7d72"><rect x="66" y="184" width="17" height="7" rx="3"/><rect x="112" y="188" width="17" height="7" rx="3"/><rect x="158" y="184" width="17" height="7" rx="3"/></g>
  <!-- slab -->
  <rect x="50" y="112" width="140" height="16" rx="5" fill="#5a3a28"/>
  <!-- house -->
  <rect x="62" y="64" width="116" height="50" rx="6" fill="#f6f1e8" stroke="#5a3a28" stroke-width="4"/>
  <path d="M52 70 L120 24 L188 70" fill="none" stroke="#5a3a28" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M60 66 L120 30 L180 66 Z" fill="#c8572a"/>
  <rect x="108" y="82" width="24" height="32" rx="4" fill="#5a3a28"/>
  <circle cx="126" cy="99" r="2" fill="#c8572a"/>
  <rect x="76" y="78" width="20" height="18" rx="3" fill="#f9e4c7" stroke="#5a3a28" stroke-width="3"/>
  <rect x="144" y="78" width="20" height="18" rx="3" fill="#f9e4c7" stroke="#5a3a28" stroke-width="3"/>
  <!-- sparkles -->
  <g fill="#c8572a"><path d="M30 40 q0 9 9 9 q-9 0 -9 9 q0 -9 -9 -9 q9 0 9 -9z"/><path d="M212 30 q0 6 6 6 q-6 0 -6 6 q0 -6 -6 -6 q6 0 6 -6z"/></g>
</svg></div>
  <h1 data-show="booked">Your call is booked <em>but not confirmed yet</em></h1>
  <h1 data-show="open">We got your answers <em>here's what happens next</em></h1>
  <p class="sub sub-lead">Thank you<span data-name></span> for choosing Sandrock</p>
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
  const colors = ['#b84c22', '#c45a28', '#e3a857', '#c9a46a', '#b4541f', '#d9944a', '#e8d3a8'];
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
try {{ booked = sessionStorage.getItem('sandrock_booked') === '1'; }} catch (_) {{}}
document.querySelectorAll('[data-show]').forEach(el => {{ if (el.dataset.show !== (booked ? 'booked' : 'open')) el.remove(); }});
try {{ const n = sessionStorage.getItem('sandrock_name'); const el = document.querySelector('[data-name]'); if (n && el) el.textContent = " " + n.replace(/[<>]/g, ''); }} catch (_) {{}}
</script>"""

privacy = """<article class="wrap doc">
  <h1>Privacy Policy</h1>
  <p class="upd">Last updated: 11 November 2026</p>
  <p>This policy explains what Sandrock collects through this website and how we use it.</p>
  <h2>What we collect</h2>
  <p>When you fill out our form, we collect your name, phone number, email and your answers to our questions. We also record the page you came from and any campaign tags in the link (such as utm_source).</p>
  <h2>How we use it</h2>
  <p>We use it to contact you about a call with Sandrock, to prepare for that call and to improve our marketing. We do not sell your information.</p>
  <h2>Calls and texts</h2>
  <p>If you agreed to it on our form, we may call or text the number you gave us about your call, including with automated messages. Msg &amp; data rates may apply. Reply STOP to opt out at any time.</p>
  <h2>Who processes it</h2>
  <p>Our website is hosted by Vercel, and form submissions are delivered to our team by email through Resend. These providers process the information only to provide their services to us.</p>
  <h2 id="recording">Call Recording Notice</h2>
  <p>Calls that Sandrock screens for contractors may be recorded and transcribed so the contractor receives accurate job details. Callers are told at the start of the call when it is recorded, as the law where they are requires.</p>
  <h2 id="accessibility">Accessibility</h2>
  <p>We want this site to work for everyone, including people who use a keyboard or a screen reader. If something doesn't work for you, email us and we'll fix it.</p>
  <h2>Your choices</h2>
  <p>You can ask us to see, correct or delete the information you gave us, or to stop contacting you, by replying to any email we have sent you.</p>
</article>"""

terms = """<article class="wrap doc">
  <h1>Terms of Service</h1>
  <p class="upd">Last updated: 11 November 2026</p>
  <p>These terms apply to your use of this website. By using the site or submitting our form, you agree to them.</p>
  <h2>What this site is</h2>
  <p>This site describes Sandrock's lead generation and booking service for foundation contractors and lets you request a call with us. Submitting the form does not create a contract for services; any service is covered by a separate written agreement.</p>
  <h2>Not engineering advice</h2>
  <p>Sandrock does not inspect homes, give engineering advice or quote prices, and does not guarantee search rankings or a number of leads. Nothing on this site is engineering advice.</p>
  <h2>Your information</h2>
  <p>You agree that the information you submit is accurate and that you are authorized to submit it. Our <a href="/privacy">Privacy Policy</a> explains how we use it.</p>
  <h2>Acceptable use</h2>
  <p>Don't misuse the site, including by submitting false information, attempting to disrupt it or accessing it by automated means.</p>
  <h2>No warranties</h2>
  <p>The site is provided as is. To the fullest extent the law allows, Sandrock is not liable for any damages arising from your use of the site.</p>
  <h2>Changes</h2>
  <p>We may update these terms. The date above shows when they last changed.</p>
  <h2>Contact</h2>
  <p>Questions? Reply to any email we have sent you.</p>
</article>"""

out = {
    "confirmation/index.html": page("Thank you · Sandrock", confirmation, robots="noindex"),
    "privacy/index.html": page("Privacy Policy · Sandrock", privacy),
    "terms/index.html": page("Terms of Service · Sandrock", terms),
}
for rel, html in out.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    print("wrote", p.relative_to(ROOT.parent.parent))
