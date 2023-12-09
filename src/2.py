import re

EXAMPLE1 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def get_game_statistics(input_str):
    game_stats = {}
    game_texts = input_str.strip().split("\n")
    for game_text in game_texts:
        game_number_match = re.match(r"Game\s(\d+):", game_text)
        if game_number_match is not None:
            game_number = int(game_number_match.groups(1)[0])
        else:
            raise ValueError("No game number provided.")
        blues = map(int, re.findall(r"(\d+)\sblue", game_text))
        reds = map(int, re.findall(r"(\d+)\sred", game_text))
        greens = map(int, re.findall(r"(\d+)\sgreen", game_text))
        game_stats[game_number] = {"blue": blues, "red": reds, "green": greens}

    return game_stats


def get_possible_games(num_cubes, game_stats):
    possible_game_numbers = []
    for game, color_stats in game_stats.items():
        for color, num_views in color_stats.items():
            if max(num_views) > num_cubes[color]:
                break
        else:
            possible_game_numbers.append(game)

    return possible_game_numbers


def get_min_cubes(game_stats):
    min_cubes = {}
    for game, color_stats in game_stats.items():
        min_cubes[game] = {color: 0 for color in ("blue", "red", "green")}
        for color, num_views in color_stats.items():
            min_cubes[game][color] = max(num_views)

    return min_cubes


def get_product_sum(min_cube_dict):
    res = 0
    for num_cubes in min_cube_dict.values():
        power = 1
        for num in num_cubes.values():
            power *= num
        res += power

    return res


if __name__ == '__main__':
    with open("../inputs/input2.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    num_cubes_in_bag = {"red": 12, "green": 13, "blue": 14}
    game_statistics = get_game_statistics(in_text)
    print(sum(get_possible_games(num_cubes_in_bag, game_statistics)))

    # PART 2
    min_cubes_per_game = get_min_cubes(get_game_statistics(in_text))
    print(get_product_sum(min_cubes_per_game))
