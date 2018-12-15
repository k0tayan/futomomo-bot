from pymongo import MongoClient

ADMIN = 100
ADMINISTRATOR = ["Uc45442e19e3f8326fc321e828003f710", "U1e73ade0030068a7f41e05e72fd54418"]

class CommandHandler:
    def __init__(self):
        pass

class CommandChecker:
    def __init__(self):

        # database
        client = MongoClient('localhost', 27017)
        db = client['LINE-USERS']
        self.collection = db['user-collection']

    def new_user(self, user_id, count=1, authority=0):
        self.collection.insert({'user_id': user_id, 'count': count, 'authority': authority})

    def count_up(self, user_id):
        users = self.collection.find({'user_id':user_id})
        if users.count():
            for user in users:
                self.collection.update({'user_id': user_id}, {'$set': {'count': user['count']+1}})
        else:
            self.new_user(user_id)

    def get_count(self, user_id):
        users = self.collection.find({'user_id':user_id})
        if users.count():
            for user in users:
                return user['count']
        else:
            self.new_user(user_id)
            return 1

    def check_authority(self, user_id, level=100):
        if user_id in ADMINISTRATOR:
            return True
        else:
            users = self.collection.find({'user_id': user_id, 'authority':{'$gte' :level}})
            if users.count():
                return True
            else:
                return False

    def update_authority(self, user_id, level):
        if user_id in ADMINISTRATOR:
            return False
        users = self.collection.find({'user_id': user_id})
        if users.count():
            self.collection.update({'user_id':user_id}, {'$set': {'authority':level}})
            return True
        else:
            self.new_user(user_id, count=1, authority=level)
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
