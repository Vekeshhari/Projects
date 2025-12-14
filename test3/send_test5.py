# send_test.py
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender="fake_ceo@company.com", receiver="user@example.com"):
    msg = MIMEText(body, "html")  # Use "html" to allow clickable links and formatting
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)

send_email(
    subject="Urgent: Invoice Payment Required",
    body="""
    <html>
        <body>
            <p>Your account is overdue.</p>
            <p>Please transfer the funds immediately to avoid suspension.</p>
            <p>Click here to <a href="https://www.eicar.org/download/eicar.com.txt">https://secure-payment.com</a></p>
            <p>Or use this short link: <a href="https://tinyurl.com/safadsecuenn">https://tinyurl.com/safadsecuenn</a></p>
        </body>
    </html>
    """
)
