# --- Day 23: A Long Walk ---

# The Elves resume water filtering operations! Clean water starts
# flowing over the edge of Island Island.

# They offer to help you go over the edge of Island Island, too! Just
# hold on tight to one end of this impossibly long rope and they'll
# lower you down a safe distance from the massive waterfall you just
# created.

# As you finally reach Snow Island, you see that the water isn't
# really reaching the ground: it's being absorbed by the air
# itself. It looks like you'll finally have a little downtime while
# the moisture builds up to snow-producing levels. Snow Island is
# pretty scenic, even without any snow; why not take a walk?

# There's a map of nearby hiking trails (your puzzle input) that
# indicates paths (.), forest (#), and steep slopes (^, >, v, and <).

# For example:

# #.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#

# You're currently on the single path tile in the top row; your goal
# is to reach the single path tile in the bottom row. Because of all
# the mist from the waterfall, the slopes are probably quite icy; if
# you step onto a slope tile, your next step must be downhill (in the
# direction the arrow is pointing). To make sure you have the most
# scenic hike possible, never step onto the same tile twice. What is
# the longest hike you can take?

# In the example above, the longest hike you can take is marked with
# O, and your starting position is marked S:

# #S#####################
# #OOOOOOO#########...###
# #######O#########.#.###
# ###OOOOO#OOO>.###.#.###
# ###O#####O#O#.###.#.###
# ###OOOOO#O#O#.....#...#
# ###v###O#O#O#########.#
# ###...#O#O#OOOOOOO#...#
# #####.#O#O#######O#.###
# #.....#O#O#OOOOOOO#...#
# #.#####O#O#O#########v#
# #.#...#OOO#OOO###OOOOO#
# #.#.#v#######O###O###O#
# #...#.>.#...>OOO#O###O#
# #####v#.#.###v#O#O###O#
# #.....#...#...#O#O#OOO#
# #.#########.###O#O#O###
# #...###...#...#OOO#O###
# ###.###.#.###v#####O###
# #...#...#.#.>.>.#.>O###
# #.###.###.#.###.#.#O###
# #.....###...###...#OOO#
# #####################O#

# This hike contains 94 steps. (The other possible hikes you could
# have taken were 90, 86, 82, 82, and 74 steps long.)

# Find the longest hike you can take through the hiking trails listed
# on your map. How many steps long is the longest hike?

import csv
import re
import sys

def input():
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        grid = [x.strip() for x in lines]
        print('w=', len(grid[0]), 'h=', len(grid))
        return grid

x_exit, y_exit = 21, 22

def print_map(m):
    for line in m:
        print(line)

def is_legal(x, y, m):
    if x < 0 or x >= len(m[0]):
        return False
    if y < 0 or y >= len(m):
        return False
    if m[y][x] == '#':
        return False
    if m[y][x] in '.<>^v':
        return True
    assert False

def f(x, y, m, depth):
    # print('f', x, y, m[y][x])
    # print_map(m)
    print('f', depth)
    if x == x_exit and y == y_exit:
        return 0

    if m[y][x] == '#':
        return 0

    moves = []
    if m[y][x] == '.':
        moves += [(x+1, y), (x-1,y), (x, y+1), (x, y-1)]
    elif m[y][x] == '>':
        moves += [(x+1, y)]
    elif m[y][x] == '<':
        moves += [(x-1,y)]
    elif m[y][x] == '^':
        moves += [(x, y-1)]
    elif m[y][x] == 'v':
        moves += [(x, y+1)]

    solutions = []
    for x_next, y_next in moves:
        if is_legal(x_next, y_next, m):
            m_new = [x for x in m]
            assert m_new[y][x] != '#'
            m_new[y] = m_new[y][0:x]+'#'+m_new[y][x+1:]
            solutions.append((x_next, y_next, 1 + f(x_next, y_next, m_new, depth+1)))
    if len(solutions) > 0:
        return max([x[2] for x in solutions])
    return 0

def part1(x, y, m):
    return f(x, y, m, 0)

import resource
print('recursion limit=', sys.getrecursionlimit())
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(2000)
print('recursion limit=', sys.getrecursionlimit())

m = input()
# print(part1(x_exit-2, y_exit-2, m))
print(part1(1, 0, m))

# Solution fails due to maximum recursion depth reached on MacOS. Python on MacOS cannot do setrlimit.
# a) move to different env, e.g., Linux and try there
# b) remove some recursions, e.g., when only possible to move in single direction
