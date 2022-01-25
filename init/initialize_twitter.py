from pymongo import MongoClient
import json
import os

MONGO_URI = os.getenv('MONGO_URI', None)
client = MongoClient(MONGO_URI)

with open("new_twitter.json", encoding="utf-8") as f:
    data = json.loads(f.read())
db = client['LINE-USERS']
collection = db['futomomo-collection']
collection.insert_many(data)

for c in collection.find():
    print(c)