import string
from .asmexceptions import (NoAddressError, BadVariableError,
        AddressOutOfBoundsError)

class Instruction():
    """
    An instruction class.

    Attributes
    ----------
    line : int
        The number in the file of the line from which the instruction
        was obtained
    inst : str
        The full instruction (excluding comments and surrounding
        whitespace) as written in the provided file

    Methods
    -------
    get_line()
        Return the line attribute
    get_inst()
        Return the inst attribute
    """
    def __init__(self, line, inst):
        self.line = line
        self.inst = inst

    def get_line(self):
        return self.line

    def get_inst(self):
        return self.inst

class AInstruction(Instruction):
    """
    Extends the Instruction class by also containing the value
    provided for the given A-Instruction.

    Attributes
    ----------
    line : int
        The number in the file of the line from which the instruction
        was obtained
    inst : str
        The full instruction (excluding comments and surrounding
        whitespace) as written in the provided file
    value : str
        The value after the '@' in the given A-Instruction
    is_numeric : bool
        True if the value attribute is numeric, false if symbolic

    Methods
    -------
    get_line()
        Return the line attribute
    get_inst()
        Return the inst attribute
    get_value()
        Return the value attribute
    is_numeric()
        Return the is_symbol attribute
    """

    def __init__(self, line, inst, value):
        super().__init__(line, inst)
        self.value = value
        self.numeric = value.isdigit()
        self._check_value()

    def get_value(self):
        return self.value

    def is_numeric(self):
        return self.numeric

    def _check_value(self):
        """Check if an A-Instruction value is valid."""
        if self.value == "":
            raise NoAddressError(self)
        if len(self.value.split()) > 1:
            raise BadVariableError(self)
        if self.numeric:
            address = int(self.value)
            if address < 0 or address > 32767:
                raise AddressOutOfBoundsError(self)
        elif self.value[0].isdigit():
            raise BadVariableError(self)
        else:
            for c in self.value:
                if c not in valid_chars:
                    raise BadVariableError(self)

class CInstruction(Instruction):
    """
    Extends the Instruction class by also containing relevant
    C-Instruction information.

    Attributes
    ----------
    line : int
        The number in the file of the line from which the instruction
        was obtained
    inst : str
        The full instruction (excluding comments and surrounding
        whitespace) as written in the provided file
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
    get_inst()
        Return the inst attribute
    get_dest()
        Return the dest attribute
    get_comp()
        Return the comp attribute
    get_jump()
        Return the jump attribute
    """
    def __init__(self, line, inst, dest, comp, jump):
        super().__init__(line, inst)
        self.dest = dest
        self.comp = comp
        self.jump = jump
    
    def get_dest(self):
        return self.dest

    def get_comp(self):
        return self.comp

    def get_jump(self):
        return self.jump

valid_chars = frozenset(string.ascii_letters + string.digits + "_.$:")
