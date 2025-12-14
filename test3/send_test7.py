import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_to_mailhog(sender, recipient, subject, body):
    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))   # Use plain text: "plain"

    # Connect to MailHog SMTP
    smtp = smtplib.SMTP("localhost", 1025)

    # Send email
    smtp.sendmail(sender, [recipient], msg.as_string())

    smtp.quit()
    print("Email sent to MailHog!")


# Example usage
send_to_mailhog(
    sender="ramkumar@gmail.com",
    recipient="victim@example.com",
    subject="Urgent Payment Request",
    body="""
        <h3>Urgent Action Required</h3>
        Click the link below to verify your account:<br>
        <a href="https://www.eicar.org/download/eicar.com.txt">Verify Now</a>
    """
)
