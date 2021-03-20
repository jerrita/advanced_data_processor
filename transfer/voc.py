import os
import shutil
import xml2dict
import logging

from bbox import BBox2D
from dict2xml import dict2xml
from transfer import BaseTransfer
from utils import check_and_mkdir, voc_template_main, voc_template_obj

from typing import List, Tuple


class VocTransfer(BaseTransfer):
    xml_parser = xml2dict
    v_template = xml_parser.parse(voc_template_main)

    def __init__(self, database='Automatic generated', store='output', overwrite=True):
        super().__init__(database, store, overwrite)

        logging.info('[+] Transfer selected: VocTransfer')
        logging.info('[+] Store in ' + store)

        # Init path
        if overwrite and os.path.exists(store):
            shutil.rmtree(store)
        check_and_mkdir(store,
                        ['Annotations', 'ImageSets',
                         'ImageSets/Action', 'ImageSets/Layout', 'ImageSets/Main', 'ImageSets/Segmentation',
                         'JPEGImages',
                         'SegmentationClass',
                         'SegmentationObject'])

        # Init template
        self.v_template['annotation']['source']['database'] = database

    def addData(self, data_path: str, details: List[Tuple[str, BBox2D]], usage='train'):
        """
        Load data in dataset.

        :param details: The detail of the data. need name(label) and bnd_box
        :param usage: Your usage of this data (default train)
        :param data_path: the path where images exists
        :return: None
        """

        basename = os.path.basename(data_path).split('.')[0]
        xml_path = os.path.join(self.store, 'Annotations', basename + '.xml')
        parsed_objects = []

        # Adjust if xml exists
        file_exists = os.path.exists(xml_path)

        data = self.v_template if not file_exists else self.xml_parser.parse(open(xml_path, 'r').read())

        for detail in details:
            obj_template = self.xml_parser.parse(voc_template_obj)['object']
            obj_template.update({
                'name': detail[0],
                'bndbox': {
                    'xmin': detail[1].x1,
                    'ymin': detail[1].y1,
                    'xmax': detail[1].x2,
                    'ymax': detail[1].y2
                }
            })
            parsed_objects.append(obj_template)

        if not file_exists:
            data['annotation']['object'] = parsed_objects
        else:
            if type(data['annotation']['object']) is dict:
                data['annotation']['object'] = [data['annotation']['object']]
            data['annotation']['object'].append(parsed_objects)

        # Save data
        xml_cont = dict2xml(data, indent='    ')
        annotation = open(os.path.join(self.store, 'Annotations', basename + '.xml'), 'w')
        annotation.write(xml_cont)
        annotation.close()

        if not file_exists:
            shutil.copyfile(data_path, os.path.join(self.store, 'JPEGImages', basename + '.jpg'))

            usage_file = open(os.path.join(self.store, 'ImageSets/Main', usage + '.txt'), 'a')
            usage_file.write(basename + '\n')
