import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "sanjanagr633@gmail.com"     # your email
receiver_email = "sanjanagr633@gmail.com"   # recipient's email
password = "1234sa"           #  your email password

# Create the email content
subject = "⚠ Packet Sniffing Alert ⚠"
body = """
Suspicious activity detected: Your network traffic may be monitored.
Please check your connection security immediately to ensure safety.
real IP-192.168.1.113 spoofed by
fake IP-28:16:ad:c0:90:36

"""

# Set up the MIME message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

message.attach(MIMEText(body, "plain"))

# Send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use your SMTP server
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Alert email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
