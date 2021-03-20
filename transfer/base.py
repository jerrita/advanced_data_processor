from typing import List


class BaseTransfer:
    store = ''  # Path to save output

    def __init__(self, database='Automatic generated', store='output', overwrite=True):
        self.store = store
        self.database = database

    def addData(self, data_path: str, details: List[dict], **kwargs):
        pass
