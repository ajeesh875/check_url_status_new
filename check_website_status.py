import os
import browser_cookie3
from selenium import webdriver

def get_chrome_cookies():
    user_profile = os.path.expanduser("~")
    chrome_cookies_path = os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Network","Cookies")

    # Provide a destination path where you have write permissions
    destination_path = "C:/Python/projects/url_status_check_selenium"

    try:
        with open(chrome_cookies_path, 'rb') as src, open(destination_path, 'wb') as dest:
            dest.write(src.read())

    except Exception as e:
        print(f"Error copying cookies file: {e}")
        return []

    chrome_cookies = browser_cookie3.chrome(cookie_file=destination_path)
    os.remove(destination_path)
    return chrome_cookies

def set_chrome_cookies(driver, cookies):
    driver.get('about:blank')  # Open a blank page to set cookies
    for cookie in cookies:
        driver.add_cookie(cookie)

def check_sharepoint_links(sharepoint_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional: Run Chrome in headless mode (without GUI)

    driver = webdriver.Chrome(options=options)
    cookies = get_chrome_cookies()
    set_chrome_cookies(driver, cookies)

    try:
        driver.get(sharepoint_url)
        button_wrappers = driver.find_elements('css selector', '.buttonwrapper')

        for wrapper in button_wrappers:
            buttons = wrapper.find_elements('tag name', 'button')
            for button in buttons:
                onclick_attribute = button.get_attribute('onclick')
                if 'http' in onclick_attribute:
                    link_url = onclick_attribute.split("'")[1]
                    driver.get(link_url)
                    print(f"Link: {link_url} - Status: {driver.title}")
                else:
                    print("No link found in the button onclick attribute.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    sharepoint_url = "https://microsoft.sharepoint.com/_forms/default.aspx"
    check_sharepoint_links(sharepoint_url)
