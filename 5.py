'''
Advent of Code 2019
Cody Shepherd

Day 5, Parts 1 & 2

Part 1 Solution:

Essentially we have a virtual machine which maniuplates state, using global
state and a global instruction pointer.

I found it easiest to use a class to provide an abstraction for the instruction
which lets us give names to its parts instead of using numeric indices
everywhere.

I also used strings for the base memory "word" type because string manipulation
is both easier (due to slicing) and faster (because of big ints) in Python.
This involved a bit more casting than I'd have liked, but then I'm not
claiming the program is optimal.
'''

from typing import List

INPUT_FILE = 'input_5.txt'

IP = 0
MEMORY: List[str] = []

class Instruction(object):

    def __init__(self,
                 op: int,
                 params: List[int],
                 modes: List[int],
                ):
        self.op = op
        self.params = params
        self.modes = modes

OPS = {
    1: lambda x: add(x),
    2: lambda x: mult(x),
    3: lambda x: _in(x),
    4: lambda x: out(x),
}

PARAMS = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
}

def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def add(inst: Instruction) -> None:
    global MEMORY
    val_a = inst.params[0] if inst.modes[0] == 1 else int(MEMORY[inst.params[0]])
    val_b = inst.params[1] if inst.modes[1] == 1 else int(MEMORY[inst.params[1]])
    MEMORY[inst.params[2]] = str(val_a + val_b)

def mult(inst: Instruction) -> None:
    global MEMORY
    val_a = int(inst.params[0]) if inst.modes[0] == 1 else int(MEMORY[inst.params[0]])
    val_b = int(inst.params[1]) if inst.modes[1] == 1 else int(MEMORY[inst.params[1]])
    MEMORY[inst.params[2]] = str(val_a * val_b)

def _in(inst: Instruction) -> None:
    global MEMORY
    inp = ''
    while not is_int(inp):
        inp = input("> ")

    address = inst.params[0]

    MEMORY[address] = inp

def out(inst: Instruction) -> None:
    output = MEMORY[inst.params[0]]
    print(f'output: {output}')

def decode() -> Instruction:
    global IP
    opcode = MEMORY[IP]
    op = int(opcode[-2:])

    if op == 99:
        return Instruction(op, [], [])

    modes = opcode[:-2]
    modes_list = list(reversed([int(x) for x in modes]))

    jump = PARAMS[op] + 1

    diff = PARAMS[op] - len(modes)
    for i in range(diff):
        modes_list.append(0)

    params: List[int] = []
    for i in range(1, jump):
        params.append(int(MEMORY[IP+i]))
    IP += jump

    return Instruction(op, params, modes_list)

def run_program() -> None:
    inst = decode()
    while inst.op != 99:
        func = OPS[inst.op]
        func(inst)
        inst = decode()


if __name__ == '__main__':
    with open(INPUT_FILE, 'r') as fh:
        raw = fh.read()

    MEMORY= raw.split(',')[:-1]

    run_program()
    print("Finished!")
