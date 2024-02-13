# Hack Assembler

The Hack Assembler is used to translate programs written in the Hack assembly language into Hack binary code.

## Usage

The assembler requires a .asm file to be provided to it in order to run, and a .hack file will be produced.

To use, clone this repository and run `python3 <path to assembler.py> <path to target .asm file>`. For example, if the current working directory is the hack-assembler directory and we add
* `example.asm` to the directory, running `python3 assembler.py example.asm` will produce `example.hack` in the hack-assembler directory.

## References
* nand2tetris Website: https://www.nand2tetris.org/
* Part 1 of the Course (Hardware): https://www.coursera.org/learn/build-a-computer
* Part 2 of the Course (Software): https://www.coursera.org/learn/nand2tetris2
