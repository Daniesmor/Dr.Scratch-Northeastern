import logging
import app.consts_drscratch as consts
from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
logger = logging.getLogger(__name__)



class ComparsionMode(Plugin):
    """
    Plugin that indicates some Comparsion info between two projects.
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
        pass