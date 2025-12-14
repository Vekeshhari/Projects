# send_test.py
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender="fake_ce0@company.com", receiver="user@example.com"):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # MailHog listens on localhost:1025
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)

# Example spoofed email with suspicious terms
send_email(
    subject="Hello Ram",
    body="""
    <html>
        <body>
            <p>Your account is overdue.</p>
            <p>Please transfer the funds immediately to avoid suspension.</p>
            <p>Or use this short link: <a href="https://tinyurl.com/safadsecuenn">https://tinyurl.com/safadsecuenn</a></p>
        </body>
    </html>
    """
)
