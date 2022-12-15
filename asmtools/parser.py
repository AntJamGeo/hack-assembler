from .instruction import AInstruction, CInstruction
from .funcs import strip_line

class Parser():
    """
    A assembly language parser.

    Loads an instruction using the parse function to determine the
    important information in a line of assembly code.

    Methods
    -------
    parse(inst)
        Parse an assembly language string.
    """

    def __init__(self):
        self._line = 0

    def parse(self, inst):
        """
        Parse an assembly language string.

        Parameters
        ----------
        inst : str
            The instruction to be parsed

        Returns
        -------
        Instruction|False
            The instruction with its important information separated. If
            whitespace or L-Instruction given, returns False.
        """
        self._inst = strip_line(inst)
        self._line += 1
        if not self._inst or self._inst.startswith("("):
            return False
        elif self._inst.startswith("@"): # A-Instruction
            return self._a_inst()
        else: # C-Instruction
            return self._c_inst()

    def _a_inst(self):
        """Parse A-Instructions."""
        return AInstruction(self._line, self._inst, self._inst[1:])

    def _c_inst(self):
        """Parse C-Instructions."""

        # Find first '=' and split into dest and comp;jump parts
        equals_index = self._inst.find("=")
        if equals_index == -1:
            dest, compjump = None, self._inst
        else:
            dest = self._inst[:equals_index]
            compjump = self._inst[equals_index+1:]

        # Find first ';' and split into comp and jump parts
        semi_colon_index = compjump.find(";")
        if semi_colon_index == -1:
            comp, jump = compjump, None 
        else:
            comp = compjump[:semi_colon_index]
            jump = compjump[semi_colon_index+1:]

        return CInstruction(self._line, self._inst, dest, comp, jump)
