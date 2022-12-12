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
    def __init__(self, line, inst):
        super().__init__(line, inst, "No address given.")

class BadAddressError(AInstructionError):
    def __init__(self, line, inst, invalid_address):
        super().__init__(line, inst, f"Invalid address: '{invalid_address}'.")

# C-Instruction Errors
class CInstructionError(InstructionError):
    def __init__(self, line, inst, c_type, invalid_field):
        super().__init__(line, inst, "c-",
                         f"Invalid {c_type}: '{invalid_field}'.")

class DestinationError(CInstructionError):
    def __init__(self, line, inst, dest):
        super().__init__(line, inst, "destination", dest) 

class ComputationError(CInstructionError):
    def __init__(self, line, inst, comp):
        super().__init__(line, inst, "computation", comp) 

class JumpError(CInstructionError):
    def __init__(self, line, inst, jump):
        super().__init__(line, inst, "jump", jump)
