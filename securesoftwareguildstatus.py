from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

def check_sharepoint_links(sharepoint_url, msedge_driver_path):
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--headless')  # Optional: Run Edge in headless mode (without GUI)
    options.add_argument('--ignore-ssl-errors=true')  # Ignore SSL certificate errors

    driver = webdriver.Edge(executable_path=msedge_driver_path, options=options)

    try:
        driver.get(sharepoint_url)
        button_wrappers = driver.find_elements_by_css_selector('.buttonwrapper')

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
    msedge_driver_path = "PATH_TO_MS_EDGE_WEBDRIVER"  # Provide the path to the Microsoft Edge WebDriver executable
    check_sharepoint_links(sharepoint_url, msedge_driver_path)
