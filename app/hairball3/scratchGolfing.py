import logging
import app.consts_drscratch as consts
from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
from collections import Counter
logger = logging.getLogger(__name__)



class ScratchGolfing(Plugin):
    """
    Plugin that indicates some Comparsion info between two projects.
    """
    
    def __init__(self, json_original_project, json_compare_project, verbose=False):
        super().__init__(json_original_project, json_compare_project, verbose)
        self.sprite_dict = [{}, {}] 
        self.sprite_dict_format = [{}, {}] 
        self.opcode_argument_reporter = "argument_reporter"
        self.json_original_project = json_original_project
        self.json_compare_project = json_compare_project


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
        
        projects = [self.json_original_project, self.json_compare_project]
        for project_num, project in enumerate(projects):
            for key, list_dict_targets in project.items():
                
                if key == "targets":
                    for dict_target in list_dict_targets:
                        project_name = project
                        sprite_name = dict_target['name']
                        
                        sprite_blocks = self.get_blocks(dict_target)
                        sprite_scripts = []

                        for key, block in sprite_blocks.items():
                            
                            if block["topLevel"]:
                                new_script = Script()
                                new_script.set_script_dict(block_dict=sprite_blocks, start=key)                            
                                sprite_scripts.append(new_script)


                        self.sprite_dict[project_num][sprite_name] = sprite_blocks 
                        script_text = "\n\n".join([script.convert_to_text() for script in sprite_scripts])
                        self.sprite_dict_format[project_num][sprite_name] = script_text
    
    
    def analyze(self):
        """
        Analyze the ammount of sprites and blocks of each projec
        """
        self.set_sprite_dict()
        self.golfing_summary = {}       
        self.golfing_summary['original'] = {}
        self.golfing_summary['new'] = {}

        original_num_sprites = len(self.sprite_dict[0]) - 1 
        new_num_sprites = len(self.sprite_dict[1]) - 1 
        
        for sprite, scripts in self.sprite_dict[0].items():
            if sprite != "Stage":
                original_num_scripts = len(scripts)
                self.golfing_summary['original'][sprite] = original_num_scripts
                
        for sprite, scripts in self.sprite_dict[1].items():
            if sprite != "Stage":
                new_num_scripts = len(scripts)
                self.golfing_summary['new'][sprite] = new_num_scripts
                
        self.golfing_summary['original']['total_blocks'] = sum(self.golfing_summary['original'].values())
        self.golfing_summary['new']['total_blocks'] = sum(self.golfing_summary['new'].values())               
        self.golfing_summary['original']['total_sprites'] = original_num_sprites
        self.golfing_summary['new']['total_sprites'] = new_num_sprites
            
        return self.golfing_summary
    
    def calc_percent(self):
        """
        This function calc the percent of difference and similarity between two projectss
        """

        # Versión 1 -> Difference

        original_total = self.golfing_summary['original']['total_blocks'] + self.golfing_summary['original']['total_sprites']
        new_total = self.golfing_summary['new']['total_blocks'] + self.golfing_summary['new']['total_sprites']

        absolute_difference = abs(original_total - new_total)
        base_value = max(original_total, new_total)
        percent_difference = (absolute_difference / base_value) * 100
        percent_difference = round(percent_difference, 2)

        self.golfing_summary['difference'] = f'{round(percent_difference, 2)}'

        # Versión 2 -> Similarity

        original_blocks = [block.get('opcode') for blocks in self.sprite_dict[0].values() for block in blocks.values()]
        new_blocks = [block.get('opcode') for blocks in self.sprite_dict[1].values() for block in blocks.values()]

        original_counter = Counter(original_blocks)
        new_counter = Counter(new_blocks)

        common_blocks = original_counter & new_counter

        common_blocks_counter = sum(common_blocks.values())  
        total_blocks_counter = sum(original_counter.values()) + sum(new_counter.values())

        similarity = (2*common_blocks_counter / total_blocks_counter) * 100 if total_blocks_counter!= 0 else 0

        self.golfing_summary['similarity'] = f'{round(similarity, 2)}'
    
    def finalize(self) -> dict:

        self.analyze()
        self.calc_percent()

        self.dict_mastery['scratch_golfing'] = self.golfing_summary
        
        if self.verbose:
            logger.info(self.dict_mastery['list_changes_scripts'])
            logger.info(self.dict_mastery['changes'])
        
        dict_result = {'plugin': 'ScratchGolfing', 'result': self.dict_mastery}

        return dict_result