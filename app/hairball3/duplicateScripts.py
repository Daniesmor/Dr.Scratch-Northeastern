from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class DuplicateScripts(Plugin):
    """
    Plugin that analyzes duplicate scripts in scratch projects version 3.0
    """

    def __init__(self, filename, json_project, verbose=False):
        super().__init__(filename, json_project, verbose)
        self.total_duplicate = 0
        self.sprite_dict = {}
        self.duplicates = {}
        self.list_duplicate = []
        self.list_csv = []

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
        Searches for intra duplicates of each sprite and outputs them
        """
        self.set_sprite_dict()
        
        for sprite, scripts in self.sprite_dict.items():
            seen = set()
            sprite_duplicates = {}
            for script in scripts:
                blocks = tuple(script.get_blocks())

                if blocks not in sprite_duplicates.keys():
                    if len(blocks) > 5:
                        sprite_duplicates[blocks] = [(script, sprite)]
                else:
                    sprite_duplicates[blocks].append((script, sprite))

                seen.add(blocks)


            for key in seen:
                if key in sprite_duplicates:
                    if len(sprite_duplicates[key]) <= 1:
                        sprite_duplicates.pop(key, None)

            self.duplicates.update(sprite_duplicates)

        for key, value in self.duplicates.items():
            duplicated_scripts = [pair[0] for pair in value]
            csv_text = [script.get_blocks() for script in duplicated_scripts]
            script_text = "\n\n".join([script.convert_to_text() for script in duplicated_scripts])
            self.total_duplicate += sum(1 for _ in duplicated_scripts)
            self.list_duplicate.append(script_text)
            self.list_csv.append(csv_text)

        return self.duplicates

    def finalize(self) -> dict:

        self.analyze()

        result = ("%d duplicate scripts found" % self.total_duplicate)
        result += "\n"
        for duplicate in self.list_duplicate:
            result += str(duplicate)
            result += "\n"

        self.dict_mastery['description'] = result
        self.dict_mastery['total_duplicate_scripts'] = self.total_duplicate
        self.dict_mastery['list_duplicate_scripts'] = self.list_duplicate
        self.dict_mastery['duplicates'] = self.duplicates
        self.dict_mastery['list_csv'] =  self.list_csv

        if self.verbose:
            logger.info(self.dict_mastery['description'])
            logger.info(self.dict_mastery['total_duplicate_scripts'])
            logger.info(self.dict_mastery['list_duplicate_scripts'])

        dict_result = {'plugin': 'duplicate_scripts', 'result': self.dict_mastery}

        return dict_result

