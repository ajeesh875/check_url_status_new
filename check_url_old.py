import requests
import time

def check_website_status(url, interval):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"The website {url} is up and running.")
            else:
                print(f"The website {url} is down with a status code: {response.status_code}.")
        except requests.ConnectionError:
            print(f"The website {url} is unreachable.")

        time.sleep(interval)

# Example usage
check_website_status("https://www.bbc.com/news", 10)  # Check every 60 seconds
