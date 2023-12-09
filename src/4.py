import math
import re

EXAMPLE1 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def read_cards(input_text):
    winning_nums = []
    drawn_nums = []
    for line in input_text.strip().split("\n"):
        winning_numbers_match = re.match(r"Card\s+\d+:((?:\s+\d+)+)\s+\|", line)
        drawn_numbers_match = re.search(r"\|((?:\s+\d+)+)", line)

        winning_nums.append([int(x) for x in winning_numbers_match.groups()[0].strip().split()])
        drawn_nums.append([int(x) for x in drawn_numbers_match.groups()[0].strip().split()])

    return winning_nums, drawn_nums


def get_card_worths(winning_nums, drawn_nums):
    card_worths = []
    for wins, drawns in zip(winning_nums, drawn_nums):
        card_worth = 0
        for drawn in drawns:
            if drawn in wins:
                if card_worth == 0:
                    card_worth = 1
                else:
                    card_worth *= 2
        card_worths.append(card_worth)

    return card_worths


def get_number_of_cards(card_worths):
    num_cards = [1] * len(card_worths)
    for i, (worth_current_card, num_current_card) in enumerate(zip(card_worths, num_cards)):
        num_wins = int(math.log2(2 * worth_current_card)) if worth_current_card >= 1 else 0
        for j in range(num_wins):
            if i + 1 + j < len(card_worths):
                num_cards[i + 1 + j] += num_current_card

    return num_cards


if __name__ == "__main__":
    with open("../inputs/input4.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    winning_numbers, drawn_numbers = read_cards(in_text)
    worths = get_card_worths(winning_numbers, drawn_numbers)
    print(sum(worths))

    # PART 2
    print(sum(get_number_of_cards(worths)))
