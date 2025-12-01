import io
import sys


def parse_input(f):

    return [line.strip() for line in f.readlines()]


def part1(f) -> int:

    # grid[y][x] - first index is y, second index is x dimension.
    grid = parse_input(f)

    # Track x, y and direction (xd, yd) to detect cycles.
    visited = set() # [(x, y, xd, yd)]

    # Start "off grid", i.e., x=-1, to correctly determine what needs to happen on first square.
    pos = [(-1, 0, 1, 0)]

    while len(pos) > 0:
        (x, y, xd, yd) = pos.pop()
        x += xd
        y += yd
        if x < 0 or x >= len(grid[0]):
            continue
        if y < 0 or y >= len(grid):
            continue
        if (x, y, xd, yd) in visited:
            continue
        visited.add((x, y, xd, yd))
        match grid[y][x]:
            case ".":
                pos.append((x, y, xd, yd))
            case "-":
                if yd == 0:
                    pos.append((x, y, xd, yd))
                else:
                    pos.append((x, y,  1, 0))
                    pos.append((x, y, -1, 0))
            case "|":
                if xd == 0:
                    pos.append((x, y, xd, yd))
                else:
                    pos.append((x, y, 0,  1))
                    pos.append((x, y, 0, -1))
            case "/":
                if xd:
                    yd = -xd
                    xd = 0
                else:
                    xd = -yd
                    yd = 0
                pos.append((x, y, xd, yd))
            case "\\":
                if xd:
                    yd = xd
                    xd = 0
                else:
                    xd = yd
                    yd = 0
                pos.append((x, y, xd, yd))            
            case _:
                assert False, "illegal state/input"

    # for (x, y, _, _) in visited:
    #     grid[y] = grid[y][:x] + "#" + grid[y][x+1:]

    # for line in grid:
    #     print(line)

    return len(set([(x, y) for (x, y, _, _) in visited]))


def part2(f) -> int:

    input = parse_input(f)

    return -1


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    test_file = sys.argv[0].replace(".py", "-test.txt")

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    print("test part1=", part1(open(test_file)))
    print("part1=", part1(open(input_file)))
    # print("test part2=", part2(open(test_file)))
    # print("part2=", part2(open(input_file)))
