# --- Day 11: Cosmic Expansion ---

# You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf
# within turns out to be a researcher studying cosmic expansion using the giant telescope here.

# He doesn't know anything about the missing machine parts; he's only visiting for this research
# project. However, he confirms that the hot springs are the next-closest area likely to have
# people; he'll even take you straight there once he's done with today's observation analysis.

# Maybe you can help him with the analysis to speed things up?

# The researcher has collected a bunch of data and compiled the data into a single giant image (your
# puzzle input). The image includes empty space (.) and galaxies (#). For example:

test_input='''\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''

# The researcher is trying to figure out the sum of the lengths of the shortest path between every
# pair of galaxies. However, there's a catch: the universe expanded in the time it took the light
# from those galaxies to reach the observatory.

# Due to something involving gravitational effects, only some space expands. In fact, the result is
# that any rows or columns that contain no galaxies should all actually be twice as big.

# In the above example, three columns and two rows contain no galaxies:

#    v  v  v
#  ...#......
#  .......#..
#  #.........
# >..........<
#  ......#...
#  .#........
#  .........#
# >..........<
#  .......#..
#  #...#.....
#    ^  ^  ^

# These rows and columns need to be twice as big; the result of cosmic expansion therefore looks
# like this:

# ....#........
# .........#...
# #............
# .............
# .............
# ........#....
# .#...........
# ............#
# .............
# .............
# .........#...
# #....#.......

# Equipped with this expanded universe, the shortest path between every pair of galaxies can be
# found. It can help to assign every galaxy a unique number:

# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# ............6
# .............
# .............
# .........7...
# 8....9.......

# In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't
# matter. For each pair, find any shortest path between the two galaxies using only steps that move
# up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is
# allowed to pass through another galaxy.)

# For example, here is one of the shortest paths between galaxies 5 and 9:

# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# .##.........6
# ..##.........
# ...##........
# ....##...7...
# 8....9.......

# This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9
# (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example
# shortest path lengths:

# Between galaxy 1 and galaxy 7: 15
# Between galaxy 3 and galaxy 6: 17
# Between galaxy 8 and galaxy 9: 5

# In this example, after expanding the universe, the sum of the shortest path between all 36 pairs
# of galaxies is 374.

# Expand the universe, then find the length of the shortest path between every pair of
# galaxies. What is the sum of these lengths?

from aoc_2023_10 import Grid
import io
import itertools
import sys

def parse_input(f):

    lines = list(map(lambda s: s.strip(), f.readlines()))

    # grid = Grid(lines)

    # print('x', 'y', grid.x_dim(), grid.y_dim())
    return lines

def expand_grid(lines):

    lines2 = []
    # Expand horizontal
    for line in lines:
        lines2.append(line)
        if not '#' in line:
            lines2.append(line)

    # print('0---')
    # print(Grid(lines2))

    lines = lines2
    lines2 = list(lines)
    empty_columns = []
    shift = 0
    for x in range(len(lines[0])):
        if not '#' in [lines[y][x] for y in range(len(lines))]:
            for (y, line) in enumerate(lines2):
                lines2[y] = lines2[y][0:x+shift] + '.' + lines2[y][x+shift:]
            shift += 1

    return Grid(lines2)

def part1(f):

    grid = parse_input(f)

    grid = expand_grid(grid)

    galaxies = [(x, y) for (x, y) in itertools.product(range(grid.x_dim()), range(grid.y_dim())) if grid[x, y] == '#']
    pairs = itertools.combinations(galaxies, 2)

    return sum([abs(x1-x2)+abs(y1-y2) for ((x1, y1), (x2, y2)) in pairs])

# Obviously, we cannot construct an actual in-memory representation of the expanded
# universe. Instead, we take the initial (x, y) position of each galaxy and add expansions to each
# dimension. The number of expansions depends on the initial position.
def part2(f):

    input = parse_input(f)
    grid = Grid(input)

    galaxies = [(x, y) for (x, y) in itertools.product(range(grid.x_dim()), range(grid.y_dim())) if grid[x, y] == '#']
    empty_rows = [y for y in range(grid.y_dim()) if all([grid[x, y] != '#' for x in range(grid.x_dim())])]
    empty_cols = [x for x in range(grid.x_dim()) if all([grid[x, y] != '#' for y in range(grid.y_dim())])]

    factor = 10**6-1

    for (nr_expansion, empty_row) in enumerate(empty_rows):
        galaxies = list(map(lambda t: t if t[1] <= (empty_row + factor * nr_expansion) else (t[0], t[1]+factor), galaxies))

    for (nr_expansion, empty_col) in enumerate(empty_cols):
        galaxies = list(map(lambda t: t if t[0] <= (empty_col + factor * nr_expansion) else (t[0]+factor, t[1]), galaxies))

    pairs = itertools.combinations(galaxies, 2)

    return sum([abs(x1-x2)+abs(y1-y2) for ((x1, y1), (x2, y2)) in pairs])

if __name__ == '__main__':

    fn = '2023-11-p1.txt'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    print('test part1=', part1(io.StringIO(test_input)))
    print('part1=', part1(open(fn)))
    print('test part2=', part2(io.StringIO(test_input)))
    print('part2=', part2(open(fn)))
