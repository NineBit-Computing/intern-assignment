import smtplib
from email.mime.text import MIMEText

def send_summary_email(to_email, content_dict):
    body = "\n".join(f"{k}: {v}" for k, v in content_dict.items())

    msg = MIMEText(body)
    msg["Subject"] = "📥 Your CIQ Summary"
    msg["From"] = "your@email.com"
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("your@email.com", "your_app_password")
        server.send_message(msg)
