class FoodItem:
    def __init__(self, itemName, attributeCategories):
        self.itemName = itemName
        self.attributeCategories = attributeCategories

    def to_dict(self):
        return {
            'itemName': self.itemName,
            'attributeCategories': [ac.to_dict() for ac in self.attributeCategories]
        }

class AttributeCategory:
    def __init__(self, attributeCategoryName, attributeCategoryValue):
        self.attributeCategoryName = attributeCategoryName
        self.attributeCategoryValue = attributeCategoryValue

    def to_dict(self):
        return {
            'attributeCategoryName': self.attributeCategoryName,
            'attributeCategoryValue': self.attributeCategoryValue
        }

class FoodCategory:
    def __init__(self, categoryName, foodItems):
        self.categoryName = categoryName
        self.foodItems = foodItems

    def to_dict(self):
        return {
            'categoryName': self.categoryName,
            'foodItems': [fi.to_dict() for fi in self.foodItems]
        }

class Day:
    def __init__(self, day, foodCategories):
        self.day = day
        self.foodCategories = foodCategories

    def to_dict(self):
        return {
            'day': self.day,
            'foodCategories': [fc.to_dict() for fc in self.foodCategories]
        }

class Month:
    def __init__(self, monthName, days):
        self.monthName = monthName
        self.days = days

    def to_dict(self):
        return {
            'monthName': self.monthName,
            'days': [d.to_dict() for d in self.days]
        }

class School:
    def __init__(self, schoolName, months):
        self.schoolName = schoolName
        self.months = months

    def to_dict(self):
        return {
            'schoolName': self.schoolName,
            'months': [m.to_dict() for m in self.months]
        }