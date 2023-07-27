import os
from msedge.selenium_tools import Edge, EdgeOptions

def check_sharepoint_links(sharepoint_url, edge_driver_path):
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--headless')  # Optional: Run Edge in headless mode (without GUI)
    options.add_argument('--ignore-ssl-errors=true')  # Ignore SSL certificate errors

    driver = Edge(executable_path=edge_driver_path, options=options)

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
    edge_driver_path = "PATH_TO_EDGE_WEBDRIVER"
    check_sharepoint_links(sharepoint_url, edge_driver_path)
