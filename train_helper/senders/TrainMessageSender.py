import os
import time

from .WechatMessageSender import WechatMessageSender
from ..env import KEY_TRAIN_MESSAGE_SEND


class TrainMessageSender:
    """
    训练时进行消息发送的发送器, 通知训练进度等。

    可以通过环境变量(train_helper.env.KEY_TRAIN_MESSAGE_SEND)开启关闭通知。
    """

    def __init__(self, name, wechat_webhook_url):
        """
        :param name: 任务名称
        :param wechat_webhook_url: 微信 webhook url
        """
        self._name = name
        self._wechat = WechatMessageSender(wechat_webhook_url)
        self._last_epoch_start_time = time.time()
        self._send = os.environ.get(KEY_TRAIN_MESSAGE_SEND, default="True") == 'True'
        print(f"[{name}]Train message send: [{self._send}]")

    def epoch_start(self, cur, total):
        """
        发送 epoch 开始的消息
        :param cur: 当前 epoch
        :param total: 总共 epoch 个数
        """
        if self._send:
            self._wechat.send_markdown(f"""# Start epoch {cur}/{total}\n
            ## Task: {self._name}""")
            self._last_epoch_start_time = time.time()

    def epoch_finish(self, cur, total, acc, loss):
        """
        发送 epoch 完成的消息
        :param cur: 当前 epoch
        :param total: 总共 epoch 个数
        :param acc: 精度
        :param loss: 损失
        """
        if self._send:
            epoch_time = time.time() - self._last_epoch_start_time
            self._wechat.send_markdown(f"""# 【{self._name} {cur}/{total}个 epoch 完成\n
            > Accuracy: {acc:>0.1f}\n
            > Loss: {loss} \n
            ###### Time: {epoch_time}""")
