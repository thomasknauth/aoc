import io
import sys


def parse_input(f):

    return [x.strip() for x in f.readlines()]


def transpose(grid):
    """ """
    new_grid = []
    for col in range(len(grid[0])):
        new_grid.append("".join([grid[i][col] for i in range(len(grid))]))
    return new_grid


def rotate_90_clockwise(g):
    g = transpose(g)
    for i in range(len(g)):
        # s[::-1] is Python's cryptic way of reversing a string.
        g[i] = g[i][::-1]
    return g


def slide_rocks(grid):

    for y in range(1, len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O" and grid[y - 1][x] == ".":
                # How far does the rock slide?
                y_target = y - 1
                while y_target >= 0:
                    if grid[y_target][x] != ".":
                        y_target += 1
                        break
                    y_target -= 1
                # Cannot slide past row 0.
                if y_target < 0:
                    y_target = 0

                grid[y_target] = grid[y_target][:x] + "O" + grid[y_target][x + 1 :]
                grid[y] = grid[y][:x] + "." + grid[y][x + 1 :]

    return grid


def score(g):
    acc = 0
    for row in range(len(g)):
        acc += g[row].count("O") * (len(g) - row)
    return acc


def part1(f):

    grid = parse_input(f)
    grid = slide_rocks(grid)
    return score(grid)


def part2(f):
    """ """
    g = parse_input(f)
    states = {}
    i = 1
    while True:
        for _ in range(4):
            g = slide_rocks(g)
            g = rotate_90_clockwise(g)

        # Hash g to make it suitable for indexing the dict/map.
        h = hash(tuple(g))

        if h in states:
            pre_cycle_steps = states[h][0]
            cycle_len = i - pre_cycle_steps
            # It took a while until I realized I had to add the pre-cycle steps to the cycle index to arrive at the correct index when looking up the final state.
            final_state = (
                1_000_000_000 - pre_cycle_steps
            ) % cycle_len + pre_cycle_steps
            return [v[1] for (k, v) in states.items() if v[0] == final_state][0]
        else:
            states[h] = (i, score(g))
        i += 1
    assert False, "unreachable"


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    test_file = sys.argv[0].replace(".py", "-test.txt")

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    print("test part1=", part1(open(test_file)))
    print("part1=", part1(open(input_file)))
    print("test part2=", part2(open(test_file)))
    print("part2=", part2(open(input_file)))
