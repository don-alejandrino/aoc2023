import copy

import numpy
import numpy as np

EXAMPLE1 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

EXAMPLE2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

EXAMPLE3 = """
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
"""


def parse_input(text):
    field = []
    for line in text.strip().split("\n"):
        field.append(list(line.strip()))

    return numpy.array(field)


def get_starting_coordinates(field):
    coords = numpy.where(field == "S")
    assert len(coords[0]) == 1, "Multiple starting points detected!"

    return coords[0][0], coords[1][0]


def get_loop(field):
    orientations = {
        "u": {"|": "u", "F": "r", "7": "l"},
        "d": {"|": "d", "L": "r", "J": "l"},
        "l": {"-": "l", "F": "d", "L": "u"},
        "r": {"-": "r", "7": "d", "J": "u"},
    }

    displacements = {
        "u": (lambda c: (c[0] - 1, c[1])),
        "d": (lambda c: (c[0] + 1, c[1])),
        "l": (lambda c: (c[0], c[1] - 1)),
        "r": (lambda c: (c[0], c[1] + 1)),
    }

    coords = get_starting_coordinates(my_field)
    loop_coords = []

    # Starting point has no initial direction. Find one of the two valid directions
    for direction, index_operation in displacements.items():
        if field[displacements[direction](coords)] in orientations[direction].keys():
            break
    else:
        raise ValueError("Starting point is isolated!")

    cycle_length = 0
    while True:
        cycle_length += 1
        coords = displacements[direction](coords)

        # Store loop_coords in a grid with double resolution. We'll need that later for Part 2
        double_res_grid_x = coords[0] * 2
        double_res_grid_y = coords[1] * 2
        loop_coords.append((double_res_grid_x, double_res_grid_y))
        if direction == 'u':
            loop_coords.append((double_res_grid_x + 1, double_res_grid_y))
        elif direction == 'd':
            loop_coords.append((double_res_grid_x - 1, double_res_grid_y))
        elif direction == 'l':
            loop_coords.append((double_res_grid_x, double_res_grid_y + 1))
        elif direction == 'r':
            loop_coords.append((double_res_grid_x, double_res_grid_y - 1))

        try:
            direction = orientations[direction][field[coords]]
        except KeyError as e:
            if e.args[0] == "S":  # Starting point reached again
                break
            else:
                raise e

    loop_tiles_double_res = np.zeros(tuple(map(lambda x: x * 2, field.shape)), dtype=int)
    loop_coords = np.array(loop_coords)
    loop_tiles_double_res[loop_coords[:, 0], loop_coords[:, 1]] = 1

    return cycle_length // 2, loop_tiles_double_res


def get_num_enclosed_tiles_using_floodfill(loop_tiles_double_res):
    filled_loop_tiles = copy.deepcopy(loop_tiles_double_res)
    coords_to_visit = []

    # Find initial "outside" point
    starting_idx_candidates = numpy.where(filled_loop_tiles == 0)
    coords_to_visit.append([starting_idx_candidates[0][0], starting_idx_candidates[1][0]])
    i_max, j_max = loop_tiles_double_res.shape
    while coords_to_visit:
        # noinspection PyUnresolvedReferences
        i, j = coords_to_visit.pop()
        if filled_loop_tiles[i, j] == 0:
            filled_loop_tiles[i, j] = 2
            if j + 1 < j_max:
                coords_to_visit.append([i, j + 1])
            if j - 1 >= 0:
                coords_to_visit.append([i, j - 1])
            if i + 1 < i_max:
                coords_to_visit.append([i + 1, j])
            if i - 1 >= 0:
                coords_to_visit.append([i - 1, j])

    filled_loop_tiles_original_res = filled_loop_tiles[::2, ::2]
    num_enclosed_tiles = len(numpy.where(filled_loop_tiles_original_res == 0)[0])

    return num_enclosed_tiles


if __name__ == "__main__":
    with open("../inputs/input10.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    my_field = parse_input(in_text)
    loop_length, loop_tiles_in_double_resolution = get_loop(my_field)
    print(loop_length)

    # PART 2
    print(get_num_enclosed_tiles_using_floodfill(loop_tiles_in_double_resolution))
