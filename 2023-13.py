import io
import sys


def parse_input(f):

    inputs = []
    one_input = []
    for line in f.readlines():
        line = line.strip()
        if line == "":
            inputs.append(one_input)
            one_input = []
        else:
            one_input.append(line)

    if len(one_input) > 0:
        inputs.append(one_input)

    return inputs


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

    inputs = parse_input(f)
    solver = Solver()
    acc = 0
    for input in inputs:
        # Check rows for horizontal reflection.
        r1 = solver.solve(input)
        if r1:
            acc += r1 * 100

        # Check columns for vertical reflection.
        r2 = solver.solve(transpose(input))
        if r2:
            acc += r2
        assert r1 or r2
    return acc


def part2(f):
    """For Part 2, instead of checking for equality between rows, sum up the number of differing
    symbols between rows. Do this for all possible "reflection lines". There must be a row or column
    where only one symbol is different, i.e., the sum of differences is 1.

    """
    inputs = parse_input(f)
    solver = Solver()
    acc = 0
    for input in inputs:
        # Check rows for horizontal reflection.
        diffs = solver.solve_part2(input)
        i = [i for (i, diff) in diffs if diff == 1]
        if i:
            acc += i[0] * 100

        # Check columns for vertical reflection.
        diffs = solver.solve_part2(transpose(input))
        i = [i for (i, diff) in diffs if diff == 1]
        if i:
            acc += i[0]
    return acc


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    print("test part1=", part1(open("2023-13-test.txt")))
    print("part1=", part1(open(input_file)))
    print("test part2=", part2(open("2023-13-test.txt")))
    print("part2=", part2(open(input_file)))
