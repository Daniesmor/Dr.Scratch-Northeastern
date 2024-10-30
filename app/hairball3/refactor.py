from app.hairball3.scriptObject import Script
from app.hairball3.duplicateScripts import DuplicateScripts

N_VARIABLES_IN_STARTER_BLOCK = {"EVENT_WHENFLAGCLICKED":0,
    "EVENT_WHENKEYPRESSED":1,
    "EVENT_WHENTHISSPRITECLICKED":0,
    "EVENT_WHENSTAGECLICKED":0,
    "EVENT_WHENTOUCHINGOBJECT":1,
    "EVENT_WHENBROADCASTRECEIVED":1,
    "EVENT_WHENBACKDROPSWITCHESTO":1,
    "EVENT_WHENGREATERTHAN":2,
    "CONTROL_START_AS_CLONE":0,
    "PROCEDURES_DEFINITION":0}

class RefactorDuplicate():
    def __init__(self, json_project, duplicates_dict):
        self.duplicates = duplicates_dict['result']['duplicates']
        self.json_project = json_project
        self.block_dict = {}
        self.sprite_dict = {}
        self.constants = []
        self.variables = []
        self.refactored = {}
        self.clones = {}
        self.arg_count = 1

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
        
        return self.sprite_dict
    
    def search_clones(self):
        """
        Searches for sprite clones
        """
        self.clones = {}

        seen = set()

        for sprite, scripts in self.sprite_dict.items():
            tuple_of_scripts = tuple([tuple(script.get_blocks()) for script in scripts])

            if tuple_of_scripts not in self.clones.keys():
                self.clones[tuple_of_scripts] = [(scripts, sprite)]

            else:
                self.clones[tuple_of_scripts].append((scripts, sprite))

            seen.add(tuple_of_scripts)
        
        for tupl in seen:
            if len(self.clones[tupl]) <= 1:
                self.clones.pop(tupl, None)

        return self.clones
    
    def refactor_duplicates(self):
        """
        Converts duplicated scripts into a custom block format. It outputs a list of tuples containing the original blocks, the refactorization
        and the sprite all in the scratchblocks text format.
        """
        duplicates = self.duplicates
        func_counter = 1
        refactored_list = []

        for key, value in duplicates.items():
            sprite_name = value[0][1]

            starting_block_type = value[0][0].get_blocks()[0]

            duplicated_scripts = [pair[0] for pair in value]

            original_text = "\n\n".join([script.convert_to_text() for script in duplicated_scripts])

            # Top Blocks (like when green flag clicked)
            try:
                starting_blocks = [script.convert_to_text().split("\n")[1] for script in duplicated_scripts]
            except IndexError:
                starting_blocks = [script.convert_to_text().split("\n")[0] for script in duplicated_scripts]

            list_script_variables = [script.get_vars() for script in duplicated_scripts]

            var_dict = {}

            for i, k in enumerate(list_script_variables[0].keys()):

                try:
                    if i < N_VARIABLES_IN_STARTER_BLOCK[starting_block_type.upper()]:
                        continue
                except KeyError:
                    pass

                var_dict[k] = [d[k] for d in list_script_variables]
            
            constants, arguments = self.search_constants_and_arguments(var_dict)


            # Custom Block refactorization
            func_script = Script()
            func_script.set_custom_script_dict(self.refactor_duplicate_script(script=duplicated_scripts[0], arguments=arguments))

            func_text_list = func_script.convert_to_text().split('\n')

            if (starting_block_type.upper() not in N_VARIABLES_IN_STARTER_BLOCK.keys()):
                func_text_list.insert(0,f"define function{func_counter}" + "".join([f" (arg{i})" for i in range(1, len(arguments)+1)]))
            else:
                func_text_list[1] = f"define function{func_counter}" + "".join([f" (arg{i})" for i in range(1, len(arguments)+1)])

            calling_text_list = []


            for i, variables in enumerate(list_script_variables):
                new_call = starting_blocks[i] + "\n" + f"function{func_counter}" 
                for arg in arguments:
                    new_call += f" [{variables[arg]}]"
                
                calling_text_list.append(new_call)

            refactored_text = "\n".join(func_text_list) + "\n" + "\n".join(calling_text_list)

            refactored_list.append({"original":original_text, "refactored":refactored_text, "sprite":sprite_name})

        return refactored_list


    def refactor_duplicate_script(self, script: Script, arguments):
        """
        Helper function to change the corresponding variables to their argument counterparts
        """
        parsed_script = script.get_script_dict()
        self.arg_count = 1

        def _next_block(curr):
            for key, value in curr.items():
                if key in arguments:
                    curr[key] = f"arg{self.arg_count}"
                    self.arg_count += 1
                else:
                    if type(curr[key]) is dict:
                        _next_block(curr[key])
        
        _next_block(parsed_script)

        return parsed_script


    def search_constants_and_arguments(self, var_dict):
        constants = []
        arguments = []

        for key, value in var_dict.items():
            if len(set(value)) == 1:
                constants.append(key)
            else:
                arguments.append(key)

        return (constants, arguments)


    def refactor_sprite_clones(self):
        pass