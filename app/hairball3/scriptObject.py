import json

BLOCK_TEXT = json.load(open("app\hairball3/block_to_text.json"))

STARTER_BLOCKS = {"EVENT_WHENFLAGCLICKED",
    "EVENT_WHENTHISSPRITECLICKED",
    "EVENT_WHENSTAGECLICKED",
    "EVENT_WHENTOUCHINGOBJECT",
    "EVENT_WHENBROADCASTRECEIVED",
    "EVENT_WHENBACKDROPSWITCHESTO",
    "EVENT_WHENGREATERTHAN",
    "CONTROL_START_AS_CLONE",
    "PROCEDURES_DEFINITION"}

class Script():
    def __init__(self):
        self.script_dict = {}
        self.child_keys = ['SUBSTACK', 'SUBSTACK2']
        self.arg_keys = ['CONDITION','KEY_OPTION']
        self.counter_block = 0
        self.counter_vars = 0
        self.c = 0
        self.vars = {}
        self.blocks = []

    def parser_block(self, block_dict, block_name):
        block = block_dict[block_name]

        current_counter = self.counter_block
        # print(current_counter)
        new_block = {f'block_{self.counter_block}': {"name":block["opcode"]}}
        self.blocks.append(block["opcode"])
        self.counter_block += 1
        
        # For conditionals
        # for arg_key in self.arg_keys:
        #     if arg_key in block["inputs"]:
        #         arg = self.parser_block(block_dict, block["inputs"][arg_key][1])
        #         new_block[f'block_{current_counter}']["inline"] = arg

        # For custom blocks
        if "mutation" in block and "proccode" in block["mutation"]:
            # print(block)
            # print("mutation found at", f'block_{current_counter}')
            func_name = block["mutation"]["proccode"]

            n_args = func_name.count('%s')

            func_name = func_name % tuple(f'(%{i})' for i in range(1, n_args+1))

            new_block[f'block_{current_counter}']['func_name'] = func_name

            if "argumentnames" in block["mutation"] and '%s' in func_name:
                # print("big yes")
                list_of_arguments = block["mutation"]["argumentnames"].replace('"', '').strip('][').split(',')
                for arg in list_of_arguments:
                    # print("counted")
                    new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = arg

                    self.vars[f'var_{self.counter_vars}'] = arg

                    self.counter_vars += 1

                return new_block

        # For conditionals and operands or any block that is inside another block
        # for arg_key in block["inputs"].keys():
        #     if arg_key not in self.child_keys:
        #         if arg_key == "CONDITION":
        #             arg = self.parser_block(block_dict, block["inputs"][arg_key][1])
        #             new_block[f'block_{current_counter}']["condition"] = arg
        #         elif arg_key == "OPERAND1" or arg_key == "NUM1":
        #             if type(block["inputs"][arg_key][1]) is str and (len(block["inputs"][arg_key][1]) == 20):
        #                 arg = self.parser_block(block_dict, block["inputs"][arg_key][1])
        #                 new_block[f'block_{current_counter}']["operand_1"] = arg
        #         elif arg_key == "OPERAND2" or arg_key == "NUM2":
        #             if type(block["inputs"][arg_key][1]) is str and (len(block["inputs"][arg_key][1]) == 20):
        #                 arg = self.parser_block(block_dict, block["inputs"][arg_key][1])
        #                 new_block[f'block_{current_counter}']["operand_2"] = arg
        #         else:
        #             if type(block["inputs"][arg_key][1]) is str and (len(block["inputs"][arg_key][1]) == 20):
        #                 arg = self.parser_block(block_dict, block["inputs"][arg_key][1])
        #                 new_block[f'block_{current_counter}']["inline"] = arg

        #For fields (variables)
        n_input = 0
        for input, value in block["fields"].items():
            new_var = value[0]

            new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = new_var

            self.vars[f'var_{self.counter_vars}'] = new_var

            self.counter_vars += 1

            n_input += 1
        

        
        for input in block["inputs"].keys():
            if input not in self.child_keys:
                value = block["inputs"][input][1]
                if type(value) is str:
                    if len(value) == 20 or value in block_dict.keys():
                        new_block[f'block_{current_counter}'][f'input_{n_input}'] = self.parser_block(block_dict, value)
                    else:
                        new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = value

                        self.vars[f'var_{self.counter_vars}'] = value

                        self.counter_vars += 1
                else:
                    value = block["inputs"][input][1][1]

                    new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = value

                    self.vars[f'var_{self.counter_vars}'] = value

                    self.counter_vars += 1
                
                n_input += 1


        #For variables (anything that is not a conditional or inside an "if" block)
        # for input, value in block["inputs"].items():
        #     if input not in self.arg_keys and input not in self.child_keys:
        #         if len(value[1]) != 20:
        #             if type(value[1]) is str:
        #                 new_var = value[1]
        #             else:
        #                 new_var = value[1][1]

        #             new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = new_var
        #             self.var_dict[f'var_{self.counter_vars}'] = new_var
        #             self.counter_vars += 1

        return new_block

    def parser_script(self, block_dict, start):
        current = start
        curr_dict = {}
        while True:
            current_block = self.parser_block(block_dict=block_dict, block_name=current)

            #For "if" blocks or "ifelse" blocks
            for i, child_key in enumerate(self.child_keys):
                if child_key in block_dict[current]['inputs']:
                    if block_dict[current]['inputs'][child_key][1]:
                        current_block[[*current_block][0]][f'child_{i}'] = self.parser_script(block_dict, block_dict[current]['inputs'][child_key][1])
                    else:
                        current_block[[*current_block][0]][f'child_{i}'] = None

            curr_dict.update(current_block)

            next_block = block_dict[current]["next"]

            if next_block:
                current = next_block
            else:
                break

        return curr_dict
    
    def set_script_dict(self, block_dict, start):

        self.counter_vars = 0
        self.counter_block = 0
        self.script_dict = self.parser_script(block_dict, start)

    def set_custom_script_dict(self, custom_dict):
        self.script_dict = custom_dict
        return

    def get_vars(self):
        return self.vars
    
    def get_blocks(self):
        return self.blocks
    
    def get_script_dict(self):
        return self.script_dict

    def convert_to_text(self, indent=0, dict=None):
        if dict == None:
            self.c = 0
            dict = self.script_dict

        new_text = ""
        for block, item in dict.items():
            # print(block)
            # print("current variable number", self.c)
            block_name = item["name"]

            if block_name == "procedures_prototype" or block_name == "procedures_call":
                block_text = item["func_name"]
            elif block_name.upper() not in BLOCK_TEXT:
                block_text = "%1"
            else:
                block_text = BLOCK_TEXT[block_name.upper()]

            n_input = 0

            for i in range(1, 4):
                # sub_text ="NOT FOUND"
                if f'%{i}' not in block_text:
                    continue

                if f"var_{self.c}" in item:
                    sub_text = str(item[f"var_{self.c}"])
                    self.c += 1
                    n_input += 1
                elif f"input_{n_input}" in item:
                    sub_text = self.convert_to_text(indent = 0, dict = item[f"input_{n_input}"])
                    n_input += 1

                # if i == 1:
                #     if f"var_{self.c}" in item:
                #         sub_text = str(item[f"var_{self.c}"])
                #         self.c += 1
                #     elif "operand_1" in item:
                #         sub_text = self.convert_to_text(indent = 0, dict = item["operand_1"])
                #     elif "condition" in item:
                #         sub_text = self.convert_to_text(indent = 0, dict = item["condition"])
                #     # elif "value" in item:
                #     #     sub_text = self.convert_to_text(indent = 0, dict = item["value"])
                #     elif "inline" in item:
                #         sub_text = self.convert_to_text(indent = 0, dict = item["inline"])
                #         # self.c += 1
                #         # sub_text = str(item["inline"][list(item["inline"].keys())[0]][f"var_{self.c-1}"])
                # elif i == 2:
                #     if f"var_{self.c}" in item:
                #         sub_text = str(item[f"var_{self.c}"])
                #         self.c += 1
                #     elif "operand_2" in item:
                #         sub_text = self.convert_to_text(indent = 0, dict = item["operand_2"])
                #     # elif "inline" in item:
                #     #     sub_text = self.convert_to_text(indent = 0, dict = item["inline"])
                #         # self.c += 1
                #         # sub_text = str(item["inline"][list(item["inline"].keys())[0]][f"var_{self.c-1}"])
                # else:
                #     # if "inline" in item:
                #     #     sub_text = self.convert_to_text(indent = 0, dict = item["inline"])
                #         # self.c += 1
                #         # sub_text = str(item["inline"][list(item["inline"].keys())[0]][f"var_{self.c-1}"])
                #     if f"var_{self.c}" in item:
                #         sub_text = str(item[f"var_{self.c}"])
                #         self.c += 1

                block_text = block_text.replace(f'%{i}', sub_text)

                
                
            if len(dict) == 1:
                new_text += block_text
            else:
                new_text += '\n' + block_text

            if "child_0" in item:
                if item["child_0"]:

                    new_text += '\n' + '\t'*indent + self.convert_to_text(indent=indent+1, dict=item["child_0"]) 
                else:
                    new_text += '\n' + '\t'*indent 
                
                if "child_1" in item:
                    if item["child_1"]:
                        new_text += '\n' + 'else' + '\n'+ '\t'*indent + self.convert_to_text(indent=indent+1, dict=item["child_1"]) + '\n' + '\t'*indent + 'end'
                    else:
                        new_text += '\n' + 'else' + '\n' + '\t'*indent + 'end'
                else:
                    new_text += '\n' + '\t'*indent + 'end'

        return new_text

    

    
# example_dict = 3

# file = open("app\hairball3\project8.json")

# proj = json.load(file)

# block_dict = {}

# for key, list_dict_targets in proj.items():
#             if key == "targets":
#                 for dict_target in list_dict_targets:
#                     block_name = dict_target['name']
#                     for dict_key, dicc_value in dict_target.items():
#                         if dict_key == "blocks":
#                             for blocks, blocks_value in dicc_value.items():
#                                 if type(blocks_value) is dict:
#                                     block_dict[blocks] = blocks_value


# list_of_scripts_text = []
# for key, value in block_dict.items():
#     if value["topLevel"] and value["opcode"].upper() in STARTER_BLOCKS:
#         print("the key is", key)
#         new_script = Script()


#         new_script.set_script_dict(block_dict, key)

#         list_of_scripts_text.append(new_script.convert_to_text())

#         print(list_of_scripts_text[-1])


# with open("test_scripts8.txt", 'w') as f:
#     f.write('\n'.join(list_of_scripts_text))

# set_of_inputs_keys = set()

# for key, value in block_dict.items():
#     for input in value['inputs'].keys():
#         set_of_inputs_keys.add((input, len(input)))

# print(set_of_inputs_keys)


# new_script = Script()

# new_script.set_script_dict(block_dict, "Ve*1kI;NKi`DpsBlbB?9")

# print(new_script.convert_to_text())

# print(json.dumps(new_script.get_script_dict(), indent=4))

