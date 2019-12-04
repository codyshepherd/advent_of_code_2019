'''
Advent of Code 2019
Cody Shepherd

Day 4, Parts 1 & 2

Part 1 & 2 Solutions:

I went for a counting algorithm which checks each possible numeral for the
required conditions.

This choice necessitates more casting back and forth than is probably
necessary; I could probably have masked bits or modded by powers of ten to
compare numerals without casting to strings and back, but fie.

Ultimately the solution is about brute-force scanning of strings, which is
tedious to write and tedious to read, so I'm not sure that I achieved my goal
of "brief, readable code" here.
'''

MIN = 234208
MAX = 765869

def is_ascending(s: str) -> bool:

    i = 0
    for i in range(len(s)):
        if i == len(s) -1:
            return True

        if int(s[i] > s[i+1]):
            return False

def count_adjacent(s: str, c: str, i: int) -> int:
    count = 1
    for i in range(i+1, len(s)):
        if s[i] != c:
            break
        else:
            count += 1

    return count

def has_adjacent(s: str) -> bool:

    i = 0
    for i in range(len(s)):
        if i == len(s)-1:
            return False
        
        if s[i] == s[i+1]:
            return True

def has_adjacent_2(s: str) -> bool:

    provisional = False
    i = 0
    while i <  len(s):
        if i < len(s)-1 and s[i] == s[i+1]:
            if count_adjacent(s, s[i], i) == 2:
                provisional = True
                i += 1
            else:
                c = s[i]
                while i < len(s)-1 and s[i+1] == c:
                    i += 1
        i += 1

    return provisional

def num_possible(start: int, end: int) -> int:

    count = 0
    for i in range(start, end+1):
        s = str(i)
        ascending = is_ascending(s)
        adjacent = has_adjacent(s)
        if ascending and adjacent:
            count += 1

    return count

def num_possible_2(start: int, end: int) -> int:

    count = 0
    for i in range(start, end+1):
        s = str(i)
        ascending = is_ascending(s)
        adjacent = has_adjacent_2(s)
        if ascending and adjacent:
            count += 1

    return count


assert(has_adjacent('111111'))
assert(is_ascending('111111'))

assert(has_adjacent('223450'))
assert(not is_ascending('223450'))

assert(not has_adjacent('123789'))
assert(is_ascending('123789'))

print(num_possible(MIN, MAX))

assert(has_adjacent_2('112233'))
assert(not has_adjacent_2('123444'))
assert(has_adjacent_2('111122'))

print(num_possible_2(MIN, MAX))
