import logging
import app.consts_drscratch as consts
from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
logger = logging.getLogger(__name__)

class Block_Sprite_Usage(Plugin):
    """
    Plugin that indicates the percentage of blocks in each category.
    """
    
    def __init__(self, filename, json_project, verbose=False):
        super().__init__(filename, json_project, verbose)
        self.sprite_dict = {} 
        self.sprite_dict_format = {}
        self.summary = {}
        self.opcode_argument_reporter = "argument_reporter"
        self.json_project = json_project
    
    def process(self):
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
        Analyzes the project and sets the categories_summary dictionary
        """

        self.set_blocks_and_sprites()
        self.set_categories_blocks()


    def finalize(self) -> dict:

        self.process()
        self.analyze()

        dict_result = {'plugin': 'Block_Sprite_Usage', 'result': self.summary}

        return dict_result
    

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
       
    def set_blocks_and_sprites(self):
        """
        Analyze the ammount of sprites and blocks of each project
        """

        self.blocks_summary = {}

        num_sprites = len(self.sprite_dict) - 1 
        
        for sprite, scripts in self.sprite_dict.items():
            if sprite != "Stage":
                original_num_scripts = len(scripts)
                self.blocks_summary[sprite] = original_num_scripts
                
                
        self.summary['total_blocks'] = sum(self.blocks_summary.values())               
        self.summary['total_sprites'] = num_sprites

    def set_categories_blocks(self):
        """
        Analyze the ammount of blocks of each category in each project
        """

        self.total_blocks = 0
        self.summary['categories'] = {}

        categories = ["motion", "looks", "sound", "event", "control", "sensing", "operator", "data", "procedures"]

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
            if self.total_blocks != 0:
                self.summary["categories"][cat] = round((count/self.total_blocks)*100, 2)
    
    
