# Automated Registration & Data Processing Workflow

## Product Requirements Document (PRD)

---

## 1. Product Overview

**Product Name:** Automated Registration & Data Processing Workflow

**Version:** 1.0

**Prepared For:** Client Requirement Implementation

**Prepared By:** [Your Name]

**Date:** [Insert Date]

### Objective

Design and implement an automation system that:

* Processes JSON files from an input directory
* Converts structured data into Excel format
* Automates a web-based registration workflow
* Handles OTP input via terminal
* Uploads documents
* Verifies submission status
* Supports both headless and headed execution modes

---

## 2. Scope

### Included

* JSON → Excel transformation
* Missing field handling with synthetic data generation
* Browser automation workflow
* OTP manual entry integration
* Document upload automation
* Verification status capture
* Logging and audit tracking
* Configurable headless/headed mode

### Excluded

* CAPTCHA bypass mechanisms
* Anti-detection fingerprint spoofing
* Security control circumvention
* Platform policy violation mechanisms
* Identity falsification

---

## 3. Functional Requirements

---

## 3.1 Data Processing Module

### Input

Directory containing `.json` files.

### Expected JSON Fields

* email
* username
* password
* dateofbirth
* phonenumber
* firstname (including middle name)
* lastname
* country
* place_of_birth
* residential_address
* city
* postal_code
* occupation_industry
* occupation_field
* occupation_experience

### Processing Logic

1. Scan input folder
2. Parse each JSON file
3. Validate schema
4. Map fields to Excel structure
5. If a field is missing:
   * Generate realistic synthetic data
   * Maintain country-city-postal consistency
   * Ensure age validation (18+ if required)

### Output

* Excel file (.xlsx)
* One row per JSON file
* Structured and validated dataset

---

## 3.2 Browser Automation Module

### Recommended Tech Stack

* Playwright (Preferred)
* Selenium (Alternative)
* Python or Node.js

### Configuration File Example

<pre class="overflow-visible! px-0!" data-start="2500" data-end="2603"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="2500" data-end="2603"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-yaml"><span><span>headless:</span><span></span><span>true</span><span>
</span><span>input_folder:</span><span></span><span>./data</span><span>
</span><span>upload_folder:</span><span></span><span>./uploads</span><span>
</span><span>log_level:</span><span></span><span>INFO</span><span>
</span><span>max_retries:</span><span></span><span>3</span><span>
</span></span></code></div></div></pre>

---

## 3.3 Registration Workflow Automation

### Step 1 – Navigation

* Navigate to target website
* Wait for DOM readiness

### Step 2 – Registration Form

* Click “Register”
* Populate fields from Excel row
* If phone checkbox present:
  * Enable checkbox
  * Insert phone number

### Step 3 – Terms & Conditions

* Scroll terms container fully
* Tick agreement checkbox
* Click “Create Account”

### Step 4 – Wallet Setup

* Detect popup
* Click “Setup Wallet”

### Step 5 – OTP Handling

* Pause automation
* Accept OTP from terminal
* Submit OTP

### Step 6 – Extended Information

Fill the following:

* First Name (including middle name)
* Last Name
* Country
* Place of Birth
* Residential Address
* City
* Postal Code
* Occupation Industry
* Occupation Field
* Occupation Experience

If missing → generate structured random values.

### Step 7 – Document Upload

* Select “Driving License”
* Match filename from input folder
* Upload:
  * Front image
  * Back image
* Click Submit

### Step 8 – Verification Status

Navigate to:

`https://stake.ac/settings/verification`

Capture:

* Screenshot
* HTML dump
* Parsed verification status
* Optional curl request log

---

## 4. Non-Functional Requirements

* Structured logging
* Retry logic (max 3 attempts)
* Explicit waits (no blind sleeps)
* Error handling
* Rate limiting
* Config-driven execution

---

## 5. System Architecture

<pre class="overflow-visible! px-0!" data-start="4077" data-end="4280"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="4077" data-end="4280"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>/automation
 ├── config.yaml
 ├── data/
 ├── uploads/
 ├── logs/
 ├── json_processor.py
 ├── excel_generator.py
 ├── browser_flow.py
 ├── otp_handler.py
 ├── document_uploader.py
 └── verifier.py
</span></span></code></div></div></pre>

---

## 6. Data Validation Rules

* Email format validation
* Password complexity validation
* DOB format: YYYY-MM-DD
* Postal code validation by country
* Phone format validation by country
* Occupation taxonomy normalization

---

## 7. Logging Structure

Each log entry must contain:

* timestamp
* module
* action
* status
* error_message (if any)
* retry_count

Logs saved to:

`/logs/execution.log`

---

## 8. Output Artifacts

After execution, system should generate:

* verification_status.png
* verification_status.html
* execution.log
* Generated Excel file
* Status summary JSON

Possible Status Values:

* VERIFIED
* PENDING
* SUBMITTED
* REJECTED
* ERROR

---

## 9. Risk & Compliance Note

Due to inclusion of:

* CAPTCHA interaction
* Account automation
* KYC document upload
* Traceability concerns

Implementation must be restricted to:

* Authorized environments
* Explicit written platform permission
* Internal QA or testing use cases

No security bypass logic should be implemented without legal authorization.

---

## 10. Client-Supplied Workflow Prompt (Original Requirement Reference)

The following is the exact instruction provided:

<pre class="overflow-visible! px-0!" data-start="5502" data-end="7079"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

<pre class="overflow-visible! px-0!" data-start="5502" data-end="7079"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>do</span><span></span><span>not</span><span> trace </span><span>from</span><span> anyweb what i am what i </span><span>do</span><span> , </span><span>all</span><span></span><span>also</span><span> headless, withhead 
</span><span>1.</span><span></span><span>in</span><span> site </span><span>do</span><span> cloudflare captha , via anything
</span><span>2.</span><span> go website stake.ac, 
</span><span>3.</span><span> tap register tab
 </span><span>----------------</span><span>
</span><span>in</span><span> parrallel 
</span><span>--------------</span><span>
</span><span>3.1</span><span></span><span>from</span><span></span><span>input</span><span> folder find .json file </span><span>from</span><span> this make excel sheet, </span><span>in</span><span> that excel 
this collumn already presents 
email,username,</span><span>password</span><span>,dateofbirth,phonenumber,firstname( including middle </span><span>name</span><span> ),lastname, country, place, </span><span>of</span><span> birth,  residental address, city , postal code, occupation industrie,  occupation field, occupation experiance

according </span><span>json</span><span></span><span>add</span><span> that detail </span><span>else</span><span></span><span>info</span><span> put random according data , 

</span><span>--------------------</span><span>
</span><span>4.</span><span></span><span>input</span><span> data </span><span>from</span><span> that excel shit , please help me </span><span>write</span><span> a comprehensive prd </span><span>for</span><span> it.
</span><span>and</span><span></span><span>for</span><span> phone number ther a </span><span>check</span><span></span><span>box</span><span> press </span><span>and</span><span></span><span>in</span><span> there put phone number
</span><span>5.</span><span> press next
</span><span>6.</span><span>scroll terms </span><span>and</span><span> condition </span><span>full</span><span>, </span><span>then</span><span> tick checkbox, </span><span>then</span><span> press crete acc.
</span><span>7.</span><span> it </span><span>show</span><span> popup </span><span>where</span><span> press setup wallet
</span><span>8.</span><span> it </span><span>show</span><span> the </span><span>in</span><span> terminal enter otp, i give </span><span>then</span><span> press submit 
</span><span>9</span><span>, </span><span>then</span><span> it asking firstname( including middle </span><span>name</span><span> ),lastname, country, place, </span><span>of</span><span> birth,  residental address, city , postal code,
</span><span>10</span><span>, </span><span>also</span><span> occupation industrie,  occupation field, occupation experiance,  put this random
</span><span>11</span><span>, press save </span><span>and</span><span> continiue 
</span><span>then</span><span> it </span><span>show</span><span> upload doc, 
</span><span>where</span><span></span><span>select</span><span> driving liccence,
according </span><span>input</span><span> folder same </span><span>name</span><span></span><span>in</span><span> front </span><span>add</span><span> front image </span><span>of</span><span> that </span><span>name</span><span> present </span><span>in</span><span> that folder, </span><span>and</span><span> same </span><span>for</span><span> back image
</span><span>12</span><span>, press submit
go this page https://stake.ac/settings/verification
</span><span>show</span><span> that page </span><span>or</span><span></span><span>show</span><span> its curl </span><span>or</span><span> visual detail its verifyed </span><span>or</span><span> submitted
</span></span></code></div></div></pre>

---

## 11. Future Enhancements

* Multi-threaded execution
* Database-backed tracking
* API-based OTP integration
* CI/CD pipeline
* Docker containerization
* Status dashboard

---

END OF DOCUMENT

---
