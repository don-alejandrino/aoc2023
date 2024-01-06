import copy
import time

import numpy as np
from tqdm import tqdm

EXAMPLE1 = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

NODE_INDEX = {}


def parse_input(text: str) -> dict[int, list[int]]:
    graph = {}
    for line in text.strip().split("\n"):
        key, vals = line.strip().split(": ")
        vals = list(vals.strip().split(" "))
        key_id = get_node_id(key)
        val_ids = [get_node_id(val) for val in vals]
        graph[key_id] = val_ids

    return graph


def get_node_id(node_name: str) -> int:
    if node_name in NODE_INDEX.keys():
        return NODE_INDEX[node_name]
    else:
        next_id = len(NODE_INDEX)
        NODE_INDEX[node_name] = next_id
        return next_id


def contract_random_edge(
        graph: dict[int, list[int]],
        node_weights: dict[str, int]
) -> tuple[dict[int, set[int]], : dict[str, int]]:
    node_keep = np.random.choice(list(graph.keys()))
    while not graph[node_keep]:
        node_keep = np.random.choice(list(graph.keys()))
    node_drop = np.random.choice(graph[node_keep])
    graph[node_keep] = graph[node_keep] + graph.pop(node_drop, [])
    for key, vals in graph.items():
        graph[key] = [
            node_keep if val == node_drop else val for val in vals
            if val != key and (val != node_drop or node_keep != key)
        ]
    if node_keep in node_weights.keys():
        node_weights[node_keep] += node_weights.pop(node_drop, 1)
    else:
        node_weights[node_keep] = 1 + node_weights.pop(node_drop, 1)

    return graph


def get_num_nodes(graph: dict[int, list[int]]) -> int:
    nodes = set()
    for key, vals in graph.items():
        nodes.add(key)
        nodes.update(set(vals))

    return len(nodes)


def get_num_edges(graph: dict[int, list[int]]) -> int:
    return sum(map(len, graph.values()))


def contract_graph(
        graph: dict[int, list[int]],
        node_weights: dict[str, int] = None,
        t: int = 2
) -> tuple[dict[int, set[int]], : dict[str, int]]:
    if node_weights is None:
        node_weights = {}
    while len(graph) > t or get_num_nodes(graph) > t:
        graph = contract_random_edge(graph, node_weights)

    return graph, node_weights


def get_three_cut_and_multiply_subgraph_sizes(graph: dict[int, list[int]], num_tries: int = 10) -> int:
    for _ in tqdm(range(num_tries)):
        new_graph = copy.deepcopy(graph)
        new_graph, node_weights = fast_min_cut(new_graph)
        if get_num_edges(new_graph) == 3:
            if len(node_weights) <= 2:
                prod = int(np.prod(np.array(list(node_weights.values()))))
            else:
                raise ValueError("Too may node weights remained after graph contraction!")
            return prod

    raise RuntimeError(f"Could not find graph three-cut after {num_tries} iterations. Please try increasing num_tries.")


def fast_min_cut(graph: dict[int, list[int]], node_weights: dict[str, int] = None, decay_fac: int = 0.666):
    if node_weights is None:
        node_weights = {}
    num_nodes = get_num_nodes(graph)
    if num_nodes <= 6:
        return contract_graph(graph, node_weights)
    else:
        t = int(np.ceil(decay_fac * (1 + num_nodes / np.sqrt(2))))
        result = fast_min_cut(*contract_graph(copy.deepcopy(graph), node_weights.copy(), t))
        if get_num_edges(result[0]) == 3:
            # Three-cut found (due to the specific problem input, there must exist one). Hence, we can abort early
            return result
        else:
            # Karger–Stein tree search
            options = [result, fast_min_cut(*contract_graph(copy.deepcopy(graph), node_weights.copy(), t))]
            return min(options, key=lambda item: get_num_edges(item[0]))


if __name__ == "__main__":
    with open("../inputs/input25.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    res = get_three_cut_and_multiply_subgraph_sizes(parse_input(in_text))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
