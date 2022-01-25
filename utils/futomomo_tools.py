import random
from utils.config import Config
from utils.objects import Futomomo, NewFutomomo
from utils.db import DB
import os

PANTIRA_RANGE_MIN = 1
PANTIRA_RANGE_MAX = 73

OPI_RANGE_MIN = 1
OPI_RANGE_MAX = 84

class FutomomoTool(Config, DB):
    def __init__(self):
        super().__init__()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.futomomo_collection = self.db['futomomo-collection']

    def get_url_from_label(self, label, sizes):
        for size in sizes:
            if size["label"] == label:
                return size["source"]
        return None

    def get_random_futomomo(self):
        urls = open(f"{self.path}/urls.txt", 'r').read().split('\n')
        photo = random.choice(urls).split(' ')
        return Futomomo(photo[0], photo[1], photo[2])

    def get_random_pantira_url(self):
        index = random.choice(range(PANTIRA_RANGE_MIN, PANTIRA_RANGE_MAX+1))
        return f"https://s3-ap-northeast-1.amazonaws.com/futomomo/pantira/{index}_pantira.jpg"

    def get_random_opi_url(self):
        index = random.choice(range(OPI_RANGE_MIN, OPI_RANGE_MAX + 1))
        return f"https://s3-ap-northeast-1.amazonaws.com/futomomo/opi/{index}_opi.jpg"

    def get_random_new_futomomo(self):
        data = list(self.futomomo_collection.aggregate([{ "$sample": { "size": 1 }}]))[0]
        # index = random.randint(0, self.futomomo_collection.count()-1)
        # data = self.futomomo_collection.find()[index]
        return NewFutomomo(text=data["text"], twitter_url=data["data"]["url"], twitter_image_url=data["image_url"],
                           twitter_id_for_model=data["data"]["id"])

    def search_futomomo(self, string):
        futomomos = list(self.futomomo_collection.aggregate([{"$match":{"$or": [{'text': {'$regex': string}}, {"tag": {"$in": [string]}}]}},{ "$sample": { "size": 1 }}]))
        if len(futomomos) > 0:
            data = futomomos[0]
            return NewFutomomo(text=data["text"], twitter_url=data["data"]["url"], twitter_image_url=data["image_url"],
                               twitter_id_for_model=data["data"]["id"])
        else:
            return None
        # futomomos =  self.futomomo_collection.find(filter={"$or": [{'text': {'$regex': string}}, {"tag": {"$in": [string]}}]})
        # if futomomos.count():
        #    index = random.randint(0, futomomos.count()-1)
        #    data = futomomos[index]
        #    return NewFutomomo(text=data["text"], twitter_url=data["data"]["url"], twitter_image_url=data["image_url"],
        #                       twitter_id_for_model=data["data"]["id"])


