from .asmexceptions import BracketError, DuplicateLabelError, BadLabelError
from .asmtools import strip_line

class SymbolTable():
    """
    A store of all symbols in the .asm file.

    Attributes
    ----------
    table : dict
        Contains all symbols and their corresponding addresses
    line_no : int
        Keeps track of which line number should be assigned to the next label

    Methods
    -------
    add_label(inst)
        Looks for an L-Instruction and adds any new label to the table
    """
    
    def __init__(self):
        self.table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                      "SCREEN": 16384, "KBD": 24576}
        for i in range(16):
            self.table["R"+str(i)] = str(i)
        self.line_no = 0

    def add_label(self, inst):
        """
        Looks for an L-Instruction and adds any new label to the table.

        Parameters
        ----------
        inst : str
            The instruction in which we want to find a symbol
        """

        self.instruction = strip_line(inst)
        if len(self.instruction) < 1:
            return

        self.line_no += 1
        if self.instruction[0] == "(":
            if self.instruction[-1] != ")":
                raise BracketError()
            symbol = self.instruction[1:-1]
            if symbol in self.table:
                raise DuplicateLabelError()
            if len(symbol.split()) > 1:
                raise BadLabelError()
            self.table[symbol] = self.line_no
            self.line_no -= 1
