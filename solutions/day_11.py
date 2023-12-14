import numpy as np
import pandas as pd


def parse_file(fd):
    image_raw = pd.DataFrame(
        list(pd.read_csv(fd, header=None).squeeze("columns").map(list))
    )
    image = image_raw.replace({'.': 0, '#': 1})
    return (image,)


def task_impl(image, amplifier):
    expander = amplifier - 1
    expanded_column = (image.sum(axis=0) == 0).tolist()
    expanded_row = (image.sum(axis=1) == 0).tolist()

    coords = [(x, y) for y, x in zip(*np.where(image.values == 1))]
    galaxies_shortest_paths_sum = 0
    for i, (x1, y1) in enumerate(coords):
        for x2, y2 in coords[i + 1 :]:
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            galaxies_shortest_paths_sum += (
                max_x - min_x + expander * sum(expanded_column[min_x:max_x])
            )
            galaxies_shortest_paths_sum += (
                max_y - min_y + expander * sum(expanded_row[min_y:max_y])
            )

    return galaxies_shortest_paths_sum


def task_1(image):
    return task_impl(image, amplifier=2)


def task_2(image):
    return task_impl(image, amplifier=1000000)


solution_function_01 = task_1
solution_function_02 = task_2
