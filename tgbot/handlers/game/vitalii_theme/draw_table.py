from typing import Union, List

import numpy as np


def horizontal_line(
    field: Union[List[List[int]], np.array, dict],
    c_symbol: str,
    h_symbol: str,
    min_cell_sizes: List[int],
):
    line = []
    for x in range(len(field)):
        line.extend([c_symbol + h_symbol * min_cell_sizes[x]])
    line.extend([c_symbol, "\n"])

    return line


def draw_table(
    field: Union[List[List[int]], np.array, dict],
    min_cell_size=5,
    c_symbol="+",
    h_symbol="-",
    v_symbol="|",
    zero_placeholder=" ",
):
    if isinstance(field, dict):
        field = [[i[1] for i in v] for k, v in field.items()]
    min_cell_sizes = []
    rotated_field = [list(row) for row in zip(*reversed(field))]
    for row in rotated_field:
        max_number_length = len(str(max(row)))
        min_cell_sizes.append(max(max_number_length, min_cell_size))

    text_data = []
    for y, row in enumerate(field):
        if y == 0:
            text_data.extend(horizontal_line(field, c_symbol, h_symbol, min_cell_sizes))

        for x, value in enumerate(row):
            text_data.extend(
                [
                    v_symbol,
                    str(zero_placeholder if value == 0 else value).center(
                        min_cell_sizes[x]
                    ),
                ],
            )
        text_data.extend([v_symbol, "\n"])

        text_data.extend(horizontal_line(field, c_symbol, h_symbol, min_cell_sizes))

    return "".join(text_data)
