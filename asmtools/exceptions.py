# Generic Instruction Error
class InstructionError(Exception):
    def __init__(self, line, inst, inst_type="", extra_info=None):
        self.line = line
        self.inst = inst
        self.inst_type = inst_type
        self.extra_info = " " + extra_info if extra_info else ""
        super().__init__(f"Bad {self.inst_type}instruction on " +
                         f"line {self.line}: '{self.inst}'.{self.extra_info}")

# L-Instruction Errors
class LInstructionError(InstructionError):
    def __init__(self, line, inst, extra_info):
        super().__init__(line, inst, "l-", extra_info)

class BracketError(LInstructionError):
    def __init__(self, line, inst):
        super().__init__(line, inst, "Brackets must wrap the whole line" +
                                     " (excluding comments).")

class DuplicateLabelError(LInstructionError):
    def __init__(self, line, inst, label):
        super().__init__(line, inst, f"Label '{label}' used multiple times.")

class BadLabelError(LInstructionError):
    def __init__(self, line, inst, label):
        super().__init__(line, inst, f"Invalid label: '{label}'.")

# A-Instruction Errors
class AInstructionError(InstructionError):
    def __init__(self, line, inst, extra_info):
        super().__init__(line, inst, "a-", extra_info)

class NoAddressError(AInstructionError):
    def __init__(self, inst):
        super().__init__(inst.get_line(), inst.get_inst(), "No address given.")

class AddressOutOfBoundsError(AInstructionError):
    def __init__(self, inst):
        super().__init__(inst.get_line(), inst.get_inst(),
                f"Address {inst.get_value()} not between 0-32767.")

class BadVariableError(AInstructionError):
    def __init__(self, inst):
        super().__init__(inst.get_line(), inst.get_inst(),
                f"Invalid variable: '{inst.get_value()}'.")

# C-Instruction Errors
class CInstructionError(InstructionError):
    def __init__(self, line, inst, c_type, invalid_field):
        super().__init__(line, inst, "c-",
                         f"Invalid {c_type}: '{invalid_field}'.")

class DestinationError(CInstructionError):
    def __init__(self, inst):
        super().__init__(inst.get_line(),
                inst.get_inst(), "destination", inst.get_dest())

class ComputationError(CInstructionError):
    def __init__(self, inst):
        super().__init__(inst.get_line(),
                inst.get_inst(), "computation", inst.get_comp())

class JumpError(CInstructionError):
    def __init__(self, inst):
        super().__init__(inst.get_line(),
                inst.get_inst(), "jump", inst.get_jump())

# Other Errors
class RAMError(InstructionError):
    def __init__(self, inst):
        super().__init__(inst.get_line(), inst.get_inst(), "",
                "RAM out of memory.")
