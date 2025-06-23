# --- Day 8: Haunted Wasteland ---

# You're still riding a camel across Desert Island when you spot a sandstorm quickly
# approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had
# just finished warning you about ghosts a few minutes ago.

# One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle
# input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of
# the documents contains a list of left/right instructions, and the rest of the documents seem to
# describe some kind of network of labeled nodes.

# It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if
# you have the camel follow the same instructions, you can escape the haunted wasteland!

# After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where
# you are now, and you have to follow the left/right instructions until you reach ZZZ.

# This format defines each node of the network individually. For example:

# RL

# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)

# Starting with AAA, you need to look up the next element based on the next left/right instruction
# in your input. In this example, start with AAA and go right (R) by choosing the right element of
# AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right
# instructions, you reach ZZZ in 2 steps.

# Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat
# the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so
# on. For example, here is a situation that takes 6 steps to reach ZZZ:

test_input='''\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''

# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

import io
import sys

def parse_input(f):

    lines = list(map(lambda s: s.strip(), f.readlines()))

    m = dict()
    for line in lines[2:]:
        key, val_left, val_right = line[0:3], line[7:10], line[12:15]
        m[key] = (val_left, val_right)

    return (lines[0], m)

def part1(f):

    moves, m = parse_input(f)
    pos = 'AAA'
    c = 0
    while True:
        for move in moves:
            assert move in ['L', 'R']
            pos = m[pos][0] if move == 'L' else m[pos][1]
            c += 1
            if pos == 'ZZZ':
                return c

def part2(f):
    return 0

if __name__ == '__main__':

    fn = '2023-08-p1.txt'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    print(part1(io.StringIO(test_input)))
    print(part1(open(fn)))
    #print(part2(io.StringIO(test_input)))
    #print(part2(open(fn)))
