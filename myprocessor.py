import pandas as pd

from bbox import BBox2D
from processor import DataProcessor


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
                    'ymax': bbox.y2,
                }
            }]
        }
