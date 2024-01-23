import requests
from bs4 import BeautifulSoup

def scrape_menu():
    url = "https://www.myschoolmenus.com/organizations/610/sites/10194/menus/47941"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the food items on the page. This will depend on the structure of the webpage.
    # Here, I'm assuming that each food item is in a div with class 'food-item'.
    # You may need to inspect the webpage and adjust this to match its actual structure.
    food_items = soup.find_all('div', class_='menu-day-wrapper')

    for item in food_items:
        print(item.get_text())

scrape_menu()

