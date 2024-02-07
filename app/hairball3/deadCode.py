import logging
import app.consts_drscratch as consts
from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
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

    def get_blocks(self, dict_target):
        """
        Gets all the blocks in json format into a dictionary
        """
        out = {}


        for dict_key, dicc_value in dict_target.items():
            if dict_key == "blocks":
                for blocks, blocks_value in dicc_value.items():
                    if type(blocks_value) is dict:
                        out[blocks] = blocks_value
        
        return out

    def analyze(self):

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
                                        print("Op1", blocks_dicc)
                                        script = Script()
                                        script.set_script_dict(block_dict={"block": blocks_dicc}, start="block")
                                        print("Dic:", script.script_dict)
                                        blocks_list.append(str(blocks_dicc["opcode"]))

                                    # Check dead loop blocks
                                    if loop_block and blocks_dicc["opcode"] not in blocks_list:
                                        if not blocks_dicc["inputs"]:
                                            print("Op2", blocks_dicc)
                                            # Empty loop block, but inside of a block structure
                                            blocks_list.append(str(blocks_dicc["opcode"]))
                                        elif "SUBSTACK" not in blocks_dicc["inputs"]:
                                            print("Op3", blocks_dicc)
                                            blocks_list.append(str(blocks_dicc["opcode"]))
                                        else: # Could be normal loop block
                                            if blocks_dicc["inputs"]["SUBSTACK"][1] is None:
                                                print("Op4", blocks_dicc)
                                                blocks_list.append(str(blocks_dicc["opcode"]))
                    if blocks_list:
                        scripts = []
                        for block in blocks_list:
                            script = Script()
                            script.set_custom_script_dict({"block_0": {"name": block}})
                            print("DeadCode", script.script_dict)
                            # script_text = script.convert_to_text()
                            # print("script_txt", script_text)
                            # cripts.append(script_text)
                        sprites[sprite] = blocks_list
                        self.dead_code_instances += 1

        self.dict_deadcode = sprites

    def finalize(self):

        self.analyze()

        result = "{}".format(self.filename)

        if self.dead_code_instances > 0:
            result += "\n"
            result += str(self.dict_deadcode)

        self.dict_mastery['description'] = result
        self.dict_mastery['total_dead_code_scripts'] = self.dead_code_instances
        self.dict_mastery['list_dead_code_scripts'] = [self.dict_deadcode]

        dict_result = {'plugin': 'dead_code', 'result': self.dict_mastery}

        return dict_result



