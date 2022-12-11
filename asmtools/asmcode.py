def code(instruction):
    if instruction[0] == "A":
        bits = bin(int(instruction[1])).replace("0b", "")
        return "0" * (16 - len(bits)) + bits
    if instruction[0] == "C":
        return "111" + dest(instruction[1]) + comp(instruction[2]) + jump(instruction[3])

def dest(mnemonic):
    return ""

def comp(mnemonic):
    return ""

def jump(mnemonic):
    return ""
