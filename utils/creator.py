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

    def __get_json_object(self, path):
        raw_flex = open(path, 'r').read()
        flex = json.loads(raw_flex)
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
        flex = self.__get_json_object('./template/flex_help_message.json')
        url = self.get_random_futomomo().url
        flex["hero"]["url"] = url
        flex["hero"]["action"]["uri"] = url
        return FlexSendMessage(alt_text='ヘルプ', contents=flex, quick_reply=self.create_quick_reply())

    def create_quick_reply(self):
        return QuickReply(items=[
            QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="ヘルプ", text="ヘルプ")),
            QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="ふともも", text="ふともも")),
            QuickReplyButton(image_url=self.get_random_futomomo().square_url, action=MessageAction(label="いっぱい", text="いっぱい")),
        ])
