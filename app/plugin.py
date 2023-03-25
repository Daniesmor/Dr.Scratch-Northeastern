import json
from zipfile import ZipFile
from zipfile import BadZipfile
from collections import Counter


class Plugin(object):

    def __init__(self, filename):
        self.dict_mastery = {}
        self.list_total_blocks = []
        self.dict_blocks = Counter()
        self.filename = filename
        self._load_json_project()

    def _load_json_project(self):
        try:
            zip_file = ZipFile(self.filename, "r")
            self.json_project = json.loads(zip_file.open("project.json").read())
        except BadZipfile:
            print('Bad zipfile')

    def process(self):
        pass

    def analyze(self):
        pass

    def finalize(self) -> str:
        pass