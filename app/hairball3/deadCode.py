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
        self.script_block_list = {}
        self.opcode_argument_reporter = "argument_reporter"
        self.dict_babia = {}

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
                    self.proccess_sprite(dicc, sprites)
                    
        self.dict_deadcode = sprites


    def proccess_sprite(self, dicc: dict, sprites: dict):
        """
        Proccess each sprite of the project.
        """
        self.sprite = dicc["name"]
        self.dict_babia[self.sprite] = {}
        sprites[self.sprite] = {}
        blocks_by_script = self.proccess_and_store_script(dicc, sprites)
        self.store_processed_blocks(blocks_by_script, sprites[self.sprite])


    def store_processed_blocks(self, blocks_by_script: dict, currSprite: dict):
        """
        Store blocks proccessed in sprites dicc.
        """
        for script_name, self.blocks_list in blocks_by_script.items():
            currSprite[script_name] = self.blocks_list


    def proccess_and_store_script(self, dicc: dict, sprites: dict) -> dict:
        """
        Proccess each script of a sprite
        """
        self.currScript = 0
        blocks_by_script = {}
        self.blocks_list = []
        for blocks, blocks_dicc in dicc["blocks"].items():
            if isinstance(blocks_dicc, dict):
                self.proccess_block(blocks_dicc, dicc, blocks)
                if self.blocks_list:
                    blocks_by_script[f'script_{self.currScript}'] = self.blocks_list
                    self.blocks_list = []
        return blocks_by_script
          
    
    def proccess_block(self, blocks_dicc: dict, dicc: dict, blocks) -> None:
        
        if blocks_dicc['topLevel'] == True:
            
            self.currScript += 1
            self.dict_babia[self.sprite][f'script_{self.currScript}'] = 0

        is_event = self.is_event_var(blocks_dicc)
        is_loop = self.is_loop_block(blocks_dicc)
        is_menu = self.is_menu_block(blocks_dicc)

            
        if is_event:
            self.handle_event_block(dicc, blocks)
            
        if not is_event and not is_menu:
            if not self.opcode_argument_reporter in blocks_dicc["opcode"]:
                self.handle_general_block(blocks_dicc, dicc, blocks) 
                
                # Check dead loop blocks
                if self.is_loop_block(blocks_dicc) and blocks_dicc["opcode"] not in self.blocks_list:
                    if blocks_dicc["parent"] == None:
                        self.handle_loop_block(blocks_dicc, dicc, blocks)                  
        self.blocks_list
    

    def is_event_var(self, blocks_dicc):
        return any(blocks_dicc["opcode"] == event for event in consts.PLUGIN_DEADCODE_LIST_EVENT_VARS)

    def is_loop_block(self, blocks_dicc):
        return any(blocks_dicc["opcode"] == loop for loop in consts.PLUGIN_DEADCODE_LIST_LOOP_BLOCKS)
    
    def is_menu_block(self, blocks_dicc):
        return any(blocks_dicc["opcode"] == menu for menu in consts.PLUGIN_DEADCODE_LIST_MENU_BLOCKS)

    def handle_event_block(self, dicc, blocks):
        if not self.has_next_block(dicc["blocks"][blocks]):
            self.store_script(dicc, blocks)


    def handle_general_block(self, blocks_dicc, dicc, blocks):
        if blocks_dicc.get("parent") == None:
            self.store_script(dicc, blocks)

            if self.has_next_block(blocks_dicc):
                next_block_id = blocks_dicc.get("next")
                while (next_block_id != None):
                    # Checks if the next block is in `dicc["blocks"]` and prints it    
                    next_block = dicc["blocks"].get(next_block_id)
                    self.store_script(dicc, blocks)
                    next_block_id = next_block.get("next")

    
    def handle_loop_block(self, blocks_dicc, dicc, blocks):   
        if not blocks_dicc["inputs"]:
            # Empty loop block, but inside of a block structure
            self.store_script(dicc, blocks)
        elif "SUBSTACK" not in blocks_dicc["inputs"]:
            self.store_script(dicc, blocks)
        else:  # Could be normal loop block            
            first_substack_id = blocks_dicc["inputs"]["SUBSTACK"][1]
            first_substack_dicc = dicc["blocks"].get(first_substack_id)
            
            if first_substack_dicc is not None:
                if self.is_loop_block(first_substack_dicc):
                    self.handle_loop_block(first_substack_dicc, dicc, blocks)
                else:
                    # Iterar sobre los bloques siguientes
                    while first_substack_dicc is not None and self.has_next_block(first_substack_dicc):
                        first_substack_id = first_substack_dicc.get("next")
                        first_substack_dicc = dicc["blocks"].get(first_substack_id)

                        if first_substack_dicc is not None:
                            if self.is_loop_block(first_substack_dicc):
                                self.handle_loop_block(first_substack_dicc, dicc, blocks)
            self.store_script(dicc, blocks)          
          

    def store_script(self, dicc, blocks):
        """
        Store script in block_list.
        """
        script_text = self.get_script_text(dicc["blocks"], blocks)
        clean_script_text = [line for line in script_text.split('\n') if line.strip()]
        
        if script_text not in self.blocks_list:
            self.blocks_list = [script_text]  
            self.dict_babia[self.sprite][f'script_{self.currScript}'] = len(clean_script_text) #Incremet one block

    def get_script_text(self, dicc_blocks, start):
        """
        Get current script in visual format.
        """
        script = Script()
        script.set_script_dict(block_dict=dicc_blocks, start=start)
        return script.convert_to_text()

    def has_next_block(self, blocks_dicc):
        """
        Check if current block has a next block
        """
        return blocks_dicc.get("next") is not None
    

    def finalize(self):

        self.analyze()

        result = "{}".format(self.filename)

        for _, scripts in self.dict_babia.items():
            for _, script_len in scripts.items():
                self.dead_code_instances += script_len

        if self.dead_code_instances > 0:
            result += "\n"
            result += str(self.dict_deadcode)

        self.dict_mastery['description'] = result
        self.dict_mastery['total_dead_code_scripts'] = self.dead_code_instances
        self.dict_mastery['list_dead_code_scripts'] = [self.dict_deadcode]

        dict_result = {'plugin': 'dead_code', 'result': self.dict_mastery, 'babia': self.dict_babia}

        return dict_result



