from itertools import zip_longest


def parse_file(fd):
    for row in fd:
        numbers = row.split(": ")[1]
        winning_numbers_str, my_numbers_str = numbers.split(" | ")
        winning_numbers, my_numbers = (
            set(map(int, numbers.split()))
            for numbers in (winning_numbers_str, my_numbers_str)
        )
        yield (winning_numbers, my_numbers)


def task_1(*cards_numbers):
    return sum(
        pow(2, common_numbers_count - 1)
        for winning_numbers, my_numbers in cards_numbers
        if (common_numbers_count := len(winning_numbers & my_numbers))
    )


def task_2(*cards_numbers):
    total_cards = 0
    copies_to_add = []
    for winning_numbers, my_numbers in cards_numbers:
        current_copies = 1
        if copies_to_add:
            current_copies += copies_to_add.pop(0)
        total_cards += current_copies
        if common_numbers_count := len(winning_numbers & my_numbers):
            copies_won = [current_copies] * common_numbers_count
            copies_to_add = [
                c1 + c2
                for c1, c2 in zip_longest(copies_to_add, copies_won, fillvalue=0)
            ]
    return total_cards


solution_function_01 = task_1
solution_function_02 = task_2
