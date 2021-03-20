# Advanced data processor

目标是做一个简单好用的数据格式转换器，当前仅实现了 voc 格式的转换



## 警告

此仓库正在开发中，不同模块还处于手动调用的阶段，api 将随时更改



## 使用方式
安装
```bash
pip install -r requirements.txt
```

使用 （详见代码内文档）

你需要新建一个类，继承至 `DataProcessor`，并重写 `data_loader` 方法

```python
import pandas as pd

from bbox import BBox2D
from processor import DataProcessor
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

    dp.load_from_csv(train_csv, stop_at=0)
```

然后就可以通过不同的 `Transfer` 进行数据转换了



## 使用截图

![screenshot](imgs/screenshot1.png)