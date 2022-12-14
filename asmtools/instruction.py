import string
from abc import ABC, abstractmethod

from .symboltable import SymbolTable
from .exceptions import (
        NoAddressError, BadVariableError, AddressOutOfBoundsError,
        DestinationError, ComputationError, JumpError, RAMError)


class Instruction(ABC):
    """
    An abstract instruction class.

    Includes an abstract _check_valid method to ensure created
    instructions are valid on initialisation.

    Methods
    -------
    get_line()
        Return number in the file of the line from which the instruction
        was obtained
    get_inst()
        Return full instruction (excluding comments and surrounding
        whitespace) as written in the provided file
    encoded()
        Return the instruction in machine language
    """

    _symbol_table = SymbolTable()
    _ram_address = 16

    def __init__(self, line, inst):
        self._line = line
        self._inst = inst
        self._check_valid()
        self._encoded = self._encode()

    def get_line(self):
        return self._line

    def get_inst(self):
        return self._inst

    def encoded(self):
        return self._encoded

    @abstractmethod
    def _check_valid(self):
        pass

    @abstractmethod
    def _encode(self):
        pass

    @classmethod
    def load_table(cls, symbol_table):
        cls._symbol_table = symbol_table


class AInstruction(Instruction):
    """
    An A-Instruction class.

    Extends the Instruction class by also containing the value
    provided for the given A-Instruction.

    Methods
    -------
    get_line()
        Return number in the file of the line from which the instruction
        was obtained
    get_inst()
        Return full instruction (excluding comments and surrounding
        whitespace) as written in the provided file
    get_value()
        Return value after the '@' in the given A-Instruction
    is_numeric()
        Return true if the given address is numeric, false if symbolic
    encoded()
        Return the instruction in machine language
    """

    _VALID_CHARS = frozenset(string.ascii_letters + string.digits + "_.$:")

    def __init__(self, line, inst, value):
        self._value = value
        self._numeric = value.isdigit()
        super().__init__(line, inst)

    def get_value(self):
        return self._value

    def is_numeric(self):
        return self._numeric

    def _check_valid(self):
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
                if c not in AInstruction._VALID_CHARS:
                    raise BadVariableError(self)

    def _encode(self):
        if self._numeric:
            address = int(self._value)
        elif Instruction._symbol_table.contains(self._value):
            address = Instruction._symbol_table.get_address(self._value)
        else:
            if Instruction._ram_address == 16383:
                raise RAMError(self)
            address = Instruction._ram_address
            Instruction._symbol_table.add_entry(self._value, address)
            Instruction._ram_address += 1
        bits = bin(address).replace("0b", "")
        return "0" * (16 - len(bits)) + bits


class CInstruction(Instruction):
    """
    A C-Instruction class.

    Extends the Instruction class by also containing relevant
    C-Instruction information.

    Methods
    -------
    get_line()
        Return number in the file of the line from which the instruction
        was obtained
    get_inst()
        Return full instruction (excluding comments and surrounding
        whitespace) as written in the provided file
    get_dest()
        Return the destination registers for the computation
    get_comp()
        Return the desired computation
    get_jump()
        Return the jump operation
    encoded()
        Return the instruction in machine language
    """

    DEST = {None: "000", "M": "001", "D": "010", "MD": "011", "A": "100",
             "AM": "101", "AD": "110", "AMD": "111"}
    COMP = {"0": "0101010", "1": "0111111", "-1": "0111010",
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
    JUMP = {None: "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100",
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
        if self._dest not in CInstruction.DEST:
            raise DestinationError(self)
        if self._comp not in CInstruction.COMP:
            raise ComputationError(self)
        if self._jump not in CInstruction.JUMP:
            raise JumpError(self)

    def _encode(self):
        return ("111" + CInstruction.COMP[self._comp] +
                CInstruction.DEST[self._dest] + CInstruction.JUMP[self._jump])


def prepare_symbol_table(file_path):
    Instruction.load_table(SymbolTable(file_path))
