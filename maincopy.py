import csv
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from flask import Flask, request, abort
import os
import time


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    CarouselColumn, CarouselTemplate, FollowEvent,
    LocationMessage, MessageEvent, TemplateSendMessage,
    TextMessage, TextSendMessage, UnfollowEvent, URITemplateAction, FlexSendMessage
)

app = Flask(__name__)


payload = {
    "type": "flex",
    "altText": "Flex Message",
    "contents": {
        "type": "bubble",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "このような「職場に着いたとき」のあいさつはどのような言葉が適切でしょうか",
                    "flex": 1,
                    "size": "lg",
                    "align": "center",
                    "gravity": "center",
                    "color": "#979797",
                    "wrap": True
                }
            ]
        },
        "hero": {
            "type": "image",
            "url": "https://developers.line.biz/assets/images/services/bot-designer-icon.png",
            "size": "xxs",
            "aspectRatio": "3:1"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "こんにちは",
                        "text": "こんにちは"
                    }
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "おはようございます",
                        "text": "おはようございます"
                    }
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "いただきます",
                        "text": "いただきます"
                    }
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "【わからない】",
                        "text": "わからない"
                    }
                }
            ]
        }
    }
}



string_chat =   "[バイト先にて]\n\nあなたは職場に着きました\n着いたとき職場には先輩が居ました\n先輩のOOさんに挨拶をしましょう"
correct_chat =   "【正解】\nその通りです！\n\n職場に着いた時間が何時でも，その日に初めて会った方には\n「おはようございます」\nと答えます．\n\n実に不思議な文化だと私も思います\n\nhttps://woman.mynavi.jp/article/130823-092/"
miss_chat =   "【残念】\n答えは「おはようございます」でした\n\n職場に着いた時間が何時でも，その日に初めて会った方には\n「おはようございます」\nと答えます．\n\n実に不思議な文化だと私も思います\n\nhttps://woman.mynavi.jp/article/130823-092/"
no_idea = "答えは「おはようございます」でした\n\n職場に着いた時間が何時でも，その日に初めて会った方には\n「おはようございます」\nと答えます．\n\n実に不思議な文化だと私も思います\n\nhttps://woman.mynavi.jp/article/130823-092/"





# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
response_json_list = []


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    container_obj = FlexSendMessage.new_from_json_dict(payload)
    if (event.message.text == "start" or event.message.text == "Start" or event.message.text == "START" or event.message.text == "スタート" or event.message.text == "すたーと" or
        event.message.text == "start " or event.message.text == "start　" or event.message.text == "Start " or event.message.text == "Start　"):
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text=string_chat))
      
      line_bot_api.push_message(
          'U86e7917ddb1d7ac485320370f87b0f5e', messages=container_obj)



    if event.message.text == "おはようございます":
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text=correct_chat))


    elif(event.message.text == "いただきます" or event.message.text == "こんにちは"):
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text=miss_chat))
      
    elif(event.message.text == "わからない"):
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text=no_idea))    

    else:
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text="項目から選んでください"))
      


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
