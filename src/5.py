import copy

EXAMPLE1 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def parse_input(text, seed_ranges=False):
    blocks = text.split("\n\n")
    maps = []
    seeds = list(map(lambda s: int(s.strip()), blocks[0].strip().replace("seeds: ", "").split(" ")))
    if seed_ranges:
        seeds = [[seeds[i], seeds[i] + seeds[i + 1] - 1] for i in range(0, len(seeds), 2)]
    for i, block in enumerate(blocks[1:]):
        maps.append([])
        lines = block.strip().split("\n")
        for line in lines[1:]:
            tgt_start, src_start, num_range = map(lambda s: int(s.strip()), line.strip().split(" "))
            src_end = src_start + num_range - 1
            shift = tgt_start - src_start
            maps[i].append([src_start, src_end, shift])

    return seeds, maps


def get_locations(seeds, maps):
    locations = []
    for seed in seeds:
        for mapping_set in maps:
            for mapping in mapping_set:
                src_start, src_end, shift = mapping
                if src_start <= seed <= src_end:
                    seed = seed + shift
                    break
        locations.append(seed)

    return locations


def get_location_ranges(seed_ranges, maps):
    for mapping_set in maps:
        iteration_seed_ranges = copy.deepcopy(seed_ranges)
        seed_ranges = []
        for seed_range in iteration_seed_ranges:
            for mapping in mapping_set:
                src_start, src_end, shift = mapping
                seed_start, seed_end = seed_range
                if src_start <= seed_start <= src_end:
                    new_seed_start = seed_range[0] + shift
                    if src_start <= seed_end <= src_end:
                        new_seed_end = seed_range[1] + shift
                    else:
                        iteration_seed_ranges.append([src_end + 1, seed_end])
                        new_seed_end = src_end + shift
                    seed_ranges.append([new_seed_start, new_seed_end])
                    break
                elif src_start <= seed_end <= src_end:
                    iteration_seed_ranges.append([seed_start, src_start - 1])
                    new_seed_start = src_start + shift
                    new_seed_end = seed_end + shift
                    seed_ranges.append([new_seed_start, new_seed_end])
                    break
                elif seed_start < src_start and seed_end > src_end:
                    iteration_seed_ranges.append([seed_start, src_start - 1])
                    seed_ranges.append([src_end + 1, seed_end])
                    new_seed_start = src_start + shift
                    new_seed_end = src_end + shift
                    seed_ranges.append([new_seed_start, new_seed_end])
                    break
            else:
                seed_ranges.append(seed_range)

    return seed_ranges


if __name__ == '__main__':
    with open("../inputs/input5.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    print(min(get_locations(*parse_input(in_text))))

    # PART 2
    print(min([x[0] for x in get_location_ranges(*parse_input(in_text, seed_ranges=True))]))
