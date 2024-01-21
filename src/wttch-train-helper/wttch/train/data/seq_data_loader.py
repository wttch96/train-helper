import random

import numpy as np


def seq_data_iter_random(corpus: np.ndarray, batch_size: int, seq_len: int) -> tuple[np.ndarray, np.ndarray]:
    """
    随机生成序列数据，只保证序列内的顺序和原始顺序一致，不能保证小批量数据之间连续。
    Args:
        corpus: 原始语料库
        batch_size: 批处理大小
        seq_len: 序列长度

    Returns:

    """
    # 偏移
    corpus = corpus[random.randint(0, seq_len - 1):]
    # -1, 因为标签 +1, 序列的下一个数据就是标签
    num_seqs = (len(corpus) - 1) // seq_len
    # 抽样开始的位置
    init_indices = list(range(0, num_seqs * seq_len, seq_len))
    # 打乱, batch 内序列不一定连续
    random.shuffle(init_indices)

    def get_data(pos): return corpus[pos: pos + seq_len]

    # 可以生成多少批数据
    num_batches = num_seqs // batch_size
    for i in range(0, batch_size * num_batches, batch_size):
        init_indices_per_batch = init_indices[i:i + batch_size]
        data_array = np.array([[get_data(j), get_data(j + 1)] for j in init_indices_per_batch])
        yield data_array[:, 0], data_array[:, 1]


def seq_data_iter_sequential(corpus: np.ndarray, batch_size: int, seq_len: int) -> tuple[np.ndarray, np.ndarray]:
    """
    顺序生成序列数据，能保证小批量数据之间连续。
    Args:
        corpus: 原始语料库
        batch_size: 批处理大小
        seq_len: 序列长度

    Returns:

    """
    corpus = corpus[random.randint(0, seq_len):]
    num_tokens = ((len(corpus) - 1) // batch_size) * batch_size

    Xs = corpus[0: num_tokens]
    Ys = corpus[1: num_tokens + 1]
    Xs, Ys = Xs.reshape(batch_size, -1), Ys.reshape(batch_size, -1)

    num_batches = Xs.shape[1] // seq_len
    for i in range(0, seq_len * num_batches, seq_len):
        X = Xs[:, i: i + seq_len]
        Y = Ys[:, i: i + seq_len]
        yield X, Y


class SeqDataLoader:

    def __init__(self, data: numpy.ndarray, batch_size: int, seq_len: int, shuffle: bool = True):
        """
        序列数据加载器。
        Args:
            data: 原始数据
            batch_size: 批处理长度
            seq_len: 序列长度
            shuffle: 批之间收否随机
        """
        # 分开处理是因为使用 yield, 也可以同一个函数处理，之后随机一下
        self.data_iter_fn = seq_data_iter_random if shuffle else seq_data_iter_sequential

        self.data = data
        self.batch_size = batch_size
        self.seq_len = seq_len

    def __iter__(self):
        return self.data_iter_fn(self.data, self.batch_size, self.seq_len)
