
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the MongoDB connection string from the .env file
uri = os.getenv('MONGODB_URL')

# uri = "mongodb+srv://food10:rwlqFtjKtCQ3Z3n5@test10.jf4yy8v.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)