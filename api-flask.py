from flask import Flask, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the MongoDB connection string from the .env file
mongodb_url = os.getenv('MONGODB_URL')

app = Flask(__name__)
app.config["MONGO_URI"] = mongodb_url
mongo = PyMongo(app)

# check if connection is successful
try:
    mongo.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("error: ", e)

@app.route('/schools/<school>/months/<month>/days/<day>/foodCategories', methods=['GET'])
def get_food_categories(school, month, day):
    try:
        school_data = mongo.db.school.find_one({"name": school})
        if not school_data:
            return jsonify({"error": "School not found"}), 404

        month_data = next((item for item in school_data['months'] if item["name"] == month), None)
        if not month_data:
            return jsonify({"error": "Month not found"}), 404

        day_data = next((item for item in month_data['days'] if item["name"] == day), None)
        if not day_data:
            return jsonify({"error": "Day not found"}), 404

        return jsonify(day_data['foodCategories'])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)