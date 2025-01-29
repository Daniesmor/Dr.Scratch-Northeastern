from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class DuplicateSprites(Plugin):
    """
    Plugin that analyzes duplicate scripts in scratch projects version 3.0
    """

    def __init__(self, filename, json_project, verbose=False):
        super().__init__(filename, json_project, verbose)
        self.total_duplicate = 0
        self.sprite_dict = {}
        self.duplicates = []

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

                    self.sprite_dict[sprite_name] = sprite_scripts

    def analyze(self):
        """
        Searches for completely identical sprites based on their scripts
        """
        self.set_sprite_dict()
        
        seen = {}
        
        for sprite_name, scripts in self.sprite_dict.items():
            # Convert script lists to sets of tuples for easier comparison
            script_set = frozenset(tuple(script.get_blocks()) for script in scripts)
            
            if script_set not in seen:
                seen[script_set] = {"sprites": {sprite_name: scripts}}
            else:
                seen[script_set]["sprites"][sprite_name] = scripts
        
        for duplicate_group in seen.values():
            if len(duplicate_group["sprites"]) > 1:
                self.duplicates.append(duplicate_group["sprites"])  # Store as a dictionary
                self.total_duplicate += len(duplicate_group["sprites"]) - 1
        
        return self.duplicates


    def finalize(self) -> dict:

        self.analyze()
        
        result = ("%d duplicate sprites found" % self.total_duplicate)
        result += "\n"
        
        self.dict_mastery['description'] = result
        self.dict_mastery['total_duplicate_sprites'] = self.total_duplicate
        self.dict_mastery['duplicates'] = self.duplicates
        
        if self.verbose:
            logger.info(self.dict_mastery['description'])
            logger.info(self.dict_mastery['total_duplicate_sprites'])
            logger.info(self.dict_mastery['duplicates'])
        
        dict_result = {'plugin': 'duplicate_sprites', 'result': self.dict_mastery}
        
        return dict_result
