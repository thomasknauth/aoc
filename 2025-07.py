import sys

def parse_input(f) -> list[bytearray]:

    # Convert string into bytearray. str is immutable while bytearray allows in-place updates.
    return list(map(lambda x: bytearray(x.strip(), "utf-8"), f.readlines()))


def part1(f) -> int:

    grid = parse_input(f)
    splits = 0

    for (row_index, line) in enumerate(grid[:-1]):
        for (column_index, c) in enumerate(grid[row_index]):
            if c == ord("S") or c == ord("|"):
                if grid[row_index+1][column_index] == ord("^"):
                    splits += 1
                    if column_index - 1 >= 0:
                        grid[row_index+1][column_index-1] = ord("|")
                    if column_index + 1 < len(grid[0]):
                        grid[row_index+1][column_index+1] = ord("|")
                else:
                    grid[row_index+1][column_index] = ord("|")

    return splits


def part2(f) -> int:

    grid = parse_input(f)

    paths = [0] * len(grid[0])
    paths[grid[0].find(ord("S"))] = 1

    # Ignore first row, since we initialized `paths` based on the x position of the "S" symbol.
    #
    # Keep track of the overall number of paths for each x position.
    # If we encounter a splitter ^, the number of paths doubles, i.e., we add them to [y+1][x+1] and [y+1][x-1].
    #
    # ......2.2......        ......2.2......   
    # ......^.^......  ===>  .....2^4^2.....
    # ...............        ...............

    for row in grid[1:]:
        next_paths = [0] * len(row)
        for (x, c) in enumerate(row):
            match chr(c):
                case ".":
                    # Just carry the number of paths forward, adding to existing number of paths.
                    next_paths[x] += paths[x]
                case "^":
                    # Number of paths doubles, i.e., add number of paths to left and right neighbors.
                    for delta_x in [-1, +1]:
                        x_new = delta_x + x
                        # Skip off-grid x coordinates.
                        if x_new < 0 or x_new >= len(row):
                            continue
                        next_paths[x_new] += paths[x]
                case _:
                    raise Exception("illegal input")
        paths = next_paths

    return sum(paths)


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    test_file = sys.argv[0].replace(".py", "-test.txt")

    print(sys.argv[0])

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    with open(test_file, encoding="utf-8") as f:
        print("test part1=", part1(f))
    with open(input_file, encoding="utf-8") as f:
        print("part1=", part1(f))
    with open(test_file, encoding="utf-8") as f:
        print("test part2=", part2(f))
    with open(input_file, encoding="utf-8") as f:
        print("part2=", part2(f))