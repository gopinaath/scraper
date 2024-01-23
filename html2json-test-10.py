from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json

# Setup webdriver
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# Open the local HTML file
driver.get("file:///D:/dev/wrksp/school-menu/scraper/test.html")

# Initialize the main dictionary
data = {}

# Add schoolName
data["schoolName"] = "Sample School"

# Initialize months as an empty list
data["months"] = []

# Create a new month
month = {}
month["monthName"] = "January"

# Initialize days in the month as an empty list
month["days"] = []

# Find the menu-day-wrapper elements
menu_day_wrappers = driver.find_elements(By.CLASS_NAME, "menu-day-wrapper")

# Loop through the menu-day-wrapper elements
for menu_day_wrapper in menu_day_wrappers:
    # Create a new day
    day = {}
    day["day"] = int(menu_day_wrapper.find_element(By.CLASS_NAME, "calendar-day").text)

    # Initialize foodCategories in the day as an empty list
    day["foodCategories"] = []

    # Find the menu-entrees element
    menu_entrees = menu_day_wrapper.find_element(By.CLASS_NAME, "menu-entrees")

    # Find the category item-data elements
    category_item_datas = menu_entrees.find_elements(By.CLASS_NAME, "category.item-data")

    # Loop through the category item-data elements
    for category_item_data in category_item_datas:
        # Create a new food category
        food_category = {}
        food_category["categoryName"] = category_item_data.get_attribute("id")

        # Initialize foodItems in the food category as an empty list
        food_category["foodItems"] = []

        # Find the recipe item-data elements
        recipe_item_datas = category_item_data.find_elements(By.CLASS_NAME, "recipe.item-data")

        # Loop through the recipe item-data elements
        for recipe_item_data in recipe_item_datas:
            # Create a new food item
            food_item = {}
            food_item["itemName"] = recipe_item_data.find_element(By.CLASS_NAME, "pop").get_attribute("title")

            # Add the food item to the food category
            food_category["foodItems"].append(food_item)

        # Add the food category to the day
        day["foodCategories"].append(food_category)

    # Add the day to the month
    month["days"].append(day)

# Add the month to the data
data["months"].append(month)

# Convert the dictionary to a JSON string
json_data = json.dumps(data, indent=4)

# Write the JSON string to a file
with open('output.json', 'w') as f:
    f.write(json_data)

# Close the browser
driver.quit()