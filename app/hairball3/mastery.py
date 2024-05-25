import json
from app.hairball3.plugin import Plugin
import app.consts_drscratch as consts
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class Mastery(Plugin):

    def __init__(self, filename: str, json_project, skill_points: dict, mode: str ,verbose=False):
        super().__init__(filename, json_project, skill_points, mode , verbose)
        self.possible_scores = {"finesse": 5, "advanced": 4, "proficient": 3, "developing": 2, "basic": 1}
        self.dict_total_blocks = {}

    def process(self):

        # print(self.json_project.items())

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

        # print("Dict:", self.dict_total_blocks)

        total_points = 0
        active_dimensions = sum(1 for value in self.skill_points.values() if value > 0)

        for skill, skill_grade in self.dict_mastery.items():
            if self.verbose:
                logger.info('Skill: {}, points: {}'.format(skill, skill_grade))
            total_points = total_points + skill_grade[0]
            total_points = round(total_points, 2)

        try:
            average_points = float(total_points) / active_dimensions
        except ZeroDivisionError:
            average_points = 0

        total_maxi_points = sum(self.skill_points.values())
        competence = self.set_competence(total_points, total_maxi_points)

        result = '{}{}{}{}'.format(self.filename, '\n', json.dumps(self.dict_mastery), '\n')
        result += ('Total mastery points: {}/{}\n'.format(total_points, total_maxi_points))
        result += ('Average mastery points: {}/{}\n'.format(average_points, consts.PLUGIN_MASTERY_AVG_POINTS))

        self.set_dict(self.dict_mastery, total_points, total_maxi_points, average_points, competence)

        if self.mode == 'Personalized':
            dict_result = {'plugin': 'mastery', 'personalized': self.dict_mastery}
        elif self.mode == 'Default':
            vanilla_dict = self.calc_extrapolation(self.dict_mastery)
            vanilla_points = sum(points[0] for points in vanilla_dict.values())
            average_points = vanilla_points / 7
            vanilla_competence = self.set_competence(vanilla_points, 21, 'Vanilla')
            self.set_dict(vanilla_dict, vanilla_points, 21, average_points, vanilla_competence)
            #self.dict_mastery['description'] = result
            if self.verbose:
                logger.info(self.dict_mastery['description'])
            dict_result = {'plugin': 'mastery', 'extended': self.dict_mastery, 'vanilla': vanilla_dict}

        print("DICT_RESULT: ", dict_result)

        return dict_result

    def set_dict(self, dict, points, max_points, average_points, competence) -> dict:
        """
        Include the mastery points, max points, average points and competence in the dictionary.
        """
        dict['total_points'] = [points, max_points]
        dict['max_points'] = max_points
        dict['average_points'] = round(average_points, 2)
        dict['competence'] = competence

        return dict

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
    
    def set_competence(self, points, max_points, mode=None):

        competence = ''

        finesse_lvl = max_points*36/45
        advanced_lvl = max_points*27/45
        proficient_lvl = max_points*18/45
        developing_lvl = max_points*9/45

        if mode == 'Vanilla':
            if points > 15:
                # result = "Overall programming competence: Proficiency"
                competence = 'Master'
            elif points > 7:
                # result = "Overall programming competence: Developing"
                competence = 'Developing'
            else:
                # result = "Overall programming competence: Basic"
                competence = 'Basic'
        else:
            if points > finesse_lvl:
                # result = "Overall programming competence: Finesse"
                competence = 'Finesse'
            elif points > advanced_lvl:
                # result = "Overall programming competence: Advanced"
                competence = 'Advanced'
            elif points > proficient_lvl:
                # result = "Overall programming competence: Proficiency"
                competence = 'Master'
            elif points > developing_lvl:
                # result = "Overall programming competence: Developing"
                competence = 'Developing'
            else:
                # result = "Overall programming competence: Basic"
                competence = 'Basic'
        """
        competence_dict = {
            'result': result, 
            'programming_competence': competence
            }       
        """

        return competence
    
    def set_dimension_score(self, scale_dict, dimension):

        score = 0

        for key, value in scale_dict.items():
            if type(value) == bool and value is True:
                if key in self.possible_scores.keys():
                    print(dimension + " : " + key)
                    score = self.extrapolate_to_rubric(dimension, key)
                    self.dict_mastery[dimension] = [score, self.skill_points[dimension]] 
                    return
        print(dimension + " : " + "None")
        self.dict_mastery[dimension] = [score, self.skill_points[dimension]] 
        return

    def extrapolate_to_rubric(self, dimension, level):
        """
        Extrapolate the points to the max points of skill rubric
        """
        if self.possible_scores[level] >= self.skill_points[dimension]:
            score = self.skill_points[dimension]
        else:
            score = self.possible_scores[level]
        return score

    def compute_logic(self):
        """
        Assign the logic skill result
        """

        basic = self.check_list({'control_if'})
        developing = self.check_list({'control_if_else'})
        master = self.check_list({'operator_and', 'operator_or', 'operator_not'})
        advanced = self.check_nested_conditionals()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "master": master, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "Logic")
        

    def compute_flow_control(self):
        """
        Calculate the flow control score
        """

        basic = self.check_block_sequence()
        developing = self.check_list({'control_repeat', 'control_forever'})
        proficient = self.check_list({'control_repeat_until'})
        advanced = self.check_nested_loops()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "proficient": proficient, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "FlowControl")
        

    def compute_synchronization(self):
        """
        Compute the syncronization score
        """

        basic = self.check_list({'control_wait'})
        developing = self.check_list({'event_broadcast', 'event_whenbroadcastreceived', 'control_stop'})
        proficient = self.check_list({'control_wait_until', 'event_whenbackdropswitchesto', 'event_broadcastandwait'})
        advanced = self.check_dynamic_msg_handling()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "proficient": proficient, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "Synchronization")


    def compute_abstraction(self):
        """
        Compute the abstraction score
        """

        basic = self.check_more_than_one()
        developing = self.check_list({'control_start_as_clone'})
        proficient = self.check_list({'procedures_definition'})
        advanced = self.check_advanced_clones()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "proficient": proficient, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "Abstraction")


    def compute_data_representation(self):
        """
        Compute data representation skill score
        """

        modifiers = self.check_list({
            'motion_movesteps', 'motion_gotoxy', 'motion_glidesecstoxy', 'motion_setx', 'motion_sety',
            'motion_changexby', 'motion_changeyby', 'motion_pointindirection', 'motion_pointtowards',
            'motion_turnright', 'motion_turnleft', 'motion_goto', 'looks_changesizeby', 'looks_setsizeto',
            'looks_switchcostumeto', 'looks_nextcostume', 'looks_changeeffectby', 'looks_seteffectto',
            'looks_show', 'looks_hide', 'looks_switchbackdropto', 'looks_nextbackdrop'
        })

        lists = self.check_list({
            'data_lengthoflist', 'data_showlist', 'data_insertatlist', 'data_deleteoflist', 'data_addtolist',
            'data_replaceitemoflist', 'data_listcontainsitem', 'data_hidelist', 'data_itemoflist'
        })
        
        boolean_logic = self.check_list({
            'operator_equals', 'operator_gt', 'operator_and', 'operator_or', 'operator_not', 'operator_lt',
        })
        
        variables = self.check_list({'data_changevariableby', 'data_setvariableto'})
        
        scale_dict = {"advanced": boolean_logic, "proficient": lists, "developing": variables, "basic": modifiers}
        
        self.set_dimension_score(scale_dict, "DataRepresentation")


    def compute_user_interactivity(self):
        """Assign the User Interactivity skill result"""

        # ----------- ADVANCED ------------------------
        advanced = self.check_ui_advanced()

        # ----------- PROFIENCY --------------
        proficient = self.check_ui_proficiency()
        
        # ---------- DEVELOPING ------------------------
        developing = self.check_ui_developing()
        
        # ----------- BASIC -------------------------------------
        basic = self.check_list({'event_whenflagclicked'})

        scale_dict = {"advanced": advanced, "proficient": proficient, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "UserInteractivity")
    
    def check_ui_advanced(self):
        """
        Check the advanced user interactivity skills
        """
        if len(self.json_project['extensions']) != 0:
            return True
        else:
            return False

        
    def compute_parallelization(self):
        """
        Assign the Parallelization skill result
        """
        
        dict_parall = self.parallelization_dict()

        # ---------- ADVANCED ----------------------------
        advanced = self.check_p_advanced(dict_parall)

        # ---------- PROFICIENT ----------------------------
        proficient = self.check_p_proficiency(dict_parall)

        # ---------- DEVELOPING ----------------------------     
        developing = self.check_p_developing(dict_parall)
        
        # ----------- BASIC ----------------------------
        basic = self.check_scripts_flag(n_scripts=2)
        
        scale_dict = {"advanced": advanced, "proficient": proficient, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "Parallelization")
    
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
        
        
    def compute_math_operators(self):
        """
        Assign the Use of Math Operators skill result
        """

        basic = self.check_list({'operator_add', 'operator_subtract', 'operator_multiply', 'operator_divide'})
        developing = self.check_list({'operator_gt', 'operator_lt', 'operator_equals'})
        proficient = self.check_list({'operator_join', 'operator_letter_of', 'operator_length', 'operator_contains'})
        advanced = self.check_trigonometry()

        scale_dict = {"advanced": advanced, "proficient": proficient, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "MathOperators")
        

    def compute_motion_operators(self):
        """
        Assign the Use of Motion Operators skill result
        """

        basic = self.check_list({'motion_movesteps', 'motion_gotoxy', 'motion_changexby', 'motion_goto', 'motion_changeyby', 'motion_setx', 'motion_sety'})
        developing = self.check_list({'motion_turnleft', 'motion_turnright', 'motion_setrotationstyles', 'motion_pointindirection', 'motion_pointtowards'})
        proficient = self.check_list({'motion_glideto', 'motion_glidesecstoxy'})
        advanced = self.check_motion_complex_sequences()
        # finesse = PREGUNTAR GREGORIO

        scale_dict = {"advanced": advanced, "proficient": proficient, "developing": developing, "basic": basic}

        self.set_dimension_score(scale_dict, "MotionOperators") 

    def check_scripts_flag(self, n_scripts):
        if self.dict_blocks['event_whenflagclicked'] >= n_scripts:  # N Scripts on green flag
            return True
        return False

    def check_scripts_key(self, dict_parall, n_scripts):
        if self.dict_blocks['event_whenkeypressed'] >= n_scripts:  # N Scripts start on the same key pressed
            if dict_parall['KEY_OPTION']:
                var_list = set(dict_parall['KEY_OPTION'])
                for var in var_list:
                    if dict_parall['KEY_OPTION'].count(var) >= n_scripts:
                        return True
        return False
    
    def check_scripts_sprite(self, n_scripts):
        if self.dict_blocks['event_whenthisspriteclicked'] >= n_scripts:  # Sprite with N scripts on clicked
            return True
        return False

    def check_list(self, list):

        for item in list:
            if item in self.dict_blocks.keys():
                return True
            
        return False
    
    def check_scripts(self, n_scripts):
        coincidences = 0
        for block in self.dict_total_blocks.values(): 
            if block['opcode'] == 'control_if':
                id_codition = block['inputs']['CONDITION'][1]
                if self.dict_total_blocks[id_codition]['opcode'] == 'operator_gt':
                    coincidences += 1
                    if coincidences >= n_scripts: # N scripts when %s is > %s,
                        return True
        return False

    def check_scripts_media(self, dict_parall, n_scripts):
        if self.dict_blocks['event_whengreaterthan'] >= n_scripts:  # N Scripts start on the same multimedia (audio, timer) event
            if dict_parall['WHENGREATERTHANMENU']:
                var_list = set(dict_parall['WHENGREATERTHANMENU'])
                for var in var_list:
                    if dict_parall['WHENGREATERTHANMENU'].count(var) >= n_scripts:
                        return True
        return False
    
    def check_scripts_backdrop(self, dict_parall, n_scripts):
        if self.dict_blocks['event_whenbackdropswitchesto'] >= n_scripts:  # N Scripts start on the same backdrop change
            if dict_parall['BACKDROP']:
                backdrop_list = set(dict_parall['BACKDROP'])
                for var in backdrop_list:
                    if dict_parall['BACKDROP'].count(var) >= n_scripts:
                        return True
        return False
    
    def check_scripts_msg(self, dict_parall, n_scripts):
        if self.dict_blocks['event_whenbroadcastreceived'] >= n_scripts:  # N Scripts start on the same received message
            if dict_parall['BROADCAST_OPTION']:
                var_list = set(dict_parall['BROADCAST_OPTION'])
                for var in var_list:
                    if dict_parall['BROADCAST_OPTION'].count(var) >= n_scripts:
                        return True
        return False
    
    def check_scripts_video(self, n_scripts):
        if self.dict_blocks['videoSensing_whenMotionGreaterThan'] >= n_scripts:  # N Scripts start on the same multimedia (video) event
            return True
        return False
    
    def check_ui_proficiency(self):
        """
        Check if the user has proficient user interactivity
        """
        proficiency = {'videoSensing_videoToggle', 'videoSensing_videoOn', 'videoSensing_whenMotionGreaterThan',
                       'videoSensing_setVideoTransparency', 'sensing_loudness'}
        
        if self.check_list(proficiency) or self.check_scripts(n_scripts=2):
            return True

        return False
    
    def check_mouse_blocks(self):
        if self.dict_blocks['motion_goto_menu'] or self.dict_blocks['sensing_touchingobjectmenu']:
            if self._check_mouse() == 1:
                return True
        return False
        
    def check_ui_developing(self):
        """
        Check if the user has developing user interactivity
        """
        developing = {'event_whenkeypressed', 'event_whenthisspriteclicked', 'sensing_mousedown', 'sensing_keypressed',
                      'sensing_askandwait', 'sensing_answer'}

        if self.check_list(developing) or self.check_mouse_blocks():
            return True
        
        return False
    
        
    def check_p_advanced(self, dict_parall):
        """
        Check the advanced parallelization skills
        """
        if (self.check_scripts(n_scripts=3) or self.check_scripts_media(dict_parall, n_scripts=3) or self.check_scripts_backdrop(dict_parall, n_scripts=3) 
            or self.check_scripts_msg(dict_parall, n_scripts=3) or self.check_scripts_video(n_scripts=3)):
            return True
        return False
        
    
    def check_p_proficiency(self, dict_parall):
        if (self.check_scripts(n_scripts=2) or self.check_scripts_media(dict_parall, n_scripts=2) or self.check_scripts_backdrop(dict_parall, n_scripts=2) 
            or self.check_list({'control_create_clone_of'}) or self.check_scripts_msg(dict_parall, n_scripts=2) or self.check_scripts_video(n_scripts=2)):
            return True
        return False
    
    def check_p_developing(self, dict_parall):
        if self.check_scripts_key(dict_parall, n_scripts=2) or self.check_scripts_sprite(n_scripts=2):
            return True
        return False

    
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

    
    def check_motion_complex_sequences(self):

        check = False
        min_motion_blocks = 5
        counter = 0
        list = {'motion_movesteps', 'motion_gotoxy', 'motion_glidesecstoxy', 'motion_glideto', 
                'motion_setx', 'motion_sety', 'motion_changexby', 'motion_changeyby', 
                'motion_pointindirection', 'motion_pointtowards', 'motion_turnright', 'motion_turnleft', 
                'motion_goto', 'motion_ifonedgebounce', 'motion_setrotationstyles'}
        
        
        for _,value in self.dict_total_blocks.items():
            print(value)
            if 'parent' in value:
                if value['parent'] is None:
                    counter = 0
            else:
                if value['opcode'] in list:
                    counter += 1
                    if counter >= min_motion_blocks:
                        check = True
                        return check

        return check
    
    
    def check_dynamic_msg_handling(self):

        check = False
        counter = 0
        min_msg = 3

        for block in self.list_total_blocks:
            if block['opcode'] == "event_broadcast" or block['opcode'] == "event_broadcastandwait":
                msg = block['inputs']['BROADCAST_INPUT'][1][2]
                if self.has_conditional_or_loop(msg):
                    counter += 1
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