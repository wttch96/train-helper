import threading
from time import sleep

from wttch.train.utils import StopWatch
from wttch.train.utils import cache_wrapper
from wttch.train.torch.utils import get_device_local, set_device_local, try_gpu


def set_device(device):
    set_device_local(device)


thread1 = threading.Thread(target=set_device, args=[try_gpu()])
thread2 = threading.Thread(target=set_device, args=[try_gpu()])

thread1.start()
thread2.start()
