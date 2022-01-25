from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', None)
client = MongoClient(MONGO_URI)

data = [{'user_id':"Uc45442e19e3f8326fc321e828003f710", 'count':1, 'authority':100},
        {'user_id':"U1e73ade0030068a7f41e05e72fd54418", 'count':1, 'authority':100}
        ]
db = client['LINE-USERS']
collection = db['user-collection']
collection.insert_many(data)

for c in collection.find():
    print(c)