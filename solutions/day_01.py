import re


def parse_file(fd):
    return (fd,)


def task_1(lines):
    re_first_digit = re.compile(r"(\d)")
    re_last_digit = re.compile(r".*(\d)")

    def _calc_calibration_value(l):
        first_digit = re_first_digit.search(l)[1]
        last_digit = re_last_digit.search(l)[1]
        return int(f"{first_digit}{last_digit}")

    return sum(_calc_calibration_value(line) for line in lines)


def task_2(lines):
    str_digits_mapping = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }
    re_first_digit = re.compile(
        r"(\d|zero|one|two|three|four|five|six|seven|eight|nine)"
    )
    re_last_digit = re.compile(
        r".*(\d|zero|one|two|three|four|five|six|seven|eight|nine)"
    )

    def _calc_calibration_value(l):
        raw_first_digit = re_first_digit.search(l)[1]
        raw_last_digit = re_last_digit.match(l)[1]
        first_digit = (
            int(raw_first_digit)
            if raw_first_digit.isdigit()
            else str_digits_mapping[raw_first_digit]
        )
        last_digit = (
            int(raw_last_digit)
            if raw_last_digit.isdigit()
            else str_digits_mapping[raw_last_digit]
        )
        return int(f"{first_digit}{last_digit}")

    return sum(_calc_calibration_value(line) for line in lines)


solution_function_01 = task_1
solution_function_02 = task_2
