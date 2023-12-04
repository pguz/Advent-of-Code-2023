import re


def parse_file(fd):
    re_game_data = re.compile(r"Game (?P<game_id>\d+): (?P<game_content>.*)")
    re_cubes = re.compile(r"(?P<cubes_number>\d+) (red|blue|green)")
    games = dict()
    for line in fd:
        game = re_game_data.match(line)
        game_id, game_content = game['game_id'], game['game_content']
        games[game_id] = [
            [(int(cn), cc) for cn, cc in re_cubes.findall(cubes_subset)]
            for cubes_subset in game_content.split(';')
        ]
    return (games,)


def task_1(games):
    cubes_max_number_validity = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    def valid_game(game_content):
        for cubes_subset in game_content:
            for cubes_number, cube_color in cubes_subset:
                if cubes_number > cubes_max_number_validity[cube_color]:
                    return False
        return True

    return sum(
        int(game_id)
        for game_id, game_content in games.items()
        if valid_game(game_content)
    )


def task_2(games):
    def _calculate_power_set_cubes(cubes_set):
        cubes = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }
        for cubes_subset in cubes_set:
            for cubes_number, cube_color in cubes_subset:
                cubes[cube_color] = max(cubes_number, cubes[cube_color])
        return cubes['red'] * cubes['green'] * cubes['blue']

    return sum(
        _calculate_power_set_cubes(game_content) for _, game_content in games.items()
    )


solution_function_01 = task_1
solution_function_02 = task_2
