import click
import itertools
import queue

from typing import (
    List,
    Optional,
    Tuple,
)

DEBUG = False

class Amplifier(object):

    def __init__(self,
                 name: str,
                 program: List[str],
                 next_amp,
                 ):
        self.name = name
        self.memory = ['0' for x in range(1000000)]
        for i, string in enumerate(program):
            self.memory[i] = program[i]
        self.modified = False
        self.ip = 0
        self.input_buffer = queue.Queue()
        self.output_buffer = queue.Queue()
        self.next_amp: Amplifier = next_amp
        self.running = False
        self.waiting_on_input = False
        self.relative_base = 0

    def adjust_relative_base(self, val: int) -> None:
        self.relative_base += val

    def display_memory(self) -> str:
        range_num = 1000 if DEBUG else len(sef.memory)
        return(' '.join([self.memory[i] if self.ip != i else '['+self.memory[i]+']' for i in range(range_num)]))

    def add_input(self, val: str) -> None:
        self.input_buffer.put(val)

    def empty_input(self) -> bool:
        if self.input_buffer.empty():
            return True
        return False

    def get_input(self) -> str:
        return self.input_buffer.get(block=True, timeout=None)

    def set_ip(self, address: int) -> None:
        self.ip = address

    def set_memory(self, address: int, val: str) -> None:
        self.memory[address] = val

    def set_modified(self, val: bool) -> None:
        self.modified = val

    def set_next_amp(self, amp) -> None:
        self.next_amp = amp

    def set_running(self, val: bool) -> None:
        self.running = val

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

OP_INFO = {
    1: {
        "FUNC": lambda x, y: add(x, y),    
        "PARAMS": 3,
        "NAME": "ADD",
    },
    2: {
        "FUNC": lambda x, y: mult(x, y),
        "PARAMS": 3,
        "NAME": "MULTIPLY",
    },
    3: {
        "FUNC": lambda x, y: _in(x, y),    
        "PARAMS": 1,
        "NAME": "INPUT",
    },
    4: {
        "FUNC": lambda x, y: out(x, y),    
        "PARAMS": 1,
        "NAME": "OUTPUT",
    },
    5: {
        "FUNC": lambda x, y: jnz(x, y),    
        "PARAMS": 2,
        "NAME": "JNZ",
    },
    6: {
        "FUNC": lambda x, y: jz(x, y),    
        "PARAMS": 2,
        "NAME": "JZ",
    },
    7: {
        "FUNC": lambda x, y: lt(x, y),    
        "PARAMS": 3,
        "NAME": "LT",
    },
    8: {
        "FUNC": lambda x, y: eq(x, y),    
        "PARAMS": 3,
        "NAME": "EQ",
    },
    8: {
        "FUNC": lambda x, y: eq(x, y),    
        "PARAMS": 3,
        "NAME": "EQ",
    },
    9: {
        "FUNC": lambda x, y: arb(x, y),    
        "PARAMS": 1,
        "NAME": "ARB",
    },
}

def add(inst: Instruction, amp: Amplifier) -> None:
    val_a, val_b = get_correct_values(inst, amp)
    address = inst.params[2] if inst.modes[2] != 2 else inst.params[2]+amp.relative_base
    amp.set_memory(address, str(val_a + val_b))

def arb(inst: Instruction, amp: Amplifier) -> None:
    val_a, _ = get_correct_values(inst, amp)
    amp.adjust_relative_base(val_a)

def decode(amp: Amplifier) -> Instruction:
    IP = amp.ip
    opcode = amp.memory[IP]
    op = int(opcode[-2:])

    if op == 99:
        return Instruction(op, [], [], 0)

    modes = opcode[:-2]
    modes_list = list(reversed([int(x) for x in modes]))

    jump = OP_INFO[op]["PARAMS"] + 1

    diff = OP_INFO[op]["PARAMS"] - len(modes)
    for i in range(diff):
        modes_list.append(0)

    params: List[int] = []
    for i in range(1, jump):
        params.append(int(amp.memory[IP+i]))

    return Instruction(op, params, modes_list, jump)

def eq(inst: Instruction, amp: Amplifier) -> None:
    val_a, val_b = get_correct_values(inst, amp)
    # address = inst.params[2]
    address = inst.params[2] if inst.modes[2] != 2 else inst.params[2]+amp.relative_base

    if val_a == val_b:
        amp.set_memory(address, '1')
    else:
        amp.set_memory(address, '0')

def get_correct_values(inst: Instruction, amp: Amplifier) -> Tuple[int, Optional[int]]:
    if inst.modes[0] == 0:
        val_a = int(amp.memory[inst.params[0]])
    elif inst.modes[0] == 1:
        val_a = inst.params[0]
    else:
        val_a = int(amp.memory[inst.params[0] + amp.relative_base])

    if len(inst.params) > 1:
        if inst.modes[1] == 0:
            val_b = int(amp.memory[inst.params[1]])
        elif inst.modes[1] == 1:
            val_b = inst.params[1]
        else:
            val_b = int(amp.memory[inst.params[1] + amp.relative_base])
    else:
        val_b = None
    return val_a, val_b

def _in(inst: Instruction, amp: Amplifier) -> None:
    if amp.empty_input():
        amp.waiting_on_input = True
        return
    inp = amp.get_input()

    address = inst.params[0] if inst.modes[0] != 2 else inst.params[0] + amp.relative_base

    amp.set_memory(address, inp)

def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def jnz(inst: Instruction, amp: Amplifier) -> None:
    val_a, address = get_correct_values(inst, amp)

    if val_a != 0:
        amp.set_ip(address)
        amp.set_modified(True)

def jz(inst: Instruction, amp: Amplifier) -> None:
    val_a, address = get_correct_values(inst, amp)

    if val_a == 0:
        amp.set_ip(address)
        amp.set_modified(True)

def lt(inst: Instruction, amp: Amplifier) -> None:
    val_a, val_b = get_correct_values(inst, amp)
    # address = inst.params[2]
    address = inst.params[2] if inst.modes[2] != 2 else inst.params[2]+amp.relative_base

    if val_a < val_b:
        amp.set_memory(address, '1')
    else:
        amp.set_memory(address, '0')

def mult(inst: Instruction, amp: Amplifier) -> None:
    val_a, val_b = get_correct_values(inst, amp)
    address = inst.params[2] if inst.modes[2] != 2 else inst.params[2]+amp.relative_base
    amp.set_memory(address, str(val_a * val_b))

def out(inst: Instruction, amp: Amplifier) -> None:
    output, _ = get_correct_values(inst, amp)
    # amp.next_amp.add_input(str(output))
    amp.output_buffer.put(str(output))

def run_program(amp: Amplifier) -> None:
    amp.set_running(True)
    inst = decode(amp)
    while inst.op != 99:

        if DEBUG:
            opname = OP_INFO[inst.op]["NAME"]
            print(f"=== {amp.name} ===")
            print(f"inst op: {inst.op} -- {opname}")
            print(f"params: {inst.params}")
            print(f"modes: {inst.modes}")
            print(f"IP: {amp.ip}")
            print(f"Word at IP: {amp.memory[amp.ip]}")
            print(f"Rel Base: {amp.relative_base}")
            region = [amp.memory[i] if amp.relative_base != i else '['+amp.memory[i]+']' for i in range(amp.relative_base-10, amp.relative_base+10)]
            print(f"RB Region: {region}")
            print("Input buf: ", list(amp.input_buffer.queue))
            print("Output buf: ", list(amp.output_buffer.queue))
            print(amp.display_memory())
            input()

        func = OP_INFO[inst.op]["FUNC"]
        func(inst, amp)

        if amp.waiting_on_input:
            amp.waiting_on_input = False
            return

        jump = inst.jump

        if amp.modified:
            amp.set_modified(False)
        else:
            amp.set_ip(amp.ip + jump)

        inst = decode(amp)

    amp.set_running(False)

    if DEBUG:
        print('run program finished')


@click.command()
@click.option('-p', '--program', type=click.Path(exists=True, dir_okay=False),
              default='input_7.txt', help='Point at a program file to run')
@click.option('--debug/--no-debug', default=False,
              help='Show debugging messages')
def main(program, debug):
    if debug:
        global DEBUG
        DEBUG = True

    with open(program, 'r') as fh:
        raw = fh.read()

    instructions = raw[:-1].split(',')

    computer = Amplifier("BOOST", instructions.copy(), None)
    computer.add_input('1')
    run_program(computer)
    print("Part 1 Output: ", ', '.join(computer.output_buffer.queue))

    new_comp = Amplifier("COMPLETE", instructions.copy(), None)
    new_comp.add_input('2')
    run_program(new_comp)
    print("Part 2 Output: ", ', '.join(new_comp.output_buffer.queue))

    print("Finished!")

if __name__ == '__main__':
    main()
