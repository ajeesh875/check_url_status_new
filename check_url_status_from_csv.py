import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from plyer import notification
import re

def get_menu_links(site_url, client_id, client_secret, tenant_id):
    try:
        ctx_auth = AuthenticationContext(f"https://login.microsoftonline.com/{tenant_id}")
        if ctx_auth.acquire_token_for_client(client_id, client_secret):
            ctx = ClientContext(site_url, ctx_auth)
            web = ctx.web
            ctx.load(web)
            ctx.execute_query()

            menu_links = []
            list_title = "Shared Documents"  # Replace with the name of your SharePoint list
            list_obj = ctx.web.lists.get_by_title(list_title)
            ctx.load(list_obj)
            ctx.execute_query()

            list_items = list_obj.get_items()
            ctx.load(list_items)
            ctx.execute_query()

            for item in list_items:
                menu_links.append(item["FileRef"])

            return menu_links
        else:
            print("Failed to authenticate with SharePoint.")
            return []

    except Exception as e:
        print(f"Failed to retrieve menu links from {site_url}. Error: {e}")
        return []

def check_link_status(url):
    try:
        link_status = "Link Status"
        response = requests.get(url)
        if response.status_code == 200:
            notification_title = link_status
            notification_message = f"The link {url} is up and running."
        else:
            notification_title = link_status
            notification_message = f"The link {url} is down with status code {response.status_code}."

        notification.notify(
            title=notification_title,
            message=str(notification_message),  # Ensure notification_message is a string
            timeout=5  # Display time for the notification in seconds
        )
    except requests.ConnectionError:
        notification_title = link_status"
        notification_message = f"The link {url} is unreachable."

        notification.notify(
            title=notification_title,
            message=str(notification_message),  # Ensure notification_message is a string
            timeout=5  # Display time for the notification in seconds
        )

# Example usage
site_url = "https://lbg.sharepoint.com/sites/shared%20Documents"
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"

# Get menu links from the SharePoint site
menu_links = get_menu_links(site_url, client_id, client_secret, tenant_id)

if menu_links:
    print(f"Total menu links found: {len(menu_links)}")
    print("Checking link status...")
    for link in menu_links:
        check_link_status(link)
else:
    print("No menu links found on the SharePoint site.")
