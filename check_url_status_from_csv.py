import csv
import requests
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

def check_website_status(csv_file, sender_email, receiver_email, password):
    website_status_list = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            website_url = row[0]
            try:
                response = requests.get(website_url)
                if response.status_code == 200:
                    status = f"The website {website_url} is up and running."
                else:
                    status = f"The website {website_url} is down with a status code: {response.status_code}."
            except requests.ConnectionError:
                status = f"The website {website_url} is unreachable."
            
            website_status_list.append(status)

    email_body = "\n".join(website_status_list)
    send_email("Website Status Update", email_body, sender_email, receiver_email, password)

# Example usage
def main():
    csv_file = 'websites.csv'
    sender_email = 'sender@gmail.com'
    receiver_email = 'receiver@gmail.com'
    password = 'password here'

    check_website_status(csv_file, sender_email, receiver_email, password)

if __name__ == "__main__":
    main()
