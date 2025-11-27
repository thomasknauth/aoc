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

test_input = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

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

    inputs = []
    for line in f.readlines():
        line = line.strip()
        t, groups = line.split()
        groups = list(map(int, groups.split(",")))
        inputs.append((t, groups))
    return inputs


def is_valid(s, gs):
    """
    Also works for prefixes, i.e., is_valid('##??', [2,1]) == True, but is_valid('##??', [1,1]) == False
    """
    i = 0
    for g in gs:
        if i >= len(s):
            return False
        while s[i] != "#":
            if s[i] == "?":
                return True
            i += 1
            if i >= len(s):
                return False
        c = 0
        while s[i] != ".":
            if s[i] == "?":
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
        if s[i] == "#":
            return False
        i += 1


def test_is_valid():

    inputs = [
        ("##??", [2, 1], True),
        ("##??", [1, 1], False),
        ("#", [1], True),
        ("#.#", [1, 1], True),
        ("###", [3], True),
        ("###", [3, 1], False),
        ("##.#", [2, 1], True),
        ("#.#.#", [2, 1], False),
    ]
    for i1, i2, o in inputs:
        assert is_valid(i1, i2) == o, f"is_valid({i1}, {i2}), expected result {o}"


def solutions(t, groups):

    # Candidates
    cs = [t]
    # Final solutions
    res = []

    while len(cs) > 0:
        s = cs.pop()
        s1, s2 = "", ""
        for i, c in enumerate(s):
            if c == "?":
                s1 += "." + s[i + 1 :]
                s2 += "#" + s[i + 1 :]
                for sn in [s1, s2]:
                    if is_valid(sn, groups):
                        cs.append(sn)
                break
            else:
                s1 += c
                s2 += c

        if s1 == s2:
            if is_valid(s1, groups):
                res.append(s1)

    return len(res)


# Use recursion and caching to speed up the computation.
class Solution:

    def __init__(self):
        self.c = {}

    def solutions(self, s: str, g: list[int]) -> int:

        assert len(g) >= 1

        # Is the result cached? This is necessary to reduce runtime to acceptable levels, i.e.,
        # couple of seconds.  Serialize g into a string such that we can use it to index the
        # map/dict.
        g_str = str(g)
        if (s, g_str) in self.c:
            res = self.c[(s, g_str)]
            return res

        i = 0
        while True:

            # Return early if string too short for valid solution.
            if i >= len(s):
                return 0

            # A # character starts a new group.
            if s[i] == "#":
                j = 1
                # Check there are g[0]-many # or ? characters following the initial # for it to be a
                # valid solution.
                while j < g[0]:
                    # Return early if string too short for valid solution.
                    if i + j >= len(s):
                        return 0
                    # A . prematurely ends the group, i.e., invalid solution.
                    if s[i + j] == ".":
                        return 0
                    j += 1

                # A . or ? must separate adjacent groups ...
                if len(g) > 1:
                    if i + j >= len(s):
                        return 0
                    if s[i + j] == "#":
                        return 0
                    # Solve recursively for remaining string and groups.
                    res = self.solutions(s[i + j + 1 :], g[1:])
                    # Cache the result.
                    self.c[(s, g_str)] = res
                    return res
                # ... unless there are no more groups, in which case only . and ? characters may follow.
                else:
                    # Check remaining characters do **not** contain #
                    for c in s[i + j :]:
                        if c == "#":
                            return 0
                    return 1
            elif s[i] == "?":
                # Create two new variants and solve recursively.
                s1 = s[0:i] + "." + s[i + 1 :]
                s2 = s[0:i] + "#" + s[i + 1 :]
                res = self.solutions(s1, g) + self.solutions(s2, g)
                # Cache the result.
                self.c[(s, g_str)] = res
                return res
            i += 1
        return 0


def test_solutions():

    solver = Solution()
    for i1, i2, o in read_tests():
        # assert solutions(i1, i2) == o, f'solutions({i1}, {i2}), expected result {o}'
        s = solver.solutions(i1, i2)
        assert s == o, f"solutions({i1}, {i2}), expected: {o}, actual: {s}"


def part1(f):

    inputs = parse_input(f)
    solver = Solution()
    acc = 0
    for input in inputs:
        r1 = solver.solutions(*input)
        r2 = solutions(*input)
        # for k, v in solver.c.items():
        #     print(k, v)
        if r1 != r2:
            print(f"{r1} {r2} {input}")
            assert False
        acc += r1
    return acc


# I struggled a lot with this puzzle. Part 1 was easy enough to solve by just enumerating all
# possible variants, discarding invalid ones early and count the number of valid solutions.
#
# This approach did not scale for Part 2 which had much larger/longer inputs. I was initially hoping
# we could solve Part 2 analytically, i.e., calculate the number of solutions for f(x) and pre- or
# postfix with ? to compute f(?x) and f(x?). It seems this is not possible for the general
# case. While it works for some inputs, the result for Part 2 computed thusly is incorrect.
#
# Ultimately, I consulted the interwebs. A better approach might be to progressively fill blanks and
# recursively solve by removing one group at a time. In combination with caching this completes in a
# reasonable amount of time.
#
# Still, there were many opportunities to debug wrong results due to +/- 1 offset errors in string
# indexing or loop count.
def part2(f):

    input = parse_input(f)
    input = map(lambda tup: ("?".join([tup[0]] * 5), tup[1] * 5), input)
    return sum(map(lambda x: Solution().solutions(*x), input))


def read_tests():
    testcases = []
    for line in open("2023-12-test.txt").readlines():
        i1, i2, o = line.split()
        i2 = list(map(int, i2.split(",")))
        o = int(o)
        testcases.append((i1, i2, o))
    return testcases


if __name__ == "__main__":

    fn = "2023-12-p1.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]

    for f in [test_solutions]:
        f()

    print("test part1=", part1(io.StringIO(test_input)))
    print("part1=", part1(open(fn)))
    print("test part2=", part2(io.StringIO(test_input)))
    print("part2=", part2(open(fn)))
