import json
from app.hairball3.plugin import Plugin
import app.consts_drscratch as consts
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class Mastery(Plugin):

    def __init__(self, filename: str, json_project, skill_points: dict,verbose=False):
        super().__init__(filename, json_project, skill_points, verbose)
        self.possible_scores = {"finesse": 5, "advanced": 4, "proficient": 3, "developing": 2, "basic": 1}
        self.dict_total_blocks = {}

    def process(self):

        for key, list_info in self.json_project.items():
            if key == "targets":
                for dict_target in list_info:
                    for dicc_key, dicc_value in dict_target.items():
                        if dicc_key == "blocks":
                            for blocks, blocks_value in dicc_value.items():
                                if type(blocks_value) is dict:
                                    self.list_total_blocks.append(blocks_value)
                                    self.dict_total_blocks[blocks] = blocks_value

        for block in self.list_total_blocks:
            for key, list_info in block.items():
                if key == "opcode":
                    self.dict_blocks[list_info] += 1

    def analyze(self):
        # print(self.list_total_blocks)
        self.compute_logic()
        self.compute_flow_control()
        self.compute_synchronization()
        self.compute_abstraction()
        self.compute_data_representation()
        self.compute_user_interactivity()
        self.compute_parallelization()
        self.compute_math_operators()
        self.compute_motion_operators()


    
    def finalize(self) -> dict:

        self.process()
        self.analyze()

        total_points = 0

        for skill, skill_grade in self.dict_mastery.items():
            if self.verbose:
                logger.info('Skill: {}, points: {}'.format(skill, skill_grade))
            total_points = total_points + skill_grade[0]
            total_points = round(total_points, 2)


        average_points = float(total_points) / 9
        total_maxi_points = sum(self.skill_points.values())

        result = '{}{}{}{}'.format(self.filename, '\n', json.dumps(self.dict_mastery), '\n')
        result += ('Total mastery points: {}/{}\n'.format(total_points, total_maxi_points))
        result += ('Average mastery points: {}/{}\n'.format(average_points, consts.PLUGIN_MASTERY_AVG_POINTS))

       
        """
        EXTENDED MODE
        """
        extended_points = total_maxi_points
        exetended_competence = self.calc_averages(average_points, 'extended')


        self.dict_mastery['total_points'] = [total_points, total_maxi_points]
        self.dict_mastery['max_points_extended'] = extended_points
        self.dict_mastery['average_points'] = round(average_points, 2)
        self.dict_mastery['competence'] = exetended_competence["programming_competence"]
        #self.dict_mastery['description'] = result

        if self.verbose:
            logger.info(self.dict_mastery['description'])
            
        extended_dict = self.dict_mastery.copy()
        
        """
        VANILLA MODE
        """
        self.dict_mastery = self.calc_extrapolation(self.dict_mastery)
        vanilla_points = sum(points[0] for points in self.dict_mastery.values())
        average_points = vanilla_points / 7
        vanilla_competence = self.calc_averages(average_points, 'vanilla')


        self.dict_mastery['total_points'] = [round(vanilla_points,2), 21]
        self.dict_mastery['max_points_vanilla'] = 21
        self.dict_mastery['average_points'] = round(average_points, 2)
        self.dict_mastery['competence'] = vanilla_competence["programming_competence"]
        #self.dict_mastery['description'] = result

        if self.verbose:
            logger.info(self.dict_mastery['description'])
            
        vanilla_dict = self.dict_mastery.copy()
        

        dict_result = {'plugin': 'mastery', 'extended': extended_dict, 'vanilla': vanilla_dict}

        return dict_result

    def calc_extrapolation(self, dict_mastery) -> dict:
        """
        Extrapolate the points of the extended mode to the vanilla mode.
        """
        mastery = {'Logic', 'FlowControl', 'Synchronization', 'Abstraction', 'DataRepresentation', 
                'UserInteractivity', 'Parallelization'}
        
        new_dict = {}
        for skill in dict_mastery:
            if skill in mastery:
                if dict_mastery[skill][0] > 3:
                    new_value = 3
                else:
                    new_value = dict_mastery[skill][0]
                new_dict[skill] = [new_value, 3]
        return new_dict

    def calc_averages(self, average_points, mode):
        result = ''
        programming_competence = ''
        if mode == 'extended':
            if average_points > 36:
                result += "Overall programming competence: Finesse"
                programming_competence = 'Finesse'
            elif average_points > 27:
                result += "Overall programming competence: Advanced"
                programming_competence = 'Advanced'
            elif average_points > 18:
                result += "Overall programming competence: Proficiency"
                programming_competence = 'Master'
            elif average_points > 9:
                result += "Overall programming competence: Developing"
                programming_competence = 'Developing'
            else:
                result += "Overall programming competence: Basic"
                programming_competence = 'Basic'
        else: #Vanilla
            if average_points > 15:
                result += "Overall programming competence: Master"
                programming_competence = 'Master'
            elif average_points > 7:
                result += "Overall programming competence: Developing"
                programming_competence = 'Developing'
            else:
                result += "Overall programming competence: Basic"
                programming_competence = 'Basic'
        
        competence_dict = {
            'result': result, 
            'programming_competence': programming_competence
            }
        return competence_dict
    
    def set_dimension_score(self, scale_dict, dimension):

        score = 0
        

        for key, value in scale_dict.items():
            if type(value) == bool and value is True:
                if key in self.possible_scores.keys():
                    score = self.skill_points[dimension] * self.possible_scores[key] / len(self.possible_scores.keys())
                    self.dict_mastery[dimension] = [score, self.skill_points[dimension]] 
                    return
            elif type(value) == set:
                for item in value:
                    if self.dict_blocks[item]:
                        if key in self.possible_scores.keys():
                            score = self.skill_points[dimension] * self.possible_scores[key] / len(self.possible_scores.keys())
                            self.dict_mastery[dimension] = [score, self.skill_points[dimension]] 
                            return

        self.dict_mastery[dimension] = [score, self.skill_points[dimension]] 
        return


    def compute_logic(self):
        """
        Assign the logic skill result
        """

        basic = {'control_if'}
        developing = {'control_if_else'}
        master = {'operator_and', 'operator_or', 'operator_not'}
        advanced = self.check_nested_conditionals()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "master": master, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "Logic")

    def check_nested_conditionals(self):
        """
        Finds if there are any nested conditionals in all the blocks of the script.
        """

        check = False

        for _, block_dict in self.dict_total_blocks.items():
            if block_dict['opcode'] == 'control_if':
                try:
                    substack =  self.dict_total_blocks.get(block_dict['inputs']['SUBSTACK'][1])
                    if self.has_nested_conditional(substack):
                        check = True
                        break
                except KeyError:
                    pass
            elif block_dict['opcode'] == 'control_if_else':
                try:
                    substack =  self.dict_total_blocks.get(block_dict['inputs']['SUBSTACK'][1])
                    substack_2 = self.dict_total_blocks.get(block_dict['inputs']['SUBSTACK2'][1])
                    if self.has_nested_conditional(substack) or self.has_nested_conditional(substack_2):
                        check = True
                        break
                except KeyError:
                    pass 
                
        return check
    
    def has_nested_conditional(self, substack):
        """
        Returns True if there is a nested conditional
        """

        while substack is not None:
            if substack['opcode'] == 'control_if' or substack['opcode'] == 'control_if_else':
                return True
            substack = self.dict_total_blocks.get(substack['next'])

        return False


    def compute_flow_control(self):
        """
        Calculate the flow control score
        """

        score = 0

        basic = self.check_block_sequence()
        developing = {'control_repeat', 'control_forever'}
        master = {'control_repeat_until'}
        advanced = self.check_nested_loops()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "master": master, "developing": developing, "basic": basic}

        for key, value in scale_dict.items():
            if type(value) == bool and value is True:
                if key in self.possible_scores.keys():
                    score = self.skill_points["Flow control"] * self.possible_scores[key] / len(self.possible_scores.keys())
                    self.dict_mastery['FlowControl'] = [score, self.skill_points['Flow control']] 
                    return
            elif type(value) == set:
                for item in value:
                    if self.dict_blocks[item]:
                        if key in self.possible_scores.keys():
                            score = self.skill_points["Flow control"] * self.possible_scores[key] / len(self.possible_scores.keys())
                            self.dict_mastery['FlowControl'] = [score, self.skill_points['Flow control']] 
                            return
                        
        self.dict_mastery['FlowControl'] = [score, self.skill_points['Flow control']] 
        return            

        self.set_dimension_score(scale_dict, "FlowControl") # CAMBIAR LA KEY DE LOS SKILL POINTS
        

    def check_block_sequence(self):

        check = False

        for _, block_dict in self.dict_total_blocks.items():
            if block_dict['next'] is not None:
                check = True
                break

        return check

    
    def check_nested_loops(self):
        """
        Finds if there are any nested conditionals in all the blocks of the script.
        """

        check = False

        for _, block_dict in self.dict_total_blocks.items():
            if block_dict['opcode'] == 'control_forever' or block_dict['opcode'] == 'control_repeat' or block_dict['opcode'] == 'control_repeat_until':
                try:
                    substack =  self.dict_total_blocks.get(block_dict['inputs']['SUBSTACK'][1])
                    if self.has_nested_loops(substack):
                        check = True
                        break
                except KeyError:
                    pass
                
        return check
    
    def has_nested_loops(self, substack):
        """
        Returns True if there is a nested conditional
        """

        while substack is not None:
            if substack['opcode'] == 'control_forever' or substack['opcode'] == 'control_repeat' or  substack['opcode'] == 'control_repeat_until':
                return True
            substack = self.dict_total_blocks.get(substack['next'])

        return False

    def compute_synchronization(self):
        """
        Compute the syncronization score
        """

        basic = {'control_wait'}
        developing = {'event_broadcast', 'event_whenbroadcastreceived', 'control_stop'}
        master = {'control_wait_until', 'event_whenbackdropswitchesto', 'event_broadcastandwait'}
        advanced = self.check_dynamic_msg_handling()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "master": master, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "Synchronization")
    
    def check_dynamic_msg_handling(self):

        check = False
        counter = 0
        min_msg = 3

        for block in self.list_total_blocks:
            if block['opcode'] == "event_broadcast" or block['opcode'] == "event_broadcastandwait":
                msg = block['inputs']['BROADCAST_INPUT'][1][2]
                if self.has_conditional_or_loop(msg):
                    counter += 1
                    print("Counter=", counter)
        if counter >= min_msg:
            check = True

        return check
    
    def has_conditional_or_loop(self, msg):

        check = False

        for block in self.list_total_blocks:
            if block['opcode'] == 'event_whenbroadcastreceived' and block['fields']['BROADCAST_OPTION'][1] == msg:
                next = self.dict_total_blocks.get(block['next'])
                while next is not None:
                    if self.check_conditional(next) or self.check_loops(next):
                        check = True
                        return check
                    next = self.dict_total_blocks.get(next['next']) 

        return check


    def compute_abstraction(self):
        """
        Compute the abstraction score
        """

        basic = self.check_more_than_one()
        developing = {'control_start_as_clone'}
        master = {'procedures_definition'}
        advanced = self.check_advanced_clones()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "master": master, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "Abstraction")

    def check_more_than_one(self):
        
        check = False

        count = 0
        for block in self.list_total_blocks:
            for key, value in block.items():
                if key == "parent" and value is None:
                    count += 1
        if count > 1:
            check = True

        return check
    
    def check_advanced_clones(self):

        check = False

        for block in self.list_total_blocks:
            if block['opcode'] == "control_start_as_clone":
                next = self.dict_total_blocks.get(block['next'])
                while next is not None:
                    if self.check_broadcast(next) or self.check_loops(next) or self.check_conditional(next):
                        check = True
                        return check
                    next = self.dict_total_blocks.get(next['next']) 

        return check
    
    def check_broadcast(self, block):

        check = False

        list = {'event_broadcast', 'event_broadcastandwait'}

        if block['opcode'] in list:
            check = True
        
        return check
    
    def check_loops(self, block):

        check = False
        counter = 0
        min_blocks = 3

        list = {'control_forever', 'control_repeat', 'control_repeat_until'}

        if block['opcode'] in list:
            try: 
                next = self.dict_total_blocks.get(block['inputs']['SUBSTACK'][1])
                while next is not None:
                    counter += 1
                    next = self.dict_total_blocks.get(next['next'])
                if counter >= min_blocks:
                    check = True
            except KeyError:
                pass
        
        return check
    
    def check_conditional(self, block):

        check = False

        if block['opcode'] == 'control_if':
            try:
                self.dict_total_blocks.get(block['inputs']['SUBSTACK'][1])
                check = True
            except KeyError:
                pass
        elif block['opcode'] == 'control_if_else':
            try:
                self.dict_total_blocks.get(block['inputs']['SUBSTACK'][1])
                self.dict_total_blocks.get(block['inputs']['SUBSTACK2'][1])
                check = True
            except KeyError:
                pass

        return check


    def compute_data_representation(self):
        """
        Compute data representation skill score
        """

        score = 0

        modifiers = {
            'motion_movesteps', 'motion_gotoxy', 'motion_glidesecstoxy', 'motion_setx', 'motion_sety',
            'motion_changexby', 'motion_changeyby', 'motion_pointindirection', 'motion_pointtowards',
            'motion_turnright', 'motion_turnleft', 'motion_goto', 'looks_changesizeby', 'looks_setsizeto',
            'looks_switchcostumeto', 'looks_nextcostume', 'looks_changeeffectby', 'looks_seteffectto',
            'looks_show', 'looks_hide', 'looks_switchbackdropto', 'looks_nextbackdrop'
        }

        lists = {
            'data_lengthoflist', 'data_showlist', 'data_insertatlist', 'data_deleteoflist', 'data_addtolist',
            'data_replaceitemoflist', 'data_listcontainsitem', 'data_hidelist', 'data_itemoflist'
        }
        
        boolean_logic = {
            'operator_equals', 'operator_gt', 'operator_and', 'operator_or', 'operator_not', 'operator_lt',
        }

        for item in boolean_logic:
            # ---------- ADVANCED -----------------------
            
            if self.dict_blocks[item]:
                print("DATA REPRESENTATION MASTERY: Boolean Logic")
                score = self.possible_scores['advanced']
                self.dict_mastery['DataRepresentation'] = [score, self.skill_points['Data representation']]
                return
        for item in lists:
            if self.dict_blocks[item]:
                # -------- PROFICIENT -------------------
                print("DATA REPRESENTATION MASTERY: Operations on lists")
                score = self.possible_scores['proficient']
                self.dict_mastery['DataRepresentation'] = [score, self.skill_points['Data representation']]
                return

        if self.dict_blocks['data_changevariableby'] or self.dict_blocks['data_setvariableto']:
            # ------------------ DEVELOPING -----------------------------------
            print("DATA REPRESENTATION MASTERY: Operations on variables")
            score = self.possible_scores['developing']
        else:
            # ------------------- BASIC ----------------------------------------
            print("DATA REPRESENTATION MASTERY: Modifiers of sprites properties")
            for modifier in modifiers:
                if self.dict_blocks[modifier]:
                    score = self.possible_scores['basic']
        self.dict_mastery['DataRepresentation'] = [score, self.skill_points['Data representation']]

    def compute_user_interactivity(self):
        """Assign the User Interactivity skill result"""
        score = 0

        proficiency = {'videoSensing_videoToggle', 'videoSensing_videoOn', 'videoSensing_whenMotionGreaterThan',
                       'videoSensing_setVideoTransparency', 'sensing_loudness'}

        developing = {'event_whenkeypressed', 'event_whenthisspriteclicked', 'sensing_mousedown', 'sensing_keypressed',
                      'sensing_askandwait', 'sensing_answer'}

        # ----------- PROFIENCY --------------
        coincidences = 0
        for block in self.dict_total_blocks.values(): # 2 scripts when %s is > %s,
            if block['opcode'] == 'control_if':
                id_codition = block['inputs']['CONDITION'][1]
                if self.dict_total_blocks[id_codition]['opcode'] == 'operator_gt':
                    coincidences += 1
                    if coincidences > 1:
                        print("USER INTERACTIVITY MASTERY: 2 scripts when %s is > %s,")
                        score = self.possible_scores['proficient']
                        self.dict_mastery['UserInteractivity'] = [score, self.skill_points['User interactivity']]
                        return    
        
        for item in proficiency:
            if self.dict_blocks[item]:
                score = self.skill_points['User interactivity']
                self.dict_mastery['UserInteractivity'] = [score, self.skill_points['User interactivity']]
                return
        # ---------- DEVELOPING ------------------------
        for item in developing:
            if self.dict_blocks[item]:
                print("USER INTERACTIVITY mastery: " + item)
                score = self.possible_scores['developing']
                self.dict_mastery['UserInteractivity'] = [score, self.skill_points['User interactivity']]
                return
        if self.dict_blocks['motion_goto_menu']:
            if self._check_mouse() == 1:
                score = self.possible_scores['developing']
                self.dict_mastery['UserInteractivity'] = [score, self.skill_points['User interactivity']]
                return
        if self.dict_blocks['sensing_touchingobjectmenu']:
            if self._check_mouse() == 1:
                score = self.possible_scores['developing']
                self.dict_mastery['UserInteractivity'] = [score, self.skill_points['User interactivity']]
                return        
            
        # ----------- BASIC -------------------------------------
        if self.dict_blocks['event_whenflagclicked']: # Green flag
            print("USER_INTERACTIVITY MASTERY: Green flag")
            score = self.possible_scores['basic']

        self.dict_mastery['UserInteractivity'] = [score, self.skill_points['User interactivity']]

    def compute_parallelization(self):
        """
        Assign the Parallelization skill result
        """
        
        parallelization_score = 0
        dict_parall = self.parallelization_dict()
        """
        if self.dict_blocks['event_whengreaterthan'] > 1:  # 2 Scripts start on the same multimedia (audio, timer) event
            if dict_parall['WHENGREATERTHANMENU']:
                var_list = set(dict_parall['WHENGREATERTHANMENU'])
                for var in var_list:
                    if dict_parall['WHENGREATERTHANMENU'].count(var) > 1:
                        parallelization_score = self.possible_scores['master']
                        #self.dict_mastery['Parallelization'] = [parallelization_score, self.skill_points['Parallelism']]
                        return
        """

        
        # ---------- PROFICIENT ----------------------------
        coincidences = 0
        for block in self.dict_total_blocks.values(): # 2 scripts when %s is > %s,
            if block['opcode'] == 'control_if':
                id_codition = block['inputs']['CONDITION'][1]
                if self.dict_total_blocks[id_codition]['opcode'] == 'operator_gt':
                    coincidences += 1
        if coincidences > 1:
            print("PARALLELISM MASTERY: 2 scripts when %s is > %s,")
            parallelization_score = self.possible_scores['proficient']
            self.dict_mastery['Parallelization'] = [parallelization_score, self.skill_points['Parallelism']]
            return
          
        if self.dict_blocks['event_whenbackdropswitchesto'] > 1:  # 2 Scripts start on the same backdrop change
            if dict_parall['BACKDROP']:
                backdrop_list = set(dict_parall['BACKDROP'])
                for var in backdrop_list:
                    if dict_parall['BACKDROP'].count(var) > 1:
                        print("PARALLELISM MASTERY: 2 Scripts start on the same received message")
                        parallelization_score = self.possible_scores['proficient']
                        self.dict_mastery['Parallelization'] = [parallelization_score, self.skill_points['Parallelism']]
                        return
                       
        if self.dict_blocks['control_create_clone_of']: # Create clone of
            print("PARALLELISM MASTERY: Create clone of")
            parallelization_score = self.possible_scores['proficient']
            self.dict_mastery['Parallelization'] = [parallelization_score, self.skill_points['Parallelism']]
            return
                                 
        
        if self.dict_blocks['event_whenbroadcastreceived'] > 1:  # 2 Scripts start on the same received message
            if dict_parall['BROADCAST_OPTION']:
                var_list = set(dict_parall['BROADCAST_OPTION'])
                for var in var_list:
                    if dict_parall['BROADCAST_OPTION'].count(var) > 1:
                        print("PARALLELISM MASTERY: 2 Scripts start on the same received message")
                        parallelization_score = self.possible_scores['proficient']
                        self.dict_mastery['Parallelization'] = [parallelization_score, self.skill_points['Parallelism']]
                        return

        """
        if self.dict_blocks['videoSensing_whenMotionGreaterThan'] > 1:  # 2 Scripts start on the same multimedia (video) event
            parallelization_score = self.possible_scores['master']
            self.dict_mastery['Parallelization'] = [parallelization_score, self.skill_points['Parallelism']]
            return
        """

        # ---------- DEVELOPING ----------------------------     

        if self.dict_blocks['event_whenkeypressed'] > 1:  # 2 Scripts start on the same key pressed
            if dict_parall['KEY_OPTION']:
                var_list = set(dict_parall['KEY_OPTION'])
                for var in var_list:
                    if dict_parall['KEY_OPTION'].count(var) > 1:
                        print("PARALLELISM MASTERY: Scripts start on the same key pressed")
                        parallelization_score = self.possible_scores['developing']

        if self.dict_blocks['event_whenthisspriteclicked'] > 1:  # Sprite with 2 scripts on clicked
            print("PARALLELISM MASTERY: Sprite with 2 scripts on clicked")
            parallelization_score = self.possible_scores['developing']
        
        # ----------- BASIC ----------------------------
        if self.dict_blocks['event_whenflagclicked'] > 1 and parallelization_score == 0:  # 2 scripts on green flag
            parallelization_score = self.possible_scores["basic"]
        
        self.dict_mastery['Parallelization'] = [parallelization_score, self.skill_points['Parallelism']]


    def parallelization_dict(self):
        dict_parallelization = {}

        for block in self.list_total_blocks:
            for key, value in block.items():
                if key == 'fields':
                    for key_pressed, val_pressed in value.items():
                        if key_pressed in dict_parallelization:
                            dict_parallelization[key_pressed].append(val_pressed[0])
                        else:
                            dict_parallelization[key_pressed] = val_pressed

        return dict_parallelization

    def _check_mouse(self):
        """
        Check whether there is a block 'go to mouse' or 'touching mouse-pointer?
        """

        for block in self.list_total_blocks:
            for key, value in block.items():
                if key == 'fields':
                    for mouse_key, mouse_val in value.items():
                        if (mouse_key == 'TO' or mouse_key == 'TOUCHINGOBJECTMENU') and mouse_val[0] == '_mouse_':
                            return 1

        return 0

    def compute_math_operators(self):
        """
        Assign the Use of Math Operators skill result
        """

        score = 0
        
        basic = {'operator_add', 'operator_subtract', 'operator_multiply', 'operator_divide'}
        developing = {'operator_gt', 'operator_lt', 'operator_equals'}
        master = {'operator_join', 'operator_letter_of', 'operator_length', 'operator_contains'}
        advanced = self.check_trigonometry()

        scale_dict = {"advanced": advanced, "master": master, "developing": developing, "basic": basic}

        for key, value in scale_dict.items():           
            if type(value) == bool and value is True:
                if key in self.possible_scores.keys():
                    score = self.skill_points["Math operators"] * self.possible_scores[key] / len(self.possible_scores.keys())
                    self.dict_mastery['MathOperators'] = [score, self.skill_points['Math operators']] 
                    return
            elif type(value) == set:
                for item in value:
                    if self.dict_blocks[item]:
                        if key in self.possible_scores.keys():
                            score = self.skill_points["Math operators"] * self.possible_scores[key] / len(self.possible_scores.keys())
                            self.dict_mastery['MathOperators'] = [score, self.skill_points['Math operators']] 
                            return
                    
        self.dict_mastery['MathOperators'] = [score, self.skill_points['Math operators']] 
        
        return
    
        self.set_dimension_score(scale_dict, "MathOperators") # CAMBIAR LA KEY DE LOS SKILL POINTS
    
    def check_trigonometry(self):

        check = False

        list = {'cos', 'sin', 'tan', 'asin', 'acos', 'atan'}

        for block in self.list_total_blocks:
            if block['opcode'] == 'operator_mathop':
                for element in block['fields']['OPERATOR']:
                    if element in list:
                        check = True
                        return check
                    
        return check


    def compute_motion_operators(self):
        """
        Assign the Use of Motion Operators skill result
        """

        score = 0

        basic = {'motion_movesteps', 'motion_gotoxy', 'motion_changexby', 'motion_goto', 'motion_changeyby', 'motion_setx', 'motion_sety'}
        developing = {'motion_turnleft', 'motion_turnright', 'motion_setrotationstyles', 'motion_pointindirection', 'motion_pointtowards'}
        master = {'motion_glideto', 'motion_glidesecstoxy'}
        advanced = self.check_motion_complex_sequences()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "master": master, "developing": developing, "basic": basic}

        for key, value in scale_dict.items():           
            if type(value) == bool and value is True:
                if key in self.possible_scores.keys():
                    score = self.skill_points["Motion operators"] * self.possible_scores[key] / len(self.possible_scores.keys())
                    self.dict_mastery['MotionOperators'] = [score, self.skill_points['Motion operators']] 
                    return
            elif type(value) == set:
                for item in value:
                    if self.dict_blocks[item]:
                        if key in self.possible_scores.keys():
                            score = self.skill_points["Motion operators"] * self.possible_scores[key] / len(self.possible_scores.keys())
                            self.dict_mastery['MotionOperators'] = [score, self.skill_points['Motion operators']] 
                            return
                    
        self.dict_mastery['MotionOperators'] = [score, self.skill_points['Motion operators']] 
        
        return
    
        self.set_dimension_score(scale_dict, "MotionOperators") # CAMBIAR LA KEY DE LOS SKILL POINTS

    
    def check_motion_complex_sequences(self):

        check = False
        min_motion_blocks = 5
        counter = 0
        list = {'motion_movesteps', 'motion_gotoxy', 'motion_glidesecstoxy', 'motion_glideto', 
                'motion_setx', 'motion_sety', 'motion_changexby', 'motion_changeyby', 
                'motion_pointindirection', 'motion_pointtowards', 'motion_turnright', 'motion_turnleft', 
                'motion_goto', 'motion_ifonedgebounce', 'motion_setrotationstyles'}
        
        for _,value in self.dict_total_blocks.items():
            if value['parent'] is None:
                counter = 0
            else:
                if value['opcode'] in list:
                    counter += 1
                    if counter >= min_motion_blocks:
                        check = True
                        return check

        return check
    
