from setuptools import setup

setup(name="wttch-train-helper", version="1.0", description="Wttch's Train Helper",
      author="wttch", py_modules=[
            'train_helper.senders',
            'train_helper.senders.DingtalkMessageSender',
            'train_helper.senders.WechatMessageSender',
            'train_helper.senders.TrainMessageSender',
            "train_helper.env"
      ])
