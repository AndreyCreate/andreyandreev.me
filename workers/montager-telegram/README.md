# Montager Telegram waitlist

Telegram waitlist. No email compatibility or migration.
Worker: `montager-telegram`, account `e9669ca4345a34d12a68545350a704cc`.
URL: https://montager-telegram.andrey-e96.workers.dev
D1 binding `DB`: database `montager-telegram`.
Secrets: `BOT_TOKEN`, `WEBHOOK_SECRET`, injected as Cloudflare secret bindings.
Plain binding `BOT_USERNAME`: `reels_by_Andrey_bot`.
Canonical bot credential: 1Password / Hermes Agent / Telegram bot — Монтажёр.

Run focused tests: `node --test workers/montager-telegram/worker.test.mjs` (Node 22).
Upload the module with multipart metadata (main_module worker.mjs, compatibility_date 2026-09-01,
DB d1 binding, BOT_USERNAME plain_text, keep_bindings secret_text).
No paid plan activation, schedules, broadcasts, old email API changes or imports.
Webhook URL `/telegram`, Telegram secret_token must equal WEBHOOK_SECRET.
Only private `/start` creates a row; source payload is attribution, not identity.

Queue and update persistence are one D1 batch transaction. Unique Telegram identity retains
its original position. Delivery is leased per update, awaited before acknowledgment, and
marked sent only after Telegram confirms. Transport failure returns 503 for Telegram retry.
A crash after Telegram accepts but before D1 marks sent can repeat a confirmation; it
cannot create another queue position. There is no unsolicited sender or cron job.
Real-user Start and authoritative row/sent readback are the final canary, not synthetic production events.

Rollback: revert only the frontend commit to restore the previous email form. Disable this
bot webhook with drop_pending_updates=false only if explicitly approved; retain D1 data.
Never delete the queue as a rollback. Old unknown email storage is untouched, not verified/migrated.
