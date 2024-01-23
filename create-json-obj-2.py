import json
from schema import FoodItem, AttributeCategory, FoodCategory, Day, Month, School

# Create the classes from the JSON data
def create_classes(data):
    school = School(data['schoolName'], [])

    for month_data in data['months']:
        month = Month(month_data['monthName'], [])
        school.months.append(month)

        for day_data in month_data['days']:
            day = Day(day_data['day'], [])
            month.days.append(day)

            for food_category_data in day_data['foodCategories']:
                food_category = FoodCategory(food_category_data['categoryName'], [])
                day.foodCategories.append(food_category)

                for food_item_data in food_category_data['foodItems']:
                    food_item = FoodItem(food_item_data['itemName'], [])
                    food_category.foodItems.append(food_item)

                    for attribute_category_data in food_item_data['attributeCategories']:
                        attribute_category = AttributeCategory(attribute_category_data['attributeCategoryName'], attribute_category_data['attributeCategoryValue'])
                        food_item.attributeCategories.append(attribute_category)

    return school

# Load the JSON data
with open('json-sample-3.json') as f:
    data = json.load(f)
school = create_classes(data)
print(school.to_dict)
print(json.dumps(school.to_dict(), indent=4))