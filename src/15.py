import time
from typing import List, Dict

EXAMPLE1 = "HASH"
EXAMPLE2 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def parse_input(text: str) -> List[str]:
    return text.strip().split(",")


def get_lens_information(lens_text: str) -> List[str]:
    if "=" in lens_text:
        return lens_text.split("=")
    elif "-" in lens_text:
        label, _ = lens_text.split("-")
        return [label, "-1"]
    else:
        raise ValueError("Wrong format for lens information found!")


def parse_input_part_2(text: str) -> List[List[str]]:
    return list(map(get_lens_information, text.strip().split(",")))


def calculate_hash(seq: str) -> int:
    curr_val = 0
    for code in seq.encode('ascii'):
        curr_val += code
        curr_val *= 17
        curr_val = curr_val % 256

    return curr_val


def fill_boxes(lens_information: List[List[str]]) -> List[Dict[str, str]]:
    boxes = [{} for _ in range(256)]
    for label, focal_length in lens_information:
        if focal_length == "-1":
            boxes[calculate_hash(label)].pop(label, None)
        else:
            boxes[calculate_hash(label)][label] = focal_length

    return boxes


def sum_focusing_powers(boxes: List[Dict[str, str]]) -> int:
    power_sum = 0
    for i, box in enumerate(boxes):
        if box:
            for j, (label, focal_length) in enumerate(box.items()):
                power_sum += (i + 1) * (j + 1) * int(focal_length)

    return power_sum


if __name__ == "__main__":
    with open("../inputs/input15.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    res = sum(list(map(calculate_hash, parse_input(in_text))))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum_focusing_powers(fill_boxes(parse_input_part_2(in_text)))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
