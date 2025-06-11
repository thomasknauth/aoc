# --- Day 3: Gear Ratios ---

# You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up
# to the water source, but this is as far as he can bring you. You go inside.

# It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

# "Aaah!"

# You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I
# wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I
# can fix it." You offer to help.

# The engineer explains that an engine part seems to be missing from the engine, but nobody can
# figure out which one. If you can add up all the part numbers in the engine schematic, it should be
# easy to work out which part is missing.

# The engine schematic (your puzzle input) consists of a visual representation of the engine. There
# are lots of numbers and symbols you don't really understand, but apparently any number adjacent to
# a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do
# not count as a symbol.)

# Here is an example engine schematic:

test_input='''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''

# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114
# (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part
# number; their sum is 4361.

# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers
# in the engine schematic?

# --- Part Two ---

# The engineer finds the missing part and installs it in the engine! As the engine springs to life,
# you jump in the closest gondola, finally ready to ascend to the water source.

# You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the
# gondola has a phone labeled "help", so you pick it up and the engineer answers.

# Before you can explain the situation, she suggests that you look out the window. There stands the
# engineer, holding a phone in one hand and waving with the other. You're going so slowly that you
# haven't even left the station. You exit the gondola.

# The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any *
# symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying
# those two numbers together.

# This time, you need to find the gear ratio of every gear and add them all up so that the engineer
# can figure out which gear needs to be replaced.

# Consider the same engine schematic again:

# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..

# In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and
# 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is
# 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.)
# Adding up all of the gear ratios produces 467835.

import sys
import io

adjacent = []
for y in [-1, 0, 1]:
    for x in [-1, 0, 1]:
        if x == 0 and y == 0:
            continue
        adjacent += [(x,y)]

def is_adjacent_to_symbol(grid, x1, x2, y):

    adjacent_cells = []
    for x in range(x1, x2+1):
        adjacent_cells += [(x+xd, y+yd) for (xd, yd) in adjacent]

    for (ax, ay) in adjacent_cells:
        if grid[ay][ax] != '.' and (not grid[ay][ax].isdigit()):
            return True

    return False

def part1(f):
    # Go line by line. If found a digit, look for adjacent symbol.
    # Add extra row and column as boundary to avoid special cases later on.
    grid = list(map(lambda s: '.' + s.strip() + '.', f.readlines()))

    padded_grid = ['.'*(len(grid[0]))]
    padded_grid += grid
    padded_grid += [('.'*(len(grid[0])))]

    grid = padded_grid

    sum = 0

    for y in range(1, len(grid)-1):

        start_digit = None
        end_digit = None

        # We need x to cover the last column we added as padding to catch numbers ending on the
        # final column of the original grid. Hence, we iterate from 1 .. len(grid[0]) instead of
        # 1 .. len(grid[0])-1
        for x in range(1, len(grid[0])):
            if grid[y][x].isdigit():
                if not start_digit:
                    start_digit = x
            else:
                if start_digit:
                    end_digit = x - 1
                    # print(y, grid[y][start_digit:end_digit+1])
                    # grid[y] = grid[y][0:start_digit] + '#'*(end_digit-start_digit+1) + grid[y][end_digit+1:]
                    if is_adjacent_to_symbol(grid, start_digit, end_digit, y):
                        sum += int(grid[y][start_digit:end_digit+1])
                start_digit = None
                end_digit = None

    return sum

def part2(fn):
    # Go line by line. If found a digit, look for adjacent symbol.
    # Add extra row and column as boundary to avoid special cases later on.
    grid = list(map(lambda s: '.' + s.strip() + '.', f.readlines()))

    padded_grid = ['.'*(len(grid[0]))]
    padded_grid += grid
    padded_grid += [('.'*(len(grid[0])))]

    grid = padded_grid

    sum = 0

    for y in range(1, len(grid)-1):

        start_digit = None
        end_digit = None

        # We need x to cover the last column we added as padding to catch numbers ending on the
        # final column of the original grid. Hence, we iterate from 1 .. len(grid[0]) instead of
        # 1 .. len(grid[0])-1
        for x in range(1, len(grid[0])):
            if grid[y][x].isdigit():
                if not start_digit:
                    start_digit = x
            else:
                if start_digit:
                    end_digit = x - 1
                    # print(y, grid[y][start_digit:end_digit+1])
                    # grid[y] = grid[y][0:start_digit] + '#'*(end_digit-start_digit+1) + grid[y][end_digit+1:]
                    if is_adjacent_to_symbol(grid, start_digit, end_digit, y):
                        sum += int(grid[y][start_digit:end_digit+1])
                start_digit = None
                end_digit = None

    return sum

if __name__ == '__main__':

    fn = '2023-03-p1.txt'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    print(part1(io.StringIO(test_input)))
    print(part1(open(fn)))
