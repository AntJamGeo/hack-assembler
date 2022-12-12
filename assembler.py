import sys
import asmtools

if __name__ == "__main__":
    file_name = sys.argv[1]
    new_file_name = sys.argv[1][:-3] + "hack"
    s = asmtools.SymbolTable()
    with open(file_name, 'r') as in_file:
        for line in in_file:
            s.add_symbol(line)
    p = asmtools.Parser()
    e = asmtools.Encoder(s)
    with open(file_name, 'r') as in_file, open(new_file_name, 'w') as out_file:
        for line in in_file:
            instruction = p.parse(line)
            if instruction:
                bits = e.encode(instruction)
                out_file.write(bits + "\n")
