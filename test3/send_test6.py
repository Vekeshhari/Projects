import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, sender="admin@example.com", receiver="user@example.com"):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # HTML body with a simulated download link
    html_body = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Download File Example</title>
    </head>
    <body>
      <h2>Download a file</h2>
      <p>
        <a href="https://all-free-download.com/?a=G&g=DL&id=6936215" download>Download PDF</a>
      </p>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    # Send email through MailHog (localhost:1025)
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)
        print("📨 HTML email with download link sent.")

# Call the function
send_email("📄 Download File Example")
