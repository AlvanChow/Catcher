const test = require('node:test');
const assert = require('node:assert');
const handler = require('../api/lead.js');

function call(body, env = {}) {
  Object.assign(process.env, { RESEND_API_KEY: 'test', LEAD_TO: 'team@example.com' }, env);
  const sent = [];
  global.fetch = async (url, opts) => { sent.push({ url, body: JSON.parse(opts.body) }); return { ok: true, status: 200, text: async () => '' }; };
  return new Promise((resolve) => {
    const res = { headers: {}, setHeader(k, v) { this.headers[k] = v; }, status(c) { this.code = c; return this; }, json(j) { resolve({ code: this.code, json: j, sent }); } };
    handler({ method: 'POST', headers: { 'x-forwarded-for': `10.0.0.${Math.floor(Math.random() * 250)}` }, body }, res);
  });
}
const contact = { name: 'Jane Smith', phone: '(213) 555-0123', email: 'jane@firm.com' };

test('step 1 sends a lead email with contact details', async () => {
  const r = await call({ stage: 'contact', ...contact });
  assert.equal(r.code, 200);
  assert.match(r.json.leadId, /^[a-f0-9]{12}$/);
  assert.equal(r.sent.length, 1);
  assert.match(r.sent[0].body.subject, /New lead \(step 1\): Jane Smith/);
  assert.deepEqual(r.sent[0].body.to, ['team@example.com']);
  assert.equal(r.sent[0].body.reply_to, 'jane@firm.com');
});

test('complete sends every answer and keeps the lead id', async () => {
  const r = await call({ stage: 'complete', leadId: 'abcdefabcdef', ...contact, answering: 'Voicemail', volume: '50 to 150', attorneys: '3 to 10', notes: 'Nights' });
  assert.equal(r.json.leadId, 'abcdefabcdef');
  const t = r.sent[0].body.text;
  for (const s of ['Voicemail', '50 to 150', '3 to 10', 'Nights']) assert.ok(t.includes(s));
});

test('escapes HTML in answers', async () => {
  const r = await call({ stage: 'contact', ...contact, name: '<b>x</b>' });
  assert.ok(!r.sent[0].body.html.includes('<b>x</b>'));
});

test('rejects bad contact details and honeypot sends nothing', async () => {
  assert.equal((await call({ stage: 'contact', ...contact, email: 'nope' })).code, 400);
  const h = await call({ stage: 'contact', ...contact, company: 'bot' });
  assert.equal(h.code, 200);
  assert.equal(h.sent.length, 0);
});

test('booked sends a booked-a-call email', async () => {
  const r = await call({ stage: 'booked', leadId: 'abcdefabcdef', ...contact });
  assert.match(r.sent[0].body.subject, /^Booked a call: Jane Smith/);
});

test('website is optional and only shows in the subject when given', async () => {
  const r = await call({ stage: 'contact', ...contact });
  assert.equal(r.sent[0].body.subject, 'New lead (step 1): Jane Smith');
  const w = await call({ stage: 'contact', ...contact, website: 'firm.com' });
  assert.equal(w.sent[0].body.subject, 'New lead (step 1): Jane Smith · firm.com');
});
