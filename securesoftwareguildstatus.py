import requests
from bs4 import BeautifulSoup
from plyer import notification
import re

def get_menu_links(url):
    try:
        response = requests.get(url)
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
            print(f"Failed to retrieve menu links from {url}. Status code: {response.status_code}")
    except requests.ConnectionError:
        print(f"Failed to retrieve menu links from {url}. Connection error.")

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
            message=notification_message,
            timeout=5  # Display time for the notification in seconds
        )
    except requests.ConnectionError:
        notification_title = "Link Status"
        notification_message = f"The link {url} is unreachable."

        notification.notify(
            title=notification_title,
            message=notification_message,
            timeout=5  # Display time for the notification in seconds
        )

# Example usage
website_url = "https://www.example.com"

# Get menu links from the website
menu_links = get_menu_links(website_url)

if menu_links:
    print(f"Total menu links found: {len(menu_links)}")
    print("Checking link status...")
    for link in menu_links:
        check_link_status(link)
else:
    print("No menu links found on the website.")
