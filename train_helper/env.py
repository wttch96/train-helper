import os

# torch 训练 device 的环境变量的 Key
KEY_TRAIN_TORCH_DEVICE = "train_helper.train.torch.device"
# 训练消息是否发送 webhook 通知的环境变量的 Key
KEY_TRAIN_MESSAGE_SEND = "train_helper.train.message.send"


def set_train_torch_device(device: str):
    """
    设置 torch 训练 device 的环境变量
    :param device: torch 训练用的 device
    """
    os.environ[KEY_TRAIN_TORCH_DEVICE] = device


def get_train_torch_device(log: bool = True) -> str:
    """
    获取 torch 训练 device 的环境变量
    :param log: 获取后, 是否打印训练用的 device 信息
    :return: 环境变量中, 训练用的 device 信息
    """
    device = os.environ.get(KEY_TRAIN_TORCH_DEVICE, default="cpu")
    if log:
        print(f"torch 使用 {device} 进行训练...")
    return device


def set_train_message_send(send: bool):
    """
    设置训练的消息是否发送 webhook 通知, 可以通过环境变量, 进行全局关闭
    :param send: 是否发送 webhook 通知
    """
    os.environ[KEY_TRAIN_MESSAGE_SEND] = "True" if send else "False"


def get_train_message_send() -> bool:
    """
    获取训练的消息是否发送 webhook 通知, 可以通过环境变量, 进行全局关闭
    :return: 训练的消息是否发送 webhook 通知, 可以通过环境变量, 进行全局关闭
    """
    return os.environ.get(KEY_TRAIN_MESSAGE_SEND, default="True") == 'True'
