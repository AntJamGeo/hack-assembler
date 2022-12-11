class Parser():
    def __init__(self):
        self.line_no = 0
    
    def parse(self, line):
        if len(line) < 1: # ignore whitespace
            return ""
        elif line[0] == "@": # A-Instruction
            self.line_no += 1
            return self._a_inst(line)
        elif line[0] == "(": # L-Instruction
            return ""
        elif line[0] in ["A", "D", "M", "0", "1", "-", "!"]: # C-Instruction
            self.line_no += 1
            return self._c_inst(line)
        elif len(line) > 1 and line[:2] == "//": # ignore comments
            return ""
        else:
            raise InstructionError(f"Invalid Instruction: {line}")

    def _a_inst(self, line):
        for i in range(1, len(line)):
            if line[i] == " ":
                break
        return ("A", line[1:i+1])

    def _l_inst(self, line):
        return ""

    def _c_inst(self, line):
        return ("C", "", "", "")

class InstructionError(Exception):
    pass
