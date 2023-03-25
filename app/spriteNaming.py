from plugin import Plugin
import consts_plugins as consts


class SpriteNaming(Plugin):
    """
    Plugin that keeps track of how often sprites default  names (like Sprite1, Sprite2) are used within a project.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.total_default = 0
        self.list_default = []

    def finalize(self):
        """
        Output the default sprite names found in the project
        """
        result = ""
        result += ("%d default sprite names found:\n" % self.total_default)

        for name in self.list_default:
            result += name
            result += "\n"

        return result

    def analyze(self):
        """
        Run and return the results from the SpriteNaming module
        """

        for key, value in self.json_project.iteritems():
            if key == "targets":
                for dicc in value:
                    for dicc_key, dicc_value in dicc.iteritems():
                        if dicc_key == "name":
                            for default in consts.PLUGIN_SPRITENAMING_DEFAULT_NAMES:
                                if default in dicc_value:
                                    self.total_default += 1
                                    self.list_default.append(dicc_value)


def main(filename):
    naming = SpriteNaming(filename)
    naming.analyze()
    return naming.finalize()




