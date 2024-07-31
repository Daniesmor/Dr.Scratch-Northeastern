import logging
import app.consts_drscratch as consts
from app.hairball3.plugin import Plugin
from app.hairball3.scriptObject import Script
logger = logging.getLogger(__name__)



class ComparsionMode(Plugin):
    """
    Plugin that indicates some Comparsion info between two projects.
    """
    
    def __init__(self, json_original_project, json_compare_project, verbose=False):
        super().__init__(json_original_project, json_compare_project, verbose)
        self.total_duplicate = 0
        self.sprite_dict = [{}, {}] 
        self.sprite_dict_format = [{}, {}] 
        self.duplicates = {}
        self.list_duplicate = []
        self.list_csv = []
        self.opcode_argument_reporter = "argument_reporter"
        self.json_original_project = json_original_project
        self.json_compare_project = json_compare_project
        print("init--")


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
                                #print("Esto es sprite_scripts --------------------------------------------")
                                #print(sprite_scripts)


                        self.sprite_dict[project_num][sprite_name] = sprite_blocks # contiene bloques y parametros
                        #self.sprite_dict_format[project_num][sprite_name] = sprite_scripts # formato <app.Hairball.scriptObject...
                        
                        
                        #csv_text = [script.get_blocks() for script in sprite_scripts]
                        script_text = "\n\n".join([script.convert_to_text() for script in sprite_scripts])
                        #print("script_text", script_text)
                        self.sprite_dict_format[project_num][sprite_name] = script_text
                        
                        #print("mi sprite scripts")
                        #print(self.sprite_dict[project_num][sprite_name])
                        #self.sprite_dict[project_num][sprite_name] = sprite_scripts # formato <app.Hairball.scriptObject...
    
    def convert_format(self, sprite_blocks):
        sprite_scripts =  []
        for key, block in sprite_blocks.items():

            if block["topLevel"]:
                new_script = Script()
                new_script.set_script_dict(block_dict=sprite_blocks, start=key)                            
                sprite_scripts.append(new_script)
                #print("Esto es sprite_scripts --------------------------------------------")
                #print(sprite_scripts)
                
        script_text = "\n\n".join([script.convert_to_text() for script in sprite_scripts])
        
        print("deupracion convert_format")
        #print(script_text)
        return script_text

    
    
    def analyze(self):
        """
        Searches for intra duplicates of each sprite and outputs them
        """
        self.set_sprite_dict()
        
        # Almacenamos scipts del mismo sprite que no estaban antes
        self.d_changes = {} #Dict que contiene cambios respectoa al proyecto original
        self.d_changes_scripts = {} 
        projects = [self.json_original_project, self.json_compare_project]

        for sprite, scripts in self.sprite_dict[1].items():
            self.d_changes["new_sprites"] = []
            self.d_changes["removed_sprites"] = []
            self.d_changes[sprite] = []
            self.d_changes_scripts[sprite] = []
            if (sprite not in self.sprite_dict[0].keys()):
                print("added")
                self.d_changes_scripts[sprite] = (self.convert_format(self.sprite_dict[1][sprite]), 'added')
                
                if (sprite not in self.d_changes["new_sprites"]):
                    self.d_changes["new_sprites"].append(sprite)  
                for block in scripts:
                    self.d_changes[sprite].append((self.sprite_dict[1][sprite][block], 'added'))
                    #self.convert_format(self.sprite_dict[1][sprite])
            else:
                for block in scripts:
                    
                    if (block not in self.sprite_dict[0][sprite]):
                        self.d_changes[sprite].append((self.sprite_dict[1][sprite][block], 'added'))
                #self.convert_format(self.sprite_dict[1][sprite])
 
        
        # Buscamos bloques del proyecto original que se han borrado en el nuevo
        for sprite, scripts in self.sprite_dict[0].items():
            if (sprite not in self.sprite_dict[1].keys()):
                print("removed")
                self.d_changes_scripts[sprite] = (self.convert_format(self.sprite_dict[0][sprite]), 'removed')
                self.d_changes[sprite] = []
                if (sprite not in self.d_changes["removed_sprites"]):
                    self.d_changes["removed_sprites"].append(sprite)  
                for block in scripts:
                    self.d_changes[sprite].append((self.sprite_dict[0][sprite][block], 'removed'))
            else:
                for script in scripts:
                    
                    if (script not in self.sprite_dict[1][sprite]):
                        if self.d_changes[sprite]:
                            self.d_changes[sprite].append((self.sprite_dict[0][sprite][script], 'removed'))      
                        else:
                            self.d_changes[sprite] = [(self.sprite_dict[0][sprite][script], 'removed')]     
        
        
        # Borramos listas vacias (sprites en los que no se ha añadido ni eliminado bloques)
        for sprite_key, sprite_value in list(self.d_changes.items()):
            if sprite_value == []:
                del self.d_changes[sprite_key]
                    
        if self.d_changes == {}:
            print("No se ha añadido ni quitado ningun bloque")
        else:
            pass
            #print(self.d_changes)
        
        
        
        # Borramos listas vacias (sprites en los que no se ha añadido ni eliminado bloques)
        for sprite_key, sprite_value in list(self.d_changes_scripts.items()):
            if sprite_value == []:
                del self.d_changes_scripts[sprite_key]

            
            
        return self.d_changes
    
    
    def finalize(self) -> dict:

        self.analyze()

        """
        result = ("%d duplicate scripts found" % self.total_duplicate)
        result += "\n"
        for duplicate in self.list_duplicate:
            result += str(duplicate)
            result += "\n"
        """
        #self.dict_mastery['description'] = result
        #self.dict_mastery['total_duplicate_scripts'] = self.total_duplicate
        #self.dict_mastery['list_duplicate_scripts'] = self.list_duplicate
        #self.dict_mastery['duplicates'] = self.duplicates
        #self.dict_mastery['list_csv'] =  self.list_csv
        self.dict_mastery['list_changes_scripts'] = self.d_changes_scripts
        self.dict_mastery['list_changes'] = self.d_changes

        print(self.dict_mastery)
        
        if self.verbose:
            #logger.info(self.dict_mastery['description'])
            logger.info(self.dict_mastery['list_changes_scripts'])
            logger.info(self.dict_mastery['changes'])
        
        dict_result = {'plugin': 'ComparsionMode', 'result': self.dict_mastery}

        return dict_result