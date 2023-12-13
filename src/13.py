import time
from typing import List

import numpy as np

EXAMPLE1 = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def parse_input(text: str) -> List[np.ndarray]:
    patterns = []
    for pattern_text in text.strip().split("\n\n"):
        pattern_lines = pattern_text.strip().split("\n")
        mat = np.empty((len(pattern_lines), len(pattern_lines[0])), dtype='bool')
        for i, line in enumerate(pattern_lines):
            for j, char in enumerate(line):
                if char == ".":
                    mat[i, j] = False
                elif char == "#":
                    mat[i, j] = True
                else:
                    raise ValueError("Found unexpected character!")
        patterns.append(mat)
    return patterns


def find_reflection_index(pattern: np.ndarray) -> int:
    i_max, j_max = pattern.shape

    # Find reflection in rows
    for i in range(i_max - 1):
        for n in range(min(i + 1, i_max - i - 1)):
            if np.any(pattern[i - n, :] != pattern[i + 1 + n, :]):
                break
        else:
            return (i + 1) * 100

    # Find reflection in columns
    for j in range(j_max - 1):
        for n in range(min(j + 1, j_max - j - 1)):
            if np.any(pattern[:, j - n] != pattern[:, j + 1 + n]):
                break
        else:
            return j + 1

    raise ValueError("Found no reflection!")


def find_new_reflection_index(pattern: np.ndarray) -> int:
    old_reflection_index = find_reflection_index(pattern)
    if old_reflection_index >= 100:  # Hacky but works since the input matrices are way smaller than 100x100
        old_reflection_row = old_reflection_index // 100 - 1
        old_reflection_col = None
    else:
        old_reflection_row = None
        old_reflection_col = old_reflection_index - 1

    i_max, j_max = pattern.shape

    # Find reflection in rows
    for i in range(i_max - 1):
        if i != old_reflection_row:
            smudge_fixed = False
            for n in range(min(i + 1, i_max - i - 1)):
                num_different_elements = np.count_nonzero(pattern[i - n, :] != pattern[i + 1 + n, :])
                if num_different_elements > 1:
                    break
                elif num_different_elements == 1:
                    if not smudge_fixed:
                        smudge_fixed = True
                    else:
                        break
            else:
                return (i + 1) * 100

    # Find reflection in columns
    for j in range(j_max - 1):
        if j != old_reflection_col:
            smudge_fixed = False
            for n in range(min(j + 1, j_max - j - 1)):
                num_different_elements = np.count_nonzero(pattern[:, j - n] != pattern[:, j + 1 + n])
                if num_different_elements > 1:
                    break
                elif num_different_elements == 1:
                    if not smudge_fixed:
                        smudge_fixed = True
                    else:
                        break
            else:
                return j + 1

    raise ValueError("Found no reflection!")


if __name__ == "__main__":
    with open("../inputs/input13.txt", "r") as fh:
        in_text = fh.read()

    patterns = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = sum(map(find_reflection_index, patterns))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum(map(find_new_reflection_index, patterns))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
