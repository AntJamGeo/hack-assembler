from .exceptions import BracketError, DuplicateLabelError, BadLabelError
from .funcs import strip_line

class SymbolTable():
    """
    A store of all symbols in the .asm file and predefined symbols.

    Methods
    -------
    add_label(inst)
        Look for an L-Instruction and adds any new label to the table
    add_entry(symbol, address)
        Add an unseen symbol to the table
    contains(symbol)
        Check if a symbol is already in the table
    get_address(symbol)
        Get address corresponding to the given symbol
    """
    
    def __init__(self):
        self._table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                      "SCREEN": 16384, "KBD": 24576}
        for i in range(16):
            self._table["R"+str(i)] = i
        self._rom_address = 0
        self._line = 0

    def add_label(self, inst):
        """
        Look for an L-Instruction and adds any new label to the table.

        Parameters
        ----------
        inst : str
            The instruction in which we want to find a label
        """

        self._inst = strip_line(inst)
        self._line += 1
        if len(self._inst) < 1:
            return

        if self._inst[0] == "(":
            if self._inst[-1] != ")":
                raise BracketError(self._line, self._inst)
            label = self._inst[1:-1]
            if label in self._table:
                raise DuplicateLabelError(self._line, self._inst, label)
            if len(label.split()) > 1:
                raise BadLabelError(self._line, self._inst, label)
            self._table[label] = self._rom_address
        else:
            self._rom_address += 1

    def add_entry(self, symbol, address):
        """Add an unseen symbol to the table."""
        self._table[symbol] = address

    def contains(self, symbol):
        """Check if a symbol is already in the table."""
        return symbol in self._table

    def get_address(self, symbol):
        """Get address corresponding to the given symbol."""
        return self._table[symbol]
