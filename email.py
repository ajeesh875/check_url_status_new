import win32com.client as win32

def send_outlook_email_with_sensitivity(subject, body, recipient_email, sensitivity_level):
    try:
        # Connect to the running instance of Outlook
        outlook = win32.Dispatch('Outlook.Application')

        # Create a new email message
        email = outlook.CreateItem(0)  # 0 represents the MailItem type (email)

        # Set the email properties
        email.Subject = subject
        email.Body = body
        email.To = recipient_email

        # Access the PropertyAccessor object to modify the sensitivity property
        pa = email.PropertyAccessor

        # Sensitivity level values:
        # 0 = Normal, 1 = Personal, 2 = Private, 3 = Confidential
        sensitivity_values = {
            "Normal": 0,
            "Personal": 1,
            "Private": 2,
            "Confidential": 3
        }

        sensitivity_value = sensitivity_values.get(sensitivity_level, 0)
        pa.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x00360003", sensitivity_value)

        # Send the email
        email.Send()

        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

# Example usage
if __name__ == "__main__":
    subject = "Your Subject Here"
    body = "Your email content here."
    recipient_email = "recipient@example.com"
    sensitivity_level = "Confidential"  # Replace with the desired sensitivity level

    send_outlook_email_with_sensitivity(subject, body, recipient_email, sensitivity_level)
