from __future__ import unicode_literals
from flask import Flask, request, abort
from utils.command import CommandChecker, ADMIN
from utils.config import Config
from utils.creator import FlexCreator
from utils.futomomo_tools import FutomomoTool
import os
import json
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

# environment
env = os.getenv('LINE_BOT', None)
if env == 'DEV':
    handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET_DEV', None))
    # line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN_DEV', None))
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN_DEV', None), endpoint='http://localhost:8080')
elif env == 'RELEASE':
    handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None))
else:
    sys.exit()

# For APP
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
    if command_checker.equal_command(event.message.text, ['test']):
        f = open('./template/flex_pattern.json', 'r')
        json_dict = json.load(f)
        flex = json_dict
        test = FlexSendMessage(alt_text='test', contents=flex, quick_reply=qr)
        line_bot_api.reply_message(event.reply_token, test)

    # profile
    if command_checker.equal_command(event.message.text, ['profile', 'p', 'pl', 'プロフィール']):
        profile = line_bot_api.get_profile(event.source.user_id)
        user = command_checker.get_user(event.source.user_id)
        if not user:
            command_checker.new_user(event.source.user_id)
        reply = creator.create_profile(profile, user['count'], user['authority'])
        line_bot_api.reply_message(event.reply_token, reply)

    # uid
    if command_checker.equal_command(event.message.text, ['uid', 'UID']):
        reply = TextSendMessage(event.source.user_id, quick_reply=qr)
        line_bot_api.reply_message(event.reply_token, reply)

    # help
    if command_checker.equal_command(event.message.text, ["ヘルプ", "help", "h"]):
        reply = creator.create_help_message()
        line_bot_api.reply_message(event.reply_token, reply)

    # bye
    if command_checker.equal_command(event.message.text, ['bye', 'ばいばい', 'バイバイ', '死ね']):
        if event.source.type == 'user':
            return
        reply = TextSendMessage('ばいばい!')
        line_bot_api.reply_message(event.reply_token, reply)
        if event.source.type == 'group':
            line_bot_api.leave_group(event.source.sender_id)
        if event.source.type == 'room':
            line_bot_api.leave_room(event.source.sender_id)

    # ふともも
    if command_checker.include_command(event.message.text, ["ふともも", "ふと", "もも", "futomomo", "桃", "momo"]):
        futomomo = futomomo_tool.get_random_futomomo()
        reply = ImageSendMessage(original_content_url=futomomo.high_quality_url, preview_image_url=futomomo.url, quick_reply=qr)
        line_bot_api.reply_message(event.reply_token, reply)
        command_checker.count_up(event.source.user_id)

    # パンチラ
    # if command_checker.include_command(event.message.text, ["ぱんちら", "パンチラ"]):
    #     if command_checker.check_authority(event.source.user_id, level=1):
    #         url = futomomo_tool.get_random_pantira_url()
    #         reply = ImageSendMessage(original_content_url=url, preview_image_url=url, quick_reply=qr)
    #         line_bot_api.reply_message(event.reply_token, reply)
    #         command_checker.count_up(event.source.user_id)
    #     else:
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(f"権限がありません。\n{event.source.user_id}", quick_reply=qr))

    # いっぱい
    if command_checker.include_command(event.message.text, ['いっぱい']):
        futomomo = creator.create_normal_futomomo()
        line_bot_api.reply_message(event.reply_token, futomomo)
        command_checker.count_up(event.source.user_id)

    # おっぱい
    # if command_checker.include_command(event.message.text, ['おっぱい', 'opi', 'π']):
    #     if command_checker.check_authority(event.source.user_id, level=1):
    #         url = futomomo_tool.get_random_opi_url()
    #         reply = ImageSendMessage(original_content_url=url, preview_image_url=url, quick_reply=qr)
    #         line_bot_api.reply_message(event.reply_token, reply)
    #         command_checker.count_up(event.source.user_id)
    #     else:
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(f"権限がありません。\n{event.source.user_id}", quick_reply=qr))

    # コマンド総実行回数
    if command_checker.equal_command(event.message.text, ['max']):
        if command_checker.check_authority(event.source.user_id, level=ADMIN):
            user = command_checker.get_max_count_user()
            profile = line_bot_api.get_profile(user['user_id'])
            count = user['count']
            reply = creator.create_max_count_user(profile, count)
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(f"権限がありません。\n{event.source.user_id}", quick_reply=qr))

    # change authority
    if command_checker.include_command(event.message.text, ['cua']):
        if command_checker.check_authority(event.source.user_id, ADMIN):
            req = event.message.text.split(' ')
            if len(req) == 3:
                cmd, user_id, level = req
                if command_checker.update_authority(user_id, int(level)):
                    reply = TextSendMessage("Change user authority succeeded")
                    line_bot_api.reply_message(event.reply_token, reply)
                else:
                    reply = TextSendMessage("Change user authority failed")
                    line_bot_api.reply_message(event.reply_token, reply)
            else:
                reply = TextSendMessage("Invalid format")
                line_bot_api.reply_message(event.reply_token, reply)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(f"権限がありません。\n{event.source.user_id}", quick_reply=qr))

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
    if env == 'DEV':
        app.run(debug=True, host='localhost', port=5000)
        # app.run(debug=True, host='0.0.0.0', port=40000)
    elif env == 'RELEASE':
        app.run(debug=False, host='0.0.0.0', port=40000)
    else:
        sys.exit(0)
