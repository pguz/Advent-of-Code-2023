import re


def parse_file(fd):
    re_seed = re.compile(r"(\d+)")
    re_categories_map = re.compile(r"(\w+)-to-(\w+) map:")
    re_src_dst_map = re.compile(r"(\d+) (\d+) (\d+)")
    seeds = list(map(int, re_seed.findall(fd.readline())))
    categories_mapping = list()
    for line in fd:
        if re_categories_map.match(line):
            src_dst_mapping = list()
            for subline in fd:
                if not (re_map_match := re_src_dst_map.match(subline)):
                    break
                dst_start, src_start, range_length = (
                    int(re_map_match[1]),
                    int(re_map_match[2]),
                    int(re_map_match[3]),
                )
                src_dst_mapping.append(
                    (src_start, src_start + range_length - 1, dst_start)
                )
            categories_mapping.append(sorted(src_dst_mapping))

    return (
        seeds,
        categories_mapping,
    )


def task_1(positions, categories_mapping):
    positions = sorted(positions)
    for src_dst_mapping in categories_mapping:
        if positions[0] < src_dst_mapping[0][0]:
            src_dst_mapping.insert(
                0, (positions[0], src_dst_mapping[0][0] - 1, positions[0])
            )
        if positions[-1] > src_dst_mapping[-1][1]:
            src_dst_mapping.append(
                (src_dst_mapping[-1][1] + 1, positions[-1], src_dst_mapping[-1][1] + 1)
            )
        i_position = 0
        new_positions = []
        for src_start, src_end, dst_start in src_dst_mapping:
            if positions[i_position] > src_end:
                continue
            while i_position < len(positions) and positions[i_position] <= src_end:
                new_positions.append(dst_start + positions[i_position] - src_start)
                i_position += 1
            if i_position == len(positions):
                break
        positions = sorted(new_positions)

    return min(positions)


def task_2(position_ranges, categories_mapping):
    position_ranges = sorted(
        [
            [position_ranges[2 * i], position_ranges[2 * i + 1]]
            for i in range(len(position_ranges) // 2)
        ]
    )
    for src_dst_mapping in categories_mapping:
        if position_ranges[0][0] < src_dst_mapping[0][0]:
            src_dst_mapping.insert(
                0,
                (
                    position_ranges[0][0],
                    src_dst_mapping[0][0] - 1,
                    position_ranges[0][0],
                ),
            )
        if position_ranges[-1][0] + position_ranges[-1][1] > src_dst_mapping[-1][1]:
            src_dst_mapping.append(
                (
                    src_dst_mapping[-1][1] + 1,
                    position_ranges[-1][0] + position_ranges[-1][1] - 1,
                    src_dst_mapping[-1][1] + 1,
                )
            )
        i_range = 0
        new_range_positions = []
        for src_start, src_end, dst_start in src_dst_mapping:
            if position_ranges[i_range][0] > src_end:
                continue
            while (
                i_range < len(position_ranges)
                and position_ranges[i_range][0] < src_start
            ):
                start_new_position_range = position_ranges[i_range][0]
                position_range_length = position_ranges[i_range][1]
                length_to_src_start = src_start - start_new_position_range
                length_new_position_range = min(
                    position_range_length, length_to_src_start
                )
                new_range_positions.append(
                    [start_new_position_range, length_new_position_range]
                )
                if position_range_length <= length_to_src_start:
                    i_range += 1
                else:
                    position_ranges[i_range][0] = src_start
                    position_ranges[i_range][1] = (
                        position_range_length - length_to_src_start
                    )
                    break

            while (
                i_range < len(position_ranges)
                and position_ranges[i_range][0] <= src_end
            ):
                start_new_position_range = position_ranges[i_range][0]
                position_range_length = position_ranges[i_range][1]
                length_to_src_end = src_end - start_new_position_range + 1
                length_new_position_range = min(
                    position_range_length, length_to_src_end
                )

                new_range_positions.append(
                    [
                        dst_start + start_new_position_range - src_start,
                        length_new_position_range,
                    ]
                )
                if position_range_length <= length_to_src_end:
                    i_range += 1
                else:
                    position_ranges[i_range][0] = src_end + 1
                    position_ranges[i_range][1] = (
                        position_range_length - length_to_src_end
                    )
                    break
            if i_range == len(position_ranges):
                break

        position_ranges = sorted(new_range_positions)

    return min(position_ranges)[0]


solution_function_01 = task_1
solution_function_02 = task_2
