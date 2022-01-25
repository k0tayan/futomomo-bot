from pymongo import MongoClient
from utils.db import DB

ADMIN = 100
ADMINISTRATOR = ["Uc45442e19e3f8326fc321e828003f710", "U1e73ade0030068a7f41e05e72fd54418"]

class CommandHandler:
    def __init__(self):
        pass

class CommandChecker(DB):
    def __init__(self):
        super().__init__()
        # database
        self.user_collection = self.db['user-collection']

    def set_new_user(self, user_id, count=1, authority=0):
        self.user_collection.insert_one({'user_id': user_id, 'count': count, 'authority': authority})

    def get_user(self, user_id):
        user = self.user_collection.find_one({'user_id':user_id})
        return user

    def count_up(self, user_id):
        user = self.user_collection.find_one({'user_id':user_id})
        if user is not None:
            self.user_collection.update_one({'user_id': user_id}, {'$set': {'count': user['count']+1}})
        else:
            self.set_new_user(user_id)

    def get_count(self, user_id):
        user = self.get_user(user_id)
        if user is not None:
            return user['count']
        else:
            self.set_new_user(user_id)
            return 1

    def get_max_count_user(self):
        return self.user_collection.find_one(sort=[("count", -1)])

    def check_authority(self, user_id, level=100):
        if user_id in ADMINISTRATOR:
            return True
        else:
            user = self.get_user(user_id)
            return user["authority"] >= level

    def update_authority(self, user_id, level):
        if user_id in ADMINISTRATOR:
            return False
        user = self.get_user(user_id)
        if user is not None:
            self.user_collection.update_one({'user_id':user_id}, {'$set': {'authority':level}})
            return True
        else:
            self.set_new_user(user_id, count=1, authority=level)
            return True


    def equal_command(self, string, commands):
        for command in commands:
            if string == command:
                return True
        return False

    def include_command(self, string, commands):
        for command in commands:
            if command in string:
                return True
        return False
