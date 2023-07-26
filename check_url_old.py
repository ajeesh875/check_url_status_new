from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
import re

def extract_links_from_sharepoint(url):
    # Set up the Edge options
    options = EdgeOptions()
    options.use_chromium = True

    # Set Edge options to run in headless mode (comment out the line below if you want to see the browser in action)
    options.add_argument('--headless')

    # Replace 'path/to/your/msedgedriver.exe' with the actual path to your Edge WebDriver executable
    edge_driver_path = 'path/to/your/msedgedriver.exe'

    # Initialize the WebDriver
    driver = webdriver.Edge(executable_path=edge_driver_path, options=options)

    # Open the SharePoint URL
    driver.get(url)

    try:
        # Find all elements with class name "buttonwrapper"
        button_wrappers = driver.find_elements_by_class_name("buttonwrapper")

        # Initialize a list to store the extracted links
        links = []

        # Loop through each "buttonwrapper" element
        for wrapper in button_wrappers:
            # Find all buttons within the current "buttonwrapper" element
            buttons = wrapper.find_elements_by_tag_name("button")

            # Extract the link URLs from the "onclick" attribute of each button
            for button in buttons:
                onclick_attribute = button.get_attribute("onclick")
                if onclick_attribute:
                    # Using regular expression to extract the URL from the onclick attribute
                    link_match = re.search(r'https?://\S+', onclick_attribute)
                    if link_match:
                        link = link_match.group()
                        links.append(link)

        # Close the browser
        driver.quit()

        return links

    except Exception as e:
        # If any exception occurs, close the browser and return an empty list
        driver.quit()
        return []

if __name__ == "__main__":
    sharepoint_url = "YOUR_SHAREPOINT_URL_HERE"
    extracted_links = extract_links_from_sharepoint(sharepoint_url)

    if extracted_links:
        print("Extracted links:")
        for link in extracted_links:
            print(link)
    else:
        print("No links were found.")
