from .asmexceptions import DestinationError, ComputationError, JumpError 

class Encoder():
    def __init__(self):
        self.table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                      "SCREEN": 16384, "KBD": 24576}
        for i in range(16):
            self.table["R"+str(i)] = str(i)

    def code(self, inst):
        if inst[0] == "A":
            bits = bin(int(inst[1])).replace("0b", "")
            return "0" * (16 - len(bits)) + bits
        if inst[0] == "C":
            if inst[1] not in _dest:
                raise DestinationError(inst[4], inst[5], inst[1])
            if inst[2] not in _comp:
                raise ComputationError(inst[4], inst[5], inst[2])
            if inst[3] not in _jump:
                raise JumpError(inst[4], inst[5], inst[3])
            return "111" + _comp[inst[2]] + _dest[inst[1]] + _jump[inst[3]]

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
