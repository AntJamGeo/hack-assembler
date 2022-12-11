class Parser():
    def __init__(self):
        self.line_no = 0

    def parse(self, line):
        """Determine which type of instruction is being given."""
        if len(line) < 1: # ignore whitespace
            return False
        elif line[0] == "@": # A-Instruction
            self.line_no += 1
            return _a_inst(line)
        elif line[0] == "(": # L-Instruction
            return False
        elif line[0] in {"A", "D", "M", "0", "1", "-", "!"}: # C-Instruction
            self.line_no += 1
            return _c_inst(line)
        elif len(line) > 1 and line[:2] == "//": # ignore comments
            return False
        raise InvalidInstructionError(line)


def _a_inst(line):
    """Parse A-Instructions."""
    line = _strip_comments(line)
    if len(line) > 1 and len(line.split()) == 1:
        return ("A", line[1:])
    else:
        raise InvalidInstructionError(line)

def _l_inst(line):
    """Parse L-Instructions."""
    return ""

def _c_inst(line):
    """Parse C-Instructions."""
    stripline = _strip_comments(line) # remove comments

    # Find first '=' and split into dest and comp;jump parts
    if stripline[0] == "=" or stripline[-1] == "=": # no initial/final '=' simplifies later calculation
        raise InvalidInstructionError(line)
    equals_index = stripline.find("=")
    if equals_index == -1:
        dest, compjump = None, stripline
    else:
        dest = stripline[:equals_index]
        compjump = stripline[equals_index+1:] # no final '=' so this is allowed

    # Find first ';' and split into comp and jump parts
    semi_colon_index = compjump.find(";")
    if semi_colon_index == -1:
        comp, jump = compjump, None 
    else:
        comp = compjump[:semi_colon_index]
        jump = compjump[semi_colon_index+1:]

    # Ensure valid dest, comp and jump
    if dest not in _valid_d:
        raise InvalidDestError(f"instruction: {line}, determined destination given: {dest}")
    if comp not in _valid_c:
        raise InvalidCompError(f"instruction: {line}, determined computation given: {comp}")
    if jump not in _valid_j:
        raise InvalidJumpError(f"instruction: {line}, determined jump given: {jump}")
    return ("C", dest, comp, jump) 

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

class InvalidInstructionError(Exception):
    pass

class InvalidDestError(InvalidInstructionError):
    pass

class InvalidCompError(InvalidInstructionError):
    pass

class InvalidJumpError(InvalidInstructionError):
    pass
