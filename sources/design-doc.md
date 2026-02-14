# 🎨 Design Aesthetic (Single Paragraph)

The UI follows a  **Dark Neo-Tech / Cyber Admin Dashboard aesthetic** , combining deep charcoal and navy backgrounds with high-contrast neon yellow accents for interaction highlights, indicators, and action buttons. The design uses glassy card containers with subtle elevation and thin borders, creating a modular panel-based layout. Typography appears modern sans-serif (similar to Inter, Poppins, or SF Pro), medium weight for headers and lighter weights for data tables, emphasizing clarity and technical precision. Buttons use rectangular shapes with sharp or slightly rounded edges, glowing accent outlines on hover, and strong visual hierarchy through color contrast (yellow for primary actions, green/red for state feedback). Data visualization includes donut charts, line graphs, and bar charts in muted gradients that complement the dark UI, creating a sleek, analytical, enterprise-grade monitoring system feel.

---

# 📘 DD – Design Document

## 1. Project Overview

**Project Name:** Internal Monitoring & Automation Dashboard

**Design Style:** Dark Neo-Tech Enterprise Dashboard

**Target User:** Single Operator (24/7 Monitoring Tool)

**Platform:** Web-based Internal Tool

---

## 2. Design Goals

* High visibility in low-light environments
* Clean modular layout
* Fast scanning of critical metrics
* Action-driven UI
* Real-time monitoring capability
* Low cognitive load for long usage sessions

---

## 3. Layout Structure

### 3.1 Global Layout

* Left Vertical Sidebar Navigation
* Top Navigation Bar
* Main Content Grid System
* Card-Based Modular Panels
* Scrollable Data Tables

---

## 4. Core UI Components

### 4.1 Sidebar

* Minimal icon-based navigation
* Hover tooltips
* Active state highlight (accent yellow border/glow)

### 4.2 Top Navbar

* Search bar (center aligned)
* Notifications icon
* User profile
* Language toggle
* Settings icon

### 4.3 Dashboard Panels

* Hexagon/Widget style stat blocks
* Card-based containers
* Charts:
  * Donut chart
  * Line chart
  * Bar chart
* Status counters

---

## 5. Color System

| Purpose        | Color Style                         |
| -------------- | ----------------------------------- |
| Background     | #0f172a / #111827 (Deep Blue-Black) |
| Card Surface   | Slightly lighter dark (#1e293b)     |
| Primary Accent | Neon Yellow / Gold (#facc15)        |
| Success        | Green (#22c55e)                     |
| Error          | Red (#ef4444)                       |
| Info           | Soft Blue (#3b82f6)                 |
| Borders        | Low opacity gray                    |

Color strategy:

* Accent used sparingly
* High contrast for CTAs
* Neutral backgrounds for long-term viewing comfort

---

## 6. Typography System

### Primary Font

Inter / Poppins / SF Pro (Recommended)

### Hierarchy

* H1: 24px – 600 weight
* H2: 20px – 600 weight
* Card Titles: 16px – 500 weight
* Table Text: 14px – 400 weight
* Labels: 12px – 400 weight
* Buttons: 14px – 500 weight (uppercase optional)

Typography intent:

* Clean
* Technical
* Professional
* Non-playful

---

## 7. Button Design System

### Primary Button

* Dark background
* Yellow border
* Yellow text
* Glow or border intensify on hover

### Success Button

* Green solid background
* White text

### Danger Button

* Red border
* Transparent background
* Red text

### Secondary Button

* Dark grey background
* Subtle border
* Muted text

Button Shape:

* Slightly rounded corners (6–8px radius)
* No heavy drop shadows

---

# 📊 Dashboard Functional Design (Step-wise Analytics + Logs)

Since this is 24/7 internal monitoring, dashboard must include:

---

# 🖥️ Main Dashboard – “Quick Review”

## Step 1 – System Overview Cards

Display:

* Total Jobs Today
* Active Jobs
* Failed Jobs
* Pending Jobs
* Success Rate %
* System Health Status

---

## Step 2 – Real-Time Automation Status

Panel shows:

* Currently Running Job
* Step of Execution
* Last Action Performed
* Timestamp
* Duration

Status Indicators:

* Green → Running Normally
* Yellow → Delayed
* Red → Error

---

## Step 3 – Cloud & Infrastructure Monitoring

Track:

* CPU Usage
* RAM Usage
* Disk Space
* Redis Status
* Database Connection
* Worker Heartbeat

Graphs:

* Line graph for CPU trend
* Area graph for RAM usage

---

## Step 4 – Application Health Panel

Show:

* API response time
* Queue length
* Average job time
* Retry count
* Error frequency

---

# 📜 Logs Section (Very Important for 24/7)

## 1. Live Process Logs

Show:

* Job ID
* Step name
* Action executed
* Result (success/fail)
* Timestamp

Auto-refresh every 5 seconds.

---

## 2. Step-Wise Automation Log Structure

Each job should log:

1. Job Created
2. JSON Processed
3. Excel Generated
4. Browser Launched
5. Registration Step
6. Terms Scrolled
7. OTP Submitted
8. Extended Info Filled
9. Document Uploaded
10. Verification Page Loaded
11. Status Extracted
12. Job Completed

Each step shows:

* Execution time
* Result
* Error (if any)
* Retry count

---

## 3. Error Monitoring Panel

Display:

* Most common failure step
* Last 10 failures
* Failure percentage
* Auto-retry trigger count

---

## 4. Background Processes (Regular Running Processes)

Dashboard should show:

* Redis running
* Worker alive heartbeat
* DB connected
* Browser instances active
* Cron/cleanup jobs

Example:

<pre class="overflow-visible! px-0!" data-start="5433" data-end="5530"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="5433" data-end="5530"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>Worker Status:</span><span></span><span>ONLINE</span><span>
</span><span>Redis:</span><span></span><span>CONNECTED</span><span>
</span><span>PostgreSQL:</span><span></span><span>ACTIVE</span><span>
</span><span>Memory Usage:</span><span></span><span>48</span><span>%</span><span>
</span><span>Queue Size:</span><span></span><span>3</span><span>
</span></span></code></div></div></pre>

---

# 📁 Pages in the System

1. Dashboard
2. Jobs
3. Logs
4. Solutions
5. System Health
6. Settings

---

# 🔁 Regular Background Processes (24/7 System)

Step-wise:

1. Worker heartbeat every 30s
2. Memory cleanup every 1 hour
3. Retry failed jobs (max 3 attempts)
4. Archive old logs daily
5. Restart browser instance after each job
6. Health check endpoint monitoring

---

# 🧠 Overall Design Personality

This design communicates:

* Technical authority
* System control
* Monitoring precision
* Enterprise SaaS maturity
* Internal ops command center feel

It’s very similar to:

* DevOps dashboards
* SOC monitoring panels
* Cloud admin consoles
* Trading analytics UI
