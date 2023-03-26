import json
from app.hairball3.plugin import Plugin


class Mastery(Plugin):

    def __init__(self, filename: str, json_project):
        super().__init__(filename, json_project)

    def process(self):

        for key, list_info in self.json_project.items():
            if key == "targets":
                for dict_target in list_info:
                    for dicc_key, dicc_value in dict_target.items():
                        if dicc_key == "blocks":
                            for blocks, blocks_value in dicc_value.items():
                                if type(blocks_value) is dict:
                                    self.list_total_blocks.append(blocks_value)

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

    def finalize(self) -> str:
        """
        Output the overall programming competence
        """
        self.process()
        self.analyze()

        # result = ""
        # result += filename
        # result += '\n'

        result = '{}{}'.format(self.filename, '\n')
        result += json.dumps(self.dict_mastery)
        result += '\n'

        total = 0
        for i in self.dict_mastery.items():
            total += i[1]

        result += ("Total mastery points: %d/21\n" % total)

        average = float(total) / 7
        result += ("Average mastery points: %.2f/3\n" % average)

        if average > 2:
            result += "Overall programming competence: Proficiency"
        elif average > 1:
            result += "Overall programming competence: Developing"
        else:
            result += "Overall programming competence: Basic"
        return result

    def compute_logic(self):
        """
        Assign the logic skill result
        """

        logic_operators = {
            'operator_and',
            'operator_or',
            'operator_not'
        }

        logic_score = 0

        for operation in logic_operators:
            if self.dict_blocks[operation]:
                logic_score = 3
                self.dict_mastery['Logic'] = logic_score
                return

        if self.dict_blocks['control_if_else']:
            logic_score = 2
        elif self.dict_blocks['control_if']:
            logic_score = 1

        self.dict_mastery['Logic'] = logic_score

    def compute_flow_control(self):
        """
        Calculate the flow control score
        """

        fc_score = 0

        if self.dict_blocks['control_repeat_until']:
            fc_score = 3
        elif self.dict_blocks['control_repeat'] or self.dict_blocks['control_forever']:
            fc_score = 2
        else:
            for block in self.list_total_blocks:
                for key, value in block.items():
                    if key == "next" and value is not None:
                        fc_score = 1
                        break

        self.dict_mastery['FlowControl'] = fc_score

    def compute_synchronization(self):
        """
        Compute the syncronization score
        """

        sync_score = 0

        if (self.dict_blocks['control_wait_until'] or self.dict_blocks['event_whenbackdropswitchesto'] or
                self.dict_blocks['event_broadcastandwait']):
            sync_score = 3
        elif (self.dict_blocks['event_broadcast'] or self.dict_blocks['event_whenbroadcastreceived'] or
              self.dict_blocks['control_stop']):
            sync_score = 2
        elif self.dict_blocks['control_wait']:
            sync_score = 1

        self.dict_mastery['Synchronization'] = sync_score

    def compute_abstraction(self):
        """
        Compute the abstraction score
        """

        abs_score = 0

        if self.dict_blocks['control_start_as_clone']:
            abs_score = 3
        elif self.dict_blocks['procedures_definition']:
            abs_score = 2
        else:
            count = 0
            for block in self.list_total_blocks:
                for key, value in block.items():
                    if key == "parent" and value is None:
                        count += 1
            if count > 1:
                abs_score = 1

        self.dict_mastery['Abstraction'] = abs_score

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

        for item in lists:
            if self.dict_blocks[item]:
                score = 3
                self.dict_mastery['DataRepresentation'] = score
                return

        if self.dict_blocks['data_changevariableby'] or self.dict_blocks['data_setvariableto']:
            score = 2
        else:
            for modifier in modifiers:
                if self.dict_blocks[modifier]:
                    score = 1

        self.dict_mastery['DataRepresentation'] = score

    def compute_user_interactivity(self):
        """Assign the User Interactivity skill result"""

        score = 0

        proficiency = {'videoSensing_videoToggle', 'videoSensing_videoOn', 'videoSensing_whenMotionGreaterThan',
                       'videoSensing_setVideoTransparency', 'sensing_loudness'}

        developing = {'event_whenkeypressed', 'event_whenthisspriteclicked', 'sensing_mousedown', 'sensing_keypressed',
                      'sensing_askandwait', 'sensing_answer'}

        for item in proficiency:
            if self.dict_blocks[item]:
                self.dict_mastery['UserInteractivity'] = 3
                return
        for item in developing:
            if self.dict_blocks[item]:
                self.dict_mastery['UserInteractivity'] = 2
                return
        if self.dict_blocks['motion_goto_menu']:
            if self._check_mouse() == 1:
                self.dict_mastery['UserInteractivity'] = 2
                return
        if self.dict_blocks['sensing_touchingobjectmenu']:
            if self._check_mouse() == 1:
                self.dict_mastery['UserInteractivity'] = 2
                return
        if self.dict_blocks['event_whenflagclicked']:
            score = 1

        self.dict_mastery['UserInteractivity'] = score

    def compute_parallelization(self):
        """
        Assign the Parallelization skill result
        """

        parallelization_score = 0

        dict_parall = self.parallelization_dict()

        if self.dict_blocks['event_whenbroadcastreceived'] > 1:  # 2 Scripts start on the same received message
            if dict_parall['BROADCAST_OPTION']:
                var_list = set(dict_parall['BROADCAST_OPTION'])
                for var in var_list:
                    if dict_parall['BROADCAST_OPTION'].count(var) > 1:
                        parallelization_score = 3
                        self.dict_mastery['Parallelization'] = parallelization_score
                        return

        if self.dict_blocks['event_whenbackdropswitchesto'] > 1:  # 2 Scripts start on the same backdrop change
            if dict_parall['BACKDROP']:
                backdrop_list = set(dict_parall['BACKDROP'])
                for var in backdrop_list:
                    if dict_parall['BACKDROP'].count(var) > 1:
                        parallelization_score = 3
                        self.dict_mastery['Parallelization'] = parallelization_score
                        return

        if self.dict_blocks['event_whengreaterthan'] > 1:  # 2 Scripts start on the same multimedia (audio, timer) event
            if dict_parall['WHENGREATERTHANMENU']:
                var_list = set(dict_parall['WHENGREATERTHANMENU'])
                for var in var_list:
                    if dict_parall['WHENGREATERTHANMENU'].count(var) > 1:
                        parallelization_score = 3
                        self.dict_mastery['Parallelization'] = parallelization_score
                        return

        if self.dict_blocks['videoSensing_whenMotionGreaterThan'] > 1:  # 2 Scripts start on the same multimedia (video) event
            parallelization_score = 3
            self.dict_mastery['Parallelization'] = parallelization_score
            return

        if self.dict_blocks['event_whenkeypressed'] > 1:  # 2 Scripts start on the same key pressed
            if dict_parall['KEY_OPTION']:
                var_list = set(dict_parall['KEY_OPTION'])
                for var in var_list:
                    if dict_parall['KEY_OPTION'].count(var) > 1:
                        parallelization_score = 2

        if self.dict_blocks['event_whenthisspriteclicked'] > 1:  # Sprite with 2 scripts on clicked
            parallelization_score = 2

        if self.dict_blocks['event_whenflagclicked'] > 1 and parallelization_score == 0:  # 2 scripts on green flag
            parallelization_score = 1

        self.dict_mastery['Parallelization'] = parallelization_score

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


# def main(filename):
#     mastery = Mastery(filename)
#     mastery.process()
#     mastery.analyze()
#     dict_result = mastery.finalize()
#     return dict_result





