PLUGIN_DEADCODE_LIST_EVENT_VARS = [
    "event_broadcastandwait", "event_whenflagclicked",
    "event_whengreaterthan", "event_whenkeypressed",
    "event_whenthisspriteclicked", "event_whenbackdropswitchesto",
    "procedures_prototype", "procedures_definition"
]

PLUGIN_BACKDROPNAMING_DEFAULT_NAMES = [
    "backdrop",
    "fondo",
    "Fondos",
    "fons",
    "atzeko oihala"
]

PLUGIN_SPRITENAMING_DEFAULT_NAMES = [
    "Sprite",
    "Objeto",
    "Personatge",
    "Figura",
    "o actor",
    "Personaia"
]

PLUGIN_DEADCODE_LIST_LOOP_BLOCKS = [
    "control_repeat",
    "control_forever",
    "control_if",
    "control_if_else",
    "control_repeat_until"
]

PLUGIN_MASTERY_MAX_POINTS = 21
PLUGIN_MASTERY_AVG_POINTS = 3.0

PLUGIN_INIT_ATTRIBUTES = [
    'costume',
    'orientation',
    'position',
    'size',
    'visibility'
]

PLUGIN_INIT_BLOCKMAPPING = {
    'costume': frozenset([('looks_switchbackdropto', 'absolute'),
                          ('looks_nextbackdrop', 'relative'),
                          ('looks_switchcostumeto', 'absolute'),
                          ('looks_nextcostume', 'relative')]),
    'orientation': frozenset([('motion_turnright', 'relative'),
                              ('motion_turnleft', 'relative'),
                              ('motion_pointindirection', 'absolute'),
                              ('motion_pointtowards_menu', 'relative')]),
    'position': frozenset([('motion_movesteps', 'relative'),
                           ('motion_gotoxy', 'absolute'),
                           ('motion_goto', 'relative'),
                           ('motion_glidesecstoxy', 'relative'),
                           ('motion_glideto', 'relative'),
                           ('motion_changexby', 'relative'),
                           ('motion_setx', 'absolute'),
                           ('motion_changeyby', 'relative'),
                           ('motion_sety', 'absolute')]),
    'size': frozenset([('looks_changesizeby', 'relative'),
                       ('looks_setsizeto', 'absolute')]),
    'visibility': frozenset([('looks_hide', 'absolute'),
                             ('looks_show', 'absolute')])
}

URL_SCRATCH_SERVER = 'https://projects.scratch.mit.edu'
# URL_GETSB3 = 'http://127.0.0.1:3030/api'
URL_GETSB3 = 'http://127.0.0.1:3000/api'
URL_SCRATCH_API = 'https://api.scratch.mit.edu/projects'

