import math

EXAMPLE1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


EXAMPLE3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def parse_input(text):
    lines = text.strip().split("\n")
    instructions_text = lines[0].strip()
    instructions_text = instructions_text.replace('L', '0').replace('R', '1')
    instructions = list(map(int, list(instructions_text)))

    nodes = {}
    for line in lines[2:]:
        start, end_text = line.split("=")
        start = start.strip()
        left, right = end_text.split(",")
        left = left.replace("(", "").strip()
        right = right.replace(")", "").strip()
        nodes[start] = (left, right)

    return nodes, instructions


def navigate(nodes, instructions, starting_node="AAA", termination_criterion=lambda x: x == "ZZZ"):
    node = starting_node
    instructions_idx = 0
    num_steps = 0
    while not termination_criterion(node):
        num_steps += 1
        node = nodes[node][instructions[instructions_idx]]
        instructions_idx += 1
        if instructions_idx >= len(instructions):
            instructions_idx = 0

    return num_steps


def navigate_ghost(nodes, instructions):
    all_nodes = nodes.keys()
    starting_nodes = []
    for node in all_nodes:
        if node.endswith("A"):
            starting_nodes.append(node)
    num_steps = []
    for node in starting_nodes:
        num_steps.append(
            navigate(nodes, instructions, starting_node=node, termination_criterion=lambda x: x.endswith("Z"))
        )

    return math.lcm(*num_steps)


if __name__ == '__main__':
    with open("../inputs/input8.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    my_nodes, my_instructions = parse_input(in_text)
    print(navigate(my_nodes, my_instructions))

    # PART 2
    print(navigate_ghost(my_nodes, my_instructions))
