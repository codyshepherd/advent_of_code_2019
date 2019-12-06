from typing import(
    Dict,
    List,
)

INPUT_FILE = 'input_6.txt'

O_I_EDGES = None

def all_edges(key: str) -> int:
    num = 1
    next_planet = O_I_EDGES[key]
    while next_planet != 'COM':
        num += 1
        next_planet = O_I_EDGES[next_planet]

    return num

def map_outer_to_inner(raw_list: List[str]) -> Dict[str, str]:
    edges = {}
    for item in raw_list:
        planets = item.split(')')
        inner = planets[0]
        outer = planets[1]
        edges[outer] = inner
    return edges

if __name__ == '__main__':
    with open(INPUT_FILE, 'r') as fh:
        raw = fh.read()

    raw_list = raw.split('\n')[:-1]
    O_I_EDGES = map_outer_to_inner(raw_list)
    num_edges = 0
    for k in O_I_EDGES.keys():
        num_edges += all_edges(k)

    print(f'num edges: {num_edges}')
