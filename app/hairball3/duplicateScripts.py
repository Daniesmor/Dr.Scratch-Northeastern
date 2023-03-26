from app.hairball3.plugin import Plugin


class DuplicateScripts(Plugin):
    """
    Plugin that analyzes duplicate scripts in scratch projects version 3.0
    """

    def __init__(self, filename, json_project):
        super().__init__(filename, json_project)
        self.total_duplicate = 0
        self.blocks_dicc = {}
        self.total_blocks = []
        self.list_duplicate = []

    def analyze(self):
        scripts_set = set()

        for key, value in self.json_project.items():
            if key == "targets":
                for dicc in value:
                    for dicc_key, dicc_value in dicc.items():
                        if dicc_key == "blocks":
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
            try: # Maybe is a control_forever block
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
        else: # Maybe is a loop block
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

    def finalize(self):

        self.analyze()

        result = ("%d duplicate scripts found" % self.total_duplicate)
        result += "\n"
        for duplicate in self.list_duplicate:
            result += str(duplicate)
            result += "\n"
        return result


# def main(filename):
#     duplicate = DuplicateScripts(filename)
#     duplicate.analyze()
#     return duplicate.finalize()


