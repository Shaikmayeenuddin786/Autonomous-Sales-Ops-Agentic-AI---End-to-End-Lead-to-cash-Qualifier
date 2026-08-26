# **Agentic AI for Sales: Lead-to-Cash Automation**
### **End-to-End Lead Qualification | BANT Scoring & Routing | Real-Time Alerts | Zero Lead Loss | 99.6% Time Savings | Revenue Acceleration**

<img width="1024" height="512" alt="image" src="https://github.com/user-attachments/assets/901fdddb-89d8-4779-8493-2ecc8ff593e5" />

---


# **Quick Overview**

| **Section** | **Details** |
| :--- | :--- |
| **Business Problem** | Sales reps waste 22 minutes per lead on manual admin (reading, scoring, logging, reminders). Leads get forgotten, and managers have zero visibility into lead volume or qualification decisions. |
| **Objectives** | 1. Automate BANT qualification<br>2. Reduce processing time from 22 min → 5 sec<br>3. Ensure zero lead loss (every lead logged)<br>4. Send real-time email alerts for qualified leads<br>5. Build production-ready error handling with auto-backup |
| **Technical Stack** | **Backend:** Python, FastAPI, Uvicorn<br>**Email:** Gmail API, OAuth 2.0<br>**Frontend:** HTML, CSS, JavaScript<br>**Storage:** CSV with auto-backup<br>**Logging:** agent.log with traceback<br>**Version Control:** Git, GitHub |
| **Key Features** | • BANT scoring engine (0-100)<br>• 55-point qualification threshold<br>• HTML email alerts for hot leads<br>• CSV logging with 3-retry logic<br>• Automatic backup on file lock<br>• Centralized manager dashboard (CSV + chart)<br>• Full error logging with traceback |
| **Start-to-End Pipeline** | **Lead Intake** (web form) → **FastAPI Backend** (validation) → **BANT Scoring** (0-100) → **Parallel Actions** (email if ≥55, always log CSV) → **Instant Response** (user sees result, rep gets email, manager views CSV) |



---

## **The Big Picture**
This project solves a real sales problem: reps wasted 22 minutes per lead on manual admin, and leads were getting lost. I built an AI agent that does the boring work in 5 seconds—scoring, logging, and alerting—so reps can focus on selling. It's a practical, business-focused automation that directly improves revenue by ensuring no lead is ever missed.


---

## Business Problem

In most sales teams, when a lead comes in, a sales representative  spends on a average of  22 minutes just doing the manual admin task like  reading the email, checking  the budget, confirming the timelines,  figuring out if the lead is worth pursuing,  logging every details into a spreadsheet then  set  a reminders for follow up .It’s tedious, it’s repetitive

That's around 22 minutes of valuable time which  is not spent on closing the deals 
and the worse is when the admins get busy and the  leads are forgotten. 
Even managers have no centralized visibility into lead volume or qualification decisions.


---

## Objectives

|  |  |
|---|----
| 1 | Automate lead qualification using BANT framework (Budget, Authority, Need, Timeline) |
| 2 | Reduce manual processing time from 22 minutes to under 5 seconds |
| 3 | Ensure zero lead loss - every lead logged, **hot or cold** |
| 4 | Deliver real-time email alerts to sales reps for qualified leads |
| 5 | Build production-ready error handling with automatic backup |

---

## Insights Deep Dive

| Insight | Finding |
|---------|---------|
| Hot lead (Acme Corp) | BANT Score 100/100 → Email sent in 5 seconds |
| Borderline lead (Mid Corp) | BANT Score 57/100 → Still qualified, email sent |
| Cold lead (Small Biz) | BANT Score 22/100 → No email, but logged to backup CSV |
| File locked scenario | System retries 3 times, then creates backup CSV automatically |
| OAuth authentication | First run opens browser; token.json saved for subsequent automated runs |

---

## Tools & Technologies

| **Category** | **Tools** |
|----------|-------|
| **Backend** | Python, FastAPI, Uvicorn |
| **Email** | Gmail API, OAuth 2.0 |
| **Frontend** | HTML, CSS, JavaScript |
| **Data Storage** | CSV with auto-backup |
| **Authentication** | OAuth 2.0 (Desktop App) |
| **Logging** | agent.log with traceback |
| **Version Control** | Git, GitHub |

---

## Key Benefits

| Benefit | Impact |
|---------|--------|
| **99.6% time reduction** | 22 minutes → 5 seconds per lead |
| **Zero lead loss** | Every lead logged (CSV + backup) |
| **Consistent qualification** | Same BANT rules applied to every lead |
| **Real-time sales alerts** | HTML email within 5 seconds of submission |
| **Production-grade reliability** | Retry logic, backup files, full error logging |
| **Manager visibility** | Centralized CSV for all leads (qualified + rejected) |


---


## **Architectural Flow** 

The system follows a 5-phase end-to-end flow:

**Phase 1 - Lead Intake:** Prospect fills out web form (Name, Company, Title, Budget, Need, Timeline). Form submits data via POST request to `/qualify` endpoint.

**Phase 2 - FastAPI Backend:** Server validates required fields, generates unique Request ID, and logs receipt to `agent.log`. Autonomous agent begins processing.

**Phase 3 - BANT Scoring:** Agent scores lead across four criteria (Budget 0-25, Authority 0-25, Need 0-25, Timeline 0-25). Total score ranges 0-100. Threshold set at 55 points for qualification.

**Phase 4 - Parallel Actions:** 
- If score ≥ 55: Gmail API sends HTML email to sales rep with lead details and BANT breakdown
- Always: Lead logged to `leads_log.csv` (with 3 retry attempts; fails over to backup CSV)
- Always: All events logged to `agent.log` with timestamps

**Phase 5 - Response:** User receives instant qualification decision on screen. Sales rep gets email within 5 seconds. Manager accesses CSV for complete lead visibility.


## Architectural Visual diagram


<img width="3564" height="12012" alt="End-to-End_Lead Qualification_Automation_Architecture " src="https://github.com/user-attachments/assets/0dbd8dc0-d0e1-49ee-a060-624eb77b64a9" />



---

## Data Flow 

<img width="830" height="687" alt="Data Flow" src="https://github.com/user-attachments/assets/30a8b96c-fd71-480e-ad76-abc01ac5da36" />


---


## Screenshots


###  | Web Form |

<img width="597" height="796" alt="Error Handling_MISSING_FIELD" src="https://github.com/user-attachments/assets/4ef11694-8e21-4efa-8daa-1c38a94559c3" />

---

### | Qualification Result | Email Alert | CSV Log |

<img width="1897" height="1048" alt="Sales Ops Agentic AI_Lead-to-Cash Automation" src="https://github.com/user-attachments/assets/94bd424c-1170-438f-a507-08a39ae278d2" />

---

### | Backup File | Error Log | agent.log | leads_log |

<img width="1855" height="1018" alt="Error Handling_leads_logBckup_CSV OPENED_5second_Completion" src="https://github.com/user-attachments/assets/454f6484-3eb8-4b22-9c90-be551391baeb" />

---

### | Leads_Log.CSV | Chart (threshold = 55) |

### A sales manager can look at this chart for 3 seconds & understand:
- Who the top leads are
- Where the threshold line is
- Which leads need immediate attention (arrange a callback)

<img width="1261" height="605" alt="image" src="https://github.com/user-attachments/assets/a6f70d65-b952-421e-b8c2-f5a08a0971d8" />
<img width="1838" height="238" alt="image" src="https://github.com/user-attachments/assets/a9eceb07-b8fd-4c6a-ab6b-9a714cfd4a05" />



  ---
  

## 📁 Project Structure

```
sales-ops-agent/
├── main.py                 # FastAPI application
├── gmail_sender.py         # Gmail API + OAuth handling
├── requirements.txt        # Python dependencies
├── credentials.json        # Google Cloud OAuth credentials
├── token.json              # OAuth token (auto-generated)
├── leads_log.csv           # Primary lead database
├── agent.log               # Error and event log
└── README.md               # This file
```

---

##  Sample Leads for Testing

| Type | Name | Company | Budget | Need | Timeline | Expected Score |
|------|------|---------|--------|------|----------|----------------|
| Hot Lead | Sarah Johnson | Acme Global | Approved | Urgent CRM integration | 30 days | 100/100 |
| Borderline | Michael Chen | Mid-Tech | Pending | Tracking challenges | 60 days | 57/100 |
| Cold Lead | John Smith | Small Biz | No budget | Just looking | Next year | 22/100 |

---

##  Environment Setup

Create `credentials.json` from Google Cloud Console:

1. Enable Gmail API
2. Create OAuth 2.0 Client ID (Desktop app type)
3. Download JSON and rename to `credentials.json`
4. Add your email as Test User in OAuth consent screen

First run will open browser for authentication. `token.json` auto-saved for subsequent runs.

---

##  Results Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Time per lead | 22 minutes | 5 seconds | 99.6% |
| Lead tracking | Inconsistent | 100% | Complete |
| Qualification consistency | Rep-dependent | Unbiased | Standardized |
| Email delivery | Manual | Real-time automated | Instant |

---

# 👤 **Author**

### **Shaik Mayeenuddin**

#### Business Analyst | Data Analytics & AI/ML | Optimizing Processes to Drive Revenue & Retention

🔗https://www.linkedin.com/in/shaikmayeenuddin


---
