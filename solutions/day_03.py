def parse_file(fd):
    numbers_info = list()
    symbols_info = list()
    for i_row, row in enumerate(fd):
        current_number_processing = False
        current_number_val = 0
        current_number_idxs = set()
        for i_col, val in enumerate(row):
            if val.isdigit():
                current_number_processing = True
                current_number_val = current_number_val * 10 + int(val)
                current_number_idxs.add((i_row, i_col))
            else:
                if current_number_processing is True:
                    numbers_info.append((current_number_val, current_number_idxs))
                    current_number_val = 0
                    current_number_idxs = set()
                    current_number_processing = False
                if val not in ['.', '\n']:
                    symbols_info.append((val, {
                        (i_row - 1, i_col - 1),
                        (i_row - 1, i_col),
                        (i_row - 1, i_col + 1),
                        (i_row, i_col - 1),
                        (i_row, i_col + 1),
                        (i_row + 1, i_col - 1),
                        (i_row + 1, i_col),
                        (i_row + 1, i_col + 1),
                    }))
    return (numbers_info, symbols_info)

def task_1(numbers_info, symbols_info):
    # compact version:
    #  symbols_area = {symbol_area_cord for _, symbol_area in symbols_info for symbol_area_cord in symbol_area}
    #  return sum(number_val for number_val, number_idxs in numbers_info if number_idxs & symbols_area)

    # detailed version:
    symbols_area = set()
    for _, symbol_area in symbols_info:
       symbols_area.update(symbol_area)

    part_numbers_sum = 0
    for number_val, number_idxs in numbers_info:
        if number_idxs & symbols_area:
            part_numbers_sum += number_val
    return part_numbers_sum

def task_2(numbers_info, symbols_info):
    gear_ratio_sum = 0
    for symbol_val, symbol_area in symbols_info:
        if symbol_val != '*':
            continue
        symbol_matches = []
        for number_val, number_idxs in numbers_info:
            if symbol_area & number_idxs:
                symbol_matches.append(number_val)
        if len(symbol_matches) == 2:
            gear_ratio_sum += (symbol_matches[0] * symbol_matches[1])
    
    return gear_ratio_sum


solution_function_01 = task_1
solution_function_02 = task_2
