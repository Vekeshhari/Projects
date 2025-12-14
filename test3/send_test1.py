# send_test.py
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender="fake_ceo@company.com", receiver="user@example.com"):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # MailHog listens on localhost:1025
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)

# Example spoofed email with suspicious terms
send_email(
    subject="Urgent: Invoice Payment Required",
    body="Your account is overdue. Please transfer the funds immediately to avoid suspension. payment link: https://www.eicar.org/download/eicar.com.txt"
)
