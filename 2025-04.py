import sys


def parse_input(f) -> list[str]:

    return [s.strip() for s in f.readlines()]


def removeable(grid) -> int:

    adjaceny_offsets = []
    for x_offset in [-1, 0, 1]:
        for y_offset in [-1, 0, 1]:
            if x_offset == 0 and y_offset == 0:
                continue
            adjaceny_offsets += [(x_offset, y_offset)]

    removable_rolls_coordinates = []

    for (y, _) in enumerate(grid):
        for (x, _) in enumerate(grid[0]):

            # If the square has no paper roll, skip.
            if grid[y][x] != "@":
                continue

            adjacent_rolls = 0

            for x_offset, y_offset in adjaceny_offsets:
                # Check y is in range.
                if y + y_offset < 0 or y + y_offset >= len(grid):
                    continue

                # Check x is in range.
                if x + x_offset < 0 or x + x_offset >= len(grid[0]):
                    continue

                adjacent_rolls += 1 if grid[y + y_offset][x + x_offset] == "@" else 0

            if adjacent_rolls < 4:
                removable_rolls_coordinates.append((x, y))

    return removable_rolls_coordinates


def part1(f) -> int:

    grid = parse_input(f)

    return len(removeable(grid))


def part2(f) -> int:
    """Determine removable rolls in a loop until there are no more.
    
    No need for any optimizations, as this runs in ~1 second for the given inputs.
    One potential optimzation is to only look at the vicinity of removable rolls for the next iteration.
    """
    grid = parse_input(f)
    xys = removeable(grid)
    total_rolls = 0
    while len(xys) > 0:
        total_rolls += len(xys)
        for x, y in xys:
            grid[y] = grid[y][:x] + "." + grid[y][x + 1 :]
        xys = removeable(grid)
    return total_rolls


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    test_file = sys.argv[0].replace(".py", "-test.txt")

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
