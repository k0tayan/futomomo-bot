from pymongo import MongoClient
import os

class DB:
    def __init__(self):
        # database
        MONGO_URI = os.getenv('MONGO_URI', None)
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['LINE-USERS']