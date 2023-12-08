import operator
import re
from functools import reduce
from math import ceil, floor, sqrt


def parse_file(fd):
    re_digit = re.compile(r"(\d+)")
    race_time_str = re_digit.findall(fd.readline())
    best_distance_str = re_digit.findall(fd.readline())
    return (race_time_str, best_distance_str)


def _possible_different_records_count(race_time, best_distance):
    t_delta = sqrt(race_time * race_time / 4 - best_distance / 1.0)
    t_1 = floor(0.5 * race_time - t_delta)
    t_2 = ceil(0.5 * race_time + t_delta)
    return t_2 - t_1 - 1


def task_1(race_time_strs, best_distance_strs):
    possible_different_records_counts = [
        _possible_different_records_count(int(race_time_str), int(best_distance_str))
        for race_time_str, best_distance_str in zip(race_time_strs, best_distance_strs)
    ]
    return reduce(
        operator.mul,
        possible_different_records_counts,
        1,
    )


def task_2(race_time_str, best_distance_str):
    race_time = int(''.join(race_time_str))
    best_distance = int(''.join(best_distance_str))
    return _possible_different_records_count(race_time, best_distance)


solution_function_01 = task_1
solution_function_02 = task_2
