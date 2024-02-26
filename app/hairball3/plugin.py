from collections import Counter


class Plugin(object):

    def __init__(self, filename, json_project, skill_points = None,verbose=False):
        self.dict_mastery = {}
        self.list_total_blocks = []
        self.dict_blocks = Counter()
        self.filename = filename
        self.verbose = verbose
        self.json_project = json_project
        self.skill_points = skill_points

    def process(self):
        pass

    def analyze(self):
        pass

    def finalize(self) -> dict:
        pass
