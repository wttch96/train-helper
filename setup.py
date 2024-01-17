from setuptools import setup

setup(name="wttch-train-helper", version="1.0", description="Wttch's Train Helper",
      author="wttch", py_modules=[
            'wttch.train.notification',
            'wttch.train.notification.base',
            'wttch.train.notification.dingtalk',
            'wttch.train.notification.wechat',
            'wttch.train.torch',
            'wttch.train.torch.utils',
            'wttch.train.utils',
            'wttch.train.utils.cache_wrapper',
            'wttch.train.utils.stopwatch',
      ])
