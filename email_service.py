import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "sensordiagnostic@gmail.com"
SENDER_PASSWORD = "zyav zdag xbbw qvxx"
RECEIVER_EMAIL = "mahesh3500j@gmail.com"

def load_sensor_details(sensor_name):
    try:
        with open("sensors.yaml", "r") as file:
            data = yaml.safe_load(file)

        for sensor in data.get("sensors", []):
            if sensor.get("label") == sensor_name:
                return sensor
    except Exception as e:
        print("YAML read error:", e)

    return None


def make_bar(label, value, total=100, width=20):
    filled = int((value / total) * width)
    empty = width - filled
    return f"{label:<18}: [{'█' * filled}{'-' * empty}] {value}%"


def make_graph(graph_data):
    return "\n".join(make_bar(label, value) for label, value in graph_data.items())


def build_email_body(sensor_name, reason, prediction=None):
    sensor_data = load_sensor_details(sensor_name)

    if not sensor_data:
        return f"""
Vehicle Monitoring Alert

Sensor Name   : {sensor_name}
Current Status: FAILED
Failure Reason: {reason}

No YAML data found for this sensor.
Please check sensors.yaml mapping.
"""

    severity = sensor_data.get("severity", "UNKNOWN")
    next_failures = sensor_data.get("next_failures", ["Unknown risk"])
    action = sensor_data.get("action", "Check manually")
    graph = sensor_data.get("graph", {"General Risk": 60})

    next_failures_text = "\n".join(f"- {item}" for item in next_failures)
    graph_text = make_graph(graph)

    prediction_block = ""
    if prediction is not None:
        prediction_block = f"""
--------------------------------------------------
ML PREDICTION
--------------------------------------------------
Predicted Status: {prediction}
"""

    body = f"""
🚨 VEHICLE DIAGNOSTIC ALERT 🚨

Dear Vehicle Owner,

A fault has been detected by the Vehicle Monitoring System.

--------------------------------------------------
SENSOR STATUS REPORT
--------------------------------------------------
Sensor Name   : {sensor_name}
Current Status: FAILED
Severity Level: {severity}
Failure Reason: {reason}
{prediction_block}
--------------------------------------------------
POSSIBLE NEXT AFFECTED PARTS
--------------------------------------------------
{next_failures_text}

--------------------------------------------------
SYSTEM HEALTH INDICATORS
--------------------------------------------------
{graph_text}

--------------------------------------------------
RECOMMENDED ACTION
--------------------------------------------------
{action}

--------------------------------------------------
PROJECT INTELLIGENCE NOTE
--------------------------------------------------
This alert is sent only after the sensor actually fails.
The message also shows possible related failures
based on the YAML configuration of the failed sensor.

Please check your vehicle immediately to avoid
further damage.

Regards,
Smart Vehicle Monitoring and Diagnostic Alert System
"""
    return body


def send_email_alert(sensor_name, reason, prediction=None):
    subject = f"Vehicle Alert: {sensor_name} Failure Detected"
    body = build_email_body(sensor_name, reason, prediction)

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
        print(f"✅ Email alert sent for {sensor_name}")
    except Exception as e:
        print("❌ Email sending failed:", e)