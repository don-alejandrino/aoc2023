import time
from typing import List, Tuple

EXAMPLE1 = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

DIRECTION_DICT = {"R": 0, "D": 1, "L": 2, "U": 3}


def parse_input_part1(text: str) -> List[Tuple[int, int]]:
    steps = []
    for line in text.strip().split("\n"):
        direction, num_steps, color = line.strip().split(" ")
        num_steps = int(num_steps)
        direction = DIRECTION_DICT[direction]
        steps.append((direction, num_steps))

    return steps


def parse_input_part2(text: str) -> List[Tuple[int, int]]:
    steps = []
    for line in text.strip().split("\n"):
        _, _, hex_code = line.strip().split(" ")
        hex_code = hex_code.replace("(", "").replace(")", "")
        num_steps = int(hex_code[1:-1], 16)
        direction = int(hex_code[-1])
        steps.append((direction, num_steps))

    return steps


def get_total_volume(plan: List[Tuple[int, int]]) -> int:
    filled_area = 0
    num_boundary_points = 0
    i = j = 0  # for convenience, start at zero
    for direction, num_steps in plan:
        num_boundary_points += num_steps
        if direction == 0:  # Go right
            j = j + num_steps
            filled_area -= i * num_steps
        elif direction == 1:  # Go down
            i = i + num_steps
        elif direction == 2:  # Go left
            j = j - num_steps
            filled_area += i * num_steps
        elif direction == 3:  # Go up
            i = i - num_steps

    # Pick's theorem: A = i + b / 2 - 1, where A is the area of a polygon, i is the number of points inside the polygon,
    # and b is the number of boundary points
    num_interior_points = filled_area - num_boundary_points // 2 + 1
    num_total_points = num_interior_points + num_boundary_points

    return num_total_points


if __name__ == "__main__":
    with open("../inputs/input18.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    dig_plan = parse_input_part1(in_text)
    res = get_total_volume(dig_plan)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    dig_plan = parse_input_part2(in_text)
    res = get_total_volume(dig_plan)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
