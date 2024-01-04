from __future__ import annotations
import re
import time

import numpy as np

EXAMPLE1 = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

DISPLACEMENTS = [
    (lambda c: (c[0], c[1] - 1)),
    (lambda c: (c[0], c[1] + 1)),
    (lambda c: (c[0] - 1, c[1])),
    (lambda c: (c[0] + 1, c[1])),
]


def parse_input(text: str, ignore_slopes: bool = False) -> np.ndarray:
    grid = []
    for line in text.strip().split("\n"):
        if ignore_slopes:
            line = re.sub(r"[<>v^]", ".", line)
        grid.append(list(line.strip()))

    return np.array(grid)


def find_start_and_end_coordinates(hiking_map: np.ndarray) -> tuple[tuple[int, int]]:
    i_max = hiking_map.shape[0]
    start_pos = (0, np.where(hiking_map[0, :] == ".")[0][0])
    end_pos = (i_max - 1, np.where(hiking_map[-1, :] == ".")[0][0])

    # noinspection PyTypeChecker
    return start_pos, end_pos


def build_map_graph(
        hiking_map: np.ndarray,
        starting_position: tuple[int, int],
        ending_position: tuple[int, int]
) -> dict[tuple[int, int], set[tuple[tuple[int, int]], int]]:
    map_graph = {}
    i_max, j_max = hiking_map.shape

    paths = [(starting_position, starting_position)]
    seen_paths = set()
    while paths:
        node_pos, pos = paths.pop(0)
        if pos in seen_paths:
            continue
        if node_pos not in map_graph.keys():
            map_graph[node_pos] = set()
        seen_paths.add(pos)

        num_steps = 0
        visited_positions_on_way_to_next_node = {node_pos}
        while True:
            visited_positions_on_way_to_next_node.add(pos)
            if pos == ending_position:
                map_graph[node_pos].add((pos, num_steps))
                break

            num_steps += 1
            next_possible_positions = []
            for next_pos in [DISPLACEMENTS[n](pos) for n in range(4)]:
                if (
                    0 <= next_pos[0] < i_max and 0 <= next_pos[1] < j_max and
                    next_pos not in visited_positions_on_way_to_next_node and
                    (
                        hiking_map[next_pos] == "." or
                        (hiking_map[next_pos] == ">" and next_pos[1] > pos[1]) or
                        (hiking_map[next_pos] == "<" and next_pos[1] < pos[1]) or
                        (hiking_map[next_pos] == "v" and next_pos[0] > pos[0]) or
                        (hiking_map[next_pos] == "^" and next_pos[0] < pos[0])
                    )
                ):
                    next_possible_positions.append(next_pos)
            if len(next_possible_positions) == 1:
                # No alternative where to go
                pos = next_possible_positions[0]
            elif len(next_possible_positions) == 0:
                # Dead end
                break
            else:
                # Next node reached
                for npp in next_possible_positions:
                    paths.append((pos, npp))
                map_graph[node_pos].add((pos, num_steps))
                break

    return map_graph


def find_longest_path(
        map_graph: dict[tuple[int, int], set[tuple[tuple[int, int]], int]],
        start_node: tuple[int, int],
        end_node: tuple[int, int],
        visited_nodes: set[tuple[int, int]]
) -> int:
    if start_node in visited_nodes:
        return -np.inf
    else:
        visited_nodes.add(start_node)

    next_nodes = map_graph.get(start_node)
    if next_nodes:
        best_sub_path_length = -np.inf
        for nn, distance in next_nodes:
            sub_path_length = find_longest_path(map_graph, nn, end_node, visited_nodes.copy()) + distance
            if sub_path_length >= best_sub_path_length:
                best_sub_path_length = sub_path_length

        return best_sub_path_length

    if start_node == end_node:
        return 0
    else:
        return -np.inf


if __name__ == "__main__":
    with open("../inputs/input23.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    hike_map = parse_input(in_text)
    # noinspection PyTupleAssignmentBalance
    start_position, end_position = find_start_and_end_coordinates(hike_map)
    graph = build_map_graph(hike_map, start_position, end_position)
    res = find_longest_path(graph, start_position, end_position, set())
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    hike_map = parse_input(in_text, ignore_slopes=True)
    # noinspection PyTupleAssignmentBalance
    start_position, end_position = find_start_and_end_coordinates(hike_map)
    graph = build_map_graph(hike_map, start_position, end_position)
    res = find_longest_path(graph, start_position, end_position, set())
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
