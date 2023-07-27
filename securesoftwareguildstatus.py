from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_sharepoint_links(sharepoint_url, msedge_driver_path):
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--headless')  # Optional: Run Edge in headless mode (without GUI)
    options.add_argument('--ignore-ssl-errors=true')  # Ignore SSL certificate errors

    service = EdgeService(executable_path=msedge_driver_path)
    driver = webdriver.Edge(service=service, options=options)

    try:
        driver.get(sharepoint_url)

        # Wait for button wrappers to be present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.buttonwrapper')))
        button_wrappers = driver.find_elements(By.CSS_SELECTOR, '.buttonwrapper')

        for wrapper in button_wrappers:
            # Wait for buttons to be present within the wrapper
            buttons = WebDriverWait(wrapper, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
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
    msedge_driver_path = "PATH_TO_MS_EDGE_WEBDRIVER"  # Provide the path to the Microsoft Edge WebDriver executable
    check_sharepoint_links(sharepoint_url, msedge_driver_path)
