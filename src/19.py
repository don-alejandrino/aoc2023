import copy
import time
from typing import List, Tuple, Dict, Union

EXAMPLE1 = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

PARAM_POSITION_MAPPING = {
    "x": 0,
    "m": 1,
    "a": 2,
    "s": 3
}


def parse_input(text: str) -> Tuple[Dict[str, List[Union[str, List[str]]]], List[List[int]]]:
    workflows = {}
    parts = []
    workflows_block, parts_block = text.strip().split("\n\n")

    for line in workflows_block.strip().split("\n"):
        name, steps = line.split("{")
        steps = steps.replace("}", "").split(",")
        step_list = []
        for step in steps:
            step_list.append(step.split(":"))
        workflows[name] = step_list

    for line in parts_block.strip().split("\n"):
        properties = line.replace("{", "").replace("}", "").split(",")
        properties = list(map(lambda s: int(s[2:]), properties))
        parts.append(properties)

    return workflows, parts


def run_workflow(
        workflows: Dict[str, List[Union[str, List[str]]]],
        workflow_name: str,
        part: List[int]
) -> int:
    x, m, a, s = part
    steps = workflows[workflow_name]
    for condition, goto in steps[:-1]:
        if eval(condition):  # Don't use with arbitrary, unchecked input ;)
            if goto == "A":
                return x + m + a + s
            elif goto == "R":
                return 0
            return run_workflow(workflows, goto, part)
    else_goto = steps[-1][0]
    if else_goto == "A":
        return x + m + a + s
    elif else_goto == "R":
        return 0
    return run_workflow(workflows, else_goto, part)


def get_num_combinations(param_ranges: List[List[int]]) -> int:
    num_combinations = 1
    for r in param_ranges:
        num_combinations *= (r[1] - r[0] + 1)

    return num_combinations


def run_workflow_using_parameter_ranges_and_get_num_accepted_combinations(
        workflows: Dict[str, List[Union[str, List[str]]]],
        workflow_name: str,
        param_ranges: List[List[int]]
) -> int:
    num_combinations = 0
    steps = workflows[workflow_name]
    for condition, goto in steps[:-1]:
        passed_param_ranges = copy.deepcopy(param_ranges)
        not_passed_param_ranges = copy.deepcopy(param_ranges)
        param_idx = PARAM_POSITION_MAPPING[condition[0]]
        boundary_val = int(condition[2:])
        if condition[1] == "<":
            allowed_start = 0
            allowed_end = boundary_val - 1
        elif condition[1] == ">":
            allowed_start = boundary_val + 1
            allowed_end = 4000
        else:
            raise ValueError("Unexpected comparison operator.")

        current_start, current_end = param_ranges[param_idx]
        if allowed_start <= current_start <= allowed_end:
            if not allowed_start <= current_end <= allowed_end:
                passed_param_ranges[param_idx] = [current_start, allowed_end]
                not_passed_param_ranges[param_idx] = [allowed_end + 1, current_end]
        elif allowed_start <= current_end <= allowed_end:
            passed_param_ranges[param_idx] = [allowed_start, current_end]
            not_passed_param_ranges[param_idx] = [current_start, allowed_start - 1]

        if goto == "A":
            num_combinations += get_num_combinations(passed_param_ranges)
        elif goto in workflows.keys():
            num_combinations += run_workflow_using_parameter_ranges_and_get_num_accepted_combinations(
                workflows, goto, passed_param_ranges
            )

        param_ranges = not_passed_param_ranges

    else_goto = steps[-1][0]
    if else_goto == "A":
        num_combinations += get_num_combinations(param_ranges)
    elif else_goto in workflows.keys():
        num_combinations += run_workflow_using_parameter_ranges_and_get_num_accepted_combinations(
            workflows, else_goto, param_ranges
        )

    return num_combinations


def run_workflows_and_sum_ratings_of_accepted_parts(
        workflows: Dict[str, List[Union[str, List[str]]]],
        parts: List[List[int]]
) -> int:
    ratings_sum = 0
    for part in parts:
        ratings_sum += run_workflow(workflows, "in", part)

    return ratings_sum


if __name__ == "__main__":
    with open("../inputs/input19.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    res = run_workflows_and_sum_ratings_of_accepted_parts(*parse_input(in_text))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = run_workflow_using_parameter_ranges_and_get_num_accepted_combinations(
        parse_input(in_text)[0], "in", [[1, 4000] for _ in range(4)]
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
