from .instruction import AInstruction, CInstruction
from .funcs import strip_line
from .exceptions import InstructionError

class Parser():
    """
    Loads an instruction using the parse function to determine the
    important information in a line of assembly code, which can then be
    passed on to the Encoder class for encoding into machine language.

    Attributes
    ----------
    line : int
        count of lines processed
    inst : str
        current instruction being processed

    Methods
    -------
    parse(inst)
        Determine which type of instruction is being given and return
        information in a suitable format to be read by an Encoder instance
    """

    def __init__(self):
        self.line = 0

    def parse(self, inst):
        """
        Determine which type of instruction is being given and return
        information in a suitable format to be read by an Encoder instance.

        Parameters
        ----------
        inst : str
            The instruction to be parsed

        Returns
        -------
        Instruction
            Useful information to be encoded by an Encoder instance

        Raises
        ------
        InstructionError
            An invalid instruction has been passed and cannot be parsed
        """

        self.inst = strip_line(inst)
        self.line += 1
        if len(self.inst) < 1: # ignore whitespace
            return False
        elif self.inst[0] == "@": # A-Instruction
            return self._a_inst()
        elif self.inst[0] == "(": # L-Instruction
            return False
        elif self.inst[0] in {"A", "D", "M", "0", "1", "-", "!"}: # C-Instruction
            return self._c_inst()
        raise InstructionError(self.line, self.inst)


    def _a_inst(self):
        """Parse A-Instructions."""
        return AInstruction(self.line, self.inst, self.inst[1:])

    def _l_inst(self):
        """Parse L-Instructions."""
        return ""

    def _c_inst(self):
        """Parse C-Instructions."""

        # Find first '=' and split into dest and comp;jump parts
        equals_index = self.inst.find("=")
        if equals_index == -1:
            dest, compjump = None, self.inst
        else:
            dest = self.inst[:equals_index]
            compjump = self.inst[equals_index+1:]

        # Find first ';' and split into comp and jump parts
        semi_colon_index = compjump.find(";")
        if semi_colon_index == -1:
            comp, jump = compjump, None 
        else:
            comp = compjump[:semi_colon_index]
            jump = compjump[semi_colon_index+1:]

        return CInstruction(self.line, self.inst, dest, comp, jump)
