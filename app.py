from __future__ import unicode_literals
from flask import Flask, request, abort
# from sanic import Sanic
# from sanic.response import text
# from sanic.exceptions import abort
from utils.command import CommandChecker
from utils.config import Config
from utils.creator import FlexCreator
from utils.futomomo_tools import FutomomoTool
import os
import json
import flickrapi
import random
import sys

from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, Base, TemplateSendMessage, FlexSendMessage, ImageSendMessage, PostbackEvent, QuickReply, FollowEvent,
JoinEvent
)

app = Flask(__name__)
# app = Sanic(__name__)

env = os.getenv('LINE_BOT', None)
if env == 'DEV':
    handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET_DEV', None))
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN_DEV', None))
elif env == 'RELEASE':
    handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None))
else:
    sys.exit()
# FLICKR_API_KEY = os.getenv('FLICKR_API_KEY', None)
# FLICKR_API_SECRET = os.getenv('FLICKR_API_SECRET', None)

command_checker = CommandChecker()
config = Config()
creator = FlexCreator()
futomomo_tool = FutomomoTool()

# quick reply
qr = creator.create_quick_reply()

@app.route("/", methods=['GET'])
def hello_word():
    return 'Hello World!'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)
    # body = request.body.decode('utf-8')
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # test
    if event.message.text in ['test']:
        f = open('./template/flex_pattern.json', 'r')
        json_dict = json.load(f)
        flex = json_dict
        test = FlexSendMessage(alt_text='test', contents=flex, quick_reply=qr)
        line_bot_api.reply_message(event.reply_token, test)
    # profile
    if event.message.text in ['profile', 'p', 'pl', 'プロフィール']:
        source_type = event.source.type
        if (source_type == "user"):
            res = line_bot_api.get_profile(event.source.sender_id)
            reply = TextSendMessage(f"[名前]:\n{res.display_name}\n[UserId]:\n{res.user_id}\n[pictureUrl]:\n{res.picture_url}\n[一言]:\n{res.status_message}")
        else:
            reply = TextSendMessage("個人チャットで使ってね!")
        line_bot_api.reply_message(event.reply_token, reply)
    # help
    if event.message.text in ["ヘルプ", "help", "h"]:
        reply = creator.create_help_message()
        line_bot_api.reply_message(event.reply_token, reply)

    # bye
    if event.message.text in ['bye', 'ばいばい', 'バイバイ', '死ね']:
        if event.source.type == 'user':
            return
        reply = TextSendMessage('ばいばい!')
        line_bot_api.reply_message(event.reply_token, reply)
        if event.source.type == 'group':
            line_bot_api.leave_group(event.source.sender_id)
        if event.source.type == 'room':
            line_bot_api.leave_room(event.source.sender_id)

    # ふともも
    if command_checker.include_command(event.message.text, ["ふともも", "ふと", "もも", "futomomo"]):
        futomomo = futomomo_tool.get_random_futomomo()
        reply = ImageSendMessage(original_content_url=futomomo.high_quality_url, preview_image_url=futomomo.url, quick_reply=qr)
        line_bot_api.reply_message(event.reply_token, reply)

    # パンチラ
    if command_checker.include_command(event.message.text, ["ぱんちら", "パンチラ"]):
        res = line_bot_api.get_profile(event.source.sender_id)
        url = futomomo_tool.get_random_pantira_url()
        if res.user_id == "Uc45442e19e3f8326fc321e828003f710":
            reply = ImageSendMessage(original_content_url=url, preview_image_url=url)
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("権限がありません。"))

    # いっぱい
    if command_checker.include_command(event.message.text, ['いっぱい']):
        futomomo = creator.create_normal_futomomo()
        line_bot_api.reply_message(event.reply_token, futomomo)

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data.startswith('get: '):
        url = event.postback.data.split(' ')
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=url[2], preview_image_url=url[1], quick_reply=qr))

# 友達追加時, グループ、ルーム参加時
@handler.add(FollowEvent)
@handler.add(JoinEvent)
def handle_follow(event):
    reply = creator.create_help_message()
    line_bot_api.reply_message(event.reply_token, reply)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)