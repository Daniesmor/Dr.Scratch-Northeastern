import json
from scriptObject import Script


class RefactorDuplicate():
    def __init__(self, json):
        self.duplicates = {}
        self.json = json
        self.block_dict = {}
        self.sprite_dict = {}
        self.constants = []
        self.variables = []
        self.refactored = {}
        self.clones = {}
        self.arg_count = 1

    def get_blocks(self, dict_target):
        out = {}


        for dict_key, dicc_value in dict_target.items():
            if dict_key == "blocks":
                for blocks, blocks_value in dicc_value.items():
                    if type(blocks_value) is dict:
                        out[blocks] = blocks_value
        
        return out


    def set_sprite_dict(self):
        block_dict = []

        for key, list_dict_targets in proj.items():
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
    
    def search_duplicates(self):
        self.duplicates = {}
        
        for sprite, scripts in self.sprite_dict.items():
            seen = set()
            for script in scripts:
                blocks = tuple(script.get_blocks())

                if blocks not in self.duplicates.keys():
                    if len(blocks) > 5:
                        self.duplicates[blocks] = [(script, sprite)]
                else:
                    self.duplicates[blocks].append((script, sprite))

                seen.add(blocks)


            for key in seen:
                if key in self.duplicates:
                    if len(self.duplicates[key]) <= 1:
                        self.duplicates.pop(key, None)

        return self.duplicates
    
    def search_clones(self):
        self.clones = {}

        seen = set()

        for sprite, scripts in self.sprite_dict.items():
            tuple_of_scripts = tuple([tuple(script.get_blocks()) for script in scripts])



            if tuple_of_scripts not in self.clones.keys():
                self.clones[tuple_of_scripts] = [(scripts, sprite)]
                # self.clones[tuple_of_scripts] = [sprite]

            else:
                self.clones[tuple_of_scripts].append((scripts, sprite))
                # self.clones[tuple_of_scripts].append(sprite)

            seen.add(tuple_of_scripts)
        
        for tupl in seen:
            if len(self.clones[tupl]) <= 1:
                self.clones.pop(tupl, None)

        return self.clones
            
    
    def refactor_duplicates(self):
        duplicates = self.search_duplicates()
        func_counter = 1
        refactored_list = []

        for key, value in duplicates.items():
            duplicated_scripts = [pair[0] for pair in value]

            list_script_variables = [script.get_vars() for script in duplicated_scripts]

            var_dict = {}

            for k in list_script_variables[0].keys():
                var_dict[k] = [d[k] for d in list_script_variables]
            
            constants, arguments = self.search_constants_and_arguments(var_dict)


            func_script = Script()
            func_script.set_custom_script_dict(self.refactor_duplicate_script(script=duplicated_scripts[0], arguments=arguments))

            func_text_list = func_script.convert_to_text().split('\n')
            starting_block = func_text_list[1]

            func_text_list[1] = f"define function{func_counter}" + "".join([f" (arg{i})" for i in range(1, len(arguments)+1)])

            calling_text_list = []


            for variables in list_script_variables:
                new_call = starting_block + "\n" + f"function{func_counter}" 
                for arg in arguments:
                    new_call += f" [{variables[arg]}]"
                
                calling_text_list.append(new_call)

            refactored_text = "\n".join(func_text_list) + "\n" + "\n".join(calling_text_list)

            refactored_list.append(refactored_text)

        return "\n".join(refactored_list)


    def refactor_duplicate_script(self, script: Script, arguments):
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
    



file = open("app\hairball3\project.json")

proj = json.load(file)



refactor = RefactorDuplicate(proj)

refactor.set_sprite_dict()

# print(refactor.search_duplicates())
print(refactor.refactor_duplicates())

# print(refactor.search_clones())

# print(refactor.search_clones())

