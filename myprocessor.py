import pandas as pd

from bbox import BBox2D, XYWH
from processor import DataProcessor


class MyProcessor(DataProcessor):
    def data_loader(self, db: pd.DataFrame) -> dict:
        bbox = BBox2D(eval(db['bbox']), mode=XYWH)

        return {
            'name': db['image_id'] + '.jpg',
            'details': [(db['source'], bbox)]
        }
