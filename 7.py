import itertools
import queue

from typing import (
    List,
    Optional,
    Tuple,
)

INPUT_FILE = 'input_7.txt'

INPUT_BUFFER = queue.Queue()
OUTPUT_BUFFER = queue.Queue() 

DEBUG = False
IP = 0
MEMORY: List[str] = []
MODIFIED = False

class Instruction(object):

    def __init__(self,
                 op: int,
                 params: List[int],
                 modes: List[int],
                 jump: int,
                ):
        self.op = op
        self.params = params
        self.modes = modes
        self.jump = jump

OPS = {
    1: lambda x: add(x),
    2: lambda x: mult(x),
    3: lambda x: _in(x),
    4: lambda x: out(x),
    5: lambda x: jnz(x),
    6: lambda x: jz(x),
    7: lambda x: lt(x),
    8: lambda x: eq(x),
}

PARAMS = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
}

def add(inst: Instruction) -> None:
    global MEMORY
    val_a, val_b = get_correct_values(inst)
    MEMORY[inst.params[2]] = str(val_a + val_b)

def decode() -> Instruction:
    opcode = MEMORY[IP]
    op = int(opcode[-2:])

    if op == 99:
        return Instruction(op, [], [], 0)

    modes = opcode[:-2]
    modes_list = list(reversed([int(x) for x in modes]))

    jump = PARAMS[op] + 1

    diff = PARAMS[op] - len(modes)
    for i in range(diff):
        modes_list.append(0)

    params: List[int] = []
    for i in range(1, jump):
        params.append(int(MEMORY[IP+i]))

    return Instruction(op, params, modes_list, jump)

def eq(inst: Instruction) -> None:
    global MEMORY

    val_a, val_b = get_correct_values(inst)
    address = inst.params[2]

    if val_a == val_b:
        MEMORY[address] = '1'
    else:
        MEMORY[address] = '0'

def get_correct_values(inst: Instruction) -> Tuple[int, Optional[int]]:
    val_a = inst.params[0] if inst.modes[0] == 1 else int(MEMORY[inst.params[0]])
    if len(inst.params) > 1:
        val_b = inst.params[1] if inst.modes[1] == 1 else int(MEMORY[inst.params[1]])
    else:
        val_b = None
    return val_a, val_b

def _in(inst: Instruction) -> None:
    global MEMORY
    global INPUT_BUFFER
    inp = INPUT_BUFFER.get(block=True, timeout=None)
    if DEBUG:
        print(f"input: {inp}")

    address = inst.params[0]

    MEMORY[address] = inp

def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def jnz(inst: Instruction) -> None:
    global IP
    global MODIFIED

    val_a, address = get_correct_values(inst)

    if val_a != 0:
        IP = address
        MODIFIED = True

def jz(inst: Instruction) -> None:
    global IP
    global MODIFIED

    val_a, address = get_correct_values(inst)

    if val_a == 0:
        IP = address
        MODIFIED = True

def lt(inst: Instruction) -> None:
    global MEMORY

    val_a, val_b = get_correct_values(inst)
    address = inst.params[2]

    if val_a < val_b:
        MEMORY[address] = '1'
    else:
        MEMORY[address] = '0'

def mult(inst: Instruction) -> None:
    global MEMORY
    val_a, val_b = get_correct_values(inst)
    MEMORY[inst.params[2]] = str(val_a * val_b)

def out(inst: Instruction) -> None:
    global OUTPUT_BUFFER
    output, _ = get_correct_values(inst)
    OUTPUT_BUFFER.put(str(output))
    if DEBUG:
        print(f'output: {output}')
        print(f'output inst jump: {inst.jump}')

def run_program() -> None:
    global IP
    global MODIFIED

    inst = decode()
    while inst.op != 99:
        if DEBUG:
            print(f"inst op: {inst.op}")
            print(f"params: {inst.params}")
            print(f"modes: {inst.modes}")
            print(f"IP: {IP}")
            print("Input buf: ", list(INPUT_BUFFER.queue))
            print("Output buf: ", list(OUTPUT_BUFFER.queue))
            print(' '.join([MEMORY[i] if IP != i else '['+MEMORY[i]+']' for i in range(len(MEMORY))]))
            input()
        func = OPS[inst.op]
        func(inst)
        jump = inst.jump

        if MODIFIED:
            MODIFIED = False
        else:
            IP += jump

        inst = decode()

    if DEBUG:
        print('run program finished')


if __name__ == '__main__':
    with open(INPUT_FILE, 'r') as fh:
        raw = fh.read()

    MASTER_MEMORY= raw[:-1].split(',')

    amplifiers = ["A", "B", "C", "D", "E"]
    combos = list(itertools.permutations(range(5)))
    largest_output = 0
    best_sequence = ''
    for combo in combos:
        outp = "0"
        for i, amp in enumerate(amplifiers):
            phase = combo[i]
            INPUT_BUFFER.put(str(phase))
            INPUT_BUFFER.put(outp)
            if DEBUG:
                print(f"phase: {phase}")
                print(f"amp: {amp}")
            MEMORY = MASTER_MEMORY.copy()
            IP = 0
            run_program()
            outp = OUTPUT_BUFFER.get()
        if int(outp) > int(largest_output):
            largest_output = outp
            best_sequence = ','.join(map(lambda x: str(x),  combo))

    print(f"Largest output: {largest_output}")
    print(f"Best sequence: {best_sequence}")
    print("Finished!")
