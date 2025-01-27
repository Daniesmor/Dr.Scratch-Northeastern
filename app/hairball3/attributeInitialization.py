from plugin import Plugin
import app.consts_drscratch  as consts


class AttributeInitialization(Plugin):
    """
    Plugin that checks if modified attributes are properly initialized.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.total_default = 0
        self.list_default = []

    def analyze(self):
        """
        Return the results from the SpriteNaming module
        """
        for key, value in self.json_project.iteritems():
            if key == "targets":
                for dicc in value:
                    blocks_set = dicc["blocks"]
                    block_list = self._iter_blocks(blocks_set)
                    for name in block_list:
                        for attribute in consts.PLUGIN_INIT_ATTRIBUTES:
                            if (name, 'absolute') in consts.PLUGIN_INIT_BLOCKMAPPING[attribute]:
                                print(name, 'absolute')
                            elif (name, 'relative') in consts.PLUGIN_INIT_BLOCKMAPPING[attribute]:
                                print(name, 'relative')
                            else:
                                print(name)

    def _iter_blocks(self, blocks_set):
        list_blocks = []
        for _, block_value in blocks_set.iteritems():
            if block_value['opcode'] == 'event_whenflagclicked':
                next_block = block_value["next"]
                for block_id, block in blocks_set.iteritems():
                    if block_id == next_block:
                        list_blocks.append(str(block['opcode']))
                        next_block = block['next']

        return list_blocks

    def finalize(self):
        result = ""
        result += ("%d default backdrop names found:\n" % self.total_default)

        for name in self.list_default:
            result += name
            result += "\n"

        return result


# def main(filename):
#     attinit = AttributeInitialization(filename)
#     attinit.analyze()
#     return attinit.finalize()



