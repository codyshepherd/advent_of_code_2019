
import click
import fractions

from typing import (
    List,
    Tuple,
)

DEBUG = False

def coord_diffs(base: Tuple[int, int], dist: Tuple[int,int]) -> Tuple[int, int]:
    return (dist[0]-base[0], dist[1]-base[1])

def coord_frac(base: Tuple[int, int], dist: Tuple[int, int]) -> Tuple[int, int]:
    xdiff, ydiff = coord_diffs(base, dist)
    if ydiff != 0 and xdiff != 0:
        f = fractions.Fraction(xdiff, ydiff)
        xfrac = f.numerator if ydiff >= 0 else f.numerator*-1
        yfrac = f.denominator if ydiff >= 0 else f.denominator*-1
    else:
        xfrac = xdiff
        yfrac = ydiff

    return (xfrac, yfrac)

def count_visible(candidate: Tuple[int, int], coords: List[Tuple[int, int]], height: int, width: int) -> int:
    visible = 0
    x = candidate[0]
    y = candidate[1]

    for coord in coords:
        if coord == candidate:
            continue
        cx = coord[0]
        cy = coord[1]

        xdiff, ydiff = coord_diffs(candidate, coord)
        xfrac, yfrac = coord_frac(candidate, coord)

        if not is_occluded(candidate, coord, [x for x in coords if (x != candidate and x != coord)], (xdiff, ydiff), (xfrac, yfrac), height, width):
            visible += 1

    return visible

def is_occluded(base: Tuple[int, int], dist: Tuple[int, int], coords: List[Tuple[int, int]], diffs: Tuple[int, int], fracs: Tuple[int, int], height: int, width: int) -> bool:
    if DEBUG:
        print(f'Checking occlusion between {base} and {dist}')
        print(f'diffs: {diffs}')
        print(f'fracs: {fracs}')

    xmult = 1 if diffs[0] >= 0 else -1
    ymult = 1 if diffs[1] >=0 else -1
    x = base[0]
    y = base[1]
    while x >= 0 and x < width and y >= 0 and y < height:
        x += fracs[0] if diffs[1] != 0 else 1*xmult
        y += fracs[1] if diffs[0] != 0 else 1*ymult
        if DEBUG:
            print(f"step: ({x}, {y})")
        if (x, y) == dist:
            if DEBUG:
                print('no')
            return False
        if (x, y) in coords:
            if DEBUG:
                print('yes')
            return True

    raise Exception('Fell off the map without finding any coords!')

def same_sign(a: int, b: int) -> bool:
    if a <= 0 and b <= 0:
        return True
    elif a >= 0 and b >= 0:
        return True
    return False

def print_visible(visible: List[int], lines: List[str]) -> str:
    string = ''
    i = 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                string += str(visible[i])
                i += 1
            else:
                if any([x > 9 for x in visible]):
                    string += ' .'
                else:
                    string += '.'
        string += '\n'

    return string


@click.command()
@click.option('-m', '--map-file', type=click.Path(exists=True, dir_okay=False),
              default='input_10.txt', help='Point at a map file to run')
@click.option('--debug/--no-debug', default=False,
              help='Show debugging messages')
def main(map_file, debug):
    if debug:
        global DEBUG
        DEBUG = True

    with open(map_file, 'r') as fh:
        raw = fh.read()

    lines = raw.split('\n')[:-1]

    height = len(lines)
    width = len(lines[0])
    coords = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                coords.append((x,y))

    if DEBUG:
        print(coords)

    visible = [0 for i in range(len(coords))]
    most_visible = 0
    best_coord = None
    for i in range(len(coords)):
        candidate = coords[i]
        num_vis = count_visible(candidate, coords, height, width)
        visible[i] = num_vis
        if num_vis > most_visible:
            most_visible = num_vis
            best_coord = candidate


    if DEBUG:
        print(print_visible(visible, lines))
    print(f'best coord: {best_coord}')
    print(f'most_visible: {most_visible}')
    print('Finished!')

if __name__ == '__main__':
    main()
