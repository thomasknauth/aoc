import sys


def parse_input(f) -> tuple[list[(int,int)], list[int]]:

    lines = f.readlines()

    ranges = []
    while True:
        line = lines.pop(0)
        line = line.strip()
        if line == "":
            break
        lower_bound, upper_bound = map(int, line.split("-"))
        ranges.append((lower_bound, upper_bound))

    ids = []
    while len(lines) > 0:
        line = lines.pop(0)
        line = line.strip()
        ids.append(int(line))

    return (ranges, ids)


def part1(f) -> int:

    ranges, ids = parse_input(f)
    fresh = 0
    for id in ids:
        for lower_bound, upper_bound in ranges:
            if id >= lower_bound and id <= upper_bound:
                fresh += 1
                break

    return fresh

def is_inclusive(r1, r2):
    """True, iff r2 is included in r1."""
    return r2[0] >= r1[0] and r2[1] <= r1[1]


def ranges_do_not_overlap(r1, r2) -> bool:
    # [....] r1
    #          [.....] r2
    # or
    #          [.....] r1
    # [....]           r2
    return r1[1] < r2[0] or r1[0] > r2[1]


def non_overlapping(r1: tuple[int, int], rs: list[tuple[int, int]]) -> list[tuple[int, int]]:

    non_overlapping = []

    # If r1 overlaps with r2, create non-overlapping ranges keeping r1 as is.
    for r2 in rs:

        if ranges_do_not_overlap(r1, r2):
            # non-overlapping
            non_overlapping += [r2]
            continue

        if is_inclusive(r1, r2):
            #    [............] r1
            #        [.....]    r2
            # r2 is included in r1 - nothing to do here.
            continue

        if is_inclusive(r2, r1):
            #      [.....]      r1
            #   [...........]   r2
            if r2[0] != r1[0]:
                non_overlapping += [(r2[0], r1[0]-1)]
            if r1[1] != r2[1]:
                non_overlapping += [(r1[1]+1, r2[1])]
            continue

        if r2[0] <= r1[1] and r1[1] <= r2[1]:
            # [.........] r1
            #        [.......] r2
            non_overlapping += [(r1[1]+1, r2[1])]
            continue

        if r2[1] >= r1[0]:
            #           [.......] r1
            #     [.........]     r2
            non_overlapping += [(r2[0], r1[0]-1)]

    non_overlapping += [r1]
    return non_overlapping

def part2(f) -> int:

    ranges, _ = parse_input(f)
    output_ranges = ranges[1:]

    # Iterate over all ranges and adjust `output_ranges` such that there is no overlap with `range`.
    for range in ranges:
        output_ranges = non_overlapping(range, output_ranges)

    return sum(map(lambda r: r[1]-r[0]+1, output_ranges))


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
