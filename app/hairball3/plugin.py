from collections import Counter


class Plugin(object):

    def __init__(self, filename, json_project):
        self.dict_mastery = {}
        self.list_total_blocks = []
        self.dict_blocks = Counter()
        self.filename = filename
        self.json_project = json_project

    def process(self):
        pass

    def analyze(self):
        pass

    def finalize(self) -> str:
        pass
