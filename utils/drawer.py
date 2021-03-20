import cv2
from bbox import BBox2D

from typing import List, Tuple


def draw(details: List[Tuple[str, BBox2D]], img_path, color):
    font = cv2.FONT_HERSHEY_COMPLEX
    img = cv2.imread(img_path)
    for det in details:
        bbox = det[1]
        x, y = bbox.x1, bbox.y1
        w, h, label = bbox.w, bbox.h, det[0]
        x, y, w, h = [int(i) for i in [x, y, w, h]]
        # color (0,255,0)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        cv2.putText(img, label, (x - 10, y - 10), font,
                    0.5, (255, 0, 255), thickness=1)
    return img


def im_show(img, name='temp'):
    cv2.imshow(name, img)
    cv2.waitKey(0)
