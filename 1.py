'''
Advent of Code 2019
Cody Shepherd

Day 1, Parts 1 & 2
'''

import functools

from typing import List

INPUT_FILE = 'input_1.txt'    # each line is a numeric string


def fuel_required(module_mass: int):

    return (module_mass//3)-2


def naive_fuel(module_masses: List[int]):
    answers = []
    for module_mass in module_masses:
        answers.append(fuel_required(module_mass))

    return functools.reduce(lambda x, y: x+y, answers)


def complete_mass(module_masses: List[int]):
    answers = []
    for module_mass in module_masses:
        additional_fuel = recursive_fuel(module_mass)
        if additional_fuel > 0:
            answers.append(additional_fuel)

    return functools.reduce(lambda x, y: x+y, answers)


def recursive_fuel(fuel_mass: int):
    if fuel_mass <= 0:
        return 0

    n_fuel = fuel_required(fuel_mass)

    if n_fuel <= 0:
        return 0

    return n_fuel + recursive_fuel(n_fuel)


if __name__ == '__main__':

    assert(fuel_required(12) == 2)
    assert(fuel_required(14) == 2)
    assert(fuel_required(1969) == 654)
    assert(fuel_required(100756) == 33583)
    assert(recursive_fuel(14) == 2)
    assert(recursive_fuel(1969) == 966)
    assert(recursive_fuel(100756) == 50346)

    print("Assertions passed. ✔️")

    with open(INPUT_FILE, 'r') as fh:
        raw = fh.read()

    lines = raw.split('\n')
    numbers = [int(x) for x in lines if x != '']

    part_1_answer = naive_fuel(numbers)
    assert(part_1_answer == 3296269)
    print(f'Part 1: {part_1_answer}')

    part_2_answer = complete_mass(numbers)
    print(f'Part 2: {part_2_answer}')
