# gmail_sender.py
# Handles Gmail API authentication and email sending

import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """
    Authenticate and return Gmail API service.
    First run will open browser for authentication.
    Token is saved to token.json for future runs.
    """
    creds = None
    token_file = 'token.json'
    creds_file = 'credentials.json'
    
    # Check if we have saved token from previous run
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        print("✅ Found existing token.json")
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        print("🔄 No valid token found. Starting OAuth flow...")
        if creds and creds.expired and creds.refresh_token:
            print("   Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_file):
                raise FileNotFoundError(
                    f"credentials.json not found. Please download it from Google Cloud Console "
                    f"and save it as '{creds_file}' in the project folder."
                )
            print("   Opening browser for authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Save credentials for next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        print(f"✅ Token saved to {token_file}")
    
    return build('gmail', 'v1', credentials=creds)

def send_real_email(to_email, lead, score_result):
    """
    Send real email using Gmail API.
    Returns dict with status and message.
    """
    try:
        # Get authenticated Gmail service
        print("📧 Authenticating with Gmail API...")
        service = get_gmail_service()
        
        # Sender email (hardcoded - avoids extra permission)
        # Sender email (my  Gmail address)
        sender_email = "shaikmay@gmail.com"  # <-- Put YOUR email here
        
        score = score_result.get('total', 0)
        company = lead.get('company', 'Unknown')
        name = lead.get('name', 'Unknown')
        
        print(f"📧 Sending email from: {sender_email}")
        print(f"📧 Sending email to: {to_email}")
        
        # Create email content
        subject = f" HOT LEAD ALERT: {company} (BANT Score: {score}/100)"
        
        # HTML email body
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h2 style="color: white; margin: 0;"> HOT LEAD ALERT</h2>
            </div>
            
            <div style="border: 1px solid #ddd; border-top: none; padding: 20px; border-radius: 0 0 10px 10px;">
                <p style="font-size: 16px;">A new lead has been <strong style="color: green;">QUALIFIED</strong> by your Sales Ops Agent.</p>
                
                <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3 style="margin-top: 0; color: #333;">📋 Lead Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 5px 0;"><strong>Name:</strong></td><td>{name}</td></tr>
                        <tr><td style="padding: 5px 0;"><strong>Company:</strong></td><td>{company}</td></tr>
                        <tr><td style="padding: 5px 0;"><strong>Title:</strong></td><td>{lead.get('title', 'N/A')}</td></tr>
                        <tr><td style="padding: 5px 0;"><strong>Budget:</strong></td><td>{lead.get('budget', 'N/A')}</td></tr>
                        <tr><td style="padding: 5px 0;"><strong>Need:</strong></td><td>{lead.get('need', 'N/A')}</td></tr>
                        <tr><td style="padding: 5px 0;"><strong>Timeline:</strong></td><td>{lead.get('timeline', 'N/A')}</td></tr>
                    </table>
                </div>
                
                <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3 style="margin-top: 0; color: #2e7d32;"> BANT Score Breakdown</h3>
                    <ul style="margin: 0;">
                        <li><strong>Budget:</strong> {score_result['breakdown']['budget']}/25</li>
                        <li><strong>Authority:</strong> {score_result['breakdown']['authority']}/25</li>
                        <li><strong>Need:</strong> {score_result['breakdown']['need']}/25</li>
                        <li><strong>Timeline:</strong> {score_result['breakdown']['timeline']}/25</li>
                    </ul>
                    <p style="font-size: 24px; text-align: center; margin: 15px 0 0;">
                        <strong>TOTAL SCORE: {score}/100</strong>
                    </p>
                </div>
                
                <p style="background: #fff3e0; padding: 10px; border-radius: 5px;">
                    <strong> Recommended Action:</strong> Contact this lead within 24 hours.
                </p>
                
                <hr style="margin: 20px 0;">
                <p style="color: #666; font-size: 12px; text-align: center;">
                    This is an automated message from your Sales Ops Automation Agent.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Create email message
        message = MIMEMultipart('alternative')
        message['to'] = to_email
        message['subject'] = subject
        message.attach(MIMEText(body_html, 'html'))
        
        # Encode and send
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"✅ Email sent successfully! Message ID: {sent_message['id']}")
        return {"sent": True, "message_id": sent_message['id']}
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return {"sent": False, "error": str(e)}

# For testing this module directly
if __name__ == "__main__":
    # Test with dummy data
    test_lead = {
        "name": "Test User",
        "company": "Test Corp",
        "title": "Test Title",
        "budget": "approved",
        "need": "Testing the system",
        "timeline": "30 days"
    }
    test_score = {
        "total": 100,
        "breakdown": {"budget": 25, "authority": 25, "need": 25, "timeline": 25}
    }
    
    print("Testing Gmail API...")
    result = send_real_email("your-email@gmail.com", test_lead, test_score)
    print(result)