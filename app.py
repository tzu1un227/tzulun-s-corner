from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage

app = Flask(__name__)

# 設定你的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'CVx7u8Oxjjk0t7gEIbtdSU1eundpHAlChMshRgrSg2+w3j3fspipXVRaQf4s6w018C/E7xebmLl3O9lO/V0hMq+Y3yFKU241bE73QY25IsISMd3FHa7JKMC5eoOAU8Ob+6yw05szKvTTuhbNACFF3AdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '82e9b9eee29714c84b7ef546b39e5362'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取請求的 X-Line-Signature 標頭
    signature = request.headers['X-Line-Signature']

    # 獲取請求的內容
    body = request.get_data(as_text=True)

    try:
        # 驗證簽名
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆收到的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='你說的是: ' + event.message.text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
