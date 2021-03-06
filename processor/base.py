import pandas as pd
import os
import logging

from tqdm import tqdm
from transfer import BaseTransfer
from bbox import BBox2D
from utils import draw, im_show

from typing import Type, List, Tuple


class DataProcessor:
    root = ''
    debug = False

    def __init__(self, transfer: Type[BaseTransfer], size=(448, 448, 3), output='output'):
        self.transfer = transfer(store=output, size=size)

    def set_data_root_path(self, path: str):
        self.root = path

    def addData(self, data_path: str, details: List[Tuple[str, BBox2D]], **kwargs):
        """
        Load data in dataset.

        :param details: The detail of the data. need name(label) and BBox2D
        :param usage: Your usage of this data (default train)
        :param data_path: the path where images exists
        :return: None
        """
        self.transfer.addData(os.path.join(self.root, data_path), details, **kwargs)

    def data_loader(self, db: pd.DataFrame) -> dict:
        pass

    def load_from_csv(self, name: str, stop_at=0):
        """
        Before use it, you need rewrite data_loader

        :param name:
        :param stop_at: stop after process n data. 0 is unset. (for debug)
        :return:
        """

        df = pd.read_csv(name)
        size = df.shape[0]

        if stop_at:
            size = min(stop_at, size)

        # preprocessing and merge
        logging.info('[+] Preprocessing start.')
        db = {}
        with tqdm(total=size) as bar:
            for index, row in df.iterrows():
                data = self.data_loader(row)
                bar.update(1)

                if not data:
                    raise ValueError('Please overwrite your data_loader ^_^')

                bar.set_description(f"Processing: {data['name']}")
                if data['name'] in db:
                    db[data['name']].append(*data['details'])
                else:
                    db[data['name']] = data['details']

                if bar.n == size:
                    break

        logging.info('[+] Done. Starting transfer.')
        bar = tqdm(db)
        for instance in bar:
            bar.set_description(f"Processing: {instance}")

            if self.debug:
                img = draw(db[instance], os.path.join(self.root, instance), (0, 255, 0))
                im_show(img)

            self.addData(instance, db[instance])
        logging.info('[+] Done.')
