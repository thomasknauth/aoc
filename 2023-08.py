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

# --- Part Two ---

# The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel
# follow the instructions, but you've barely left your starting position. It's going to take
# significantly more steps to escape!

# What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the
# laws of spacetime? Only one way to find out.

# After examining the maps a bit longer, your attention is drawn to a curious fact: the number of
# nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd
# probably just start at every node that ends with A and follow all of the paths at the same time
# until they all simultaneously end up at nodes that end with Z.

# For example:

test_input_part2='''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''

# Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each
# left/right instruction, use that instruction to simultaneously navigate away from both nodes
# you're currently on. Repeat this process until all of the nodes you're currently on end with
# Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue
# as normal.) In this example, you would proceed as follows:

# Step 0: You are at 11A and 22A.
# Step 1: You choose all of the left paths, leading you to 11B and 22B.
# Step 2: You choose all of the right paths, leading you to 11Z and 22C.
# Step 3: You choose all of the left paths, leading you to 11B and 22Z.
# Step 4: You choose all of the right paths, leading you to 11Z and 22B.
# Step 5: You choose all of the left paths, leading you to 11B and 22C.
# Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
# So, in this example, you end up entirely on nodes that end in Z after 6 steps.

# Simultaneously start on every node that ends with A. How many steps does it take before you're
# only on nodes that end with Z?

import io
import math
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
        for (i, move) in enumerate(moves):
            assert move in ['L', 'R']
            # Array indexing via True(1)/False(0) ¯\_(ツ)_/¯
            pos = m[pos][move == 'R']
            c += 1
            if pos == 'ZZZ':
                return c

def solve_one(loc, moves, m):
    c = 0
    states = set()

    while True:
        for (idx, move) in enumerate(moves):
            assert move in ['L', 'R']
            states.add((loc, idx))
            if loc[-1] == 'Z':
                return c
            loc = m[loc][0] if move == 'L' else m[loc][1]
            c += 1

def part2(f):

    moves, m = parse_input(f)

    # Lemma 1: Cycles can only appear after having found at least one solution, i.e., if there is a
    # cycle before a solution is found, there is no solution.

    # Lemma 2: All graphs are independent of each other
    # print(sum([len(loc2states[k]) for k in loc2states.keys()]))
    # print(len(set().union(*loc2states.values())))

    # Lemma 3: Start states have no incoming edges.

    # Lemma 4: Periodicity of loop is identical to # of steps from start state till end state (I
    # guess it has to be this way if we want to solve using least common multiple).

    # Lemma 5: There is only one start and end state for each cycle.

    locs = [key for key in m.keys() if key[-1] == 'A']

    cycles_lens = []
    for loc in locs:
        cycles_lens.append(solve_one(loc, moves, m))

    return math.lcm(*cycles_lens)

if __name__ == '__main__':

    fn = '2023-08-p1.txt'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    print(part1(io.StringIO(test_input)))
    print(part1(open(fn)))
    print(part2(io.StringIO(test_input_part2)))
    print(part2(open(fn)))
