import tracemalloc
from memory_profiler import profile
import gc

BLOCK_TEXT = {
    "CONTROL_FOREVER": "forever",
    "CONTROL_REPEAT": "repeat (%1)",
    "CONTROL_IF": "if <%1> then",
    "CONTROL_IF_ELSE": "if <%1> then",
    "CONTROL_ELSE": "else",
    "CONTROL_STOP": "stop [%1 v]",
    "CONTROL_STOP_ALL": "all",
    "CONTROL_STOP_THIS": "this script",
    "CONTROL_STOP_OTHER": "other scripts in sprite",
    "CONTROL_WAIT": "wait (%1) seconds",
    "CONTROL_WAIT_UNTIL": "wait until <%1>",
    "CONTROL_REPEAT_UNTIL": "repeat until <%1>",
    "CONTROL_WHILE": "while <%1>",
    "CONTROL_FOREACH": "for each %1 in %2",
    "CONTROL_START_AS_CLONE": "when I start as a clone",
    "CONTROL_CREATE_CLONE_OF": "create clone of (%1 v)",
    "CONTROL_CREATE_CLONE_OF_MYSELF": "myself",
    "CONTROL_DELETE_THIS_CLONE": "delete this clone",
    "CONTROL_COUNTER": "counter",
    "CONTROL_INCRCOUNTER": "increment counter",
    "CONTROL_CLEARCOUNTER": "clear counter",
    "CONTROL_ALLATONCE": "all at once",
    "CONTROL_FOR_EACH": "for each [%1 v] in (%2)",
    "DATA_SETVARIABLETO": "set [%1 v] to (%2)",
    "DATA_CHANGEVARIABLEBY": "change [%1 v] by (%2)",
    "DATA_SHOWVARIABLE": "show variable [%1 v]",
    "DATA_HIDEVARIABLE": "hide variable [%1 v]",
    "DATA_ADDTOLIST": "add (%2) to [%1 v]",
    "DATA_DELETEOFLIST": "delete (%2) of [%1 v]",
    "DATA_DELETEALLOFLIST": "delete all of [%1 v]",
    "DATA_INSERTATLIST": "insert (%2) at (%3) of [%1 v]",
    "DATA_REPLACEITEMOFLIST": "replace item (%2) of [%1 v] with (%3)",
    "DATA_ITEMOFLIST": "item (%2) of [%1 v]",
    "DATA_ITEMNUMOFLIST": "item # of (%2) in [%1 v]",
    "DATA_LENGTHOFLIST": "length of [%1 v]",
    "DATA_LISTCONTAINSITEM": "[%1 v] contains (%2)?",
    "DATA_SHOWLIST": "show list [%1 v]",
    "DATA_HIDELIST": "hide list [%1 v]",
    "DATA_INDEX_ALL": "all",
    "DATA_INDEX_LAST": "last",
    "DATA_INDEX_RANDOM": "random",
    "EVENT_WHENFLAGCLICKED": "when flag clicked",
    "EVENT_WHENTHISSPRITECLICKED": "when this sprite clicked",
    "EVENT_WHENSTAGECLICKED": "when stage clicked",
    "EVENT_WHENTOUCHINGOBJECT": "when this sprite touches (%1 v)",
    "EVENT_WHENBROADCASTRECEIVED": "when I receive [%1 v]",
    "EVENT_WHENBACKDROPSWITCHESTO": "when backdrop switches to [%1 v]",
    "EVENT_WHENGREATERTHAN": "when [%1 v] > (%2)",
    "EVENT_WHENGREATERTHAN_TIMER": "timer",
    "EVENT_WHENGREATERTHAN_LOUDNESS": "loudness",
    "EVENT_BROADCAST": "broadcast (%1 v)",
    "EVENT_BROADCASTANDWAIT": "broadcast (%1 v) and wait",
    "EVENT_WHENKEYPRESSED": "when [%1 v] key pressed",
    "EVENT_WHENKEYPRESSED_SPACE": "space",
    "EVENT_WHENKEYPRESSED_LEFT": "left arrow",
    "EVENT_WHENKEYPRESSED_RIGHT": "right arrow",
    "EVENT_WHENKEYPRESSED_DOWN": "down arrow",
    "EVENT_WHENKEYPRESSED_UP": "up arrow",
    "EVENT_WHENKEYPRESSED_ANY": "any",
    "LOOKS_SAYFORSECS": "say (%1) for (%2) seconds",
    "LOOKS_SAY": "say (%1)",
    "LOOKS_HELLO": "Hello!",
    "LOOKS_THINKFORSECS": "think (%1) for (%2) seconds",
    "LOOKS_THINK": "think (%1)",
    "LOOKS_HMM": "Hmm...",
    "LOOKS_SHOW": "show",
    "LOOKS_HIDE": "hide",
    "LOOKS_HIDEALLSPRITES": "hide all sprites",
    "LOOKS_EFFECT_COLOR": "color",
    "LOOKS_EFFECT_FISHEYE": "fisheye",
    "LOOKS_EFFECT_WHIRL": "whirl",
    "LOOKS_EFFECT_PIXELATE": "pixelate",
    "LOOKS_EFFECT_MOSAIC": "mosaic",
    "LOOKS_EFFECT_BRIGHTNESS": "brightness",
    "LOOKS_EFFECT_GHOST": "ghost",
    "LOOKS_CHANGEEFFECTBY": "change [%1 v] effect by (%2)",
    "LOOKS_SETEFFECTTO": "set [%1 v] effect to (%2)",
    "LOOKS_CLEARGRAPHICEFFECTS": "clear graphic effects",
    "LOOKS_CHANGESIZEBY": "change size by (%1)",
    "LOOKS_SETSIZETO": "set size to (%1) %",
    "LOOKS_SIZE": "size",
    "LOOKS_CHANGESTRETCHBY": "change stretch by (%1)",
    "LOOKS_SETSTRETCHTO": "set stretch to (%1) %",
    "LOOKS_SWITCHCOSTUMETO": "switch costume to (%1 v)",
    "LOOKS_NEXTCOSTUME": "next costume",
    "LOOKS_SWITCHBACKDROPTO": "switch backdrop to (%1 v)",
    "LOOKS_GOTOFRONTBACK": "go to [%1 v] layer",
    "LOOKS_GOTOFRONTBACK_FRONT": "front",
    "LOOKS_GOTOFRONTBACK_BACK": "back",
    "LOOKS_GOFORWARDBACKWARDLAYERS": "go [%1 v] (%2) layers",
    "LOOKS_GOFORWARDBACKWARDLAYERS_FORWARD": "forward",
    "LOOKS_GOFORWARDBACKWARDLAYERS_BACKWARD": "backward",
    "LOOKS_BACKDROPNUMBERNAME": "backdrop [%1 v]",
    "LOOKS_COSTUMENUMBERNAME": "costume [%1 v]",
    "LOOKS_COSTUME": "costume",
    "LOOKS_NUMBERNAME_NUMBER": "number",
    "LOOKS_NUMBERNAME_NAME": "name",
    "LOOKS_SWITCHBACKDROPTOANDWAIT": "switch backdrop to (%1 v) and wait",
    "LOOKS_NEXTBACKDROP_BLOCK": "next backdrop",
    "LOOKS_NEXTBACKDROP": "next backdrop",
    "LOOKS_PREVIOUSBACKDROP": "previous backdrop",
    "LOOKS_RANDOMBACKDROP": "random backdrop",
    "MOTION_MOVESTEPS": "move (%1) steps",
    "MOTION_TURNLEFT": "turn left (%1) degrees",
    "MOTION_TURNRIGHT": "turn right (%2) degrees",
    "MOTION_POINTINDIRECTION": "point in direction (%1)",
    "MOTION_POINTTOWARDS": "point towards (%1 v)",
    "MOTION_POINTTOWARDS_POINTER": "mouse-pointer",
    "MOTION_POINTTOWARDS_RANDOM": "random direction",
    "MOTION_POINTTOWARDS_MENU": "point towards (%1 v)",
    "MOTION_GOTO": "go to (%1 v)",
    "MOTION_GOTO_MENU": "go to (%1 v)",
    "MOTION_GOTO_POINTER": "mouse-pointer",
    "MOTION_GOTO_RANDOM": "random position",
    "MOTION_GOTOXY": "go to x: (%1) y: (%2)",
    "MOTION_GLIDESECSTOXY": "glide (%1) secs to x: (%2) y: (%3)",
    "MOTION_GLIDETO": "glide (%1) secs to (%2 v)",
    "MOTION_GLIDETO_POINTER": "mouse-pointer",
    "MOTION_GLIDETO_RANDOM": "random position",
    "MOTION_CHANGEXBY": "change x by (%1)",
    "MOTION_SETX": "set x to (%1)",
    "MOTION_CHANGEYBY": "change y by (%1)",
    "MOTION_SETY": "set y to (%1)",
    "MOTION_IFONEDGEBOUNCE": "if on edge, bounce",
    "MOTION_SETROTATIONSTYLE": "set rotation style [%1 v]",
    "MOTION_SETROTATIONSTYLE_LEFTRIGHT": "left-right",
    "MOTION_SETROTATIONSTYLE_DONTROTATE": "don't rotate",
    "MOTION_SETROTATIONSTYLE_ALLAROUND": "all around",
    "MOTION_XPOSITION": "x position",
    "MOTION_YPOSITION": "y position",
    "MOTION_DIRECTION": "direction",
    "MOTION_SCROLLRIGHT": "scroll right %1",
    "MOTION_SCROLLUP": "scroll up %1",
    "MOTION_ALIGNSCENE": "align scene %1",
    "MOTION_ALIGNSCENE_BOTTOMLEFT": "bottom-left",
    "MOTION_ALIGNSCENE_BOTTOMRIGHT": "bottom-right",
    "MOTION_ALIGNSCENE_MIDDLE": "middle",
    "MOTION_ALIGNSCENE_TOPLEFT": "top-left",
    "MOTION_ALIGNSCENE_TOPRIGHT": "top-right",
    "MOTION_XSCROLL": "x scroll",
    "MOTION_YSCROLL": "y scroll",
    "MOTION_STAGE_SELECTED": "Stage selected: no motion blocks",
    "OPERATOR_ADD": "(%1) + (%2)",
    "OPERATOR_SUBTRACT": "(%1) - (%2)",
    "OPERATOR_MULTIPLY": "(%1) * (%2)",
    "OPERATOR_DIVIDE": "(%1) / (%2)",
    "OPERATOR_RANDOM": "pick random (%1) to (%2)",
    "OPERATOR_GT": "(%1) > (%2)",
    "OPERATOR_LT": "(%1) < (%2)",
    "OPERATOR_EQUALS": "(%1) = (%2)",
    "OPERATOR_AND": "<%1> and <%2>",
    "OPERATOR_OR": "<%1> or <%2>",
    "OPERATOR_NOT": "not <%1>",
    "OPERATOR_JOIN": "join (%1) (%2)",
    "OPERATOR_JOIN_APPLE": "apple",
    "OPERATOR_JOIN_BANANA": "banana",
    "OPERATOR_LETTER_OF": "letter (%1) of (%2)",
    "OPERATOR_LETTEROF_APPLE": "a",
    "OPERATOR_LENGTH": "length of (%1)",
    "OPERATOR_CONTAINS": "(%1) contains (%2)?",
    "OPERATOR_MOD": "(%1) mod (%2)",
    "OPERATOR_ROUND": "round (%1)",
    "OPERATOR_MATHOP": "[%1 v] of (%2)",
    "OPERATOR_MATHOP_ABS": "abs",
    "OPERATOR_MATHOP_FLOOR": "floor",
    "OPERATOR_MATHOP_CEILING": "ceiling",
    "OPERATOR_MATHOP_SQRT": "sqrt",
    "OPERATOR_MATHOP_SIN": "sin",
    "OPERATOR_MATHOP_COS": "cos",
    "OPERATOR_MATHOP_TAN": "tan",
    "OPERATOR_MATHOP_ASIN": "asin",
    "OPERATOR_MATHOP_ACOS": "acos",
    "OPERATOR_MATHOP_ATAN": "atan",
    "OPERATOR_MATHOP_LN": "ln",
    "OPERATOR_MATHOP_LOG": "log",
    "OPERATOR_MATHOP_EEXP": "e ^",
    "OPERATOR_MATHOP_10EXP": "10 ^",
    "PROCEDURES_DEFINITION": "define %1",
    "SENSING_TOUCHINGOBJECT": "touching (%1 v)?",
    "SENSING_TOUCHINGOBJECT_POINTER": "mouse-pointer",
    "SENSING_TOUCHINGOBJECT_EDGE": "edge",
    "SENSING_TOUCHINGCOLOR": "touching color (%1)?",
    "SENSING_COLORISTOUCHINGCOLOR": "color (%1) is touching (%2)?",
    "SENSING_DISTANCETO": "distance to (%1 v)",
    "SENSING_DISTANCETOMENU": "distance to (%1 v)",
    "SENSING_DISTANCETO_POINTER": "mouse-pointer",
    "SENSING_ASKANDWAIT": "ask (%1) and wait",
    "SENSING_ASK_TEXT": "What's your name?",
    "SENSING_ANSWER": "answer",
    "SENSING_KEYPRESSED": "key (%1 v) pressed?",
    "SENSING_MOUSEDOWN": "mouse down?",
    "SENSING_MOUSEX": "mouse x",
    "SENSING_MOUSEY": "mouse y",
    "SENSING_SETDRAGMODE": "set drag mode [%1 v]",
    "SENSING_SETDRAGMODE_DRAGGABLE": "draggable",
    "SENSING_SETDRAGMODE_NOTDRAGGABLE": "not draggable",
    "SENSING_LOUDNESS": "loudness",
    "SENSING_LOUD": "loud?",
    "SENSING_TIMER": "timer",
    "SENSING_RESETTIMER": "reset timer",
    "SENSING_OF": "[%1 v] of (%2 v)",
    "SENSING_OF_XPOSITION": "x position",
    "SENSING_OF_YPOSITION": "y position",
    "SENSING_OF_DIRECTION": "direction",
    "SENSING_OF_COSTUMENUMBER": "costume #",
    "SENSING_OF_COSTUMENAME": "costume name",
    "SENSING_OF_SIZE": "size",
    "SENSING_OF_VOLUME": "volume",
    "SENSING_OF_BACKDROPNUMBER": "backdrop #",
    "SENSING_OF_BACKDROPNAME": "backdrop name",
    "SENSING_OF_STAGE": "Stage",
    "SENSING_OF_OBJECT_MENU": "[%1 v] of (%2 v)",
    "SENSING_CURRENT": "current [%1 v]",
    "SENSING_CURRENT_YEAR": "year",
    "SENSING_CURRENT_MONTH": "month",
    "SENSING_CURRENT_DATE": "date",
    "SENSING_CURRENT_DAYOFWEEK": "day of week",
    "SENSING_CURRENT_HOUR": "hour",
    "SENSING_CURRENT_MINUTE": "minute",
    "SENSING_CURRENT_SECOND": "second",
    "SENSING_DAYSSINCE2000": "days since 2000",
    "SENSING_USERNAME": "username",
    "SENSING_USERID": "user id",
    "SENSING_KEYOPTIONS": "key (%1 v) pressed?",
    "SOUND_PLAY": "start sound (%1 v)",
    "SOUND_PLAYUNTILDONE": "play sound (%1 v) until done",
    "SOUND_STOPALLSOUNDS": "stop all sounds",
    "SOUND_SETEFFECTTO": "set [%1 v] effect to (%2)",
    "SOUND_CHANGEEFFECTBY": "change [%1 v] effect by (%2)",
    "SOUND_CLEAREFFECTS": "clear sound effects",
    "SOUND_EFFECTS_PITCH": "pitch",
    "SOUND_EFFECTS_PAN": "pan left/right",
    "SOUND_CHANGEVOLUMEBY": "change volume by (%1)",
    "SOUND_SETVOLUMETO": "set volume to (%1)%",
    "SOUND_VOLUME": "volume",
    "SOUND_RECORD": "record...",
    "CATEGORY_MOTION": "Motion",
    "CATEGORY_LOOKS": "Looks",
    "CATEGORY_SOUND": "Sound",
    "CATEGORY_EVENTS": "Events",
    "CATEGORY_CONTROL": "Control",
    "CATEGORY_SENSING": "Sensing",
    "CATEGORY_OPERATORS": "Operators",
    "CATEGORY_VARIABLES": "Variables",
    "CATEGORY_MYBLOCKS": "My Blocks",
    "DUPLICATE": "Duplicate",
    "DELETE": "Delete",
    "ADD_COMMENT": "Add Comment",
    "REMOVE_COMMENT": "Remove Comment",
    "DELETE_BLOCK": "Delete Block",
    "DELETE_X_BLOCKS": "Delete %1 Blocks",
    "DELETE_ALL_BLOCKS": "Delete all %1 blocks?",
    "CLEAN_UP": "Clean up Blocks",
    "HELP": "Help",
    "UNDO": "Undo",
    "REDO": "Redo",
    "EDIT_PROCEDURE": "Edit",
    "SHOW_PROCEDURE_DEFINITION": "Go to definition",
    "WORKSPACE_COMMENT_DEFAULT_TEXT": "Say something...",
    "COLOUR_HUE_LABEL": "Color",
    "COLOUR_SATURATION_LABEL": "Saturation",
    "COLOUR_BRIGHTNESS_LABEL": "Brightness",
    "CHANGE_VALUE_TITLE": "Change value:",
    "RENAME_VARIABLE": "Rename variable",
    "RENAME_VARIABLE_TITLE": "Rename all \"%1\" variables to:",
    "RENAME_VARIABLE_MODAL_TITLE": "Rename Variable",
    "NEW_VARIABLE": "Make a Variable",
    "NEW_VARIABLE_TITLE": "New variable name:",
    "VARIABLE_MODAL_TITLE": "New Variable",
    "VARIABLE_ALREADY_EXISTS": "A variable named \"%1\" already exists.",
    "VARIABLE_ALREADY_EXISTS_FOR_ANOTHER_TYPE": "A variable named \"%1\" already exists for another variable of type \"%2\".",
    "DELETE_VARIABLE_CONFIRMATION": "Delete %1 uses of the \"%2\" variable?",
    "CANNOT_DELETE_VARIABLE_PROCEDURE": "Can't delete the variable \"%1\" because it's part of the definition of the function \"%2\"",
    "DELETE_VARIABLE": "Delete the \"%1\" variable",
    "NEW_PROCEDURE": "Make a Block",
    "PROCEDURE_ALREADY_EXISTS": "A procedure named \"%1\" already exists.",
    "PROCEDURE_DEFAULT_NAME": "block name",
    "PROCEDURE_USED": "To delete a block definition, first remove all uses of the block",
    "NEW_LIST": "Make a List",
    "NEW_LIST_TITLE": "New list name:",
    "LIST_MODAL_TITLE": "New List",
    "LIST_ALREADY_EXISTS": "A list named \"%1\" already exists.",
    "RENAME_LIST_TITLE": "Rename all \"%1\" lists to:",
    "RENAME_LIST_MODAL_TITLE": "Rename List",
    "DEFAULT_LIST_ITEM": "thing",
    "DELETE_LIST": "Delete the \"%1\" list",
    "RENAME_LIST": "Rename list",
    "NEW_BROADCAST_MESSAGE": "New message",
    "NEW_BROADCAST_MESSAGE_TITLE": "New message name:",
    "BROADCAST_MODAL_TITLE": "New Message",
    "DEFAULT_BROADCAST_MESSAGE_NAME": "message1",
    "PEN_SETPENCOLORTOCOLOR": "set pen color to (%1)",
    "PEN_SETPENCOLORPARAMTO": "set pen (%1 v) to (%2)",
    "PEN_SETPENSIZETO": "set pen size to (%1)",
    "PEN_CHANGEPENCOLORPARAMBY": "change pen (%1 v) by (%2)",
    "PEN_CHANGEPENSIZEBY": "change pen size by (%1)",
    "PEN_CHANGEPENHUEBY": "change color by (%1)",
    "PEN_PENDOWN": "pen down",
    "PEN_PENUP": "pen up",
    "PEN_CLEAR": "erase all",
    "PEN_STAMP": "stamp",
    "SOUND_SOUNDS_MENU": "start sound (%1)",
    "LOOKS_BACKDROPS": "looks_backdrops (%1)",
    "MUSIC_CHANGETEMPO": "change tempo by (%1)",
    "MUSIC_SETTEMPOTO": "set tempo to (%1)",
    "MUSIC_SETINSTRUMENT": "set instrument to (%1 v)",
    "MUSIC_PLAYNOTEFORBEATS": "play note (%1) for (%2) beats",
    "MUSIC_RESTFORBEATS": "rest for (%1) beats",
    "MUSIC_PLAYDRUMFORBEATS": "play drum (%1 v) for (%2) beats",
    "VIDEOSENSING_WHENMOTIONGREATERTHAN": "when video motion > (%1)",
    "VIDEOSENSING_VIDEOON": "video (%1 v) on (%2 v)",
    "VIDEOSENSING_VIDEOTOGGLE": "turn video (%1 v)",
    "VIDEOSENSING_SETVIDEOTRANSPARENCYTO": "set video transparency to (%1)",
    "TRANSLATE_GETTRANSLATE": "translate (%1) to (%2 v)",
    "TEXT2SPEECH_SPEAKANDWAIT": "speak (%1)",
    "TEXT2SPEECH_SETVOICE": "set voice to (%1 v)",
    "TEXT2SPEECH_SETLANGUAGE": "set language to (%1 v)",
    "MAKEYMAKEY_WHENCODEPRESSED": "when (%1 v) in order",
    "MAKEYMAKEY_KEYPRESSED": "when (%1 v) key pressed",
    "VIDEOSENSING_SETVIDEOTRANSPARENCY": "when video motion > (%1)",
    "MICROBIT_WHENBUTTONPRESSED": "when (%1 v) button pressed",
    "MICROBIT_ISBUTTONPRESSED": "(%1 v) button pressed?",
    "MICROBIT_WHENGESTURE" : "when (%1 v)",
    "MICROBIT_DISPLAYSYMBOL": "display (%1 v)",
    "MICROBIT_DISPLAYTEXT": "display text (%1)",
    "MICROBIT_DISPLAYCLEAR": "clear display",
    "MICROBIT_WHENTILTED": "when titled (%1 v)",
    "MICROBIT_ISTILTED": "titled (%1 v)",
    "MICROBIT_GETTILTANGLE": "tilt angle (%1 v)",
    "MICROBIT_WHENPINCONNECTED": "when pin (%1 v) connected",
    "EV3_MOTORTURNCLOCKWISE": "motor (%1 v) turn this way for (%2) seconds",
    "EV3_MOTORTURNCOUNTERCLOCKWISE": "motor (%1 v) turn that way for (%2) seconds",
    "EV3_MOTORSETPOWER": "motor (%1 v) set power (%2)%",
    "EV3_GETMOTORPOSITION": "motor (%1 v) position",
    "EV3_WHENBUTTONPRESSED": "button (%1 v) pressed",
    "EV3_WHENDISTANCELESSTHAN": "when distance < (%1)",
    "EV3_WHENBRIGHTNESSLESSTHAN": "when brightness < (%1)",
    "EV3_BUTTONPRESSED": "button (%1 v) pressed?",
    "EV3_GETDISTANCE": "distance",
    "EV3_GETBRIGHTNESS": "brightness",
    "EV3_BEEP": "beep note (%1) for (%2) secs",
    "BOOST_MOTORONFOR": "turn motor (%1 v) for (%2) seconds",
    "BOOST_MOTORONFORROTATION": "turn motor (%1 v) for (%2) rotations",
    "BOOST_MOTORON": "turn motor (%1) on",
    "BOOST_MOTOROFF": "turn motor (%1) off",
    "BOOST_SETMOTORPOWER": "set motor (%1 v) speed to (%2)%",
    "BOOST_SETMOTORDIRECTION": "set motor (%1 v) direction (%2 v)",
    "BOOST_GETMOTORPOSITION": "motor (%1 v) position",
    "BOOST_WHENCOLOR": "when (%1 v) brick seen",
    "BOOST_GETTILTANGLE": "tilt angle (%1 v)",
    "BOOST_SEEINGCOLOR": "seeing (%1 v) brick?",
    "BOOST_WHENTILTED": "when tilted (%1 v)",
    "BOOST_SETLIGHTHUE": "set light color to (%1)",
    "WEDO2_MOTORONFOR": "turn (%1 v) on for (%2) seconds",
    "WEDO2_MOTORON": "turn (%1 v) on",
    "WEDO2_MOTOROFF": "turn (%1 v) off",
    "WEDO2_STARTMOTORPOWER": "set (%1 v) power to (%2)",
    "WEDO2_SETMOTORDIRECTION": "set (%1 v) direction to (%2 v)",
    "WEDO2_SETLIGHTHUE": "set light color to (%1)",
    "WEDO2_WHENDISTANCE": "when distance (%1 v) (%2)",
    "WEDO2_WHENTILTED": "when tilted (%1 v)",
    "WEDO2_GETDISTANCE": "distance",
    "WEDO2_ISTILTED": "tilted (%1 v)",
    "WEDO2_GETTILTANGLE": "tilt angle (%1 v)",
    "GDXFOR_WHENGESTURE": "when (%1 v)",
    "GDXFOR_WHENFORCEPUSHEDORPULLED": "when force sensor (%1 v)",
    "GDXFOR_GETFORCE": "force",
    "GDXFOR_WHENTILTED": "whenTilted (%1 v)",
    "GDXFOR_ISTILTED": "tilted (%1 v)?",
    "GDXFOR_GETTILT": "tilt angle (%1 v)",
    "GDXFOR_ISFREEFALLING": "falling?",
    "GDXFOR_GETSPINSPEED": "spin speed (%1 v)",
    "GDXFOR_GETACCELERATION": "acceleration (%1 v)"
}

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
        """
        Searches through each block and outputs a dictionary with all the contents inside the block
        """
        block = block_dict[block_name]
        
        current_counter = self.counter_block

        new_block = {f'block_{self.counter_block}': {"name":block["opcode"]}}
        self.blocks.append(block["opcode"])
        self.counter_block += 1
        
        # For custom blocks
        if "mutation" in block and "proccode" in block["mutation"]:
            func_name = block["mutation"]["proccode"]

            n_args = func_name.count('%s') + func_name.count('%n')

            # Create a List with the arguments spots
            args = [f'({i})' for i in range(1, n_args + 1)]

            # Replace the arguments in the function name
            for arg in args:
                if '%s' in func_name:
                    func_name = func_name.replace('%s', arg, 1)
                elif '%n' in func_name:
                    func_name = func_name.replace('%n', arg, 1)

            new_block[f'block_{current_counter}']['func_name'] = func_name

            if "argumentnames" in block["mutation"] and '%s' in func_name:
                list_of_arguments = block["mutation"]["argumentnames"].replace('"', '').strip('][').split(',')
                for arg in list_of_arguments:
                    new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = arg

                    self.vars[f'var_{self.counter_vars}'] = arg

                    self.counter_vars += 1

            return new_block

        #For fields (variables)
        n_input = 0
        for input, value in block["fields"].items():
            new_var = value[0]

            new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = new_var

            self.vars[f'var_{self.counter_vars}'] = new_var

            self.counter_vars += 1

            n_input += 1
        
        # For inputs that either are another block (with key input_{i}) or just a variable (with key var_{i})
        for input in block["inputs"].keys():
            if input not in self.child_keys:
                value = block["inputs"][input][1]
                if type(value) is str:
                    # Case where there is another block instead of a variable
                    if len(value) == 20 or value in block_dict.keys():
                        new_block[f'block_{current_counter}'][f'input_{n_input}'] = self.parser_block(block_dict, value)
                    else:
                        new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = value

                        self.vars[f'var_{self.counter_vars}'] = value

                        self.counter_vars += 1
                else:
                    if (value != None):
                        value = block["inputs"][input][1][1]
                        new_block[f'block_{current_counter}'][f'var_{self.counter_vars}'] = value
                        self.vars[f'var_{self.counter_vars}'] = value
                        self.counter_vars += 1
                n_input += 1
        return new_block

    def parser_script(self, block_dict, start):
        """
        Goes through the JSON file of a Scratch script and outputs a dictionary 
        containing all the blocks and variables of such script.
        """
        current = start
        curr_dict = {}

        #tracemalloc.start()
        #MEMORY_LIMIT_GB = 0.5

        while True:
            current_block = self.parser_block(block_dict=block_dict, block_name=current)

            #current_memory = tracemalloc.get_traced_memory()[1] / (1024 ** 3) 
            #print(f"    Memory used at the moment parsing the script: {current_memory:.2f} GB")
            #if current_memory > MEMORY_LIMIT_GB:
                #print(f"    Detected huge use of memory: {current_memory:.2f} GB. Finalized.")
                #break

            # For "if" blocks or "ifelse" blocks
            for i, child_key in enumerate(self.child_keys):
                if child_key in block_dict[current]['inputs']:
                    input_block = block_dict[current]['inputs'][child_key][1]
                    if input_block:
                        current_block[[*current_block][0]][f'child_{i}'] = self.parser_script(block_dict, input_block)
                        del input_block
                    else:
                        current_block[[*current_block][0]][f'child_{i}'] = None

            curr_dict.update(current_block)

            next_block = block_dict[current]["next"]
            if next_block:
                current = next_block
            else:
                break

        #tracemalloc.stop()
        del current, current_block, next_block
        #gc.collect()

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
    
    def convert_block_to_text(self, block_name):
        """
        Converts an unique block into a text format using the syntax from scratchblocks (https://en.scratch-wiki.info/wiki/Block_Plugin/Syntax)
        """
        name = str(block_name["opcode"]).upper()
        print("block name:", block_name)
        print("name:", name)
        if name not in BLOCK_TEXT and name not in STARTER_BLOCKS:
            block_text = block_name["mutation"]["proccode"]
        else:
            block_text = BLOCK_TEXT[name]

        placeholders = ["%1", "%2", "%3", "%4", "%s"]
        for placeholder in placeholders:
            if placeholder == "%s":
                block_text = block_text.replace(placeholder, "()")
            else:
                block_text = block_text.replace(placeholder, "")

        return block_text

    def convert_to_text(self, indent=0, dict=None):
        """
        Converts a script into a text format using the syntax from scratchblocks (https://en.scratch-wiki.info/wiki/Block_Plugin/Syntax)
        """
        if dict == None:
            self.c = 0
            dict = self.script_dict

        new_text = ""
        for block, item in dict.items():
            block_name = item["name"]

            # Case for custom blocks
            if block_name == "procedures_prototype" or block_name == "procedures_call":
                block_text = item["func_name"]
            elif block_name.upper() not in BLOCK_TEXT:
                block_text = "%1"
            else:
                block_text = BLOCK_TEXT[block_name.upper()]

            n_input = 0

            for i in range(1, 4):
                sub_text =""
                if f'%{i}' not in block_text:
                    continue

                if f"var_{self.c}" in item:
                    sub_text = str(item[f"var_{self.c}"])
                    self.c += 1
                    n_input += 1
                elif f"input_{n_input}" in item:
                    sub_text = self.convert_to_text(indent = 0, dict = item[f"input_{n_input}"])
                    n_input += 1

                block_text = block_text.replace(f'%{i}', sub_text)

                
                
            if len(dict) == 1:
                new_text += block_text
            else:
                new_text += '\n' + block_text

            # For children/inner blocks 
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