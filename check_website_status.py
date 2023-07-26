from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_to_sharepoint(username, password):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # Replace 'your_sharepoint_login_url' with the actual login page URL
    login_url = 'your_sharepoint_login_url'
    driver.get(login_url)

    # Find and fill in the username and password fields
    username_field = driver.find_element_by_id('username_input_id')
    password_field = driver.find_element_by_id('password_input_id')

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    login_button = driver.find_element_by_id('login_button_id')
    login_button.click()

    # Add a sleep to allow the page to load after login (you can use WebDriverWait for more robust waits)
    time.sleep(5)
    return driver

def extract_links_from_sharepoint_page(driver):
    # Replace 'your_sharepoint_page_url' with the URL of the page you want to scrape
    page_url = 'your_sharepoint_page_url'
    driver.get(page_url)

    # Find all links on the page
    links = driver.find_elements_by_tag_name('a')

    # Extract and print the URLs
    for link in links:
        print(link.get_attribute('href'))

    driver.quit()

if __name__ == "__main__":
    username = "your_username"
    password = "your_password"

    driver = login_to_sharepoint(username, password)
    extract_links_from_sharepoint_page(driver)
