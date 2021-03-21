import pandas as pd

from bbox import BBox2D, XYWH
from processor import DataProcessor


class MyProcessor(DataProcessor):
    def __init__(self, transfer, output):
        super().__init__(transfer, size=(1024, 1024, 3),
                         output=output)

    def data_loader(self, db: pd.DataFrame) -> dict:
        bbox = BBox2D(eval(db['bbox']), mode=XYWH)

        return {
            'name': db['image_id'] + '.jpg',
            'details': [('baseclass', bbox)]
        }
