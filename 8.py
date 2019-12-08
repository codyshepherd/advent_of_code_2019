'''
Advent of Code 2019
Cody Shepherd

Day 8, Parts 1 & 2

These solutions just involved creation and manipulation of nested lists, which
is easy to do in python.
'''

import click

from typing import (
    List
)
DEBUG = False
WIDE = 25
TALL = 6

BLACK = 0
WHITE = 1
TRANSPARENT = 2


def find_densest_layer(layers: List[List[List[int]]]) -> List[List[int]]:
    lowest_zeros = sum([len(row) for row in layers[0]]) # num pixels per layer
    densest_layer = []

    for layer in layers:
        if DEBUG:
            print(f'layer:\n{layer}')
        zeros = sum([row.count(0) for row in layer])
        if zeros < lowest_zeros:
            lowest_zeros = zeros
            densest_layer = layer

    return densest_layer


def layers(raw: str, wide: int, tall: int) -> List[List[List[int]]]:
    pixels_per_layer = wide * tall
    num_layers = len(raw) // pixels_per_layer
    all_layers = []

    raw_index = 0
    for layer in range(num_layers):
        layer = []
        for row in range(tall):
            layer_row = []
            for col in range(wide):
                pixel = int(raw[raw_index])
                layer_row.append(pixel)
                raw_index += 1
            layer.append(layer_row)
        all_layers.append(layer)

    return all_layers

def convert(i: int) -> str:
    if i == BLACK:
        return '   '
    if i == WHITE:
        return '[=]'
    if i == TRANSPARENT:
        return ' '


def show(layer: List[List[int]]) -> str:
    string = ''
    for r, row in enumerate(layer):
        string += ''.join(list(map(lambda i: convert(i), row))) + '\n'

    return string

def stack_layers(layers: List[List[List[int]]], wide: int, tall: int) -> List[List[int]]:
    final_layer = [[TRANSPARENT for c in range(wide)] for r in range(tall)]

    for layer in layers:
        for r in range(tall):
            for c in range(wide):
                if layer[r][c] != TRANSPARENT and final_layer[r][c] == TRANSPARENT:
                    final_layer[r][c] = layer[r][c]

    return final_layer


@click.command()
@click.option('-p', '--program', type=click.Path(exists=True, dir_okay=False),
              default='input_8.txt', help='Point at a program file to run')
@click.option('--debug/--no-debug', default=False,
              help='Show debugging messages')
@click.option('-w', '--wide', type=int, default=WIDE,
              help='The number of pixels wide for each layer')
@click.option('-t', '--tall', type=int, default=TALL,
              help='The number of pixels tall for each layer')
def main(program, debug, wide, tall):
    if debug:
        global DEBUG
        DEBUG = True

    with open(program, 'r') as fh:
        raw = fh.read()[:-1]

    if DEBUG:
        print(f"raw: {raw}")

    layers_list = layers(raw, wide, tall)
    if DEBUG:
        print(layers_list)

    densest = find_densest_layer(layers_list)
    ones = sum([row.count(1) for row in densest])
    twos = sum([row.count(2) for row in densest])
    solution = ones*twos

    if DEBUG:
        print(f'densest layer:\n{densest}')
        print(f'layers list:\n{layers_list}')

    print(f"Part 1 Solution: {solution}")
    final_layer = stack_layers(layers_list, wide, tall)
    if DEBUG:
        print(f"final layer: {final_layer}")
    print(show(final_layer))
    print("Finished!")

if __name__ == '__main__':
    main()
