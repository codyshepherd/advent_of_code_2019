'''
Advent of Code 2019
Cody Shepherd

Day 7, Parts 1 & 2

Part 1 Solution:

This was just a matter of making copies of main memory and repeating
computation in sequence. I passed input and output between "amplifiers" in
a klunky way, which ended up biting me in Part 2.

Part 2 Solution:

Achieving this so that it could run freely required a major overhaul from Part
1. This exercise was a great argument for why I should have gone back over
this Intcode computer after the last exercise and made it more modular and
self contained. I'm getting pretty far into the weeds here with this VM
abstraction that I'm just evolving frantically as I try to do the next
exercise that requires it.

Maybe I'll take some time over the weekend to refactor it into a more sensible
form. Right now it works, but it is far from elegant and difficult to debug.
'''

import itertools
import queue

from typing import (
    List,
    Optional,
    Tuple,
)

INPUT_FILE = 'input_7.txt'

DEBUG = False

class Amplifier(object):

    def __init__(self,
                 name,
                 memory,
                 next_amp,
                 ):
        self.name = name
        self.memory = memory
        self.modified = False
        self.ip = 0
        self.input_buffer = queue.Queue()
        self.output_buffer = queue.Queue()
        self.next_amp = next_amp
        self.running = False
        self.get_input_failed = False

    def add_input(self, val: str):
        self.input_buffer.put(val)

    def add_output(self, val: str):
        self.output_buffer.put(val)

    def empty_input(self) -> bool:
        if self.input_buffer.empty():
            return True
        return False

    def get_input(self) -> str:
        return self.input_buffer.get(block=True, timeout=None)

    def get_output(self) -> str:
        return self.output_buffer.get()

    def set_ip(self, address: int):
        self.ip = address

    def set_memory(self, address: int, val: str):
        self.memory[address] = val

    def set_modified(self, val: bool):
        self.modified = val

    def set_next_amp(self, amp):
        self.next_amp = amp

    def set_running(self, val: bool):
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

OPS = {
    1: lambda x, y: add(x, y),
    2: lambda x, y: mult(x, y),
    3: lambda x, y: _in(x, y),
    4: lambda x, y: out(x, y),
    5: lambda x, y: jnz(x, y),
    6: lambda x, y: jz(x, y),
    7: lambda x, y: lt(x, y),
    8: lambda x, y: eq(x, y),
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

def add(inst: Instruction, amp: Amplifier) -> None:
    val_a, val_b = get_correct_values(inst, amp)
    amp.set_memory(inst.params[2], str(val_a + val_b))

def decode(amp: Amplifier) -> Instruction:
    IP = amp.ip
    opcode = amp.memory[IP]
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
        params.append(int(amp.memory[IP+i]))

    return Instruction(op, params, modes_list, jump)

def eq(inst: Instruction, amp: Amplifier) -> None:
    val_a, val_b = get_correct_values(inst, amp)
    address = inst.params[2]

    if val_a == val_b:
        amp.set_memory(address, '1')
    else:
        amp.set_memory(address, '0')

def get_correct_values(inst: Instruction, amp: Amplifier) -> Tuple[int, Optional[int]]:
    val_a = inst.params[0] if inst.modes[0] == 1 else int(amp.memory[inst.params[0]])
    if len(inst.params) > 1:
        val_b = inst.params[1] if inst.modes[1] == 1 else int(amp.memory[inst.params[1]])
    else:
        val_b = None
    return val_a, val_b

def _in(inst: Instruction, amp: Amplifier) -> None:
    if amp.empty_input():
        amp.get_input_failed = True
        return
    inp = amp.get_input()
    if DEBUG:
        print(f"input: {inp}")

    address = inst.params[0]

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
    address = inst.params[2]

    if val_a < val_b:
        amp.set_memory(address, '1')
    else:
        amp.set_memory(address, '0')

def mult(inst: Instruction, amp: Amplifier) -> None:
    val_a, val_b = get_correct_values(inst, amp)
    amp.set_memory(inst.params[2], str(val_a * val_b))

def out(inst: Instruction, amp: Amplifier) -> None:
    output, _ = get_correct_values(inst, amp)
    amp.next_amp.add_input(str(output))
    if DEBUG:
        print(f'output: {output}')
        print(f'output inst jump: {inst.jump}')

def run_program(amp: Amplifier) -> None:
    amp.set_running(True)
    inst = decode(amp)
    while inst.op != 99:
        if DEBUG:
            print(f"amp name: {amp.name}")
            print(f"inst op: {inst.op}")
            print(f"params: {inst.params}")
            print(f"modes: {inst.modes}")
            print(f"IP: {amp.ip}")
            print("Input buf: ", list(amp.input_buffer.queue))
            print("Output buf: ", list(amp.output_buffer.queue))
            print(' '.join([amp.memory[i] if amp.ip != i else '['+amp.memory[i]+']' for i in range(len(amp.memory))]))
            input()
        func = OPS[inst.op]
        func(inst, amp)
        if amp.get_input_failed:
            amp.get_input_failed = False
            return
        jump = inst.jump

        if amp.modified:
            amp.set_modified(False)
        else:
            amp.set_ip(amp.ip + jump)

        inst = decode(amp)

    amp.set_running(False)
    if amp.name == 'E':
        if DEBUG:
            print("E Final Output: ", amp.output_buffer.queue)
    if DEBUG:
        print('run program finished')


if __name__ == '__main__':
    with open(INPUT_FILE, 'r') as fh:
        raw = fh.read()

    MASTER_MEMORY= raw[:-1].split(',')

    amp_names = ["A", "B", "C", "D", "E"]

    combos = list(itertools.permutations(range(5, 10)))

    largest_output = 0
    best_sequence = ''

    for combo in combos:
        amps = []
        old_amp = None
        for i, a_n in enumerate(amp_names):
            new_amp = Amplifier(a_n, MASTER_MEMORY.copy(), None)
            new_amp.add_input(str(combo[i]))
            amps.append(new_amp)
            if old_amp is not None:
                old_amp.set_next_amp(new_amp)
            old_amp = new_amp
        amp_A = amps[0]
        amp_E = amps[-1]
        amp_E.set_next_amp(amp_A)


        amp_A.add_input('0')
        running = True
        i = -1
        while running:
            if i == len(amps) -1:
                i = 0
            else:
                i += 1
            amp = amps[i]
            run_program(amp)
            running = any([x.running for x in amps])
        outp = amp_A.get_input()
        if int(outp) > int(largest_output):
            largest_output = outp
            best_sequence = ','.join(map(lambda x: str(x),  combo))

    print(f"Largest output: {largest_output}")
    print(f"Best sequence: {best_sequence}")
    print("Finished!")
