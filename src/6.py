import math
import re
import time

EXAMPLE1 = """
Time:      7  15   30
Distance:  9  40  200
"""


def parse_input(text):
    lines = text.strip().split("\n")
    race_times = list(
        map(
            lambda s: int(s.strip()),
            re.sub(r"\s+", " ", lines[0].replace("Time:", "").strip()).split(" ")
        )
    )
    record_distances = list(
        map(
            lambda s: int(s.strip()),
            re.sub(r"\s+", " ", lines[1].replace("Distance:", "").strip()).split(" ")
        )
    )

    return list(zip(race_times, record_distances))


def parse_input_kerning(text):
    lines = text.strip().split("\n")
    race_time = int(re.sub(r"\s+", "", lines[0].replace("Time:", "")))
    record_distance = int(re.sub(r"\s+", "", lines[1].replace("Distance:", "")))

    return race_time, record_distance


def get_num_wins_using_brute_force(race):
    num_winning_possibilities = 0
    race_time, record_distance = race
    for button_time in range(race_time + 1):
        distance = (race_time - button_time) * button_time
        if distance > record_distance:
            num_winning_possibilities += 1

    return num_winning_possibilities


def get_num_wins_using_basic_analysis(race):
    """
    We need to find the integer range of x where x * (b - x) > c, see get_num_wins_using_brute_force.
    """
    b, c = race
    x_min = math.floor((b - math.sqrt(b ** 2 - 4 * c)) / 2 + 1)
    x_max = math.ceil((b + math.sqrt(b ** 2 - 4 * c)) / 2 - 1)
    num_wins = x_max - x_min + 1

    return num_wins


if __name__ == "__main__":
    with open("../inputs/input6.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    print("==================== PART 2 ====================")
    print("Brute force:")
    start = time.time()
    res = math.prod(get_num_wins_using_brute_force(r) for r in parse_input(in_text))
    end = time.time()
    print(f"\tResult: {res}\t\t time: {(end - start) * 1000:.3f} ms")
    print("Basic analysis:")
    start = time.time()
    res = math.prod(get_num_wins_using_basic_analysis(r) for r in parse_input(in_text))
    end = time.time()
    print(f"\tResult: {res}\t\t time: {(end - start) * 1000:.3f} ms")

    # PART 2
    print("\n==================== PART 1 ====================")
    print("Brute force:")
    start = time.time()
    res = get_num_wins_using_brute_force(parse_input_kerning(in_text))
    end = time.time()
    print(f"\tResult: {res}\t\t time: {(end - start) * 1000:.3f} ms")
    print("Basic analysis:")
    start = time.time()
    res = get_num_wins_using_basic_analysis(parse_input_kerning(in_text))
    end = time.time()
    print(f"\tResult: {res}\t\t time: {(end - start) * 1000:.3f} ms")
