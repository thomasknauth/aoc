# --- Day 12: Hot Springs ---

# You finally reach the hot springs! You can see steam rising from secluded areas attached to the
# primary, ornate building.

# As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot
# springs, weren't you?" You indicate that this definitely looks like hot springs to you.

# "Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."

# You look in the direction the researcher is pointing and suddenly notice the massive metal helixes
# towering overhead. "This way!"

# It only takes you a few more steps to reach the main gate of the massive fenced-off area
# containing the springs. You go through the gate and into a small administrative building.

# "Hello! What brings you to the hot springs today? Sorry they're not very hot right now; we're
# having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.

# "Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, not
# until we get more lava to heat our forges. And our springs. The springs aren't very springy unless
# they're hot!"

# "Say, could you go up and see why the lava stopped flowing? The springs are too cold for normal
# operation, but we should be able to find one springy enough to launch you up there!"

# There's just one problem - many of the springs have fallen into disrepair, so they're not actually
# sure which springs would even be safe to use! Worse yet, their condition records of which springs
# are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged
# records.

# In the giant field just outside, the springs are arranged into rows. For each row, the condition
# records show every spring and whether it is operational (.) or damaged (#). This is the part of
# the condition records that is itself damaged; for some springs, it is simply unknown (?) whether
# the spring is operational or damaged.

# However, the engineer that produced the condition records also duplicated some of this information
# in a different format! After the list of springs for a given row, the size of each contiguous
# group of damaged springs is listed in the order those groups appear in the row. This list always
# accounts for every damaged spring, and each number is the entire size of its contiguous group
# (that is, groups are always separated by at least one operational spring: #### would always be 4,
# never 2,2).

# So, condition records with no unknown spring conditions might look like this:

# #.#.### 1,1,3
# .#...#....###. 1,1,3
# .#.###.#.###### 1,3,1,6
# ####.#...#... 4,1,1
# #....######..#####. 1,6,5
# .###.##....# 3,2,1

# However, the condition records are partially damaged; some of the springs' conditions are actually
# unknown (?). For example:

# test_input='''\
# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# '''
test_input='''\
?###???????? 3,2,1
'''

# Equipped with this information, it is your job to figure out how many different arrangements of
# operational and broken springs fit the given criteria in each row.

# In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three
# broken springs (in that order) can appear in that row: the first three unknown springs must be
# broken, then operational, then broken (#.#), making the whole row #.#.###.

# The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different
# arrangements. The last ? must always be broken (to satisfy the final contiguous group of three
# broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be
# both broken springs or they would form a single contiguous group of two; if that were true, the
# numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are
# four possible arrangements of springs.

# The last line is actually consistent with ten different arrangements! Because the first number is
# 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or
# higher). However, the remaining run of unknown spring conditions have many different ways they
# could hold groups of two and one broken springs:

# ?###???????? 3,2,1
# .###.##.#...
# .###.##..#..
# .###.##...#.
# .###.##....#
# .###..##.#..
# .###..##..#.
# .###..##...#
# .###...##.#.
# .###...##..#
# .###....##.#

# In this example, the number of possible arrangements for each row is:

# ???.### 1,1,3 - 1 arrangement
# .??..??...?##. 1,1,3 - 4 arrangements
# ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
# ????.#...#... 4,1,1 - 1 arrangement
# ????.######..#####. 1,6,5 - 4 arrangements
# ?###???????? 3,2,1 - 10 arrangements
# Adding all of the possible arrangement counts together produces a total of 21 arrangements.

# For each row, count all of the different arrangements of operational and broken springs that meet
# the given criteria. What is the sum of those counts?

import io
import itertools
import sys

def parse_input(f):

    lines = list(map(lambda s: s.strip(), f.readlines()))

    return lines

def is_valid(s, gs):
    '''
    Also works for prefixes, i.e., is_valid('##??', [2,1]) == True, but is_valid('##??', [1,1]) == False
    '''
    i = 0
    for g in gs:
        if i >= len(s):
            return False
        while s[i] != '#':
            if s[i] == '?':
                return True
            i += 1
            if i >= len(s):
                return False
        c = 0
        while s[i] != '.':
            if s[i] == '?':
                return c <= g
            c += 1
            i += 1
            if i >= len(s):
                break
        if c != g:
            return False
    
    while True:
        if i >= len(s):
            return True
        if s[i] == '#':
            return False
        i += 1

def test_is_valid():

    inputs = [
        ('##??', [2,1], True),
        ('##??', [1,1], False),
        ('#', [1], True),
        ('#.#', [1,1], True),
        ('###', [3], True),
        ('###', [3,1], False),
        ('##.#', [2,1], True),
        ('#.#.#', [2,1], False),
    ];
    for (i1, i2, o) in inputs:
        assert is_valid(i1, i2) == o, f'is_valid({i1}, {i2}), expected result {o}'

def solutions(line):
    
    t, groups = line.split()
    groups = list(map(int, groups.split(',')))

    cs = [t]
    res = 0

    while len(cs) > 0:
        s = cs.pop()
        s1, s2 = '', ''
        for (i, c) in enumerate(s):
            if c == '?':
                s1 += '.' + s[i+1:]
                s2 += '#' + s[i+1:]
                for sn in [s1, s2]:
                    if is_valid(sn, groups):
                        cs.append(sn)
                break
            else:
                s1 += c
                s2 += c
        
        if s1 == s2:
            if is_valid(s1, groups):
                res += 1

    return res

def part1(f):

    lines = parse_input(f)
    all_results = list(map(solutions, lines))
    print(all_results)
    return sum(all_results)

def part2(f):

    input = parse_input(f)
    return input

if __name__ == '__main__':

    fn = '2023-12-p1.txt'
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    for f in [test_is_valid]:
        f()

    # print('test part1=', part1(io.StringIO(test_input)))
    print('part1=', part1(open(fn)))
    #print('test part2=', part2(io.StringIO(test_input)))
    # print('part2=', part2(open(fn)))
