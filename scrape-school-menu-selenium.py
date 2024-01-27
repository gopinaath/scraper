from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from schema import FoodItem, AttributeCategory, FoodCategory, Day, Month, School
import hashlib

from pymongo import MongoClient
import logging

from dotenv import load_dotenv
import os

load_dotenv()


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')
# Create a stream handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Add the stream handler to the root logger
logging.getLogger('').addHandler(console)

#  Food categories and days
BREAK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Empty Calendar Day"]
NO_SCHOOL_DAYS = ["WINTER BREAK", "NO SCHOOL", "SCHOOL HOLIDAY", "MARTIN LUTHER KING DAY", "PRESIDENTS DAY", "SPRING BREAK", "MEMORIAL DAY", "LAST DAY OF SCHOOL"]
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

monthName = driver.find_element(By.CLASS_NAME, 'msm-calender-month').text
print("month = ", monthName)
month = Month(monthName, [])
school.months.append(month)

# Find the divs with class 'menu-day-wrapper'
day_wrappers = driver.find_elements(By.CLASS_NAME, 'menu-day-wrapper')

# Print the text of each div
for day_text in day_wrappers:
    print("day.text = ", day_text.text)
    day_parts = day_text.text.split("\n")
    day_of_week = day_parts[0]
    if len(day_parts) > 1:
        day_of_month = day_parts[1]
        day_string = f"{day_of_week}, {day_of_month}"
    else:
        day_string = day_of_week
    print("day_string = ", day_string)
    day = Day(day_string, [])
    month.days.append(day)

    food_categories_and_food_items = day_text.find_elements(By.CLASS_NAME, 'menu-entrees')
    print("food_categories_and_food_items = ", food_categories_and_food_items)
   
    if(len(food_categories_and_food_items) == 0):
        continue

    food_categories_items = food_categories_and_food_items[0]
    food_array = food_categories_items.text.split("\n")
   
    for item in food_array:
        if(item in NO_SCHOOL_DAYS):
            continue
        food_category_old = []
        food_item_old ={}
        # within day, find the category.item-data
        category_item_datas = day_text.find_elements(By.CLASS_NAME, 'category.item-data')
        for category_item_data in category_item_datas:
            print(category_item_data)
        
        current_food_category = ""
        is_new_food_category = False
        food_category = []
        for food_text in food_array:
            print("food_text = ", food_text)
            if food_text in BREAK_FOOD_CATEGORIES:
                print("food_category = ", food_text)
                food_category = FoodCategory(food_text, [])
                day.foodCategories.append(food_category)
            else:
                print("food_item = ", food_text)
                food_item = FoodItem(food_text, [])
                food_category.foodItems.append(food_item)
    
# Close the browser
driver.quit()

# print(school.to_dict)
# print(json.dumps(school.to_dict(), indent=4))
with open('school.json', 'w') as f:
    json.dump(school.to_dict(), f, indent=4)

print("School data written to school.json")

dict_bytes = json.dumps(school.to_dict()).encode()
hash_obj = hashlib.sha256(dict_bytes)
hash_hex = hash_obj.hexdigest()
print(hash_hex)


try:
    mongodb_url = os.getenv('MONGODB_URL')

    client = MongoClient(mongodb_url)
    db = client['your_database']
    collection = db['school']
    school_dict = school.to_dict()

    collection.insert_one(school_dict)

    logging.info("School data inserted into MongoDB")

except Exception as e:
    logging.error("An error occurred while inserting data into MongoDB: %s", str(e))
finally:
    client.close()

logging.info("Done")