def parse_file(fd):
    return (list(map(int, line.split())) for line in fd)


def task_1(*report_lines):
    extrapolated = 0
    for line in report_lines:
        while any(value != 0 for value in line):
            extrapolated += line[-1]
            line = [b - a for (a, b) in zip(line[:-1], line[1:])]
    return extrapolated


def task_2(*report_lines):
    extrapolated = 0
    for line in report_lines:
        i = 1
        while any(value != 0 for value in line):
            extrapolated += line[0] * i
            line = [b - a for (a, b) in zip(line[:-1], line[1:])]
            i *= -1
    return extrapolated


solution_function_01 = task_1
solution_function_02 = task_2
