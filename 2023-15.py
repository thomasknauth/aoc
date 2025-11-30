from collections import defaultdict
import io
import sys


def parse_input(f):

    return f.readlines()[0].strip()


def hash(s: str) -> int:
    acc = 0
    for c in s:
        acc += ord(c)
        acc *= 17
        acc = acc % 256
    return acc


def part1(f) -> int:

    input = parse_input(f)
    print("HASH ", hash("HASH"))
    # print([(s, hash(s)) for s in map(lambda s: s[:-1] if s[-1] == "-" else s[:-2], input.split(","))])
    return sum(map(hash, input.split(",")))


def score(boxes):
    acc = 0
    for box_nr in range(256):
        for (slot, t) in enumerate(boxes[box_nr]):
            acc += (box_nr+1) * (slot+1) * t[1]
    return acc

def part2(f) -> int:
    """ """
    input = parse_input(f)
    boxes = defaultdict(list)
    for step in input.split(","):
        if step[-1] == "-":
            label = step[0:-1]
            box_nr = hash(label)

            # If label exists, remove while keeping order of existing entries.
            for (i, tuple) in enumerate(boxes[box_nr]):
                if tuple[0] == label:
                    boxes[box_nr] = boxes[box_nr][:i] + boxes[box_nr][i+1:]
                    break
        else:
            label, focal_length = step.split("=")
            focal_length = int(focal_length)
            box_nr = hash(label)
            # print("=", label, focal_length, box_nr)
            lenses = boxes[box_nr]

            # Find index for `label`, if it exists.
            idx = -1
            for (i, tuple) in enumerate(lenses):
                if tuple[0] == label:
                    idx = i
                    break

            # If `label` exists, update its `focal_length`. Otherwise, append new entry.
            if idx >= 0:
                boxes[box_nr] = lenses[:idx] + [(label, focal_length)] + lenses[idx+1:]
            else:
                lenses += [(label, focal_length)]

    return score(boxes)


if __name__ == "__main__":

    input_file = sys.argv[0].replace(".py", "-input.txt")
    test_file = sys.argv[0].replace(".py", "-test.txt")

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    print("test part1=", part1(open(test_file)))
    print("part1=", part1(open(input_file)))
    print("test part2=", part2(open(test_file)))
    print("part2=", part2(open(input_file)))
