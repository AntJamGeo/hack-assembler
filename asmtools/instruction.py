import string
from abc import ABC, abstractmethod
from .exceptions import (NoAddressError, BadVariableError,
        AddressOutOfBoundsError, DestinationError, ComputationError,
        JumpError)

class Instruction(ABC):
    """
    An abstract instruction class. Includes an abstract _check_valid
    method to ensure created instructions are valid on initialisation.

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
        self._line = line
        self._inst = inst
        self._check_valid()

    def get_line(self):
        return self._line

    def get_inst(self):
        return self._inst

    @abstractmethod
    def _check_valid(self):
        pass

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

    _valid_chars = frozenset(string.ascii_letters + string.digits + "_.$:")

    def __init__(self, line, inst, value):
        self._value = value
        self._numeric = value.isdigit()
        super().__init__(line, inst)

    def get_value(self):
        return self._value

    def is_numeric(self):
        return self._numeric

    def _check_valid(self):
        """Check if an A-Instruction value is valid."""
        if self._value == "":
            raise NoAddressError(self)
        if len(self._value.split()) > 1:
            raise BadVariableError(self)
        if self._numeric:
            address = int(self._value)
            if address < 0 or address > 32767:
                raise AddressOutOfBoundsError(self)
        elif self._value[0].isdigit():
            raise BadVariableError(self)
        else:
            for c in self._value:
                if c not in AInstruction._valid_chars:
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

    dest = {None: "000", "M": "001", "D": "010", "MD": "011", "A": "100",
             "AM": "101", "AD": "110", "AMD": "111"}

    comp = {"0": "0101010", "1": "0111111", "-1": "0111010",
             "D": "0001100", "A": "0110000", "M": "1110000",
             "!D": "0001101", "!A": "0110001", "!M": "1110001",
             "-D": "0001111", "-A": "0110011", "-M": "1110011",
             "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
             "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
             "D+A": "0000010", "D+M": "1000010",
             "D-A": "0010011", "D-M": "1010011",
             "A-D": "0000111", "M-D": "1000111",
             "D&A": "0000000", "D&M": "1000000",
             "D|A": "0010101", "D|M": "1010101"}

    jump = {None: "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100",
             "JNE": "101", "JLE": "110", "JMP": "111"}

    def __init__(self, line, inst, dest, comp, jump):
        self._dest = dest
        self._comp = comp
        self._jump = jump
        super().__init__(line, inst)
    
    def get_dest(self):
        return self._dest

    def get_comp(self):
        return self._comp

    def get_jump(self):
        return self._jump

    def _check_valid(self):
        if self._dest not in CInstruction.dest:
            raise DestinationError(self)
        if self._comp not in CInstruction.comp:
            raise ComputationError(self)
        if self._jump not in CInstruction.jump:
            raise JumpError(self)

