import time
from functools import cache

EXAMPLE1 = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def parse_input(text, num_copies=1):
    rows = []
    for line in text.strip().split("\n"):
        springs, groups_text = map(lambda s: s.strip(), line.strip().split(" "))
        groups = list(map(int, groups_text.strip().split(",")))
        springs += "?"
        rows.append([(springs * num_copies)[:-1], tuple(groups * num_copies)])

    return rows


def get_next_position_of_unknown_springs(springs):
    for i, char in enumerate(springs):
        if char == "?":
            return i

    raise ValueError('No unknown position existing anymore.')


def get_first_group_of_operational_springs(springs):
    group_length = 0
    for i, char in enumerate(springs):
        if char == "#":
            group_length += 1
        elif char == ".":
            return group_length, i
        else:
            return 0, i
    else:
        return group_length, len(springs)


def get_all_groups_of_operational_springs(springs):
    operational_springs = []
    group_length = 0
    for char in springs:
        if char == "#":
            group_length += 1
        elif group_length > 0:
            operational_springs.append(group_length)
            group_length = 0
    if group_length != 0:
        operational_springs.append(group_length)

    return tuple(operational_springs)


@cache
def get_num_combinations(springs, operational_spring_groups):
    first_group, end_idx = get_first_group_of_operational_springs(springs)
    if first_group > 0:
        if first_group == operational_spring_groups[0]:
            operational_spring_groups = operational_spring_groups[1:]
            # Add trailing "." to avoid index overflow
            springs = (springs + ".")[end_idx:]
        else:
            return 0
    springs = springs.strip(".")

    try:
        next_unknown_idx = get_next_position_of_unknown_springs(springs)
    except ValueError:
        if get_all_groups_of_operational_springs(springs) == operational_spring_groups:
            return 1
        else:
            return 0

    num_set_operational_springs = len([i for i in springs if i == "#"])
    num_overall_operational_springs = sum(operational_spring_groups)
    num_set_broken_springs = len([i for i in springs if i == "."])
    num_overall_broken_springs = len(springs) - num_overall_operational_springs
    num_possibilities = 0
    if num_set_broken_springs < num_overall_broken_springs:
        springs = springs[:next_unknown_idx] + "." + springs[next_unknown_idx + 1:]
        num_possibilities += get_num_combinations(springs, operational_spring_groups)
    if num_set_operational_springs < num_overall_operational_springs:
        springs = springs[:next_unknown_idx] + "#" + springs[next_unknown_idx + 1:]
        num_possibilities += get_num_combinations(springs, operational_spring_groups)

    return num_possibilities


def get_num_combinations_all_rows(damaged_spring_records):
    num_combinations = []
    for springs, operational_spring_groups in damaged_spring_records:
        num_combinations.append(get_num_combinations(springs, operational_spring_groups))

    return num_combinations


if __name__ == "__main__":
    with open("../inputs/input12.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    res = sum(get_num_combinations_all_rows(parse_input(in_text)))
    end = time.perf_counter()
    print(f"Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum(get_num_combinations_all_rows(parse_input(in_text, num_copies=5)))
    end = time.perf_counter()
    print(f"Result: {res}. Took {(end - start) * 1000:.2f} ms.")
