from distutils.core import setup

setup(
    name='wttch-train-helper',
    version='0.0.4',
    description="Wttch's Train Helper",
    author="wttch",
    packages=[
        'wttch',
        'wttch.train',
        'wttch.train.notification',
        'wttch.train.torch',
        'wttch.train.utils',
    ],
    package_dir={
        '': 'src/wttch-train-helper'
    }
)
