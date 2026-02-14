Good. Internal tool + single operator + potentially 24/7 runtime changes the design slightly.

Now we’re not building a toy script.

We’re building a **stable long-running service** .

You need:

- Stability
- Crash recovery
- Job queueing
- Logging
- Controlled automation execution
- Resource monitoring

Let’s design this properly.

---

# 🎯 Final Recommended Stack (24/7 Single Operator Internal Tool)

## 🧱 Core Stack

| Layer                | Technology                         | Why                                   |
| -------------------- | ---------------------------------- | ------------------------------------- |
| Backend              | FastAPI                            | Lightweight, async, production ready  |
| Automation           | Playwright (Python)                | Stable browser automation             |
| Database             | PostgreSQL                         | Better for long-running + concurrency |
| Queue                | RQ (Redis Queue)                   | Clean background job handling         |
| Cache / Queue Broker | Redis                              | Required for RQ                       |
| Web UI               | FastAPI Templates OR Minimal React | Depends on UI complexity              |
| Deployment           | Docker + systemd or Docker Compose | Stable 24/7 execution                 |

---

# ⚠️ Why NOT SQLite for 24/7?

SQLite is fine for light tools.

But for:

- Continuous writes
- Status updates
- Logging
- Parallel jobs
- Crash recovery

PostgreSQL is much safer.

You don’t want DB locking issues after 10 hours of runtime.

---

# 🧠 Architecture for 24/7 Stability

<pre class="overflow-visible! px-0!" data-start="1244" data-end="1393"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="1244" data-end="1393"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>User (You)
   ↓
Web Dashboard (FastAPI)
   ↓
API Layer
   ↓
Redis Queue
   ↓
Automation Worker (Playwright)
   ↓
PostgreSQL
   ↓
File Storage
</span></span></code></div></div></pre>

---

# 🔄 Execution Model (Very Important)

Never run automation inside API request thread.

Instead:

1. API receives request
2. Job stored in DB
3. Job ID pushed to Redis queue
4. Worker picks job
5. Worker runs Playwright
6. Worker updates DB
7. UI polls status

This prevents:

- Server freeze
- Timeout errors
- Broken sessions
- Memory leaks crashing entire app

---

# 📦 Deployment Design

## Recommended Setup

- VPS (4GB RAM minimum if 24/7 browser)
- Docker Compose:

<pre class="overflow-visible! px-0!" data-start="1874" data-end="1925"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="1874" data-end="1925"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>services:</span><span>
  api
  worker
  redis
  postgres
</span></span></code></div></div></pre>

- Nginx reverse proxy
- systemd auto-restart if crash

---

# 🖥️ Headless vs Headed

For 24/7 production:

Use headless.

But keep debug flag:

<pre class="overflow-visible! px-0!" data-start="2072" data-end="2094"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="2072" data-end="2094"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>HEADLESS</span><span>=</span><span>false</span><span>
</span></span></code></div></div></pre>

so you can visually debug when needed.

---

# 📊 Logging Strategy

You need:

- Per-job log file
- Global log
- Browser console logs
- Network error logs

Store logs like:

<pre class="overflow-visible! px-0!" data-start="2270" data-end="2363"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="2270" data-end="2363"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>/logs/{job_id}/execution.log
/logs/{job_id}/network.log
/logs/{job_id}/screenshot.png
</span></span></code></div></div></pre>

---

# 🧯 Crash Recovery Design

If worker crashes:

- On startup:
  - Check DB for jobs with status "RUNNING"
  - Mark them as "FAILED_RECOVERED"
  - Requeue if necessary

Add:

- Max retry = 3
- Exponential backoff

---

# 🔒 Security (Even Internal)

- Use local VPN access
- Don’t expose publicly
- Add basic auth
- Environment variables for secrets
- Do NOT log OTP or passwords

---

# 🧮 Performance Planning

If running 24/7:

Playwright browser consumes:

- ~200–400MB per instance
- Spikes during heavy pages

If single concurrent job:

2GB RAM minimum

4GB recommended

If 2–3 parallel jobs:

8GB recommended

---

# 🧠 Realistic Expectation

Running browser automation 24 hours continuously will:

- Leak memory over time
- Build zombie Chromium processes if not handled
- Crash if not cleaned properly

So implement:

- Browser restart after each job
- Garbage collection trigger
- Periodic worker restart (cron)

---

# 🏁 Final Recommendation (Stable Setup)

Backend:

→ FastAPI

Automation:

→ Playwright (Python)

Queue:

→ RQ + Redis

Database:

→ PostgreSQL

Deployment:

→ Docker Compose on VPS

Monitoring:

→ Basic health endpoint + systemd restart

---

# 🧨 Very Important

If the automation interacts with third-party platforms in ways that violate their policies:

24/7 activity increases detection probability massively.

Internal tool ≠ invisible.

Stability and stealth are two different things.

Design ethically and legally.

---
