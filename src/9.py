import numpy

EXAMPLE1 = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
0 0 0 0 0 0
"""


def parse_input(text):
    return [
        numpy.array(list(map(lambda s: int(s.strip()), line.strip().split(" ")))) for line in text.strip().split("\n")
    ]


def get_differences(series):
    all_diffs = []
    diffs = numpy.diff(series)
    all_diffs.append(diffs)
    while not numpy.all(diffs == diffs[0]):
        diffs = numpy.diff(diffs)
        all_diffs.append(diffs)

    return all_diffs


def extrapolate(series):
    all_diffs = get_differences(series)
    iterator = list(reversed(all_diffs))
    iterator.append(series)
    extrap = 0
    for diffs in iterator:
        extrap += diffs[-1]

    return extrap


if __name__ == "__main__":
    with open("../inputs/input9.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    print(sum([extrapolate(time_series) for time_series in parse_input(in_text)]))

    # PART 2
    print(sum([extrapolate(time_series[::-1]) for time_series in parse_input(in_text)]))
