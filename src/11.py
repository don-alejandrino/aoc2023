import numpy as np

EXAMPLE1 = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def parse_input(text):
    input_as_list_of_lists = []
    for line in text.strip().split("\n"):
        input_as_list_of_lists.append(list(line.strip()))

    return np.array(input_as_list_of_lists)


def get_empty_space(matrix):
    i_max, j_max = matrix.shape

    empty_row_idcs = []
    for i in range(i_max):
        row_elements = np.unique(matrix[i, :])
        if len(row_elements) == 1 and row_elements[0] == ".":
            empty_row_idcs.append(i)

    empty_col_idcs = []
    for j in range(j_max):
        col_elements = np.unique(matrix[:, j])
        if len(col_elements) == 1 and col_elements[0] == ".":
            empty_col_idcs.append(j)

    return empty_row_idcs, empty_col_idcs


def index_galaxies(matrix, empty_row_idcs, empty_col_idcs, blow_up_factor):
    galaxy_idcs = {}
    counter = 0
    for (i, j), val in np.ndenumerate(matrix):
        if val == "#":
            blown_up_i = i
            for r in empty_row_idcs:
                if r < i:
                    blown_up_i += blow_up_factor - 1
                else:
                    break

            blown_up_j = j
            for c in empty_col_idcs:
                if c < j:
                    blown_up_j += blow_up_factor - 1
                else:
                    break

            galaxy_idcs[counter] = (blown_up_i, blown_up_j)
            counter += 1

    return galaxy_idcs


def get_sum_of_path_lengths(galaxy_idcs):
    sum_of_path_lengths = 0
    galaxy_keys = list(galaxy_idcs.keys())
    for i in galaxy_keys:
        for j in galaxy_keys[i + 1:]:
            i_x, i_y = galaxy_idcs[i]
            j_x, j_y = galaxy_idcs[j]
            sum_of_path_lengths += abs(j_x - i_x) + abs(j_y - i_y)

    return sum_of_path_lengths


if __name__ == "__main__":
    with open("../inputs/input11.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    observation_array = parse_input(in_text)
    empty_rows, empty_cols = get_empty_space(observation_array)
    print(get_sum_of_path_lengths(index_galaxies(observation_array, empty_rows, empty_cols, 2)))

    # PART 2
    print(get_sum_of_path_lengths(index_galaxies(observation_array, empty_rows, empty_cols, 1000000)))
