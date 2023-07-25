from office365.sharepoint.client_context import ClientContext

# Replace these values with your SharePoint URL, username, and password
sharepoint_url = "https://your-sharepoint-site-url.com"
username = "your_username"
password = "your_password"

ctx = ClientContext(sharepoint_url)
ctx.with_user_credentials(username, password)

web = ctx.web.get().execute_query()
print(web.url)
