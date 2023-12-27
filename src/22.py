import copy
import time
from typing import Tuple, List

from tqdm import tqdm

EXAMPLE1 = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


def parse_input(text: str) -> List[Tuple[List[int], List[int], List[int]]]:
    blocks = []
    for line in text.strip().split("\n"):
        start_text, end_text = line.strip().split("~")
        (x_start, y_start, z_start) = tuple(map(int, start_text.split(",")))
        (x_end, y_end, z_end) = tuple(map(int, end_text.split(",")))
        blocks.append(([x_start, x_end], [y_start, y_end], [z_start, z_end]))

    return sorted(blocks, key=lambda x: x[2][0])


def is_empty_space_below(
    block: Tuple[List[int], List[int], List[int]],
    blocks_below: List[Tuple[List[int], List[int], List[int]]],
    ground_level: int = 1
) -> bool:
    if block[2][0] <= ground_level:
        return False
    for bb in blocks_below:
        if (
                (
                    bb[0][0] <= block[0][0] <= bb[0][1] or
                    bb[0][0] <= block[0][1] <= bb[0][1] or
                    (block[0][0] < bb[0][0] and block[0][1] > bb[0][1])
                ) and (
                    bb[1][0] <= block[1][0] <= bb[1][1] or
                    bb[1][0] <= block[1][1] <= bb[1][1] or
                    (block[1][0] < bb[1][0] and block[1][1] > bb[1][1])
                ) and bb[2][1] == block[2][0] - 1
        ):
            return False

    return True


def stack_blocks(blocks: List[Tuple[List[int], List[int], List[int]]]) -> List[Tuple[List[int], List[int], List[int]]]:
    stacked_blocks = []
    for block_position in tqdm(blocks):
        new_block_position = copy.deepcopy(block_position)
        while is_empty_space_below(
            new_block_position, [sb for sb in stacked_blocks if sb[2][1] == new_block_position[2][0] - 1]
        ):
            new_block_position[2][0] -= 1
            new_block_position[2][1] -= 1
        stacked_blocks.append(new_block_position)

    return stacked_blocks


def are_blocks_stable(blocks: List[Tuple[List[int], List[int], List[int]]], current_level: int) -> bool:
    for i, block_position in enumerate(blocks):
        if is_empty_space_below(
            block_position,
            [sb for sb in blocks if sb[2][1] == block_position[2][0] - 1],
            ground_level=current_level
        ):
            return False

    return True


def get_num_falling_blocks(blocks: List[Tuple[List[int], List[int], List[int]]], current_level: int) -> int:
    num_falling_blocks = 0
    other_blocks = blocks.copy()
    for i, block_position in enumerate(blocks):
        if is_empty_space_below(
            block_position,
            [sb for sb in other_blocks if sb[2][1] == block_position[2][0] - 1],
            ground_level=current_level
        ):
            num_falling_blocks += 1
            other_blocks.remove(block_position)

    return num_falling_blocks


def get_num_disintegratable_blocks(blocks: List[Tuple[List[int], List[int], List[int]]]) -> int:
    num_disintegratable_blocks = 0
    for i, block in enumerate(tqdm(blocks)):
        other_blocks = blocks.copy()
        other_blocks.pop(i)
        if are_blocks_stable(
            [ob for ob in other_blocks if ob[2][1] == block[2][1] or ob[2][0] == block[2][1] + 1],
            block[2][1]
        ):
            num_disintegratable_blocks += 1

    return num_disintegratable_blocks


def get_num_overall_falling_blocks(blocks: List[Tuple[List[int], List[int], List[int]]]) -> int:
    num_falling_blocks = 0
    for i, block in enumerate(tqdm(blocks)):
        other_blocks = blocks.copy()
        other_blocks.pop(i)
        num_falling_blocks += get_num_falling_blocks(
            [ob for ob in other_blocks if ob[2][1] >= block[2][1]],
            block[2][1]
        )

    return num_falling_blocks


if __name__ == "__main__":
    with open("../inputs/input22.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    stacked_blocks_after_falling = stack_blocks(parse_input(in_text))
    res = get_num_disintegratable_blocks(stacked_blocks_after_falling)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_num_overall_falling_blocks(stacked_blocks_after_falling)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
