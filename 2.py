from typing import List

INPUT_FILE = 'input_2.txt'

OPS = {
    1: lambda x, y: x+y,
    2: lambda x, y: x*y,
}


def run_program(vector: List[int]) -> List[int]:
    indices = [0, 1, 2, 3]
    opcode = vector[indices[0]]
    while opcode != 99:
        op = OPS[opcode]
        operand_a_target = vector[indices[1]]
        operand_b_target = vector[indices[2]]
        result_target = vector[indices[3]]
        vector[result_target] = op(vector[operand_a_target],
                                   vector[operand_b_target])
        indices = list(map(lambda x: x+4, indices))
        opcode = vector[indices[0]]

    return vector


if __name__ == '__main__':
    assert(run_program([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])[0] == 3500)
    assert(run_program([1, 0, 0, 0, 99])[0] == 2)
    assert(run_program([2, 3, 0, 3, 99])[3] == 6)
    assert(run_program([2, 4, 4, 5, 99, 0])[5] == 9801)
    assert(run_program([1, 1, 1, 4, 99, 5, 6, 0, 99])[0] == 30)

    print("Assertions passed. ✔️")

    with open(INPUT_FILE, 'r') as fh:
        raw = fh.read()

    vector = raw.split('\n')[0]
    vector = [int(x) for x in vector.split(',')]
    part_1_vector = vector.copy()
    part_1_vector[1] = 12
    part_1_vector[2] = 2

    answer = run_program(part_1_vector)[0]
    print(f'Part 1: {answer}')

    pairs = [(x, y) for x in range(0, 100) for y in range(0, 100)]
    pair_ind = 0
    result = -1
    while result != 19690720:
        pair = pairs[pair_ind]
        pair_ind += 1
        new_vec = vector.copy()
        new_vec[1] = pair[0]
        new_vec[2] = pair[1]
        result = run_program(new_vec)[0]

    noun = pair[0]
    verb = pair[1]
    p2_answer = 100 * noun + verb
    print(f'Part 2: {p2_answer}')
