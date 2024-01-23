from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from schema import FoodItem, AttributeCategory, FoodCategory, Day, Month, School

#  Food categories and days
BREAK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Empty Calendar Day"]
NO_SCHOOL_DAYS = ["WINTER BREAK", "NO SCHOOL", "MARTIN LUTHER KING DAY", "PRESIDENTS DAY", "SPRING BREAK", "MEMORIAL DAY", "LAST DAY OF SCHOOL"]
BREAK_FOOD_CATEGORIES = ["Lunch Entree", "Vegetables", "Fruit", "Milk"]

# Setup webdriver
webdriver_service = Service(ChromeDriverManager().install())

# Add options to ignore SSL errors
options = Options()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(service=webdriver_service, options=options)

# Navigate to the webpage
# driver.get('https://www.myschoolmenus.com/organizations/610/sites/10194/menus/47941')
driver.get('http://127.0.0.1:5500/test3.html')

# hard code school 
school = School('TestSchool', [])

month = driver.find_element(By.CLASS_NAME, 'msm-calender-month').text
print("month = ", month)

# Find the divs with class 'menu-day-wrapper'
day_wrappers = driver.find_elements(By.CLASS_NAME, 'menu-day-wrapper')


# Print the text of each div
for day in day_wrappers:
    print("day.text = ", day.text)


    food_categories_and_food_items = day.find_elements(By.CLASS_NAME, 'menu-entrees')
    print("food_categories_and_food_items = ", food_categories_and_food_items)
   
    if(len(food_categories_and_food_items) == 0):
        continue

    food_categories_items = food_categories_and_food_items[0]
    # TODO Continue here

    food_array = food_categories_items.text.split("\n")
   
    for item in food_array:
        if(item in NO_SCHOOL_DAYS):
            continue
        food_category = []
        food_item ={}
        # within day, find the category.item-data
        category_item_datas = day.find_elements(By.CLASS_NAME, 'category.item-data')
        for category_item_data in category_item_datas:
            print(category_item_data)
        
        current_food_category = ""
        for food_text in food_array:
            print("food_text = ", food_text)
            if food_text in BREAK_FOOD_CATEGORIES:
                print("food_category = ", food_text)

                # TODO continue from here
                food_category.append(food_text)
                current_food_category = food_text
                food_category["foodItems"] = []
            else:
                print("food_item = ", food_text)
                food_item.append = food_text
                food_category["foodItems"].append(food_text)
        # print JSON of day
        
    
# Close the browser
driver.quit()



"Tuesday\n09\nLunch Entree\nMac 'n' Cheese\nGrab 'n' Go Lunch\nVegetables\nFresh Fruit Variety\nFruit\nFresh Fruit Variety\nMilk\n1% Organic Milk, Unflavored\nFat Free Milk, Unflavored"