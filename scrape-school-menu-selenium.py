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

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

# Create a stream handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)

isWriteToFile = True
isWriteToDatabase = True

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
driver.get('https://www.myschoolmenus.com/organizations/610/sites/10194/menus/47941')
# driver.get('http://127.0.0.1:5500/test3.html')

# hard code school 
school = School('TestSchool', [])

monthName = driver.find_element(By.CLASS_NAME, 'msm-calender-month').text
logging.info("month = %s", monthName)  # Fix: Add '%s' to format the log message
month = Month(monthName, [])
school.months.append(month)

# Find the divs with class 'menu-day-wrapper'
day_wrappers = driver.find_elements(By.CLASS_NAME, 'menu-day-wrapper')

# Print the text of each div
for day_text in day_wrappers:
    logging.info("day.text = %s", day_text.text)
    day_parts = day_text.text.split("\n")
    if len(day_parts) > 1:
        day_of_month = day_parts[1]
        day_string = f"{day_of_month}"
        logging.info("day_string = %s", day_string)
        day = Day(day_string, [])
        month.days.append(day)      
    else:
        continue

    food_categories_and_food_items = day_text.find_elements(By.CLASS_NAME, 'menu-entrees')
    logging.info("food_categories_and_food_items = %s", food_categories_and_food_items)
   
    if(len(food_categories_and_food_items) == 0):
        continue

    food_categories_items = food_categories_and_food_items[0]
    food_array = food_categories_items.text.split("\n")
   
    if(food_array[0] in NO_SCHOOL_DAYS):
        continue
    # within day, find the category.item-data
    category_item_datas = day_text.find_elements(By.CLASS_NAME, 'category.item-data')

    food_category = []
    for food_text in food_array:
        logging.info("food_text = %s", food_text)
        if food_text in BREAK_FOOD_CATEGORIES:
            logging.info("food_category = %s", food_text)
            food_category = FoodCategory(food_text, [])
            day.foodCategories.append(food_category)
        else:
            logging.info("food_item = %s", food_text)
            food_item = FoodItem(food_text, [])
            food_category.foodItems.append(food_item)
    
# Close the browser
driver.quit()

if isWriteToFile:
    with open('school.json', 'w') as f:
        json.dump(school.to_dict(), f, indent=4)

    logging.info("School data written to school.json")

dict_bytes = json.dumps(school.to_dict()).encode()
hash_obj = hashlib.sha256(dict_bytes)
hash_hex = hash_obj.hexdigest()
logging.info(hash_hex)

if isWriteToDatabase:
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