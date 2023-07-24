import requests
import time
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender_email, receiver_email, password):
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def check_website_status(url, interval, sender_email, receiver_email, password):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                message = f"The website {url} is up and running."
            else:
                message = f"The website {url} is down with a status code: {response.status_code}."
        except requests.ConnectionError:
            message = f"The website {url} is unreachable."

        send_email("Website Status", message, sender_email, receiver_email, password)
        time.sleep(interval)

# Example usage
check_website_status("https://www.bbc.com/news", 5, "ajeesh875@gmail.com", "ajeeshmukaluvila@gmail.com", "qngjzknnyeofccxm")
