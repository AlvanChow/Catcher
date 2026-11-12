# Booking confirmation by text (planned, not built)

Decided 11 Nov 2026: a Calendly booking should only count once the lead replies YES to a text.
Provider: Twilio. Wire it later.

| Item | What changes | Done when |
| --- | --- | --- |
| Twilio account + number | Alvan creates the account; register A2P 10DLC for US business texting (can take 1–3 weeks) | Number can send to US mobiles |
| Confirmation text | On each new Calendly booking, text the lead "Reply YES to confirm your Catcher call on {date} at {time}" | Text arrives within a minute of booking |
| YES handling | Twilio inbound webhook → `/api/sms` marks the booking confirmed | Replying YES marks it confirmed |
| Reminder | Text again the day before if still unconfirmed | Reminder sent once |
| Auto-cancel | No YES by **2 hours before the call** → cancel the event through the Calendly API | Unconfirmed slot frees up |
| Thank-you page | Step 3 names the real texting number | Number shown matches Twilio |

Notes
- New bookings: Calendly webhooks need a paid Standard plan; polling the Calendly API works on the free plan but needs a frequent scheduler (Vercel Hobby crons run once a day).
- Needs a small datastore for booking state (e.g. Vercel KV / Upstash).
- Until this ships, bookings are final when made and no confirmation text is sent.
