from typing import Optional
import threading

import torch

# 线程保存的 device
_device_local = threading.local()


def try_gpu(device_no: Optional[int] = None) -> torch.device:
    """
    尝试获取 GPU 设备。
    先获取 cuda，没有选择 mps，还没有使用 cpu。
    :param device_no: 设备号，只对 cuda 有效
    :return: GPU 设备
    """
    if torch.cuda.is_available():
        if device_no is not None and device_no < torch.cuda.device_count():
            #
            return torch.device(f'cuda:{device_no}')

        return torch.device('cuda')
    return torch.device('mps' if torch.mps else 'cpu')


def set_device_local(device: torch.device):
    """
    设置线程变量：训练用设备
    :param device: 训练用设备
    """
    _device_local.device = device
    print(f'设置线程变量 device = {device.type}:{device.index} [{threading.currentThread().name}]')


def get_device_local() -> torch.device:
    """
    获取线程变量：训练用设备
    :return: 训练用设备
    """
    device = getattr(_device_local, 'device', None)
    if device is None:
        device = try_gpu()
        set_device_local(device)
    return device
