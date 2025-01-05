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

def input(fn):
    with open(fn) as file:
        lines = file.readlines()
        grid = [x.strip() for x in lines]
        print('w=', len(grid[0]), 'h=', len(grid))
        return grid

x_exit, y_exit = 21, 22

def print_map(m, path=[]):
    for (x, y) in path:
        m
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

# import resource
# print('recursion limit=', sys.getrecursionlimit())
# resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
# sys.setrecursionlimit(2000)
# print('recursion limit=', sys.getrecursionlimit())

# m = input(sys.argv[1])
# print(part1(x_exit-2, y_exit-2, m))
# print(part1(1, 0, m))

# Solution fails due to maximum recursion depth reached on MacOS. Python on MacOS cannot do setrlimit.
# a) move to different env, e.g., Linux and try there
# b) remove some recursions, e.g., when only possible to move in single direction

# _ = (x, y)
DOWN = (0, 1)
UP = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = [DOWN, UP, LEFT, RIGHT]

shortcut = {}
x_start, y_start = 1, 0

# REVERSE = {DOWN: UP, UP: DOWN, LEFT: RIGHT, RIGHT: LEFT}
# def reverse(d):
#     return REVERSE[d]

def reverse(d):
    return -d[0], -d[1]

assert reverse(UP) == DOWN
assert reverse(LEFT) == RIGHT


# direction .. up, down, left, right
# x, y is an intersection
# returns x, y, steps
def next_intersection(x, y, direction, m):

    # print('next_intersection', x, y, direction)
    x_end, y_end = len(m[0])-2, len(m)-1
    assert direction in DIRECTIONS

    if (x, y, direction) in shortcut:
        return shortcut[x, y, direction]

    xprev, yprev = x, y
    x2, y2 = x+direction[0], y+direction[1]

    assert m[y2][x2] != '#'

    steps = 1

    while True:
        xy = [(x2+d[0], y2+d[1]) for d in [UP, DOWN, LEFT, RIGHT] if is_legal(x2+d[0], y2+d[1], m) and not (x2+d[0]==xprev and y2+d[1]==yprev)]
        # xy.remove((xprev, yprev))
        # print(xy)
        if len(xy) > 1:
            break
        elif len(xy) == 1:
            xprev, yprev = x2, y2
            x2, y2 = xy[0][0], xy[0][1]
            steps += 1
            if (x2, y2) == (x_end, y_end):
                break
            if (x2, y2) == (x_start, y_start):
                break
        else:
            assert False

    shortcut[x,y,direction] = (x2, y2, steps, xprev, yprev)
    # shortcut[x2,y2,reverse(direction)] = (x, y, steps, x-reverse(direction)[0], y-reverse(direction)[1])
    # shortcut[x2,y2,(x2-xprev,y2-yprev)] = (x, y, steps, x-reverse(direction)[0], y-reverse(direction)[1])

    # print(x, y, direction, '-->', shortcut[x,y,direction])
    # print(x2, y2, (x2-xprev, y2-yprev), '-->', shortcut[x2,y2,(x2-xprev,y2-yprev)])

    return shortcut[x,y,direction]

# g_m = input('2023-23-test.txt')
g_m = input('2023-23-input.txt')

(x_end, y_end) = (len(g_m[0])-2, len(g_m)-1)

# assert next_intersection(x_start, y_start, DOWN, g_m) == (3, 5, 15, 3, 4)
# assert next_intersection(x_start, y_start, DOWN, g_m) == (3, 5, 15, 3, 4)
# assert next_intersection(3, 5, UP, g_m) == (x_start, y_start, 15, 1, 1)
# assert next_intersection(11, 3, DOWN, g_m) == (13, 13, 24, 13, 12)
# assert next_intersection(13, 13, UP, g_m) == (11, 3, 24, 11, 4)

def possible_moves(x, y, m):
    assert m[y][x] != '#'
    return [(x+d[0], y+d[1]) for d in [UP, DOWN, LEFT, RIGHT] if is_legal(x+d[0], y+d[1], m)]

# assert possible_moves(x_start, y_start, g_m) == [(1,1)]
# assert set(possible_moves(3, 5, g_m)) == set([(3,4),(4,5),(3,6)])
# assert set(possible_moves(13, 13, g_m)) == set([(12,13),(14,13),(13,14),(13,12)])

def part2(x, y, direction, m, depth=0):

    print('part2', depth, x, y, direction)

    if (x, y) == (x_end, y_end):
        print_map(m)
        return 0

    x1, y1, steps1, xprev, yprev = next_intersection(x, y, direction, g_m)

    if (x1, y1) == (x_end, y_end):
        print_map(m)
        return steps1

    # Already visited some intersection.
    if m[y1][x1] != '.':
        return 0

    m1 = [m[i] for i in range(len(m))]
    m1[y] = m1[y][0:x] + '&' + m1[y][x+1:]

    results = []
    for xd, yd in [UP, DOWN, LEFT, RIGHT]:
        if x1+xd < 0 or x1+xd > len(m[0])-1:
            continue
        if y1+yd < 0 or y1+yd > len(m)-1:
            continue
        if (x1+xd, y1+yd) == (xprev, yprev):
            continue
        if m1[y1+yd][x1+xd] == '#':
            continue
        results += [(x1, y1, (xd, yd), part2(x1, y1, (xd, yd), m1, depth+1))]

    results.sort(key= lambda v: v[3], reverse=True)
    print(results)

    return steps1 + results[0][3]

# print(part2(x_start, y_start, DOWN, g_m))
# print(next_intersection(13, 19, UP, g_m))

# 2025-01-02, Spent a lot of time trying to build a recursive
# solution. Ultimately, we cannot exclude any partial solution based
# on min/max at any point since the partial solution may represent
# only a local min/max and we exclude possible valid solutions this
# way.

# x ... horizontal starting position
# y ... vertical starting position
# m ... map/grid
# Returns list of (x,y) pairs representing longest path and length of longest path
def part2_2(x0, y0, m):

    candidates = [([(x0, y0)], 0)]
    solutions = []

    print_ok = False

    while len(candidates) > 0:
        path, length = candidates.pop(0)
        # print(path, length)

        (x, y) = path[-1]

        if (x, y) == (13, 19):
            print_ok = False

        for xd, yd in [UP, DOWN, LEFT, RIGHT]:

            if print_ok:
                print(xd, yd)

            if not is_legal(x+xd, y+yd, m):
                if print_ok:
                    print('illegal', x, y, xd, yd)
                continue
            x1, y1, steps, xprev, yprev = next_intersection(x, y, (xd, yd), m)

            if print_ok:
                print('abc', x, y, xd, yd, x1, y1)

            if (x1, y1) in path:
                continue

            path1 = list(path)
            path1 += [(x1,y1)]

            if print_ok:
                print('path1', path1, length + steps)

            if (x1, y1) == (x_end, y_end):
                solutions += [(path1, length + steps)]
                print(solutions[-1], '# candidates=', len(candidates))
            else:
                candidates += [(path1, length + steps)]
                # if (x1,y1) == (5, 13):
                #     print(candidates)
                #     return []

    return solutions

# print(*part2_2(x_start, y_start, g_m), sep='\n')

# graph[x,y] -> [(x,y,distance)]
graph = {}

# return [(x,y,distance)]
def neighbours(x, y, m):
    assert m[y][x] != '#'
    if (x,y) in graph:
        return graph[x,y]
    graph[x,y] = []
    for (xd, yd) in DIRECTIONS:
        if x+xd >= len(m[0]):
            continue
        if y+yd >= len(m):
            continue
        if m[y+yd][x+xd] == '#':
            continue
        x1, y1, steps, _, _ = next_intersection(x, y, (xd, yd), m)
        graph[x, y] += [(x1, y1, steps)]

    return graph[x, y]

class Test1:
    def run():
        m = input('2023-23-test.txt')
        print(neighbours(1, 0, m))
        print(neighbours(3, 5, m))
        print(neighbours(19, 19, m))
        print(neighbours(21, 22, m))

# Test1.run()

def longest_path(x, y, m, visited, path_length):

    if (x, y) == (len(m[0])-2, len(m)-1):
        return path_length

    visited[x,y] = True
    max_length = float('-inf')
    for x1, y1, steps in neighbours(x, y, m):
        if (x1, y1) in visited and visited[x1,y1] == True:
            continue
        max_length = max(max_length, longest_path(x1, y1, m, visited, path_length+steps))
    visited[x,y] = False
    return max_length

visited = {}

# print(longest_path(1, 0, input('2023-23-test.txt'), visited, 0))
print(longest_path(1, 0, input('2023-23-input.txt'), visited, 0))

# 2025-01-05
#
# After several fruitless attempts and hours spent debugging the
# solution, I realized that I was running some test code prior to the
# real problem every time. Since both the test code and the real
# problem were using the same global map to record connections in the
# graph, the map had connections from the test code which were
# obviously not correct for the real problem. Hence, while the
# algorithm might have been correct for a while, the left over state
# from the test code was leading to incorrect results. So much for
# global state ...
#
# Also, the eventual algorithm was due to ChatGPT while I had created
# the "condensed graph" based on the original input data.
