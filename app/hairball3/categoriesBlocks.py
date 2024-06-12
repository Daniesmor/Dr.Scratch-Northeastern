import logging
import app.consts_drscratch as consts
from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
logger = logging.getLogger(__name__)

CONTROL_BLOCKS = ["CONTROL_FOREVER", "CONTROL_REPEAT", "CONTROL_IF", "CONTROL_IF_ELSE", "CONTROL_ELSE", "CONTROL_STOP_ALL", 
                  "CONTROL_STOP_THIS", "CONTROL_STOP_OTHER", "CONTROL_WAIT", "CONTROL_WAIT_UNTIL", "CONTROL_REPEAT_UNTIL",
                  "CONTROL_WHILE", "CONTROL_FOREACH", "CONTROL_START_AS_CLONE", "CONTROL_CREATE_CLONE_OF", "CONTROL_CREATE_CLONE_OF_MYSELF",
                  "CONTROL_DELETE_THIS_CLONE", "CONTROL_COUNTER", "CONTROL_INCRCOUNTER", "CONTROL_CLEARCOUNTER", "CONTROL_ALLATONCE"]

VARIABLES_BLOCKS = ["DATA_SETVARIABLETO", "DATA_CHANGEVARIABLEBY", "DATA_SHOWVARIABLE", "DATA_HIDEVARIABLE", "DATA_ADDTOLIST",
                    "DATA_DELETEOFLIST", "DATA_DELETEALLOFLIST", "DATA_INSERTATLIST", "DATA_REPLACEITEMOFLIST", "DATA_ITEMOFLIST",
                    "DATA_ITEMNUMOFLIST", "DATA_LENGTHOFLIST", "DATA_LISTCONTAINSITEM", "DATA_SHOWLIST", "DATA_HIDELIST",
                    "DATA_INDEX_ALL", "DATA_INDEX_LAST", "DATA_INDEX_RANDOM"]

class CategoriesBlocks(Plugin):
    """
    Plugin that indicates the percentage of blocks in each category.
    """
    
    def __init__(self, filename, json_project, verbose=False):
        super().__init__(filename, json_project, verbose)
        self.sprite_dict = {} 
        self.sprite_dict_format = {}
        self.opcode_argument_reporter = "argument_reporter"
        self.json_project = json_project


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
    
    def set_sprite_dict(self):
        """
        Sets a dictionary containing the scripts of each sprite in Script() format
        """
        
        for key, list_dict_targets in self.json_project.items():
            
            if key == "targets":
                for dict_target in list_dict_targets:
                    sprite_name = dict_target['name']
                    
                    sprite_blocks = self.get_blocks(dict_target)
                    sprite_scripts = []

                    for key, block in sprite_blocks.items():
                        
                        if block["topLevel"]:
                            new_script = Script()
                            new_script.set_script_dict(block_dict=sprite_blocks, start=key)                            
                            sprite_scripts.append(new_script)


                    self.sprite_dict[sprite_name] = sprite_blocks 
                    script_text = "\n\n".join([script.convert_to_text() for script in sprite_scripts])
                    self.sprite_dict_format[sprite_name] = script_text
    
    
    def analyze(self):
        """
        Analyze the ammount of sprites and blocks of each projec
        """
        self.set_sprite_dict()
        self.categories_summary = {}
        self.total_blocks = 0

        categories = ["motion", "data", "operator", "control", "event", "sounds", "looks", "sensing"]

        count = {cat: 0 for cat in categories}

        for sprite_name, sprite_blocks in self.sprite_dict.items():
            for key, block in sprite_blocks.items():
                self.total_blocks += 1
                for cat in categories:
                    if block.get('opcode').startswith(cat):
                        count[cat] += 1
                        break
        if self.total_blocks != sum(count.values()):
            count['others'] = self.total_blocks - sum(count.values())

        for cat, count in count.items():
            self.categories_summary[cat] = round((count/self.total_blocks)*100, 2)
                
            
        return self.categories_summary
    
    
    def finalize(self) -> dict:

        self.analyze()

        
        dict_result = {'plugin': 'BlockCategories', 'result': self.categories_summary}

        return dict_result