import itertools
from heapq import heappop, heappush, nlargest
import math
import sys


def parse_input(f) -> list[bytearray]:

    # Use tuple() for the coordinates, such that we can use the tuple() as a dict() key.
    return list(map(lambda s: tuple(map(int, s.strip().split(","))), f.readlines()))


def solve(f, nr_pairs) -> int:

    points = parse_input(f)
    distances = []

    # Compute distance between all possible pairs of points.
    for p, q in itertools.combinations(points, 2):
        distance = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2
        distance = math.sqrt(distance)
        heappush(distances, (distance, (p, q)))

    # Use a map to quickly look up if a given point is part of a circuit.
    point2circuit = {}

    for _ in range(nr_pairs):
        _, (p, q) = heappop(distances)

        # If both points are already part of a circuit,
        # combine the circuits.
        if p in point2circuit and q in point2circuit:
            # Use set() to dedup points.
            l = list(set(point2circuit[p] + point2circuit[q]))
            # Update mapping for each point in the combined circuit.
            for p in l:
                point2circuit[p] = l
        # Add new point to existing circuit.
        elif p in point2circuit:
            point2circuit[p] += [q]
            point2circuit[q] = point2circuit[p]
        # Add new point to existing circuit.
        elif q in point2circuit:
            point2circuit[q] += [p]
            point2circuit[p] = point2circuit[q]
        # Create new circuit.
        else:
            point2circuit[p] = [p, q]
            point2circuit[q] = point2circuit[p]

        # Exit condition for Part 2: If all points form a single circuite, we are done.
        if len(point2circuit[p]) == len(points):
            return p[0] * q[0]

    circuit_sizes = []
    # Convert list[int] into tuple[int] such that we can use set() to deduplicate circuits.
    # Push circuits, ordered by size, into a heap queue.
    for circuit in set(map(tuple, point2circuit.values())):
        heappush(circuit_sizes, (len(circuit), circuit))

    # Pick the 3 largest circuits and multiply their sizes
    return math.prod([size for size, _ in nlargest(3, circuit_sizes)])


def part1(f, nr_pairs) -> int:

    return solve(f, nr_pairs)


def part2(f) -> int:

    return solve(f, 10**9)


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    test_file = sys.argv[0].replace(".py", "-test.txt")

    print(sys.argv[0])

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    with open(test_file, encoding="utf-8") as f:
        print("test part1=", part1(f, 10))
    with open(input_file, encoding="utf-8") as f:
        print("part1=", part1(f, 1000))
    with open(test_file, encoding="utf-8") as f:
        print("test part2=", part2(f))
    with open(input_file, encoding="utf-8") as f:
        print("part2=", part2(f))
