import requests
from bs4 import BeautifulSoup

def get_bbc_navigation_menu():
    url = "https://www.bbc.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    menu_items = soup.find_all("li", class_="orb-nav-{menu_item}")
    navigation_menu = []

    for item in menu_items:
        navigation_menu.append(item.text.strip())

    return navigation_menu

# Example usage
bbc_menu = get_bbc_navigation_menu()
print(bbc_menu)