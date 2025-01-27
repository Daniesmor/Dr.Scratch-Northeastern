from app.hairball3.plugin import Plugin
import app.consts_drscratch as consts
from app.hairball3.scriptObject import Script


class LongScripts(Plugin):
    """
    Plugin that keeps track of how often sprites default names (like Sprite1, Sprite2) are used within a project.
    """

    def __init__(self, filename, json_project):
        super().__init__(filename, json_project)
        self.total_long_blocks = 0
        self.list_long_blocks = []
        self.sprite_dict = {}

    def get_blocks(self, dict_target):
        """
        Gets all the blocks in json format into a dictionary
        """

        out = {}

        for dict_key, dicc_value in dict_target.items():
            if dict_key == "blocks":
                for blocks, blocks_value in dicc_value.items():
                    if isinstance(blocks_value, dict):
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
                        if block.get("topLevel", False):
                            new_script = Script()
                            new_script.set_script_dict(block_dict=sprite_blocks, start=key)
                            sprite_scripts.append(new_script)

                    self.sprite_dict[sprite_name] = sprite_scripts

    def analyze_sprite(self, sprite_name, sprite_scripts, length_threshold=10):
        """
        Analyzes a sprite's scripts and detects long scripts, removing menu blocks first.
        """
        
        menu_blocks = set(consts.PLUGIN_DEADCODE_LIST_MENU_BLOCKS)
        
        for script in sprite_scripts:
            filtered_blocks = [block for block in script.get_blocks() if block not in menu_blocks]
            script_length = len(filtered_blocks)  # Obtiene el número de bloques filtrados en el script
            
            if script_length > length_threshold:
                self.total_long_blocks += 1
                self.list_long_blocks.append({
                    'sprite': sprite_name,
                    'script_length': script_length,
                    'script_text': script.convert_to_text()
                })


    def analyze(self):
        """
        Run and return the results from the SequentialBlocks plugin.
        """

        self.set_sprite_dict()

        for sprite_name, sprite_scripts in self.sprite_dict.items():
            self.analyze_sprite(sprite_name, sprite_scripts)

    def finalize(self):

        self.analyze()
        
        self.dict_mastery['total_long_blocks'] = self.total_long_blocks
        self.dict_mastery['list_long_blocks'] = self.list_long_blocks

        dict_result = {'plugin': 'long_blocks', 'result': self.dict_mastery}

        return dict_result