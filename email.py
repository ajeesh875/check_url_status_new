import win32com.client as win32

def send_outlook_email_with_label(subject, body, recipient_email, label):
    try:
        # Connect to the running instance of Outlook
        outlook = win32.Dispatch('Outlook.Application')

        # Create a new email message
        email = outlook.CreateItem(0)  # 0 represents the MailItem type (email)

        # Set the email properties
        email.Subject = subject
        email.Body = body
        email.To = recipient_email

        # Set the label (category) of the email
        email.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/string/{00020329-0000-0000-C000-000000000046}/Keywords", label)

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
    label = "Public"  # Replace with the desired label

    send_outlook_email_with_label(subject, body, recipient_email, label)
