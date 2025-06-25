# --- Day 10: Pipe Maze ---

# You use the hang glider to ride the hot air from Desert Island all the way up to the floating
# metal island. This island is surprisingly cold and there definitely aren't any thermals to glide
# on, so you leave your hang glider behind.

# You wander around for a while, but you don't find any people or animals. However, you do
# occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction;
# maybe you can find someone at the hot springs and ask them where the desert-machine parts are
# made.

# The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire
# some metal grass, you notice something metallic scurry away in your peripheral vision and jump
# into a big pipe! It didn't look like any animal you've ever seen; if you want a better look,
# you'll need to get ahead of it.

# Scanning the area, you discover that the entire field you're standing on is densely packed with
# pipes; it was hard to tell at first because they're the same metallic silver color as the
# "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

# The pipes are arranged in a two-dimensional grid of tiles:

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.

# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't
# show what shape the pipe has.  Based on the acoustics of the animal's scurrying, you're confident
# the pipe that contains the animal is one large, continuous loop.

# For example, here is a square loop of pipe:

# .....
# .F-7.
# .|.|.
# .L-J.
# .....

# If the animal had entered this loop in the northwest corner, the sketch would instead look like
# this:

# .....
# .S-7.
# .|.|.
# .L-J.
# .....

# In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the
# adjacent pipes connect to it.

# Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the
# same loop as above:

# -L|F7
# 7S-7|
# L|7||
# -L-J|
# L|-JF

# In the above diagram, you can still figure out which pipes form the main loop: they're the ones
# connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe
# in the main loop connects to its two neighbors (including S, which will have exactly two pipes
# connecting to it, and which is assumed to connect back to those two pipes).

# Here is a sketch that contains a slightly more complex main loop:

# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...

# Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

# 7-F7-
# .FJ|7
# SJLL7
# |F--J
# LJ.LJ

# If you want to get out ahead of the animal, you should find the tile in the loop that is farthest
# from the starting position. Because the animal is in the pipe, it doesn't make sense to measure
# this by direct distance. Instead, you need to find the tile that would take the longest number of
# steps along the loop to reach from the starting point - regardless of which way around the loop
# the animal went.

# In the first example with the square loop:

# .....
# .S-7.
# .|.|.
# .L-J.
# .....
# You can count the distance each tile in the loop is from the starting point like this:

# .....
# .012.
# .1.3.
# .234.
# .....
# In this example, the farthest point from the start is 4 steps away.

# Here's the more complex loop again:

# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...
# Here are the distances for each tile on that loop:

# ..45.
# .236.
# 01.78
# 14567
# 23...

# Find the single giant loop starting at S. How many steps along the loop does it take to get from
# the starting position to the point farthest from the starting position?

import io
import sys

# Simple wrapper such that we can index using [x,y].
class Grid:

    def __init__(self, lines):
        self.lines = lines

    def __getitem__(self, i):
        x, y = i

        if x < 0 or y < 0:
            return 'o'
        if x >= len(self.lines[0]):
            return 'o'
        if y >= len(self.lines):
            return 'o'

        return self.lines[y][x]

    def __setitem__(self, key, value):
        x, y = key
        if x < 0 or y < 0:
            return
        if x > len(self.lines[0]) or y > len(self.lines):
            return
        self.lines[y] = self.lines[y][0:x] + value + self.lines[y][x+1:]

    def save(self, file):
        for line in self.lines:
            file.write(line+'\n')

def parse_input(f):

    lines = list(map(lambda s: s.strip(), f.readlines()))
    return Grid(lines)


def next_move(grid, x, y, x_prev, y_prev):
    '''
    Returns x,y coordinates after moving a single step.
    '''

    for xd, yd in m[grid[x,y]]:
        if (x+xd, y+yd) == (x_prev, y_prev):
            continue
        return (x+xd, y+yd)

def possible_start_moves(grid, x, y):

    assert grid[x, y] == 'S'

    moves = []
    if grid[x-1, y] in '-LF':
        moves.append((-1, 0))
    if grid[x+1, y] in '-J7':
        moves.append((1, 0))
    if grid[x, y-1] in '|F7':
        moves.append((0, -1))
    if grid[x, y+1] in '|LJ':
        moves.append((0, 1))

    return moves

m = {'|': [(0, i) for i in [1, -1]],
     '-': [(i, 0) for i in [1, -1]],
     'J': [(-1, 0), (0, -1)],
     'F': [(0, 1), (1, 0)],
     'L': [(1, 0), (0, -1)],
     '7': [(-1, 0), (0, 1)]
     }

def part1(f):

    input = parse_input(f)

    # Start position
    y0 = next(i for i, s in enumerate(input.lines) if 'S' in s)
    x0 = input.lines[y0].index('S')

    # for yd in [-1, 0, 1]:
    #     for xd in [-1, 0, 1]:
    #         print(input[x0+xd,y0+yd], end='')
    #     print('')

    xd, yd = possible_start_moves(input, x0, y0)[0]
    x1, y1 = x0+xd, y0+yd
    # print('start move', xd, yd)

    steps = 1
    while input[x1, y1] != 'S':
        x2, y2 = next_move(input, x1, y1, x0, y0)
        x0, y0 = x1, y1
        x1, y1 = x2, y2
        steps += 1

    return steps//2

def fill(grid, x, y, heading):

    xd, yd = 0, 0
    if heading == (0, -1): # up
        xd = 1
    elif heading == (0, 1): # down
        xd = -1
    elif heading == (-1, 0): # left
        yd = -1
    elif heading == (1, 0): # right
        yd = 1
    else:
        raise RuntimeError()

    while grid[x+xd, y+yd] in '.x':

        grid[x+xd, y+yd] = 'x'
        x += xd
        y += yd

def part2(f):

    input = parse_input(f)

    # Start position
    y0 = next(i for i, s in enumerate(input.lines) if 'S' in s)
    x0 = input.lines[y0].index('S')

    # print('start', x0, y0)

    xd, yd = possible_start_moves(input, x0, y0)[0]
    x1, y1 = x0+xd, y0+yd

    # print('start move', xd, yd)

    steps = 1
    outline = [(x0, y0)]
    while input[x1, y1] != 'S':
        outline.append((x1, y1))
        x2, y2 = next_move(input, x1, y1, x0, y0)
        xd, yd = x2-x1, y2-y1
        # print(xd, yd)
        x0, y0 = x1, y1
        x1, y1 = x2, y2
        steps += 1

    clean_grid = Grid(['.'*len(input.lines[0]) for _ in range(len(input.lines))])

    for (x, y) in outline:
        clean_grid[x, y] = input[x, y]

    # clean_grid.save(open('no_junk_grid.txt', 'wt'))

    # The insight is that if we always move clockwise along the perimeter, the inside will always be to the right in the direction we are moving.
    # We fill all tiles to the right of the current tile until we hit a wall or grid edge.
    # The tricky bit is that corners "have two directions", marked 1 and 2 in the below illustration.

    x0, y0 = outline[0]
    for (x1, y1) in outline[1:]:
        xd, yd = x1-x0, y1-y0
        # print('fill', x1, y1, xd, yd)
        fill(clean_grid, x1, y1, (xd, yd))
        fill(clean_grid, x0, y0, (xd, yd))
        x0, y0 = x1, y1

    # clean_grid.save(open('final_grid.txt', 'wt'))

    return sum([l.count('x') for l in clean_grid.lines])

if __name__ == '__main__':

    fn = '2023-10-p1.txt'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    # print(part1(io.StringIO(test_input)))
    print(part1(open(fn)))
    # print(part2(io.StringIO(test_input)))
    print(part2(open(fn)))
