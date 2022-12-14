import sys

import asmtools

if __name__ == "__main__":
    in_file_path = sys.argv[1]
    out_file_path = sys.argv[1][:-3] + "hack"
    s = asmtools.SymbolTable(in_file_path)
    p = asmtools.Parser()
    e = asmtools.Encoder(s)
    with open(in_file_path, 'r') as in_file, \
         open(out_file_path, 'w') as out_file:
        for line in in_file:
            instruction = p.parse(line)
            if instruction:
                bits = e.encode(instruction)
                out_file.write(bits + "\n")
