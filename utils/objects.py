class Futomomo:
    def __init__(self, url, high_quality_url, square_url):
        self.url = url
        self.high_quality_url = high_quality_url
        self.square_url = square_url

class NewFutomomo:
    def __init__(self, text, twitter_url, twitter_image_url, twitter_id_for_model):
        self.text = text
        self.twitter_url = twitter_url
        self.twitter_image_url = twitter_image_url
        self.twitter_id_for_model = twitter_id_for_model
        self.twitter_url_for_model = "https://twitter.com/" + twitter_id_for_model