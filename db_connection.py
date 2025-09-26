from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["leafcareDB"]
collection = db["diseases"]

def get_disease_info(predicted_class):
    result = collection.find_one({"class": predicted_class})
    if result:
        return {
            "plant": result["plant"],
            "disease": result["disease"],
            "description": result["description"],
            "solution": result["solution"]
        }
    else:
        return None
