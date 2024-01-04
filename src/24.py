import itertools
import time

import numpy as np
from numpy.linalg import LinAlgError
import sympy as sp

EXAMPLE1 = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


def parse_input(text: str, ignore_z: bool = True) -> list[tuple[np.ndarray, np.ndarray]]:
    hailstones = []
    for line in text.strip().split("\n"):
        p_text, v_text = line.strip().split(" @ ")
        p = np.array(list(map(int, p_text.split(", "))))
        v = np.array(list(map(int, v_text.split(", "))))
        if ignore_z:
            p = p[:-1]
            v = v[:-1]
        hailstones.append((p, v))

    return hailstones


def do_trajectories_intersect_in_x_y_plane(
        traj_1: tuple[np.ndarray, np.ndarray],
        traj_2: tuple[np.ndarray, np.ndarray],
        plane_min: int,
        plane_max: int
) -> bool:
    """
    Two trajectories traj_1 = ((x_1, y_1), (u_1, v_1)) and traj_2 = ((x_2, y_2), (u_2, v_2)) intersect iff ∃ t_1, t_2
    so that (x_1, y_1) + t_1 * (u_1, v_1) = (x_2, y_2) + t_2 * (u_2, v_2)
    """
    try:
        times = np.linalg.solve(np.vstack((traj_1[1], -1 * traj_2[1])).T, traj_2[0] - traj_1[0])
        if (
                (times >= 0).all() and
                (plane_min <= traj_1[0] + times[0] * traj_1[1]).all() and
                (traj_1[0] + times[0] * traj_1[1] <= plane_max).all()
        ):
            return True
        else:
            return False
    except LinAlgError as e:
        if str(e) == "Singular matrix":
            # No solution -> trajectories are parallel
            return False
        else:
            raise e


def get_initial_coordinates_of_rock(
        all_trajectories: list[tuple[np.ndarray, np.ndarray]],
) -> np.ndarray:
    """
    The parametrized trajectory of the rock is given by (x_r, y_r, z_r) + (u_r, v_r, w_r) * t. That is, for the rock to
    hit a hailstone (without loss of generality, we choose the first one with index 1), the following system of
    equations must hold:

    (x_1, y_1, z_1) + (u_1, v_1, w_1) * t_1 = (x_r, y_r, z_r) + (u_r, v_r, w_r) * t_1.

    Here, (x_r, y_r, z_r), (u_r, v_r, w_r), and t_1 are unknown. We can eliminate t_1 from the above equations and get:

    I)  y_1 * (u_1 - u_r) + v_1 * (x_r - x_1) = y_r * (u_1 - u_r) + v_r * (x_r - x_1)
    II) z_1 * (u_1 - u_r) + w_1 * (x_r - x_1) = z_r * (u_1 - u_r) + w_r * (x_r - x_1).

    That is, we have two equations but six unknown variables. Considering not only one, but all the N hailstones,
    we arrive at 2N (slightly non-linear) equations for the six unknowns. This system is clearly overdetermined, but due
    to the special structure of the problem input, it turns out to have one unique solution. In principle, the whole
    system of equations for all N hailstones has to be solved, which can indeed be done analytically using a CAS (here
    sympy) in a reasonable amount of time. However, it turns out that only four hailstones need to be considered for the
    solution to be unique.
    """

    x_r, y_r, z_r, u_r, v_r, w_r = sp.symbols("x_r, y_r, z_r, u_r, v_r, w_r")
    eqs = []
    for n in range(4):
        (x, y, z), (u, v, w) = all_trajectories[n]
        eqs.append(sp.Eq(y * (u - u_r) + v * (x_r - x), y_r * (u - u_r) + v_r * (x_r - x)))
        eqs.append(sp.Eq(z * (u - u_r) + w * (x_r - x), z_r * (u - u_r) + w_r * (x_r - x)))

    sol = sp.solve(eqs, [x_r, y_r, z_r, u_r, v_r, w_r])

    return sum(sol[0][:3])


def get_num_intersecting_trajectories(
        all_trajectories: list[tuple[np.ndarray, np.ndarray]],
        plane_min: int,
        plane_max: int
) -> int:
    num_intersections = 0
    for traj_1, traj_2 in itertools.combinations(all_trajectories, 2):
        if do_trajectories_intersect_in_x_y_plane(traj_1, traj_2, plane_min, plane_max):
            num_intersections += 1

    return num_intersections


if __name__ == "__main__":
    with open("../inputs/input24.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    trajectories = parse_input(in_text)
    res = get_num_intersecting_trajectories(trajectories, 200000000000000, 400000000000000)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    trajectories = parse_input(in_text, ignore_z=False)
    res = get_initial_coordinates_of_rock(trajectories)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
