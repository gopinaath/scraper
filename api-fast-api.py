from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import uvicorn
from bson.json_util import dumps
from bson import json_util
import json
from datetime import datetime, timedelta

from datetime import datetime, timedelta
import holidays

# Load the .env file
load_dotenv()

skip_to_next_working_day = True  

# Get the MongoDB connection string from the .env file
mongodb_url = os.getenv('MONGODB_URL')

# Create a new client and connect to the server
client = MongoClient(mongodb_url)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app = FastAPI()


@app.get('/schools/{school}/months/{month}/days/{day}/foodCategories')
async def get_food_categories(school: str, month: str, day: str):
    try:
        # Create a new client and connect to the server
        client = MongoClient(mongodb_url)

        # Get or create the 'school' collection
        school_collection = client.get_database('school').get_collection('menu')
        print("school_collection = ", school_collection)

        # # Now creating a Cursor instance 
        # # using find() function 
        # cursor = school_collection.find() 
        
        # # Converting cursor to the list  
        # # of dictionaries 
        # list_cur = list(cursor) 
        
        # # Converting to the JSON 
        # json_data = dumps(list_cur, indent = 2)  
        # print(json_data)

        school_data = school_collection.find_one({"schoolName": school})
        if not school_data:
            raise HTTPException(status_code=404, detail="School not found :"+school)

        # month_data = next((item for item in school_data['months'] if item['monthName'] == month), None)
        month_data = None
        for item in school_data['months']:
            if item['monthName'] == month:
                month_data = item
                break
        if not month_data:
            raise HTTPException(status_code=404, detail="Month not found")

        # day_data = next((item for item in month_data['days'] if item['name'] == day), None)
        day_data = None
        for item in month_data['days']:
            if item['day'] == day:
                day_data = item
                break
        if not day_data:
            raise HTTPException(status_code=404, detail="Day not found")

        return day_data['foodCategories']

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/schools')
async def get_all_schools():
    try:
        # Create a new client and connect to the server
        client = MongoClient(mongodb_url)

        # Get the 'school' collection
        school_collection = client.get_database('your_database').get_collection('school')

        # Get all documents in the collection
        schools_data = list(school_collection.find())

        # Close the client
        client.close()

        return json.loads(json_util.dumps(schools_data))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/schools/{school}/months/{month}/days/{day}')
async def get_day_data(school: str, month: str, day: str):
    try:
        # Create a new client and connect to the server
        client = MongoClient(mongodb_url)

        # Get the 'school' collection
        school_collection = client.get_database('your_database').get_collection('school')

        # Get the school data
        school_data = school_collection.find_one({"schoolName": school})
        if not school_data:
            raise HTTPException(status_code=404, detail="School not found")
        else:
            # Get the month data
            month_data = next((item for item in school_data['months'] if item["monthName"] == month), None)
            if not month_data:
                raise HTTPException(status_code=404, detail="Month not found")

            # Get the day data
            day_data = next((item for item in month_data['days'] if item["day"] == day), None)
            if not day_data:
                raise HTTPException(status_code=404, detail="Day not found")

        # Close the client
        client.close()

        return json.loads(json_util.dumps(day_data))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/schools/{school}/today')
async def get_menu_today(school: str):
    if skip_to_next_working_day:
        now = get_next_working_day()
    else:
        now = datetime.now()
    month = now.strftime('%B')
    date = str(now.day+1)
    print(f"Month: {month}, Date: {date}")
    menu_today = await get_day_data(school, month, date)
    return menu_today


def get_next_working_day():
    us_holidays = holidays.US()
    now = datetime.now()

    # If today is a holiday, get the next day
    if now in us_holidays:
        now += timedelta(days=1)

    # If the next day is a weekend, get the next weekday
    while now.weekday() > 4 or now in us_holidays:  # 0-4 corresponds to Monday-Friday
        now += timedelta(days=1)

    return now

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)