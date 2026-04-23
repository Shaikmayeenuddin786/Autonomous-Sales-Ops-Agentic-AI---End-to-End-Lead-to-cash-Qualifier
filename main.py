# main.py - Complete FastAPI Web Application with Error Handling
# Also , real email 

from gmail_sender import send_real_email
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import Dict, Any
import csv
import os
import logging
import traceback

# ============================================
# ERROR HANDLING SETUP (Complete main.py with Error Handling)
# ============================================

# Setup logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),  # Save to file
        logging.StreamHandler()            # Also print to console
    ]
)

logger = logging.getLogger(__name__)

# ============================================
# PART 1: BANT SCORING (Same as before)
# ============================================

def score_budget(budget_value):
    """Score the budget - max 25 points"""
    try:
        budget_lower = budget_value.lower() if budget_value else ""
        if budget_lower in ["approved", "yes", "ready", "available"]:
            return 25
        elif budget_lower in ["pending", "in review", "discussing"]:
            return 12
        else:
            return 0
    except Exception as e:
        logger.error(f"Error in score_budget: {e}")
        return 0

def score_authority(job_title):
    """Score authority based on job title - max 25 points"""
    try:
        title_lower = job_title.lower() if job_title else ""
        if any(word in title_lower for word in ["director", "vp", "vice president", "head", "chief", "c-level", "cmo", "cto", "ceo"]):
            return 25
        elif any(word in title_lower for word in ["manager", "lead", "senior"]):
            return 18
        elif any(word in title_lower for word in ["specialist", "analyst", "associate", "coordinator"]):
            return 10
        else:
            return 5
    except Exception as e:
        logger.error(f"Error in score_authority: {e}")
        return 5

def score_need(need_text):
    """Score urgency of need - max 25 points"""
    try:
        need_lower = need_text.lower() if need_text else ""
        urgent_words = ["urgent", "asap", "critical", "need", "required", "must have", "problem", "issue"]
        if any(word in need_lower for word in urgent_words):
            return 25
        else:
            return 12
    except Exception as e:
        logger.error(f"Error in score_need: {e}")
        return 12

def score_timeline(timeline_text):
    """Score timeline - max 25 points"""
    try:
        timeline_lower = timeline_text.lower() if timeline_text else ""
        if any(word in timeline_lower for word in ["immediate", "now", "today", "30 days", "within a month"]):
            return 25
        elif any(word in timeline_lower for word in ["60 days", "90 days", "quarter", "this quarter"]):
            return 15
        else:
            return 5
    except Exception as e:
        logger.error(f"Error in score_timeline: {e}")
        return 5

def calculate_bant_score(lead):
    """Calculate total BANT score for a lead. Max 100."""
    try:
        budget_score = score_budget(lead.get("budget", ""))
        authority_score = score_authority(lead.get("title", ""))
        need_score = score_need(lead.get("need", ""))
        timeline_score = score_timeline(lead.get("timeline", ""))
        
        total_score = budget_score + authority_score + need_score + timeline_score
        
        return {
            "total": total_score,
            "breakdown": {
                "budget": budget_score,
                "authority": authority_score,
                "need": need_score,
                "timeline": timeline_score
            }
        }
    except Exception as e:
        logger.error(f"Error in calculate_bant_score: {e}")
        logger.error(traceback.format_exc())
        return {
            "total": 0,
            "breakdown": {
                "budget": 0,
                "authority": 0,
                "need": 0,
                "timeline": 0
            }
        }

# ============================================
# PART 2: CSV LOGGING WITH ERROR HANDLING
# ============================================

def log_lead_to_csv(lead, score_result, qualified):
    """Save every lead to a CSV file - with retry logic"""
    filename = "leads_log.csv"
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Check if file exists
            file_exists = os.path.isfile(filename)
            
            # Prepare the row with safe defaults
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                lead.get("name", "Unknown"),
                lead.get("company", "Unknown"),
                lead.get("title", "Unknown"),
                lead.get("budget", "Unknown"),
                lead.get("need", "Unknown"),
                lead.get("timeline", "Unknown"),
                score_result.get("total", 0),
                score_result.get("breakdown", {}).get("budget", 0),
                score_result.get("breakdown", {}).get("authority", 0),
                score_result.get("breakdown", {}).get("need", 0),
                score_result.get("breakdown", {}).get("timeline", 0),
                "Yes" if qualified else "No"
            ]
            
            # Write to CSV
            with open(filename, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    headers = ["Timestamp", "Name", "Company", "Title", "Budget", 
                              "Need", "Timeline", "Total Score", "Budget Score",
                              "Authority Score", "Need Score", "Timeline Score", "Qualified"]
                    writer.writerow(headers)
                writer.writerow(row)
            
            logger.info(f"Lead logged to CSV: {lead.get('company')} - Score: {score_result.get('total', 0)}")
            return filename
            
        except PermissionError as e:
            logger.warning(f"Permission error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed to write to CSV after {max_retries} attempts")
                # Try alternative filename
                backup_filename = f"leads_log_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                try:
                    with open(backup_filename, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)
                    logger.info(f"Saved to backup file: {backup_filename}")
                    return backup_filename
                except Exception as backup_error:
                    logger.error(f"Even backup failed: {backup_error}")
                    return None
        except Exception as e:
            logger.error(f"Unexpected error logging to CSV: {e}")
            if attempt == max_retries - 1:
                return None
            continue
    
    return None

# ============================================
# PART 3: MOCK EMAIL WITH ERROR HANDLING
# ============================================

def send_mock_email(lead, score_result):
    """Mock email - prints to console with error handling"""
    try:
        score = score_result.get("total", 0)
        company = lead.get("company", "Unknown")
        
        print("\n" + "=" * 60)
        print(f" [MOCK EMAIL SENT]")
        print(f"   To: salesrep@company.com")
        print(f"   Subject:  HOT LEAD ALERT: {company} (BANT Score: {score}/100)")
        print(f"   Body: Lead from {lead.get('name', 'Unknown')} at {company} scored {score}/100")
        print("=" * 60 + "\n")
        
        logger.info(f"Mock email sent for: {company}")
        return {"sent": True, "to": "salesrep@company.com"}
        
    except Exception as e:
        logger.error(f"Error sending mock email: {e}")
        return {"sent": False, "error": str(e)}

# ============================================
# PART 4: THE MAIN AGENT WITH FULL ERROR HANDLING
# ============================================

THRESHOLD = 55

def autonomous_sales_agent(lead: Dict[str, Any]) -> Dict[str, Any]:
    """
    Complete agent that scores leads and takes action.
    Includes error handling for each step.
    """
    company = lead.get("company", "Unknown")
    name = lead.get("name", "Unknown")
    
    logger.info(f"Starting agent for lead: {name} from {company}")
    
    try:
        print(f"\n{'='*60}")
        print(f" Processing lead: {name} from {company}")
        print(f"{'='*60}")
        
        # Step 1: Score the lead (with error handling)
        try:
            score_result = calculate_bant_score(lead)
            score = score_result.get("total", 0)
            print(f" BANT Score: {score}/100")
            logger.info(f"BANT Score for {company}: {score}/100")
        except Exception as e:
            logger.error(f"Scoring failed for {company}: {e}")
            logger.error(traceback.format_exc())
            return {
                "lead_name": name,
                "company": company,
                "score": 0,
                "qualified": False,
                "email_sent": False,
                "logged_to": None,
                "error": "Scoring failed",
                "message": "System error during scoring. Our team has been notified."
            }
        
        # Step 2: Determine qualification
        qualified = score >= THRESHOLD
        logger.info(f"Lead qualified: {qualified} (Score: {score}, Threshold: {THRESHOLD})")
        
        # Step 3: Log to CSV (with error handling - doesn't stop the process)
        log_file = None
        try:
            log_file = log_lead_to_csv(lead, score_result, qualified)
            if log_file:
                print(f"📝 Logged to: {log_file}")
            else:
                print(f"⚠️ Warning: Could not log to CSV")
        except Exception as e:
            logger.error(f"CSV logging failed but continuing: {e}")
            print(f"⚠️ Warning: Logging failed but processing continues")
        
        # Step 4: Send email if qualified (with error handling)
        email_sent = False
        if qualified:
            try:
                print(f" Qualified - Sending alert...")
                email_result = send_real_email("shaikmay@gmail.com", lead, score_result)
                email_sent = email_result.get("sent", False)
                if email_sent:
                    logger.info(f"Email sent for qualified lead: {company}")
                else:
                    logger.warning(f"Email sending reported failure: {email_result}")
            except Exception as e:
                logger.error(f"Email sending failed for {company}: {e}")
                print(f"⚠️ Warning: Email failed but lead is still qualified")
        else:
            print(f"❌ Not qualified (Score {score} < {THRESHOLD})")
        
        # Return result
        result = {
            "lead_name": name,
            "company": company,
            "score": score,
            "qualified": qualified,
            "email_sent": email_sent,
            "logged_to": log_file,
            "message": f"Lead processed. Score: {score}/100. {'Email sent.' if qualified else 'No email sent.'}"
        }
        
        logger.info(f"Agent completed for {company}: Qualified={qualified}, Email={email_sent}")
        return result
        
    except Exception as e:
        logger.error(f"CRITICAL: Agent failed for {company}: {e}")
        logger.error(traceback.format_exc())
        return {
            "lead_name": name,
            "company": company,
            "score": 0,
            "qualified": False,
            "email_sent": False,
            "logged_to": None,
            "error": str(e),
            "message": "System error. Our team has been notified. Please try again later."
        }

# ============================================
# PART 5: FASTAPI WEB APPLICATION
# ============================================

# Create FastAPI app
app = FastAPI(title="Sales Ops Automation Agent", description="Autonomous lead qualification system with error handling")

# Allow web form to call this API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what a lead looks like (for validation)
class LeadData(BaseModel):
    name: str
    company: str
    title: str
    budget: str
    need: str
    timeline: str

# ============================================
# ENDPOINT 1: Serve the HTML Form
# ============================================

@app.get("/", response_class=HTMLResponse)
async def serve_form():
    """Show the web form when someone visits the homepage"""
    try:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Lead Qualification System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 500px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                    margin-bottom: 10px;
                }
                .subtitle {
                    color: #666;
                    margin-bottom: 30px;
                    font-size: 14px;
                }
                label {
                    display: block;
                    margin: 15px 0 5px;
                    font-weight: bold;
                    color: #555;
                }
                input, select, textarea {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 14px;
                    box-sizing: border-box;
                }
                textarea {
                    resize: vertical;
                    min-height: 80px;
                }
                button {
                    background: #007bff;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    margin-top: 20px;
                    width: 100%;
                }
                button:hover {
                    background: #0056b3;
                }
                .result {
                    margin-top: 20px;
                    padding: 15px;
                    border-radius: 5px;
                    display: none;
                }
                .result.success {
                    background: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                    display: block;
                }
                .result.error {
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    display: block;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1> Request a Quote</h1>
                <div class="subtitle">Fill out the form below and our sales team will get back to you within 24 hours.</div>
                
                <form id="leadForm">
                    <label>Full Name *</label>
                    <input type="text" id="name" required placeholder="e.g., Sarah Johnson">
                    
                    <label>Company Name *</label>
                    <input type="text" id="company" required placeholder="e.g., Acme Corp">
                    
                    <label>Job Title *</label>
                    <input type="text" id="title" required placeholder="e.g., Marketing Director">
                    
                    <label>Budget Status *</label>
                    <select id="budget" required>
                        <option value="approved">✅ Approved - Budget ready</option>
                        <option value="pending"> Pending - Under review</option>
                        <option value="no">❌ No budget allocated</option>
                    </select>
                    
                    <label>What challenge are you trying to solve? *</label>
                    <textarea id="need" required placeholder="e.g., We need a CRM integration solution for our 50-person sales team"></textarea>
                    
                    <label>Timeline *</label>
                    <select id="timeline" required>
                        <option value="30 days"> Within 30 days (Urgent)</option>
                        <option value="60 days">📅 60 days</option>
                        <option value="90 days">🗓️ 90 days</option>
                        <option value="next year">📆 Next year</option>
                    </select>
                    
                    <button type="submit">Submit Lead</button>
                </form>
                
                <div id="result" class="result"></div>
            </div>

            <script>
                document.getElementById('leadForm').onsubmit = async (e) => {
                    e.preventDefault();
                    
                    const data = {
                        name: document.getElementById('name').value,
                        company: document.getElementById('company').value,
                        title: document.getElementById('title').value,
                        budget: document.getElementById('budget').value,
                        need: document.getElementById('need').value,
                        timeline: document.getElementById('timeline').value
                    };
                    
                    const resultDiv = document.getElementById('result');
                    resultDiv.className = 'result';
                    resultDiv.innerHTML = 'Processing your request...';
                    
                    try {
                        const response = await fetch('/qualify', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(data)
                        });
                        
                        const result = await response.json();
                        
                        if (result.error) {
                            resultDiv.className = 'result error';
                            resultDiv.innerHTML = `
                                ❌ <strong>System Error</strong><br>
                                ${result.message}<br>
                                <small>Our team has been notified. Please try again later.</small>
                            `;
                        } else if (result.qualified) {
                            resultDiv.className = 'result success';
                            resultDiv.innerHTML = `
                                 <strong>Lead Qualified!</strong><br>
                                Score: ${result.score}/100<br>
                                ${result.message}<br>
                                <small>A sales representative will contact you within 24 hours.</small>
                            `;
                        } else {
                            resultDiv.className = 'result error';
                            resultDiv.innerHTML = `
                                 <strong>Lead Not Qualified</strong><br>
                                Score: ${result.score}/100<br>
                                ${result.message}<br>
                                <small>We'll keep your information on file for future opportunities.</small>
                            `;
                        }
                        
                        document.getElementById('leadForm').reset();
                        
                    } catch (error) {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = '❌ Error submitting form. Please try again.';
                    }
                };
            </script>
        </body>
        </html>
        """
        return html_content
        
    except Exception as e:
        logger.error(f"Error serving form: {e}")
        return HTMLResponse(content="<h1>System Error</h1><p>Please try again later.</p>", status_code=500)

# ============================================
# ENDPOINT 2: Process the Lead (with validation error handling)
# ============================================

@app.post("/qualify")
async def qualify_lead(lead: LeadData):
    """Process a lead submission and return qualification result"""
    request_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    logger.info(f"Request {request_id}: Received lead submission")
    
    try:
        # Validate required fields
        if not lead.name or not lead.name.strip():
            logger.warning(f"Request {request_id}: Missing name field")
            return {
                "qualified": False,
                "error": "missing_field",
                "message": "Name is required. Please fill all fields."
            }
        
        if not lead.company or not lead.company.strip():
            logger.warning(f"Request {request_id}: Missing company field")
            return {
                "qualified": False,
                "error": "missing_field",
                "message": "Company name is required. Please fill all fields."
            }
        
        # Convert to dictionary
        lead_dict = lead.dict()
        logger.info(f"Request {request_id}: Processing lead for {lead_dict.get('company')}")
        
        # Run the agent
        result = autonomous_sales_agent(lead_dict)
        
        # Add request ID to result for tracking
        result["request_id"] = request_id
        
        logger.info(f"Request {request_id}: Completed with result: Qualified={result.get('qualified')}")
        return result
        
    except ValidationError as e:
        logger.error(f"Request {request_id}: Validation error: {e}")
        return {
            "qualified": False,
            "error": "validation_error",
            "message": "Invalid data format. Please check your inputs."
        }
    except Exception as e:
        logger.error(f"Request {request_id}: Unexpected error: {e}")
        logger.error(traceback.format_exc())
        return {
            "qualified": False,
            "error": "system_error",
            "message": "An unexpected error occurred. Our team has been notified."
        }

# ============================================
# ENDPOINT 3: Health Check (For testing and monitoring)
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "threshold": THRESHOLD,
        "timestamp": datetime.now().isoformat()
    }

# ============================================
# ENDPOINT 4: Error Log Viewer (For debugging - optional)
# ============================================

@app.get("/logs")
async def view_logs():
    """View recent error logs (for debugging only)"""
    try:
        if os.path.exists("agent.log"):
            with open("agent.log", "r") as f:
                lines = f.readlines()
                # Return last 50 lines
                last_lines = lines[-50:] if len(lines) > 50 else lines
                return {"logs": last_lines}
        else:
            return {"logs": ["No log file found"]}
    except Exception as e:
        return {"error": str(e)}

# ============================================
# RUN THE APP
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print(" Sales Ops Automation Agent is running!")
    print("📋 Open your browser and go to: http://localhost:8000")
    print("📝 Logs are being saved to: agent.log")
    print("=" * 60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)