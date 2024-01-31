from app.hairball3.plugin import Plugin
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


class DuplicateScripts(Plugin):
    """
    Plugin that analyzes duplicate scripts in scratch projects version 3.0
    """

    def __init__(self, filename, json_project, verbose=False):
        super().__init__(filename, json_project, verbose)
        self.total_duplicate = 0
        self.blocks_dicc = {}
        self.total_blocks = []
        self.list_duplicate = []

    def analyze(self):

        json_scratch_project = self.json_project.copy()
        scripts_set = set()

        for key, list_dict_targets in json_scratch_project.items():
            if key == "targets":
                for dict_target in list_dict_targets:
                    block_name = dict_target['name']
                    for dict_key, dicc_value in dict_target.items():
                        if dict_key == "blocks":
                            for blocks, blocks_value in dicc_value.items():
                                if type(blocks_value) is dict:
                                    self.blocks_dicc[blocks] = blocks_value
                                    self.total_blocks.append(blocks_value)

        for key_block in self.blocks_dicc:
            block = self.blocks_dicc[key_block]

            if block["topLevel"]:
                block_list = []
                block_list.append(block["opcode"])
                next = block["next"]
                aux_next = None
                self._search_next(next, block_list, key_block, aux_next)

                blocks_tuple = tuple(block_list)

                if blocks_tuple in scripts_set:
                    if len(block_list) > 5:
                        if not block_list in self.list_duplicate:
                            self.total_duplicate += 1
                            self.list_duplicate.append(block_list)
                else:
                    scripts_set.add(blocks_tuple)

    def _search_next(self, next, block_list, key_block, aux_next):
        if next is None:
            try:
                next = self.blocks_dicc[key_block]["inputs"]["SUBSTACK"][1]
                if next is None:
                    return
            except:
                if aux_next is not None:
                    next = aux_next
                    aux_next = None
                else:
                    next = None
                    return
        else: # loop block
            if "SUBSTACK" in self.blocks_dicc[key_block]["inputs"]:
                loop_block = self.blocks_dicc[key_block]["inputs"]["SUBSTACK"][1]
                if loop_block is not None: #Check if is a loop block but EMPTY
                    aux_next = next          #Save the real next until the end of the loop
                    next = loop_block

        block = self.blocks_dicc[next]
        block_list.append(block["opcode"])
        key_block = next
        next = block["next"]
        self._search_next(next, block_list, key_block, aux_next)

    def finalize(self) -> dict:

        self.analyze()

        result = ("%d duplicate scripts found" % self.total_duplicate)
        result += "\n"
        for duplicate in self.list_duplicate:
            result += str(duplicate)
            result += "\n"

        self.dict_mastery['description'] = result
        self.dict_mastery['total_duplicate_scripts'] = self.total_duplicate
        self.dict_mastery['list_duplicate_scripts'] = self.list_duplicate

        if self.verbose:
            logger.info(self.dict_mastery['description'])
            logger.info(self.dict_mastery['total_duplicate_scripts'])
            logger.info(self.dict_mastery['list_duplicate_scripts'])

        dict_result = {'plugin': 'duplicate_scripts', 'result': self.dict_mastery}

        return dict_result





