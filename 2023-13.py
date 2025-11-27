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

    # def __init__(self):
    #     pass

    def solve(self, grid) -> int:

        # Scan rows.
        i = 1

        while i < len(grid):
            up, down = i-1, i
            while up >= 0 and down < len(grid):
                # rows are identical
                if grid[up] != grid[down]:
                    break
                up -= 1
                down += 1
            if up < 0 or down >= len(grid):
                return i
            i+=1

        return None

def transpose(grid):
    """
    """
    new_grid = []
    for col in range(len(grid[0])):
        new_grid.append(''.join([grid[i][col] for i in range(len(grid))]))
    return new_grid

def test_solver():

    solver = Solver()
    for i1, i2, o in read_tests():
        s = solver.solver(i1, i2)
        assert s == o, f"solutions({i1}, {i2}), expected: {o}, actual: {s}"

def part1(f):

    inputs = parse_input(f)
    solver = Solver()
    acc = 0
    for input in inputs:
        r1 = solver.solve(input)
        if r1:
            acc += r1 * 100

        r2 = solver.solve(transpose(input))
        if r2:
            acc += r2
        assert r1 or r2
    return acc

def part2(f):
    return 0

def read_tests():
    testcases = []
    # for line in open("2023-13-test.txt").readlines():
    #     i1, i2, o = line.split()
    #     i2 = list(map(int, i2.split(",")))
    #     o = int(o)
    #     testcases.append((i1, i2, o))
    return testcases

if __name__ == "__main__":

    fn = "2023-13-input.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    print("test part1=", part1(open('2023-13-test.txt')))
    print("part1=", part1(open(fn)))
    # print("test part2=", part2(open('2023-13-test.txt')))
    # print("part2=", part2(open(fn)))
