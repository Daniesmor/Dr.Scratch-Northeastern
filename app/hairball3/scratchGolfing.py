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
        self.sprite_dict = {'original': {}, 'new': {}} 
        self.secuences_dict = {'original': {}, 'new': {}} 
        self.sprite_dict_format = {'original': {}, 'new': {}} 
        self.golfing_summary = {'original': {}, 'new': {}}
        self.opcode_argument_reporter = "argument_reporter"
        self.json_original_project = json_original_project
        self.json_compare_project = json_compare_project

    
    def process(self):
        """
        Sets a dictionary containing the scripts of each sprite in Script() format
        """
        
        projects = {"original": self.json_original_project,"new": self.json_compare_project}
        for project_num, project in projects.items():
            counter = 0
            for key, list_dict_targets in project.items():
                if key == "targets":
                    for dict_target in list_dict_targets:
                        project_name = project
                        sprite_name = dict_target['name']
                        
                        sprite_blocks = self.get_blocks(dict_target)
                        sprite_scripts = []

                        for key, block in sprite_blocks.items():
                            # print("Block: ", block)
                            
                            if block["topLevel"]:
                                counter += 1
                                new_script = Script()
                                new_script.set_script_dict(block_dict=sprite_blocks, start=key)                            
                                sprite_scripts.append(new_script)
                            
                            if counter not in self.secuences_dict[project_num]:
                                self.secuences_dict[project_num][counter] = []
                            self.secuences_dict[project_num][counter].append(block.get("opcode"))


                        self.sprite_dict[project_num][sprite_name] = sprite_blocks 
                        script_text = "\n\n".join([script.convert_to_text() for script in sprite_scripts])
                        self.sprite_dict_format[project_num][sprite_name] = script_text
    
    
    def analyze(self):
        self.calc_percent()


    def finalize(self) -> dict:
        """
        Analyze the changes between two projects and return a dictionary with the results
        """

        self.process()
        self.analyze()

        self.dict_mastery['scratch_golfing'] = self.golfing_summary
        
        if self.verbose:
            logger.info(self.dict_mastery['list_changes_scripts'])
            logger.info(self.dict_mastery['changes'])
        
        dict_result = {'plugin': 'ScratchGolfing', 'result': self.dict_mastery}

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
    
    def calc_percent(self):
        """
        This function calc the percent of similarity between two projectss
        """

        original_secuences = [secuence for secuence in self.secuences_dict["original"].values()]
        new_secuences = [secuence for secuence in self.secuences_dict["new"].values()]

        original_counter = Counter(map(tuple, original_secuences))
        new_counter = Counter(map(tuple, new_secuences))
        
        common_secuences = original_counter & new_counter

        common_secuences_counter = sum(common_secuences.values())  
        total_secuences_counter = sum(original_counter.values()) + sum(new_counter.values())

        similarity = (2*common_secuences_counter / total_secuences_counter) * 100 if total_secuences_counter!= 0 else 0

        self.golfing_summary['similarity'] = f'{round(similarity, 2)}'

    
