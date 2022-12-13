from .asmexceptions import BracketError, DuplicateLabelError, BadLabelError
from .asmtools import strip_line

class SymbolTable():
    """
    A store of all symbols in the .asm file.

    Attributes
    ----------
    table : dict
        Contains all symbols and their corresponding addresses
    rom_address: int
        Keeps track of which rom address should be assigned to the next label
    line : int
        Keeps track of which line in the file is being accessed

    Methods
    -------
    add_label(inst)
        Looks for an L-Instruction and adds any new label to the table
    """
    
    def __init__(self):
        self.table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                      "SCREEN": 16384, "KBD": 24576}
        for i in range(16):
            self.table["R"+str(i)] = i
        self.rom_address = 0
        self.line = 0

    def add_label(self, inst):
        """
        Looks for an L-Instruction and adds any new label to the table.

        Parameters
        ----------
        inst : str
            The instruction in which we want to find a label
        """

        self.inst = strip_line(inst)
        self.line += 1
        if len(self.inst) < 1:
            return

        if self.inst[0] == "(":
            if self.inst[-1] != ")":
                raise BracketError(self.line, self.inst)
            label = self.inst[1:-1]
            if label in self.table:
                raise DuplicateLabelError(self.line, self.inst, label)
            if len(label.split()) > 1:
                raise BadLabelError(self.line, self.inst, label)
            self.table[label] = self.rom_address
        else:
            self.rom_address += 1

    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        return self.table[symbol]
