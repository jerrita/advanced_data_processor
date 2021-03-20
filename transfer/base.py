from bbox import BBox2D

from typing import List, Tuple


class BaseTransfer:
    store = ''  # Path to save output

    def __init__(self, database='Automatic generated', store='output', size=(448, 448), overwrite=True):
        self.store = store
        self.database = database

    def addData(self, data_path: str, details: List[Tuple[str, BBox2D]], **kwargs):
        pass
