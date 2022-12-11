class Parser():
    def __init__(self):
        self.line_no = 0
    
    def parse(self, line):
        if len(line) < 1: # ignore whitespace
            return False
        elif line[0] == "@": # A-Instruction
            self.line_no += 1
            return self._a_inst(line)
        elif line[0] == "(": # L-Instruction
            return False
        elif line[0] in {"A", "D", "M", "0", "1", "-", "!"}: # C-Instruction
            self.line_no += 1
            return self._c_inst(line)
        elif len(line) > 1 and line[:2] == "//": # ignore comments
            return False
        else:
            raise InvalidInstructionError(line)

    def _a_inst(self, line):
        comment_index = line.find("//")
        if comment_index != -1:
            line = line[:comment_index].strip()
        if len(line) > 1 and len(line.split()) == 1:
            return ("A", line[1:])
        else:
            raise InvalidInstructionError(line)

    def _l_inst(self, line):
        return ""

    def _c_inst(self, line):
        return ("C", "", "", "")

class InvalidInstructionError(Exception):
    pass
