# noinspection SpellCheckingInspection
EXAMPLE1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

# noinspection SpellCheckingInspection
EXAMPLE2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def get_calibration_number(input_text):
    res = 0
    for line in input_text.strip().split("\n"):
        first_char = next_char = None
        for char in line:
            if str.isdigit(char):
                if first_char is None:
                    first_char = int(char)
                next_char = int(char)
        assert first_char is not None and next_char is not None, (
            "No number found in input line " + line
        )
        res += int(f"{first_char}{next_char}")

    return res


def get_corrected_calibration_number(input_text):
    num_dict = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    res = 0
    for line in input_text.strip().split("\n"):
        first_char = next_char = None
        for i, char in enumerate(line):
            found_num = None
            if str.isdigit(char):
                found_num = int(char)
            else:
                for n in range(3, 6):
                    lookahead = line[i:i + n]
                    found_num = num_dict.get(lookahead, None)
                    if found_num is not None:
                        break
            if found_num is not None:
                if first_char is None:
                    first_char = found_num
                next_char = found_num

        assert first_char is not None and next_char is not None, (
                "No number found in input line " + line
        )
        res += int(f"{first_char}{next_char}")

    return res


if __name__ == '__main__':
    with open("../inputs/input1.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    print(get_calibration_number(in_text))

    # PART 2
    print(get_corrected_calibration_number(in_text))
