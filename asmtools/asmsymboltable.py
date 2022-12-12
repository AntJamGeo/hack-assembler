from .asmexceptions import NoAddressError, BadAddressError
from .asmtools import strip_line

class SymbolTable():
    def __init__(self):
        self.table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                      "SCREEN": 16384, "KBD": 24576}
        for i in range(16):
            self.table["R"+str(i)] = str(i)
        self.rom_no = 16
        self.line_no = 0

    def add_symbol(self, instruction):
        self.instruction = strip_line(instruction)
        if len(self.instruction) < 1:
            return

        if self.instruction[0] == "@":
            self._add_a_symbol()
        elif self.instruction[0] == "(":
            self._add_l_symbol()

    def _add_a_symbol(self):
        symbol = self.instruction[1:]
        if self._contains(symbol):
            return
        if self.instruction == "@":
            raise NoAddressError(self.total_lines, self.instruction)
        if len(self.instruction.split()) > 1:
            raise BadAddressError(self.total_lines, self.instruction, symbol) 
        self._update(symbol, self.rom_no)
        self.rom_no += 1
        

    def _add_l_symbol(self):
        pass

    def _update(self, symbol, address):
        self.table[symbol] = address

    def _contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        return self.table[symbol]
