import hmac
import hashlib
import base64
import logging
import time
import os
from train_helper.env import KEY_TRAIN_MESSAGE_SEND
import json
import requests


class DingtalkMessageSender:

    def __init__(self, webhook_url: str, secret: str):
        self._url = webhook_url
        self._secret = secret
        self._secret_enc = secret.encode('utf8')
        self._header = {
            "Content-Type": "application/json"
        }

    def _params(self) -> dict:
        timestamp = str(round(time.time() * 1000))
        string_to_sign = f'{timestamp}\n{self._secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(self._secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code)
        # sign = urllib.parse.quote_plus(tmp)
        return {
            "timestamp": timestamp,
            "sign": sign
        }

    def _send(self, data: dict):
        resp = requests.post(self._url, params=self._params(), data=json.dumps(data), headers=self._header)
        print(resp.text)

    def send_text(self, txt: str):
        self._send({
            # "at": {
            #     "atMobiles": [
            #         "18701269358"
            #     ],
            #     "atUserIds": [
            #         "wttch96"
            #     ],
            #     "isAtAll": False
            # },
            "text": {
                "content": txt
            },
            "msgtype": "text"
        })

    def send_markdown(self, markdown: str):
        self._send({
            "msgtype": "markdown",
            "markdown": {
                "title": "杭州天气",
                "text": "#### 杭州天气 @150XXXXXXXX \n9度，西北风1级，空气良<font color=\"warning\">89</font>，相对温度73%\n"
                        "> ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n"
                        "> ###### 10点20分发布 [天气](https://www.dingalk.com) \n"
            },
        })


# 		"mentioned_list":["wangqing","@all"],
# 		"mentioned_mobile_list":["13800001111","@all"]
class WechatMessageSender:

    def __init__(self, webhook_url):
        self._url = webhook_url
        self._header = {
            "Content-Type": "application/json"
        }

    def send_text(self, txt: str):
        self._send({
            "msgtype": "text",
            "text": {
                "content": txt
            }
        })

    def send_markdown(self, markdown: str):
        self._send({
            "msgtype": "markdown",
            "markdown": {
                "content": markdown
            }
        })

    def _send(self, data: dict):
        resp = requests.post(self._url, data=json.dumps(data), headers=self._header)
        print(resp.text)


class TrainMessageSender:

    def __init__(self, name, wechat_webhook_url):
        self._name = name
        self._wechat = WechatMessageSender(wechat_webhook_url)
        self._last_epoch_start_time = time.time()
        self._send = os.environ.get(KEY_TRAIN_MESSAGE_SEND, default="True") == 'True'
        logging.info(f"[{name}]Train message send: [{self._send}]")

    def epoch_start(self, cur, total):
        if self._send:
            self._wechat.send_markdown(f"""# Start epoch {cur}/{total}\n
            ## Task: {self._name}""")
            self._last_epoch_start_time = time.time()

    def epoch_finish(self, cur, total, acc, loss):
        if self._send:
            epoch_time = time.time() - self._last_epoch_start_time
            self._wechat.send_markdown(f"""# 【{self._name} {cur}/{total}个 epoch 完成\n
            > Accuracy: {acc:>0.1f}\n
            > Loss: {loss} \n
            ###### Time: {epoch_time}""")
