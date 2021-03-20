import pandas as pd

from bbox import BBox2D
from processer import DataProcessor
from transfer import VocTransfer
from private import *


class MyProcessor(DataProcessor):
    def data_loader(self, db: pd.DataFrame) -> dict:
        bbox = BBox2D(eval(db['bbox']))
        return {
            'name': db['image_id'] + '.jpg',
            'details': [{
                'name': db['source'],
                'bndbox': {
                    'xmin': bbox.x1,
                    'ymin': bbox.y1,
                    'xmax': bbox.x2,
                    'ymax': bbox.y2
                }
            }]
        }


if __name__ == '__main__':
    train_csv = csv_path

    dp = MyProcessor(VocTransfer, output='output')
    dp.set_data_root_path(data_root_path)

    dp.load_from_csv(train_csv, stop_at=1000)
