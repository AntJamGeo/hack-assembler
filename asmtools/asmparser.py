from .asmexceptions import InstructionError, NoAddressError, BadAddressError
from .asmtools import strip_line

class Parser():
    """
    Loads an instruction using the parse function to determine the
    important information in a line of assembly code, which can then be
    passed on to the Encoder class for encoding into machine language.

    Attributes
    ----------
    inst_no : int
        count of valid instructions processed
    line_no : int
        count of lines processed
    instruction : str
        current instruction being processed

    Methods
    -------
    parse(instruction)
        Determine which type of instruction is being given and return
        information in a suitable format to be read by an Encoder instance
    """

    def __init__(self):
        self.inst_no = 0
        self.line_no = 0

    def parse(self, instruction):
        """
        Determine which type of instruction is being given and return
        information in a suitable format to be read by an Encoder instance.

        Parameters
        ----------
        instruction : str
            The instruction to be parsed

        Returns
        -------
        tuple
            Useful information to be encoded by an Encoder instance

        Raises
        ------
        InstructionError
            An invalid instruction has been passed and cannot be parsed
        """

        self.instruction = strip_line(instruction)
        self.line_no += 1
        if len(self.instruction) < 1: # ignore whitespace
            return False
        elif self.instruction[0] == "@": # A-Instruction
            self.inst_no += 1
            return self._a_inst()
        elif self.instruction[0] == "(": # L-Instruction
            return False
        elif self.instruction[0] in {"A", "D", "M", "0", "1", "-", "!"}: # C-Instruction
            self.inst_no += 1
            return self._c_inst()
        raise InstructionError(self.line_no, self.instruction)


    def _a_inst(self):
        """Parse A-Instructions."""
        if self.instruction == "@":
            raise NoAddressError(self.total_lines, self.instruction)
        if len(self.instruction.split()) > 1:
            raise BadAddressError(self.total_lines, self.instruction, symbol) 
        return ("A", self.instruction[1:])

    def _l_inst(self):
        """Parse L-Instructions."""
        return ""

    def _c_inst(self):
        """Parse C-Instructions."""

        # Find first '=' and split into dest and comp;jump parts
        if self.instruction[-1] == "=": # no final '=' simplifies later calculation
            raise InstructionError(self.line_no, self.instruction)
        equals_index = self.instruction.find("=")
        if equals_index == -1:
            dest, compjump = None, self.instruction
        else:
            dest = self.instruction[:equals_index]
            compjump = self.instruction[equals_index+1:] # no final '=' so this is allowed

        # Find first ';' and split into comp and jump parts
        semi_colon_index = compjump.find(";")
        if semi_colon_index == -1:
            comp, jump = compjump, None 
        else:
            comp = compjump[:semi_colon_index]
            jump = compjump[semi_colon_index+1:]

        return ("C", dest, comp, jump, self.line_no, self.instruction) 

