# monitor_mailhog.py
# Used for terminal
import time
import requests
import datetime
from mail_analyzer import analyze_email

MAILHOG_API = "http://localhost:8025/api/v2/messages"
CHECK_INTERVAL = 5  # seconds
seen_ids = set()  # Keep track of already processed emails

def fetch_emails():
    try:
        response = requests.get(MAILHOG_API)
        response.raise_for_status()
        return response.json().get("items", [])
    except Exception as e:
        print(f"Error fetching from MailHog: {e}")
        return []

def extract_fields(item):
    sender = item['Content']['Headers'].get('From', ['unknown@example.com'])[0]
    subject = item['Content']['Headers'].get('Subject', [''])[0]
    body = item['Content']['Body']
    time_received = datetime.datetime.now()  # Approximate
    return sender, subject, body, time_received

def main():
    print("📡 Email monitoring started. Watching for new messages in MailHog...")
    while True:
        emails = fetch_emails()
        for item in emails:
            msg_id = item['ID']
            if msg_id not in seen_ids:
                seen_ids.add(msg_id)

                sender, subject, body, time_received = extract_fields(item)
                print(f"\n📨 New Email from: {sender}")
                print(f"Subject: {subject}")
                
                result = analyze_email(
                    email_id=sender,
                    subject=subject,
                    body=body,
                    time_received=time_received
                )
                print(f"🛡️  Analysis Result: {result}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
