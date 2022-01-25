import json
from utils.futomomo_tools import FutomomoTool
from linebot.models import (
    FlexSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction
)


class FlexCreator(FutomomoTool):
    def __init__(self):
        super().__init__()

    def __get_json_object(self, path, replace=None):
        with open(path, 'r', encoding='utf-8') as f:
            raw_flex = f.read()
        if replace:
            for r in replace:
                raw_flex = raw_flex.replace(r, replace[r])
        flex = json.loads(raw_flex, strict=False)
        return flex

    def create_normal_futomomo(self):
        flex = self.__get_json_object('./template/flex_normal_futomomo.json')
        for i in range(5):
            bubble = self.__get_json_object('./template/carousel_contents.json')
            futomomo = self.get_random_futomomo()
            bubble["hero"]["url"] = futomomo.url
            for content in bubble["footer"]["contents"]:
                if content["action"]["label"] == "Get":
                    content["action"]["data"] = f"get: {futomomo.url} {futomomo.high_quality_url}"
            flex["contents"].append(bubble)
        return FlexSendMessage(alt_text='ふともも', contents=flex, quick_reply=self.create_quick_reply())

    def create_help_message(self):
        flex = self.__get_json_object('./template/flex_new_help_message.json')
        url = self.get_random_new_futomomo().twitter_image_url
        flex["hero"]["url"] = url
        flex["hero"]["action"]["uri"] = url
        return FlexSendMessage(alt_text='ヘルプ', contents=flex, quick_reply=self.create_quick_reply())

    def create_quick_reply(self):
        return QuickReply(items=[
            QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="ヘルプ", text="ヘルプ")),
            QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="ふともも", text="ふともも")),
            # QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="いっぱい", text="いっぱい")),
            # QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="ぱんちら", text="ぱんちら")),
            # QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="おっぱい", text="おっぱい"))
        ])

    def create_profile(self, profile, count, authority):
        flex = self.__get_json_object('./template/flex_profile.json',
                                      {'INSERT_ICON_URL':profile.picture_url,
                                       'INSERT_NAME':profile.display_name,
                                       'INSERT_UserID':profile.user_id,
                                       'INSERT_COUNT':str(count),
                                       'INSERT_AUTHORITY':str(authority)})
        return FlexSendMessage(alt_text='profile', contents=flex, quick_reply=self.create_quick_reply())

    def create_max_count_user(self, profile, count):
        flex = self.__get_json_object('./template/flex_max_count.json',{
            'INSERT_ICON_URL': profile.picture_url,
            'INSERT_NAME': profile.display_name,
            'INSERT_COUNT': str(count) + '回',
        })
        return FlexSendMessage(alt_text='max', contents=flex, quick_reply=self.create_quick_reply())

    def create_new_futomomo(self, string=None):
        if string:
            futomomo = self.search_futomomo(string)
            if futomomo is None:
                return None
        else:
            futomomo = self.get_random_new_futomomo()
        futomomo.text = '-' + futomomo.text + '-'
        flex = self.__get_json_object('./template/carousel_fb_twitter.json', {
            'TWITTER_TEXT':futomomo.text,
            'TWITTER_IMAGE_URL':futomomo.twitter_image_url
        })
        if futomomo.twitter_id_for_model != '':
            flex["contents"][1]["body"]["contents"].append({
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": futomomo.twitter_id_for_model,
                    "uri": futomomo.twitter_url_for_model
                },
                "style": "primary",
                "color": "#F1789B",
                "margin": "md"
            })
        flex["contents"][1]["body"]["contents"].append({
            "type": "button",
            "action": {
                "type": "uri",
                "label": "ふとももbot",
                "uri": futomomo.twitter_url
            },
            "style": "primary",
            "color": "#1DA1F2"
        })
        return FlexSendMessage(alt_text="ふともも", contents=flex, quick_reply=self.create_quick_reply())
