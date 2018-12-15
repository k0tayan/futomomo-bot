from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['LINE-USERS']
collection = db['user-collection']
users = collection.find()
if users.count():
    print('found')
else:
    print('not found')
for user in users:
    print(user)