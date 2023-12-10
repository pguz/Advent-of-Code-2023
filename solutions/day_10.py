from enum import Enum


class Pipe(Enum):
    GROUND = 0
    STARTING = 1
    NORTH_SOUTH = 2
    EAST_WEST = 3
    NORTH_EAST = 4
    NORTH_WEST = 5
    SOUTH_WEST = 6
    SOUTH_EAST = 7


TILES_TO_PIPE_MAPPING = {
    '.': Pipe.GROUND,
    'S': Pipe.STARTING,
    '|': Pipe.NORTH_SOUTH,
    '-': Pipe.EAST_WEST,
    'L': Pipe.NORTH_EAST,
    'J': Pipe.NORTH_WEST,
    '7': Pipe.SOUTH_WEST,
    'F': Pipe.SOUTH_EAST,
}


def _check_if_pipe_connected(maze, _x, _y, _check_func, allowed_pipes):
    _pipe = maze[_y][_x]
    return _check_func(_x, _y) and _pipe in allowed_pipes


CHECK_IF_NORTH_CONNECTED = lambda maze, x, y: _check_if_pipe_connected(
    maze,
    x,
    y - 1,
    lambda _, y: y >= 0,
    [Pipe.NORTH_SOUTH, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST],
)
CHECK_IF_EAST_CONNECTED = lambda maze, x, y: _check_if_pipe_connected(
    maze,
    x + 1,
    y,
    lambda x, _: x < len(maze[0]),
    [Pipe.EAST_WEST, Pipe.NORTH_WEST, Pipe.SOUTH_WEST],
)
CHECK_IF_SOUTH_CONNECTED = lambda maze, x, y: _check_if_pipe_connected(
    maze,
    x,
    y + 1,
    lambda _, y: y < len(maze),
    [Pipe.NORTH_SOUTH, Pipe.NORTH_EAST, Pipe.NORTH_WEST],
)
CHECK_IF_WEST_CONNECTED = lambda maze, x, y: _check_if_pipe_connected(
    maze,
    x - 1,
    y,
    lambda x, _: x >= 0,
    [Pipe.EAST_WEST, Pipe.NORTH_EAST, Pipe.SOUTH_EAST],
)

CONNECTIONS_TO_PIPE_MAPPING = {
    (True, True, False, False): Pipe.NORTH_EAST,
    (True, False, True, False): Pipe.NORTH_SOUTH,
    (True, False, False, True): Pipe.NORTH_WEST,
    (False, True, True, False): Pipe.SOUTH_EAST,
    (False, True, False, True): Pipe.EAST_WEST,
    (False, False, True, True): Pipe.SOUTH_WEST,
}


def parse_file(fd):
    maze = list()
    starting_coords = None
    for j, line in enumerate(fd):
        row = list()
        for i, tile in enumerate(list(line.rstrip())):
            pipe = TILES_TO_PIPE_MAPPING[tile]
            if pipe == Pipe.STARTING:
                starting_coords = (i, j)
            row.append(pipe)
        maze.append(row)

    x_starting, y_starting = starting_coords
    starting_connections = tuple(
        check_if_func(maze, x_starting, y_starting)
        for check_if_func in [
            CHECK_IF_NORTH_CONNECTED,
            CHECK_IF_EAST_CONNECTED,
            CHECK_IF_SOUTH_CONNECTED,
            CHECK_IF_WEST_CONNECTED,
        ]
    )
    starting_pipe = CONNECTIONS_TO_PIPE_MAPPING[starting_connections]
    maze[y_starting][x_starting] = starting_pipe

    return (maze, (starting_pipe, starting_coords))


def _next_move(maze, node, loop, waiting_for_move, steps_number):
    pipe, (x, y) = node

    def _check_if_connected_wrapper(_check_if_connected_func, new_coords):
        _pipe = maze[new_coords[1]][new_coords[0]]
        if new_coords not in loop and _check_if_connected_func(maze, x, y):
            loop.add(new_coords)
            waiting_for_move.append(((_pipe, new_coords), steps_number))

    if pipe in [Pipe.NORTH_SOUTH, Pipe.NORTH_EAST, Pipe.NORTH_WEST]:
        _check_if_connected_wrapper(CHECK_IF_NORTH_CONNECTED, (x, y - 1))
    if pipe in [Pipe.EAST_WEST, Pipe.NORTH_EAST, Pipe.SOUTH_EAST]:
        _check_if_connected_wrapper(CHECK_IF_EAST_CONNECTED, (x + 1, y))
    if pipe in [Pipe.NORTH_SOUTH, Pipe.SOUTH_WEST, Pipe.SOUTH_EAST]:
        _check_if_connected_wrapper(CHECK_IF_SOUTH_CONNECTED, (x, y + 1))
    if pipe in [Pipe.EAST_WEST, Pipe.NORTH_WEST, Pipe.SOUTH_WEST]:
        _check_if_connected_wrapper(CHECK_IF_WEST_CONNECTED, (x - 1, y))


def _go_through_loop(maze, starting_node):
    loop, waiting_for_move = set(starting_node[1]), [(starting_node, 0)]
    steps_number = 0
    while waiting_for_move:
        current_node, steps_number = waiting_for_move.pop(0)
        _next_move(maze, current_node, loop, waiting_for_move, steps_number + 1)
    return loop, steps_number


def task_1(maze, starting_node):
    return _go_through_loop(maze, starting_node)[1]


def task_2(maze, starting_node):
    loop = _go_through_loop(maze, starting_node)[0]

    class State(Enum):
        OPEN_AREA = 1
        ON_PATH_FROM_NORTH = 2
        ON_PATH_FROM_SOUTH = 3

    enclosed_by_the_loop = set()
    for j in range(len(maze)):
        current_state = State.OPEN_AREA
        in_loop = False
        for i in range(len(maze[0])):
            if current_state == State.OPEN_AREA:
                if (i, j) in loop:
                    if maze[j][i] == Pipe.NORTH_SOUTH:
                        in_loop ^= True
                    elif maze[j][i] == Pipe.NORTH_EAST:
                        current_state = State.ON_PATH_FROM_NORTH
                    elif maze[j][i] == Pipe.SOUTH_EAST:
                        current_state = State.ON_PATH_FROM_SOUTH
                    else:
                        raise RuntimeError('Invalid State')
                elif in_loop:
                    enclosed_by_the_loop.add((i, j))
            else:
                assert (i, j) in loop
                if maze[j][i] == Pipe.EAST_WEST:
                    continue
                elif maze[j][i] == Pipe.NORTH_WEST:
                    if current_state == State.ON_PATH_FROM_SOUTH:
                        in_loop ^= True
                    current_state = State.OPEN_AREA
                elif maze[j][i] == Pipe.SOUTH_WEST:
                    if current_state == State.ON_PATH_FROM_NORTH:
                        in_loop ^= True
                    current_state = State.OPEN_AREA
                else:
                    raise RuntimeError('Invalid State')

    return len(enclosed_by_the_loop)


solution_function_01 = task_1
solution_function_02 = task_2
