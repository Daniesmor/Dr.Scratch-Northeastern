from collections import Counter


class Plugin(object):

    def __init__(self, filename, json_project, verbose=False):
        self.dict_mastery = {}
        self.list_total_blocks = []
        self.dict_blocks = Counter()
        self.filename = filename
        self.verbose = verbose
        self.json_project = json_project

    def process(self):
        pass

    def analyze(self):
        pass

    def finalize(self) -> dict:
        pass
