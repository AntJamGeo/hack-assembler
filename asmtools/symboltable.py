from .exceptions import BracketError, DuplicateLabelError, BadLabelError
from .funcs import strip_line

class SymbolTable():
    """
    A store of all symbols in the .asm file and predefined symbols.

    Methods
    -------
    add_entry(symbol, address)
        Add an unseen symbol to the table
    contains(symbol)
        Check if a symbol is already in the table
    get_address(symbol)
        Get address corresponding to the given symbol
    """
    
    def __init__(self, file_path=None):
        """
        Initialise a SymbolTable.

        Parameters
        ----------
        file_path : str (optional)
            If provided, all labels in the loaded .asm file are
            added to the table.
        """
        self._table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                      "SCREEN": 16384, "KBD": 24576}
        for i in range(16):
            self._table["R"+str(i)] = i

        if file_path:
            rom_address = 0
            with open(file_path, 'r') as in_file:
                line_no = 0
                for line in in_file:
                    inst = strip_line(line)
                    line_no += 1
                    if not inst:
                        continue
                    if inst.startswith("("):
                        if not inst.endswith(")"):
                            raise BracketError(line_no, inst)
                        label = inst[1:-1]
                        if label in self._table:
                            raise DuplicateLabelError(line_no, inst, label)
                        if len(label.split()) > 1:
                            raise BadLabelError(line_no, inst, label)
                        self._table[label] = rom_address
                    else:
                        rom_address += 1

    def add_entry(self, symbol, address):
        """Add an unseen symbol to the table."""
        self._table[symbol] = address

    def contains(self, symbol):
        """Check if a symbol is already in the table."""
        return symbol in self._table

    def get_address(self, symbol):
        """Get address corresponding to the given symbol."""
        return self._table[symbol]
