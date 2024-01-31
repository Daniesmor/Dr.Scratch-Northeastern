from app.hairball3.plugin import Plugin
import app.consts_drscratch as consts


class SpriteNaming(Plugin):
    """
    Plugin that keeps track of how often sprites default  names (like Sprite1, Sprite2) are used within a project.
    """

    def __init__(self, filename, json_project):
        super().__init__(filename, json_project)
        self.total_default = 0
        self.list_default = []

    def analyze(self):
        """
        Run and return the results from the SpriteNaming module
        """

        json_scratch_project = self.json_project.copy()

        for key, value in json_scratch_project.items():
            if key == "targets":
                for dicc in value:
                    for dicc_key, dicc_value in dicc.items():
                        if dicc_key == "name":
                            for default in consts.PLUGIN_SPRITENAMING_DEFAULT_NAMES:
                                if default in dicc_value:
                                    self.total_default += 1
                                    self.list_default.append(dicc_value)

    def finalize(self):

        self.analyze()

        result = ""
        result += ("%d default sprite names found:\n" % self.total_default)

        for name in self.list_default:
            result += name
            result += "\n"

        return result




