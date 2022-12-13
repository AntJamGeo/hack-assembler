from .asminstruction import AInstruction, CInstruction
from .asmexceptions import (RAMError, DestinationError, ComputationError,
        JumpError)

class Encoder():
    """
    Uses information from an assembly language instruction that has been
    parsed using a Parser instance to produce the corresponding machine
    language instruction.

    Attributes
    ----------
    table : SymbolTable
        Contains all the symbols used in the .asm file with their
        corresponding addresses

    Methods
    -------
    encode(inst)
        Converts parsed instruction into machine language
    """
    
    def __init__(self, table):
        self.table = table
        self.ram_address = 16

    def encode(self, inst):
        """
        Converts parsed instruction into machine language.

        Parameters
        ----------
        inst : Instruction
            Parsed instruction to be encoded

        Returns
        -------
        str
            Instruction in machine language

        Raises
        ------
        DestinationError
            The destination provided in a C-Instruction is invalid
        ComputationError
            The computation provided in a C-Instruction is invalid
        JumpError
            The jump provided in a C-Instruction is invalid
        """

        self.inst = inst
        if isinstance(self.inst, AInstruction):
            return self._a_encode()
        if isinstance(self.inst, CInstruction):
            return self._c_encode()

    def _a_encode(self):
        value = self.inst.get_value()
        if self.inst.is_numeric():
            address = int(value)
        elif self.table.contains(value):
            address = self.table.get_address(value)
        else:
            if self.ram_address == 16383:
                raise RAMError(self.inst)
            address = self.ram_address
            self.table.add_entry(value, address)
            self.ram_address += 1
        bits = bin(address).replace("0b", "")
        return "0" * (16 - len(bits)) + bits

    def _c_encode(self):
        dest = self.inst.get_dest()
        comp = self.inst.get_comp()
        jump = self.inst.get_jump()
        if dest not in _dest:
            raise DestinationError(self.inst)
        if comp not in _comp:
            raise ComputationError(self.inst)
        if jump not in _jump:
            raise JumpError(self.inst)
        return "111" + _comp[comp] + _dest[dest] + _jump[jump]

_dest = {None: "000", "M": "001", "D": "010", "MD": "011", "A": "100",
         "AM": "101", "AD": "110", "AMD": "111"}

_comp = {"0": "0101010", "1": "0111111", "-1": "0111010",
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

_jump = {None: "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100",
         "JNE": "101", "JLE": "110", "JMP": "111"}
