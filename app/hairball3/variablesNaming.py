from app.hairball3.plugin import Plugin
import app.consts_drscratch as consts


class VariablesNaming(Plugin):
    """
    Plugin that keeps track of how often variables default  names (like variable1, my variable, ...) are used within a project.
    """

    def __init__(self, filename, json_project):
        super().__init__(filename, json_project)
        self.total_default = 0
        self.list_default = []

    def analyze(self):
        """
        Run and return the results from the VariablesNaming module
        """

        json_scratch_project = self.json_project.copy()

        for key, value in json_scratch_project.items():
            if key == "targets":
                for dicc in value:
                    for dicc_key, dicc_value in dicc.items():
                        if dicc_key == "variables":
                            for key, name in dicc_value.items():
                                for default in consts.PLUGIN_VARIABLESNAMING_DEFAULT_NAMES:
                                    if default in name[0]:
                                        self.total_default += 1
                                        self.list_default.append(name[0])

    def finalize(self):

        self.analyze()

        result = ""
        result += ("%d default variables names found:\n" % self.total_default)

        for name in self.list_default:
            result += name
            result += "\n"

        return result