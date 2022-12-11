import sys
from asmparser import Parser

if __name__ == "__main__":
    file_name = sys.argv[1]
    new_file_name = sys.argv[1][:-3] + "hack"
    p = Parser()
    with open(sys.argv[1], 'r') as in_file, open(new_file_name, 'w') as out_file:
        for line in in_file:
            out_line = p.parse(line)
            if out_line:
                out_file.write(out_line)