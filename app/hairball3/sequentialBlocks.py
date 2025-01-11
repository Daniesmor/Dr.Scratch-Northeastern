from app.hairball3.plugin import Plugin
import app.consts_drscratch as consts
from app.hairball3.scriptObject import Script


class SequentialBlocks(Plugin):
    """
    Plugin that keeps track of how often sprites default names (like Sprite1, Sprite2) are used within a project.
    """

    def __init__(self, filename, json_project):
        super().__init__(filename, json_project)
        self.total_sequential = 0
        self.list_sequential = []
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

    def find_repeated_patterns(self, script):
        """
        Detects repeated patterns in a script
        """

        # Extract the blocks from the script with their variables
        script_dict = script.get_script_dict()  
        block_list = [
            {"opcode": block["name"], "vars": list(block[key] for key in block if key.startswith("var_"))}
            for block in script_dict.values()
        ] 
        n = len(block_list)
        detected_patterns = []

        # Detection of all posible patterns
        for length in range(1, n):  
            for start in range(n - length + 1):  
                pattern = block_list[start:start + length]

                repetitions = 1
                while start + repetitions * length + length <= n and \
                        block_list[start + repetitions * length:start + (repetitions + 1) * length] == pattern:
                    repetitions += 1

                if repetitions > 1:
                    pattern_script = Script()
                    custom_dict = {
                        f'block_{i}': {"name": block["opcode"], **{f"var_{j}": value for j, value in enumerate(block["vars"])}}
                        for i, block in enumerate(pattern)
                    }
                    pattern_script.set_custom_script_dict(custom_dict)

                    detected_patterns.append({
                        'pattern': [pattern_script.convert_to_text()],  
                        'start': start,
                        'length': length * repetitions,
                        'repetitions': repetitions
                    })

        # Filter patterns that are contained within other patterns
        filtered_patterns = []
        for candidate in detected_patterns:
            is_contained = any(
                candidate['start'] >= other['start'] and
                candidate['start'] + candidate['length'] <= other['start'] + other['length'] and
                other['length'] > candidate['length']
                for other in detected_patterns
            )
            if not is_contained:
                filtered_patterns.append(candidate)

        # Order patterns by start position
        filtered_patterns.sort(key=lambda x: x['start'])
        return filtered_patterns




    def analyze_sprite(self, sprite_name, sprite_scripts):
        """
        Analyzes a sprite's scripts and detects repeated patterns.
        """

        for script in sprite_scripts:
            patterns = self.find_repeated_patterns(script)

            for pattern_info in patterns:
                self.total_sequential += 1
                self.list_sequential.append({
                    'sprite': sprite_name,
                    'pattern': pattern_info['pattern'],
                    'start': pattern_info['start'],
                    'length': pattern_info['length'],
                    'repetitions': pattern_info['repetitions']
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
        
        self.dict_mastery['total_sequential'] = self.total_sequential
        self.dict_mastery['list_sequential'] = self.list_sequential

        dict_result = {'plugin': 'seq_blocks', 'result': self.dict_mastery}

        return dict_result
