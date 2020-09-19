from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)

with open("new_twitter.json") as f:
    data = json.loads(f.read())
db = client['LINE-USERS']
collection = db['futomomo-collection']
collection.insert_many(data)

for c in collection.find():
    print(c)