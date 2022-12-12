from .asmexceptions import InstructionError, NoAddressError, BadAddressError

class Parser():
    def __init__(self):
        self.line_no = 0
        self.total_lines = 0
        self.instruction = None

    def parse(self, instruction):
        self.instruction = instruction
        self.total_lines += 1
        """Determine which type of instruction is being given."""
        if len(self.instruction) < 1: # ignore whitespace
            return False
        elif self.instruction[0] == "@": # A-Instruction
            self.line_no += 1
            return self._a_inst()
        elif self.instruction[0] == "(": # L-Instruction
            return False
        elif self.instruction[0] in {"A", "D", "M", "0", "1", "-", "!"}: # C-Instruction
            self.line_no += 1
            return self._c_inst()
        elif len(self.instruction) > 1 and self.instruction[:2] == "//": # ignore comments
            return False
        raise InstructionError(self.total_lines, self.instruction)


    def _a_inst(self):
        """Parse A-Instructions."""
        inst = _strip_comments(self.instruction)
        if inst == "@":
            raise NoAddressError(self.total_lines, self.instruction)
        if len(inst.split()) > 1:
            raise BadAddressError(self.total_lines, self.instruction, inst[1:]) 
        return ("A", inst[1:])

    def _l_inst(self):
        """Parse L-Instructions."""
        return ""

    def _c_inst(self):
        """Parse C-Instructions."""
        inst = _strip_comments(self.instruction) # remove comments

        # Find first '=' and split into dest and comp;jump parts
        if inst[-1] == "=": # no final '=' simplifies later calculation
            raise InstructionError(self.total_lines, self.instruction)
        equals_index = inst.find("=")
        if equals_index == -1:
            dest, compjump = None, inst
        else:
            dest = inst[:equals_index]
            compjump = inst[equals_index+1:] # no final '=' so this is allowed

        # Find first ';' and split into comp and jump parts
        semi_colon_index = compjump.find(";")
        if semi_colon_index == -1:
            comp, jump = compjump, None 
        else:
            comp = compjump[:semi_colon_index]
            jump = compjump[semi_colon_index+1:]

        return ("C", dest, comp, jump, self.total_lines, self.instruction) 

def _strip_comments(line):
    """Remove any comments from a line."""
    comment_index = line.find("//")
    if comment_index != -1:
        return line[:comment_index].strip()
    return line

_valid_d = {None, "M", "D", "MD", "A", "AM", "AD", "AMD"}
_valid_c = {"0", "1", "-1", "D", "A", "M", "!D", "!A", "!M", "-D",
            "-A", "-M", "D+1", "A+1", "M+1", "D-1", "A-1", "M-1",
            "D+A", "D+M", "D-A", "D-M", "A-D", "M-D", "D&A", "D&M",
            "D|A", "D|M"}
_valid_j = {None, "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"}
