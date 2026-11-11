// POST /api/lead: receives the apply form and emails it to the team through Resend.
//
// The form posts up to three times: stage "contact" after step 1 (so a lead who drops off is not lost)
// stage "complete" with every answer, and stage "booked" once they pick a time in Calendly. Both carry the same leadId so the two emails pair up.
//
// Environment (set in Vercel, never committed):
//   RESEND_API_KEY  Resend API key
//   LEAD_TO         where leads go; comma-separated for several addresses
//   LEAD_FROM       sender, e.g. "Catcher Leads <leads@catchersolutions.com>" once that domain
//                   is verified in Resend; defaults to Resend's test sender
const crypto = require('node:crypto');

const LIMIT = 20; // requests per IP per hour, per function instance
const hits = new Map();

const clean = (v, max = 500) => (typeof v === 'string' ? v.trim().slice(0, max) : '');
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

function limited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < 3600e3);
  recent.push(now);
  hits.set(ip, recent);
  return recent.length > LIMIT;
}

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') return JSON.parse(req.body || '{}');
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (limited(ip)) return res.status(429).json({ error: 'Too many attempts' });

  let b;
  try {
    b = await readBody(req);
  } catch {
    return res.status(400).json({ error: 'Bad JSON' });
  }

  const stage = ['complete', 'booked'].includes(b.stage) ? b.stage : 'contact';
  const leadId = /^[a-f0-9]{12}$/.test(b.leadId || '') ? b.leadId : crypto.randomBytes(6).toString('hex');

  // Honeypot: bots fill the hidden "company" field. Pretend success, send nothing.
  if (clean(b.company)) return res.status(200).json({ ok: true, leadId });

  const lead = {
    name: clean(b.name, 120),
    phone: clean(b.phone, 40),
    email: clean(b.email, 200),
    website: clean(b.website, 200),
    answering: clean(b.answering, 80),
    volume: clean(b.volume, 80),
    attorneys: clean(b.attorneys, 80),
    notes: clean(b.notes, 2000),
  };
  const digits = lead.phone.replace(/\D/g, '');
  if (!lead.name || digits.length < 10 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(lead.email) || !lead.website) {
    return res.status(400).json({ error: 'Missing or invalid contact details' });
  }

  const key = process.env.RESEND_API_KEY;
  const to = (process.env.LEAD_TO || '').split(',').map((s) => s.trim()).filter(Boolean);
  const from = process.env.LEAD_FROM || 'Catcher Leads <onboarding@resend.dev>';
  if (!key || !to.length) {
    console.error('lead: RESEND_API_KEY or LEAD_TO is not set');
    return res.status(500).json({ error: 'Not configured' });
  }

  const utm = b.utm && typeof b.utm === 'object' ? b.utm : {};
  const rows = [
    ['Name', lead.name],
    ['Phone', lead.phone],
    ['Email', lead.email],
    ['Firm website', lead.website],
    ['Who answers when the team can’t', lead.answering],
    ['New injury calls a month', lead.volume],
    ['Attorneys', lead.attorneys],
    ['Handle first', lead.notes],
    ['Page', clean(b.page, 200)],
    ['Referrer', clean(b.referrer, 300)],
    ...Object.entries(utm).slice(0, 10).map(([k, v]) => [clean(k, 40), clean(v, 200)]),
    ['Lead ID', leadId],
    ['Received', new Date().toISOString()],
  ].filter(([, v]) => v);

  const title = { contact: 'New lead (step 1)', complete: 'Finished the form', booked: 'Booked a call' }[stage];
  const subject = `${title}: ${lead.name} · ${lead.website}`;
  const html = `<div style="font-family:-apple-system,Helvetica,Arial,sans-serif;color:#1b1f2e">
<h2 style="margin:0 0 4px;font-size:20px">${esc(title)}</h2>
<p style="margin:0 0 16px;color:#596078">${{ contact: 'They gave their contact details. Answers follow if they finish the form.', complete: 'Every answer is below. Next they pick a time.', booked: 'They booked a call in Calendly. The time is in the Calendly invite.' }[stage]}</p>
<table cellpadding="8" style="border-collapse:collapse;font-size:14px">${rows
    .map(([k, v]) => `<tr><td style="border-top:1px solid #cde0e4;color:#596078;white-space:nowrap;vertical-align:top">${esc(k)}</td><td style="border-top:1px solid #cde0e4">${esc(v)}</td></tr>`)
    .join('')}</table></div>`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n');

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', 'Idempotency-Key': `${leadId}-${stage}-${crypto.createHash('sha1').update(text).digest('hex').slice(0, 12)}` },
    body: JSON.stringify({ from, to, subject, html, text, reply_to: lead.email }),
  });
  if (!r.ok) {
    console.error('lead: resend failed', r.status, await r.text().catch(() => ''));
    return res.status(502).json({ error: 'Could not send' });
  }
  return res.status(200).json({ ok: true, leadId });
};
