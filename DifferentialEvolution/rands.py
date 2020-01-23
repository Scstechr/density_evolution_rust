import numpy as np
import random
import string

from defaults import KMAX

N = 1000


def random_dist():
    lst = np.random.randint(0, N, 21)
    while lst[2] == 0:
        lst = np.random.randint(0, N, 21)
    lst = [l if idx <= KMAX and idx > 1 else 0 for idx, l in enumerate(lst)]
    lst_sum = sum(lst)
    return [l / lst_sum for l in lst]


def random_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=15))


if __name__ == '__main__':
    [print(l) for l in random_dist()]
