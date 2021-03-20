import os

from typing import List


def check_and_mkdir(base_path: str, dir_list: List[str]):
    """
    Check and mkdir base_path, and use is as root to create dir_list.

    :param base_path: root path
    :param dir_list: the dirs need to create
    :return:
    """
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    for name in dir_list:
        dir_name = os.path.join(base_path, name)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
