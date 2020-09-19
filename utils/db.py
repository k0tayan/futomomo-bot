from pymongo import MongoClient

class DB:
    def __init__(self):
        # database
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['LINE-USERS']