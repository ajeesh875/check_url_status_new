from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def check_sharepoint_links(sharepoint_url, chrome_driver_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional: Run Chrome in headless mode (without GUI)

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(sharepoint_url)
        button_wrappers = driver.find_elements_by_class_name('buttonwrapper')

        for wrapper in button_wrappers:
            buttons = wrapper.find_elements_by_tag_name('button')
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
    chrome_driver_path = "PATH_TO_CHROME_WEBDRIVER"
    check_sharepoint_links(sharepoint_url, chrome_driver_path)
