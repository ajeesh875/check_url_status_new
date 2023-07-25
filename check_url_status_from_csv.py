import requests
from bs4 import BeautifulSoup
from plyer import notification
import re
import win32cred
from requests_ntlm import HttpNtlmAuth  # Import HttpNtlmAuth from requests_ntlm library

def get_credential(target_name):
    try:
        credential = win32cred.CredRead(target_name, win32cred.CRED_TYPE_GENERIC)
        return credential['UserName'], credential['CredentialBlob'].decode()
    except win32cred.error as e:
        print(f"Failed to read credentials from Windows Credential Manager: {e}")
        return None, None

def get_menu_links(site_url, username, password):
    try:
        response = requests.get(site_url, auth=HttpNtlmAuth(username, password))
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            menu_links = []
            button_wrapper = soup.find("div", class_="buttonwrapper")
            if button_wrapper:
                buttons = button_wrapper.find_all("button")
                for button in buttons:
                    onclick_value = button.get("onclick")
                    if onclick_value:
                        url_match = re.search(r"'(https?://[^']*)'", onclick_value)
                        if url_match:
                            menu_links.append(url_match.group(1))
            return menu_links
        else:
            print(f"Failed to retrieve menu links from {site_url}. Status code: {response.status_code}")
            return []

    except requests.ConnectionError:
        print(f"Failed to retrieve menu links from {site_url}. Connection error.")
        return []

def check_link_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            notification_title = "Link Status"
            notification_message = f"The link {url} is up and running."
        else:
            notification_title = "Link Status"
            notification_message = f"The link {url} is down with status code {response.status_code}."

        notification.notify(
            title=notification_title,
            message=str(notification_message),  # Ensure notification_message is a string
            timeout=5  # Display time for the notification in seconds
        )
    except requests.ConnectionError:
        notification_title = "Link Status"
        notification_message = f"The link {url} is unreachable."

        notification.notify(
            title=notification_title,
            message=str(notification_message),  # Ensure notification_message is a string
            timeout=5  # Display time for the notification in seconds
        )

# Example usage
site_url = "https://lbg.sharepoint.com/sites/shared%20Documents"
username = "your_sharepoint_username"
password = "your_sharepoint_password"

# Get menu links from the SharePoint site
menu_links = get_menu_links(site_url, username, password)

if menu_links:
    print(f"Total menu links found: {len(menu_links)}")
    print("Checking link status...")
    for link in menu_links:
        check_link_status(link)
else:
    print("No menu links found on the SharePoint site.")
