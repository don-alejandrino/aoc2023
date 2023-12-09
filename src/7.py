import copy

EXAMPLE1 = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def parse_input(text):
    games = []
    bids = []
    for line in text.strip().split("\n"):
        cards, bid = line.split(" ")
        # Make sorting easier
        cards = cards.replace("T", "a")
        cards = cards.replace("J", "b")
        cards = cards.replace("Q", "c")
        cards = cards.replace("K", "d")
        cards = cards.replace("A", "e")
        games.append(cards)
        bids.append(int(bid))

    return [games, bids]


def downvote_jokers(games):
    joker_voted_cards = []
    for cards in games:
        cards = cards.replace("b", "1")
        joker_voted_cards.append(cards)

    return joker_voted_cards


def bin_by_types(games, original_games=None):
    types = [
        [], [], [], [], [], [], []
    ]
    for i, cards in enumerate(games):
        if len(set(cards)) == 1:
            hand_type = 0
        elif len(set(cards)) == 2:
            occurrences_of_first_card = sum([c == cards[0] for c in cards])
            if occurrences_of_first_card == 4 or occurrences_of_first_card == 1:
                hand_type = 1
            else:
                hand_type = 2
        elif len(set(cards)) == 3:
            occurrences_of_first_card = sum([c == cards[0] for c in cards])
            occurrences_of_second_card = sum([c == cards[1] for c in cards])
            occurrences_of_third_card = sum([c == cards[2] for c in cards])
            if occurrences_of_first_card == 3 or occurrences_of_second_card == 3 or occurrences_of_third_card == 3:
                hand_type = 3
            else:
                hand_type = 4
        elif len(set(cards)) == 4:
            hand_type = 5
        else:
            hand_type = 6

        if original_games is not None:
            cards = original_games[i]
        types[hand_type].append((i, cards))

    return types


def bin_by_types_with_jokers(games):
    joker_games = []
    for cards in games:
        if '1' in cards:
            used_cards = set(cards)
            used_cards.remove("1")
            if not used_cards:  # Only Jokers
                most_frequent_card = "e"
            else:
                most_frequent_card = max(max(used_cards, key=cards.count))
            cards = cards.replace("1", most_frequent_card)
        joker_games.append(cards)

    return bin_by_types(joker_games, games)


def get_sorted_game_ids(bins):
    sorted_bins = copy.deepcopy(bins)
    for b in sorted_bins:
        b.sort(key=lambda x: x[1], reverse=True)

    return reversed([game[0] for sorted_bin in sorted_bins for game in sorted_bin])


def get_winnings(sorted_games, bids):
    winnings_output = []
    for i, game_id in enumerate(sorted_games):
        winnings_output.append((i + 1) * bids[game_id])

    return winnings_output


if __name__ == "__main__":
    with open("../inputs/input7.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    my_games, my_bids = parse_input(in_text)
    sorted_game_ids = get_sorted_game_ids(bin_by_types(my_games))
    print(sum(get_winnings(sorted_game_ids, my_bids)))

    # Part 2
    my_games = downvote_jokers(my_games)
    sorted_game_ids = get_sorted_game_ids(bin_by_types_with_jokers(my_games))
    print(sum(get_winnings(sorted_game_ids, my_bids)))
