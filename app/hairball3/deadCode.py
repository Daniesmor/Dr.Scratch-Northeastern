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
                print("DICC VALUEEE")
                print(dicc_value)
                for blocks, blocks_value in dicc_value.items():
                    if type(blocks_value) is dict:
                        out[blocks] = blocks_value
        
        return out

    def analyze(self):

        sprites = {}

        for key, value in self.json_project.items():
            if key == "targets":
                for dicc in value:
                    sprite = dicc["name"]
                    self.dict_babia[sprite] = {}
                    #print(self.dict_babia)
                    currScript = 0
                    blocks_list = []
                    for _, blocks_dicc in dicc["blocks"].items():
                        if type(blocks_dicc) is dict:
                            if blocks_dicc['topLevel'] == True:
                                currScript += 1
                                #print("Dentro del sprite:", sprite)
                                #print("Estamos definiendo el script:",currScript)
                                
                                self.dict_babia[sprite][f'script_{currScript}'] = 0

                            event_var = any(blocks_dicc["opcode"] == event for event in consts.PLUGIN_DEADCODE_LIST_EVENT_VARS)
                            loop_block = any(blocks_dicc["opcode"] == loop for loop in consts.PLUGIN_DEADCODE_LIST_LOOP_BLOCKS)
                            menu_block = any(blocks_dicc["opcode"] == menu for menu in consts.PLUGIN_DEADCODE_LIST_MENU_BLOCKS)

                            if not event_var and not menu_block:
                                if not self.opcode_argument_reporter in blocks_dicc["opcode"]:
                                    if blocks_dicc.get("parent",) is None:
                                        script = Script()
                                        block = script.convert_block_to_text(blocks_dicc)
                                        blocks_list.append(str(block))
                                        
                                        print("MI DEADCODE -----------------------------------------")
                                        if blocks_dicc.get("next",) != None:
                                            next_block_id = blocks_dicc.get("next",)
                                            while (next_block_id != None):
                                                # Verifica si el siguiente bloque está en `dicc["blocks"]` y lo imprime
                                                next_block = dicc["blocks"].get(next_block_id)
                                                
                                                print("Bloque actual:", blocks_dicc)
                                                print("ID del siguiente bloque:", next_block_id)
                                                block = script.convert_block_to_text(next_block)
                                                blocks_list.append(str(block))
                                                self.dict_babia[sprite][f'script_{currScript}'] += 1 
                                                next_block_id = next_block.get("next",)
                                                """ 
                                                if next_block:
                                                    print("Siguiente bloque encontrado:", next_block)
                                                else:
                                                    print("Siguiente bloque no encontrado en `dicc['blocks']`")
                                                """
                                        #print("SE HAN EOCONTRADO 1")
                                        #print("Estoy en el sprite:", sprite)
                                        #print("Estoy en el script:", currScript)
                                        self.dict_babia[sprite][f'script_{currScript}'] += 1 #Incremet one block 
                                    # Check dead loop blocks
                                    if loop_block and blocks_dicc["opcode"] not in blocks_list:
                                        if not blocks_dicc["inputs"]:
                                            # Empty loop block, but inside of a block structure
                                            script = Script()
                                            block = script.convert_block_to_text(blocks_dicc)
                                            blocks_list.append(str(block))
                                            #print("SE HAN EOCONTRADO 2")
                                            self.dict_babia[sprite][f'script_{currScript}'] += 1 #Incremet one block 

                                        elif "SUBSTACK" not in blocks_dicc["inputs"]:
                                            script = Script()
                                            block = script.convert_block_to_text(blocks_dicc)
                                            blocks_list.append(str(block))
                                            #print("SE HAN EOCONTRADO 3")
                                            self.dict_babia[sprite][f'script_{currScript}'] += 1 #Incremet one block 

                                        else: # Could be normal loop block
                                            if blocks_dicc["inputs"]["SUBSTACK"][1] is None:
                                                script = Script()
                                                block = script.convert_block_to_text(blocks_dicc)
                                                blocks_list.append(str(block))
                                                #print("SE HAN EOCONTRADO 4")
                                                self.dict_babia[sprite][f'script_{currScript}'] += 1 #Incremet one block 

                    if blocks_list:
                        scripts = []
                        for block in blocks_list:
                            sprites[sprite] = blocks_list
                            self.dead_code_instances += 1

        self.dict_deadcode = sprites

    def finalize(self):

        self.analyze()

        result = "{}".format(self.filename)

        if self.dead_code_instances > 0:
            result += "\n"
            result += str(self.dict_deadcode)

        self.dict_mastery['description'] = result
        self.dict_mastery['total_dead_code_scripts'] = self.dead_code_instances
        self.dict_mastery['list_dead_code_scripts'] = [self.dict_deadcode]

        dict_result = {'plugin': 'dead_code', 'result': self.dict_mastery, 'babia': self.dict_babia}

        return dict_result



