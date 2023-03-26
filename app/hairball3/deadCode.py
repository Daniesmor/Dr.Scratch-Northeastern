import logging
import app.consts_drscratch as consts
from app.hairball3.plugin import Plugin
logger = logging.getLogger(__name__)


class DeadCode(Plugin):
    """
    Plugin that indicates unreachable code in Scratch files
    """

    def __init__(self, filename, json_project):
        super().__init__(filename, json_project)
        self.dead_code_instances = 0
        self.dict_deadcode = {}
        self.opcode_argument_reporter = "argument_reporter"

    def analyze(self):
        """
        Run and return the results form the DeadCode plugin
        """

        sprites = {}

        for key, value in self.json_project.items():
            if key == "targets":
                for dicc in value:
                    sprite = dicc["name"]
                    blocks_list = []
                    for _, blocks_dicc in dicc["blocks"].items():
                        if type(blocks_dicc) is dict:
                            event_var = any(blocks_dicc["opcode"] == event for event in consts.PLUGIN_DEADCODE_LIST_EVENT_VARS)
                            loop_block = any(blocks_dicc["opcode"] == loop for loop in consts.PLUGIN_DEADCODE_LIST_LOOP_BLOCKS)

                            if not event_var:
                                if not self.opcode_argument_reporter in blocks_dicc["opcode"]:
                                    if blocks_dicc["parent"] is None and blocks_dicc["next"] is None:
                                        blocks_list.append(str(blocks_dicc["opcode"]))

                                    # Check dead loop blocks
                                    if loop_block and blocks_dicc["opcode"] not in blocks_list:
                                        if not blocks_dicc["inputs"]:
                                            # Empty loop block, but inside of a block structure
                                            blocks_list.append(str(blocks_dicc["opcode"]))
                                        elif "SUBSTACK" not in blocks_dicc["inputs"]:
                                            blocks_list.append(str(blocks_dicc["opcode"]))
                                        else: # Could be normal loop block
                                            if blocks_dicc["inputs"]["SUBSTACK"][1] is None:
                                                blocks_list.append(str(blocks_dicc["opcode"]))

                    if blocks_list:
                        sprites[sprite] = blocks_list
                        self.dead_code_instances += 1

        self.dict_deadcode = sprites

    def finalize(self):

        self.analyze()

        result = "{}".format(self.filename)

        if self.dead_code_instances > 0:
            result += "\n"
            result += str(self.dict_deadcode)

        return result


# def main(filename):
#     dead_code = DeadCode(filename)
#     dead_code.analyze()
#     return dead_code.finalize()
