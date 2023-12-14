import hashlib
import time
from typing import Tuple, List

import numpy as np

EXAMPLE1 = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def parse_input(text: str) -> np.ndarray:
    lines = text.strip().split("\n")
    platform_grid = np.empty((len(lines[0]), len(lines)), dtype=np.uint8)
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            if char == "#":
                platform_grid[i, j] = 2
            elif char == "O":
                platform_grid[i, j] = 1
            elif char == ".":
                platform_grid[i, j] = 0
            else:
                raise ValueError("Invalid character.")

    return platform_grid


def tilt(col: np.ndarray, left: bool = True) -> np.ndarray:
    if left:
        sub_cols = np.split(col, np.where(col == 2)[0])
        sorted_sub_cols = list(map(lambda a: np.sort(a)[::-1], sub_cols))
    else:
        sub_cols = np.split(col, np.where(col == 2)[0] + 1)
        sorted_sub_cols = list(map(lambda a: np.sort(a), sub_cols))
    return np.concatenate(sorted_sub_cols)


def tilt_north(platform: np.ndarray):
    for j in range(platform.shape[1]):
        platform[:, j] = tilt(platform[:, j])


def tilt_south(platform: np.ndarray):
    for j in range(platform.shape[1]):
        platform[:, j] = tilt(platform[:, j], left=False)


def tilt_west(platform: np.ndarray):
    for i in range(platform.shape[0]):
        platform[i, :] = tilt(platform[i, :])


def tilt_east(platform: np.ndarray):
    for i in range(platform.shape[0]):
        platform[i, :] = tilt(platform[i, :], left=False)


def calculate_north_load(platform: np.ndarray) -> int:
    i_max, j_max = platform.shape
    return ((platform == 1) * np.arange(i_max, 0, -1)[:, None]).sum()


def spin_cycle(platform: np.ndarray):
    tilt_north(platform)
    tilt_west(platform)
    tilt_south(platform)
    tilt_east(platform)


def spin_cycles_until_stationary(platform: np.ndarray, max_cycles: int) -> Tuple[int, int, List[int]]:
    visited_platform_states = {}
    calculated_north_loads = []
    current_platform_state = None
    n = 0
    for n in range(max_cycles):
        if current_platform_state in visited_platform_states.keys():
            break
        visited_platform_states[current_platform_state] = n
        calculated_north_loads.append(calculate_north_load(platform))
        spin_cycle(platform)
        current_platform_state = hashlib.sha256(platform.data).hexdigest()

    periodic_sequence_length = n - visited_platform_states[current_platform_state]
    periodic_sequence_offset = visited_platform_states[current_platform_state]

    return periodic_sequence_length, periodic_sequence_offset, calculated_north_loads


def calculate_north_load_after_cycles(platform: np.ndarray, num_cycles: int = 1000000000) -> int:
    periodic_seq_length, periodic_seq_offset, north_loads = spin_cycles_until_stationary(platform, num_cycles)
    target_idx = (num_cycles - periodic_seq_offset) % periodic_seq_length + periodic_seq_offset

    return north_loads[target_idx]


if __name__ == "__main__":
    with open("../inputs/input14.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    platform_arr = parse_input(in_text)
    tilt_north(platform_arr)
    res = calculate_north_load(platform_arr)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    platform_arr = parse_input(in_text)
    res = calculate_north_load_after_cycles(platform_arr)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
