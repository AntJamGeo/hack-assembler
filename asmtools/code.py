from .instruction import AInstruction, CInstruction
from .exceptions import RAMError

class Encoder():
    """
    Uses information from an assembly language instruction that has been
    parsed using a Parser instance to produce the corresponding machine
    language instruction.

    Attributes
    ----------
    _table : SymbolTable
        Contains all the symbols used in the .asm file with their
        corresponding addresses

    Methods
    -------
    encode(inst)
        Converts parsed instruction into machine language
    """
    
    def __init__(self, table):
        self._table = table
        self._ram_address = 16

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
        elif self._table.contains(value):
            address = self._table.get_address(value)
        else:
            if self._ram_address == 16383:
                raise RAMError(self.inst)
            address = self._ram_address
            self._table.add_entry(value, address)
            self._ram_address += 1
        bits = bin(address).replace("0b", "")
        return "0" * (16 - len(bits)) + bits

    def _c_encode(self):
        dest = self.inst.get_dest()
        comp = self.inst.get_comp()
        jump = self.inst.get_jump()
        return ("111" + CInstruction.comp[comp] + CInstruction.dest[dest] +
                CInstruction.jump[jump])

