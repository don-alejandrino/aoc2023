import numpy

EXAMPLE1 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def get_special_symbols(input_text):
    return {c for c in input_text if not (str.isdigit(c) or c in (".", "\n"))}


def get_number_coordinates(input_matrix):
    number_coords = []
    reversed_number_coord_ids = {}
    number_ids = {}
    number_id_counter = 0

    def update_reversed_number_coords(row_idx, col_idx_left, col_idx_right, value, id_counter):
        for k in range(col_idx_left, col_idx_right + 1):
            reversed_number_coord_ids[(row_idx, k)] = id_counter
        number_ids[id_counter] = value

        return id_counter + 1

    num_rows, num_cols = input_matrix.shape
    for i in range(num_rows):
        found_number = ""
        start_idx = 0
        for j in range(num_cols):
            char = input_matrix[i, j]
            if str.isdigit(char):
                if found_number == "":
                    start_idx = j
                found_number += char
            else:
                if found_number != "":
                    number_coords.append([int(found_number), i, start_idx, j - 1])
                    number_id_counter = update_reversed_number_coords(
                        i, start_idx, j - 1, int(found_number), number_id_counter
                    )
                    found_number = ""
            if j == num_cols - 1 and found_number != "":
                number_coords.append([int(found_number), i, start_idx, j])
                number_id_counter = update_reversed_number_coords(
                    i, start_idx, j, int(found_number), number_id_counter
                )

    return number_coords, reversed_number_coord_ids, number_ids


def get_schematic_matrix(input_text):
    input_arr = input_text.strip().split("\n")
    mat = numpy.empty((len(input_arr), len(input_arr[0])), dtype='str')
    for i, line in enumerate(input_arr):
        for j, char in enumerate(line):
            mat[i, j] = char

    return mat


def get_part_numbers(number_coords, overall_matrix, special_syms):
    part_numbers = []
    # Pad matrix with "." symbols, so that we don't have to deal with boundary edge cases
    overall_matrix = numpy.pad(overall_matrix, 1, constant_values=".")
    for item in number_coords:
        number = item[0]
        # Index needs to be shifted due to padding of the original matrix
        i = item[1] + 1
        j_left = item[2] + 1
        j_right = item[3] + 1
        neighbor_coords = [(i, j_left - 1), (i, j_right + 1)]
        for n in range(j_left - 1, j_right + 2):
            neighbor_coords.extend([(i - 1, n), (i + 1, n)])
        for i, j in neighbor_coords:
            if overall_matrix[i, j] in special_syms:
                part_numbers.append(number)
                break

    return part_numbers


def get_gear_ratios(input_matrix, reversed_number_coord_ids, number_ids):
    gear_ratios = []
    num_rows, num_cols = input_matrix.shape
    for i in range(num_rows):
        for j in range(num_cols):
            char = input_matrix[i, j]
            if char == "*":
                neighbor_coords = [(i, j - 1), (i, j + 1)]
                for n in range(j - 1, j + 2):
                    neighbor_coords.extend([(i - 1, n), (i + 1, n)])
                gear_number_ids = set()
                for n, m in neighbor_coords:
                    gear_number = reversed_number_coord_ids.get((n, m))
                    if gear_number is not None:
                        gear_number_ids.add(gear_number)
                if len(gear_number_ids) == 2:
                    gear_ratios.append(numpy.prod([number_ids[num_id] for num_id in gear_number_ids]))

    return gear_ratios


if __name__ == '__main__':
    with open("../inputs/input3.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    matrix = get_schematic_matrix(in_text)
    number_coordinates, reversed_number_coordinate_ids, number_id_dict = get_number_coordinates(matrix)
    special_symbols = get_special_symbols(in_text)
    print(sum(get_part_numbers(number_coordinates, matrix, special_symbols)))

    # PART 2
    print(sum(get_gear_ratios(matrix, reversed_number_coordinate_ids, number_id_dict)))
