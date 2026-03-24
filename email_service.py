import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "sensordiagnostic@gmail.com"
SENDER_PASSWORD = "zyav zdag xbbw qvxx"
RECEIVER_EMAIL = "mahesh3500j@gmail.com"

def send_email_alert(sensor_name, reason):
    subject = f"Vehicle Alert: {sensor_name} Failure Detected"
    body = f"""
Alert from Vehicle Monitoring System

Sensor: {sensor_name}
Status: FAILED
Reason: {reason}

Please check your vehicle immediately.
"""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"Email alert sent for {sensor_name}")
    except Exception as e:
        print("Email sending failed:", e)