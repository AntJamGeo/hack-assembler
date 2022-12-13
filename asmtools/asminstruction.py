class Instruction():
    """
    An instruction class.

    Attributes
    ----------
    line : int
        The number in the file of the line from which the instruction
        was obtained

    Methods
    -------
    get_line()
        Return the line attribute
    """
    def __init__(self, line):
        self.line = line

    def get_line(self):
        return self.line

class AInstruction(Instruction):
    """
    Extends the Instruction class by also containing the value
    provided for the given A-Instruction.

    Attributes
    ----------
    line : int
        The number in the file of the line from which the instruction
        was obtained
    value : str
        The value after the '@' in the given A-Instruction
    is_symbol : bool
        True if the value attribute is symbolic, false if numeric

    Methods
    -------
    get_line()
        Return the line attribute
    get_value()
        Return the value attribute
    is_symbol()
        Return the is_symbol attribute
    """

    def __init__(self, value, line):
        super().__init__(line)
        self.value = value
        self.is_symbol = not value.isdigit()

    def get_value(self):
        return self.value

    def is_symbol(self):
        return self.is_symbol

class CInstruction(Instruction):
    """
    Extends the Instruction class by also containing relevant
    C-Instruction information.

    Attributes
    ----------
    line : int
        The number in the file of the line from which the instruction
        was obtained
    dest : str
        Destination registers for the computation
    comp : str
        The desired computation
    jump : str
        The desired jump operation

    Methods
    -------
    get_line()
        Return the line attribute
    get_dest()
        Return the dest attribute
    get_comp()
        Return the comp attribute
    get_jump()
        Return the jump attribute
    """
    def __init__(self, dest, comp, jump, line):
        super().__init__(line)
        self.dest = dest
        self.comp = comp
        self.jump = jump
    
    def get_dest(self):
        return self.dest

    def get_comp(self):
        return self.comp

    def get_jump(self):
        return self.jump
