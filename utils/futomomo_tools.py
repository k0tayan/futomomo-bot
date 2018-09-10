import flickrapi
import random
from utils.config import Config
from  utils.objects import Futomomo
import os

class FutomomoTool(Config):
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))

    def get_url_from_label(self, label, sizes):
        for size in sizes:
            if size["label"] == label:
                return size["source"]
        return None

    def get_random_futomomo(self):
        # photos = self.flicker.photos_search(user_id=self.yuria_user_id, per_page=self.per_page)['photos']['photo']
        # photo_sets = self.flicker.photosets.getPhotos(photoset_id=self.fetish_id, user_id=self.yuria_user_id, page=1)["photoset"]["photo"]
        # photo_sets.append(self.flicker.photosets.getPhotos(photoset_id=self.fetish_id, user_id=self.yuria_user_id, page=2)["photoset"]["photo"])
        # photo = random.choice(photo_sets)
        # title, farm, server, _id, secret = photo['title'], str(photo["farm"]), photo["server"], photo["id"], photo["secret"]
        # sizes = self.flicker.photos.getSizes(photo_id=_id)['sizes']['size']
        # url = self.get_url_from_label("Medium", sizes)
        # url = f"https://farm{str(farm)}.static.flickr.com/{server}/{_id}_{secret}.jpg"
        # largest_url = sizes.pop()["source"]
        # square_url = self.get_url_from_label("Square", sizes)
        urls = open(f"{self.path}/urls.txt", 'r').read().split('\n')
        photo = random.choice(urls).split(' ')
        return Futomomo(photo[0], photo[1], photo[2])

