
import click
import fractions

from typing import (
    List,
    Tuple,
)

DEBUG = False
DEBUG2 = False

def coord_diffs(base: Tuple[int, int], dist: Tuple[int,int]) -> Tuple[int, int]:
    return (dist[0]-base[0], dist[1]-base[1])

def frac(x: int, y: int) -> Tuple[int, int]:
    if y != 0 and x != 0:
        f = fractions.Fraction(x, y)
        xfrac = f.numerator if y>= 0 else f.numerator*-1
        yfrac = f.denominator if y>= 0 else f.denominator*-1
    else:
        xfrac = x
        yfrac = y

    return (xfrac, yfrac)


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

def print_map(coord: Tuple[int, int], original: List[Tuple[int, int]], remaining: List[Tuple[int, int]], height: int, width: int) -> str:
    string = ''
    i = 0
    for h in range(height):
        for w in range(width):
            if (w, h) == coord:
                string += 'X'
            elif (w, h) in original and (w,h) in remaining:
                string += '#'
            elif (w,h) in original:
                string += '*'
            else:
                string += '.'

        string += '\n'

    return string

def order_of_vaporization(best_coord: Tuple[int, int], coords: List[Tuple[int, int]], height: int, width: int) -> List[Tuple[int, int]]:
    sequence = []
    landmarks = [1,2,3,10,20,50,100,199,200,201,299]
    counter = 0
    master_x = best_coord[0]
    master_y = best_coord[1]

    range_up = 0 - master_y
    range_right = width - master_x - 1
    range_down = height - master_y - 1
    range_left = 0 - master_x
    if DEBUG2:
        print(f'master x: {master_x}\nmaster y: {master_y}')
        print(f'range_up: {range_up}\nrange_right: {range_right}\nrange_down: {range_down}\nrange_left: {range_left}')

    beam_path = [(master_x,y) for y in range(master_x+1, -1, -1)]
    step_x, step_y = (0, range_up)
    quadrant = 'u'
    steps = []
    xmult = 1
    ymult = -1
    if DEBUG2:
        print(f"steps:\n{steps}")
    remaining_asteroids = coords
    while len(remaining_asteroids) > 0:
        if DEBUG2:
            print(f'beam path:\n{beam_path}')
        for coord in beam_path:
            if coord in remaining_asteroids:
                counter += 1
                if DEBUG2:
                    print(f'Hit #{counter}: {coord}')
                sequence.append(coord)
                remaining_asteroids = list(filter(lambda x: x != coord, remaining_asteroids))
                print(f"Remaining asteroids: {len(remaining_asteroids)}")
                break

        key = lambda t: fractions.Fraction(t[1], t[0])
        if len(steps) == 0:
            if DEBUG2:
                print("Changing quadrant")
            if quadrant == 'u':
                quadrant = 'tr'
                steps = sorted(set([frac(x,y) for x in range(1, range_right+1) for y in range(range_up, 0)]), key=key)
            elif quadrant == 'tr':
                quadrant = 'r'
                steps = []
                beam_path = [(x,master_y) for x in range(master_x+1, master_x+range_right+1)]
                continue
            elif quadrant == 'r':
                quadrant = 'br'
                steps = sorted(set([frac(x,y) for x in range(range_right, 0, -1) for y in range(1, range_down+1)]), key=key)
            elif quadrant == 'br':
                quadrant = 'd'
                steps = []
                beam_path = [(master_x,y) for y in range(master_y+1, master_y+range_down+1)]
                continue
            elif quadrant == 'd':
                quadrant = 'bl'
                steps = sorted(set([frac(x,y) for x in range(-1, range_left-1, -1) for y in range(range_down, 0, -1)]), key=key)
            elif quadrant == 'bl':
                quadrant = 'l'
                steps = []
                beam_path = [(x, master_y) for x in range(master_x-1, master_x+range_left-1, -1)]
                continue
            elif quadrant == 'l':
                quadrant = 'tl'
                steps = sorted(set([frac(x,y) for x in range(range_left, 0) for y in range(-1, range_up-1, -1)]), key=key)
            elif quadrant == 'tl':
                quadrant = 'u'
                steps = []
                beam_path = [(master_x,y) for y in range(master_y-1, master_y+range_up-1, -1)]
                continue

        if DEBUG2:
            print(f"current steps: {steps}")

        step_x, step_y = steps[0]
        del steps[0] 

        beam_path = []
        shot_x = master_x + step_x
        shot_y = master_y + step_y
        if DEBUG2:
            print(f"New step: ({step_x},{step_y})")
        while 0 <= shot_x <= width and 0 <= shot_y <= height:
            if DEBUG2:
                print(f"shot x: {shot_x}, shot y: {shot_y}")
            beam_path.append((shot_x, shot_y))
            shot_x += step_x
            shot_y += step_y

        if DEBUG2:
            if len(sequence) in landmarks:
                del landmarks[0]
                print(print_map(best_coord, coords, remaining_asteroids, height, width))
                input()

    return sequence


@click.command()
@click.option('-m', '--map-file', type=click.Path(exists=True, dir_okay=False),
              default='input_10.txt', help='Point at a map file to run')
@click.option('--debug/--no-debug', default=False,
              help='Show debugging messages')
@click.option('--debug-2/--no-debug-2', default=False,
              help='Show debugging messages')
def main(map_file, debug, debug_2):
    if debug:
        global DEBUG
        DEBUG = True

    if debug_2:
        global DEBUG2
        DEBUG2 = True

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
    print('Part 1 output')
    print(f'best coord: {best_coord}')
    print(f'most_visible: {most_visible}')

    filtered_coords = [x for x in coords if x != best_coord]

    asteroid_sequence = order_of_vaporization(best_coord, filtered_coords, height, width)
    print(f'200th: {asteroid_sequence[199]}')
    print('Finished!')

if __name__ == '__main__':
    main()
