'''
Advent of Code 2019
Cody Shepherd

Day 3, Parts 1 & 2

Part 1 Solution:

Generate the coordinates that comprise each wire path, do set intersection,
and compare rectilinear distances to find the closest.

Part 2 Solution:

Because the way we generated coordinates in part 1 was sequential or path-like,
we can simply go through each coordinate in the set intersection and follow
the wire path while counting. Sum this figure for each wire for each relevant
coordinate, and we can find the closest one.
'''

from typing import (
    Generator,
    List,
    Tuple,
)

INPUT_FILE = 'input_3.txt'

dirs = {
    'R': lambda x, y: [(x[0]+i, x[1]) for i in range(1, y+1)],
    'L': lambda x, y: [(x[0]-i, x[1]) for i in range(1, y+1)],
    'U': lambda x, y: [(x[0], x[1]+i) for i in range(1, y+1)],
    'D': lambda x, y: [(x[0], x[1]-i) for i in range(1, y+1)],
}

def all_coords(pairs: List[Tuple[str, int]]) -> List[Tuple[int, int]]:

    coords: List[Tuple[int, int]] = []
    last_coord = (0, 0)
    for pair in pairs:
        direction = pair[0]
        distance = pair[1]
        coords += dirs[direction](last_coord, distance)
        last_coord = coords[-1]
    
    return coords

def separate(lst: List[str]) -> Generator[Tuple[str, int], None, None]:

    for item in lst:
        s = item[0]
        i = int(item[1:])
        yield (s, i)

def closest_intersection(string1: str, string2: str) -> int:

    list1 = string1.split(',')
    list2 = string2.split(',')

    t_list1 = [(s, i) for (s, i) in separate(list1)]
    t_list2 = [(s, i) for (s, i) in separate(list2)]

    set1 = set(all_coords(t_list1))
    set2 = set(all_coords(t_list2))

    intersection = set1.intersection(set2)

    min_dist = -1
    closest_coord = (0, 0)
    for item in intersection:
        rect_dist = abs(item[0]) + abs(item[1])
        if min_dist < 0 or rect_dist < min_dist:
            min_dist = rect_dist
            closest_coord = item

    print(closest_coord, ': ', min_dist)
    return min_dist

def how_far(coord: Tuple[int, int], path: List[Tuple[int, int]]) -> int:

    dist = 0
    for item in path:
        dist += 1
        if item == coord:
            break

    return dist

def least_steps_intersection(string1: str, string2: str) -> int:

    list1 = string1.split(',')
    list2 = string2.split(',')

    t_list1 = [(s, int(i)) for (s, i) in separate(list1)]
    t_list2 = [(s, int(i)) for (s, i) in separate(list2)]

    coords1 = all_coords(t_list1)
    coords2 = all_coords(t_list2)

    intersection = set(coords1).intersection(set(coords2))

    min_dist = -1
    best_coord = (0, 0)
    for item in intersection:
        traveled_dist = how_far(item, coords1) + how_far(item, coords2)
        if traveled_dist < min_dist or min_dist < 0:
            min_dist = traveled_dist
            best_coord = item

    print(f'best coord: {best_coord} - ', min_dist)
    return min_dist

if __name__ == '__main__':
    raw_1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    raw_2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    raw_1a = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    raw_2a = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

    assert(closest_intersection(raw_1, raw_2) == 159)
    assert(closest_intersection(raw_1a, raw_2a) == 135)

    print("Assertions passed. ✔️")

    with open(INPUT_FILE, 'r') as fh:
        raw = fh.read()

    lists = raw.split('\n')[:-1]
    
    part_1_answer = closest_intersection(lists[0], lists[1])
    assert(part_1_answer == 2193)

    assert(least_steps_intersection(raw_1, raw_2) == 610)
    assert(least_steps_intersection(raw_1a, raw_2a) == 410)
    part_2_answer = least_steps_intersection(lists[0], lists[1])
    print(f'Part 2 answer: {part_2_answer}')
