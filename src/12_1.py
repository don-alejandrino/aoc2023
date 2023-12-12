import time

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
        for i in range(num_copies - 1):
            groups.extend(groups)
            springs += springs
        springs = springs[:-1]
        rows.append([list(springs), groups, get_positions_of_unknown_springs(springs)])

    return rows


def get_positions_of_unknown_springs(springs):
    unknown_positions = []
    for i, char in enumerate(springs):
        if char == "?":
            unknown_positions.append(i)

    return unknown_positions


def get_groups_of_operational_springs(springs):
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

    return operational_springs


def get_num_combinations(springs, num_operational_springs, num_broken_springs, positions_of_unknown_springs,
                         operational_spring_groups):
    if not positions_of_unknown_springs:
        if get_groups_of_operational_springs(springs) == operational_spring_groups:
            return 1
        else:
            return 0

    springs = springs.copy()
    positions_of_unknown_springs = positions_of_unknown_springs.copy()
    num_already_set_operational_springs = len([i for i in springs if i == "#"])
    num_already_set_broken_springs = len([i for i in springs if i == "."])
    fill_idx = positions_of_unknown_springs.pop()
    num_possibilities = 0
    if num_already_set_broken_springs < num_broken_springs:
        springs[fill_idx] = "."
        num_possibilities += get_num_combinations(
            springs,
            num_operational_springs,
            num_broken_springs,
            positions_of_unknown_springs,
            operational_spring_groups
        )
    if num_already_set_operational_springs < num_operational_springs:
        springs[fill_idx] = "#"
        num_possibilities += get_num_combinations(
            springs,
            num_operational_springs,
            num_broken_springs,
            positions_of_unknown_springs,
            operational_spring_groups
        )

    return num_possibilities


def get_num_combinations_all_rows(damaged_spring_records):
    num_combinations = []
    for springs, operational_spring_groups, unknown_springs in damaged_spring_records:
        num_overall_operational_springs = sum(operational_spring_groups)
        num_combinations.append(
            get_num_combinations(
                springs,
                num_overall_operational_springs,
                len(springs) - num_overall_operational_springs,
                unknown_springs,
                operational_spring_groups
            )
        )

    return num_combinations


if __name__ == "__main__":
    with open("../inputs/input12.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    res = sum(get_num_combinations_all_rows(parse_input(in_text)))
    end = time.perf_counter()
    print(f"Result: {res}. Brute force approach took {(end - start) * 1000:.2f} ms.")

    # Too slow for Part 2
