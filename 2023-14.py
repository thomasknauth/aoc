import io
import sys


def parse_input(f):

    return [x.strip() for x in f.readlines()]
    # inputs = []
    # one_input = []
    # for line in f.readlines():
    #     line = line.strip()
    #     if line == "":
    #         inputs.append(one_input)
    #         one_input = []
    #     else:
    #         one_input.append(line)

    # if len(one_input) > 0:
    #     inputs.append(one_input)

    # return inputs


class Solver:

    def solve(self, grid) -> int:
        """
        Scan for horizontal reflections.
        
        To check for vertical reflections, transpose() the input.
        """

        for i in range(1, len(grid)):
            up, down = i - 1, i
            while up >= 0 and down < len(grid):
                # If rows differ, this is not a flection.
                if grid[up] != grid[down]:
                    break
                up -= 1
                down += 1
            # If either index/direction reached the end of the grid, all up/down line pairs up to
            # this point where identical, i.e., this is the solution.
            if up < 0 or down >= len(grid):
                return i

        return None

    def solve_part2(self, grid) -> list[int]:

        diffs = []

        for i in range(1, len(grid)):
            up, down = i - 1, i
            diff = 0
            while up >= 0 and down < len(grid):
                diff += sum([a != b for (a, b) in zip(grid[up], grid[down])])
                up -= 1
                down += 1
            diffs += [(i, diff)]

        return diffs


def transpose(grid):
    """ """
    new_grid = []
    for col in range(len(grid[0])):
        new_grid.append("".join([grid[i][col] for i in range(len(grid))]))
    return new_grid


def part1(f):

    # grid[y][x]
    grid = parse_input(f)

    # Slide rocks.
    for y in range(1, len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O" and grid[y-1][x] == '.':
                # How far does the rock slide?
                y_target = y-1
                while y_target >= 0:
                    if grid[y_target][x] != '.':
                        y_target += 1
                        break
                    y_target -= 1
                # Cannot slide past row 0.
                if y_target < 0:
                    y_target = 0

                grid[y_target] = grid[y_target][:x] + "O" + grid[y_target][x+1:]
                grid[  y] = grid[  y][:x] + "." + grid[  y][x+1:]

    acc = 0
    for row in range(len(grid)):
        acc += grid[row].count("O") * (len(grid)-row)
    return acc


def part2(f):
    """
    """
    inputs = parse_input(f)
    solver = Solver()
    return 0


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    test_file = sys.argv[0].replace(".py", "-test.txt")

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    print("test part1=", part1(open(test_file)))
    print("part1=", part1(open(input_file)))
    # print("test part2=", part2(open(test_file)))
    # print("part2=", part2(open(input_file)))
