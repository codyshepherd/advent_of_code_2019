'''
Advent of Code 2019
Cody Shepherd

Day 6, Parts 1 & 2

Part 1 Solution:

This was pretty easy -- just construct a digraph, count the path from each
node to COM.

Part 2 Solution:

This is a simple BFS problem, which requires an undirected graph. DFS would be
fine here as well, since we have no danger of loops or infinite branches, but
I wanted to use something different than recursion (though ofc that wouldn't be
strictly necessary).
'''

import collections
import queue

from typing import(
    Dict,
    List,
)

INPUT_FILE = 'input_6.txt'

GRAPH = None
O_I_EDGES = None

def all_edges(key: str) -> int:
    num = 1
    next_planet = O_I_EDGES[key]
    while next_planet != 'COM':
        num += 1
        next_planet = O_I_EDGES[next_planet]

    return num

def bfs(yours: str, santas: str) -> int:
    xfers = 0
    q = queue.Queue()
    visited = {
        yours: True
    }
    yr_edges = GRAPH[yours]
    for edge in yr_edges:
        q.put((edge, xfers+1))

    while not q.empty():
        next_p, xfers = q.get()
        if next_p == santas:
            return xfers
        visited[next_p] = True
        edges_p = GRAPH[next_p]
        for edge in edges_p:
            if visited.get(edge, None) is None:
                q.put((edge, xfers+1))
    return -1

    
def map_graph(raw_list: List[str]) -> Dict[str, List[str]]:
    edges = collections.defaultdict(list)
    for item in raw_list:
        planets = item.split(')')
        inner = planets[0]
        outer = planets[1]
        edges[inner].append(outer)
        edges[outer].append(inner)
    return edges

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

    GRAPH = map_graph(raw_list)

    yours = O_I_EDGES['YOU']
    santas = O_I_EDGES['SAN']
    xfers = bfs(yours, santas)
    print(f'xfers: {xfers}')
