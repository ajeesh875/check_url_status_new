import os
import browser_cookie3
from selenium import webdriver

def get_chrome_cookies():
    chrome_cookies = browser_cookie3.chrome()
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
    sharepoint_url = "YOUR_SHAREPOINT_URL"
    check_sharepoint_links(sharepoint_url)
