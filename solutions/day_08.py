import numpy as np
import re


def parse_file(fd):
    instruction_mapping = {
        'L': 0,
        'R': 1,
    }
    instructions = [instruction_mapping[i] for i in list(fd.readline().rstrip())]
    fd.readline()
    network_nodes = dict()
    re_network_node = re.compile(r"([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)")
    for line in fd:
        network_node_match = re_network_node.match(line)
        network_nodes[network_node_match[1]] = (
            network_node_match[2],
            network_node_match[3],
        )
    return (instructions, network_nodes)


def _traverse_network(network, instructions, starting_node, stop_condition_func):
    current_node = starting_node
    instruction_counter = 0
    while not (stop_condition_func(current_node)):
        current_instruction = instructions[instruction_counter % len(instructions)]
        current_node = network[current_node][current_instruction]
        instruction_counter += 1
    return instruction_counter


def task_1(instructions, network):
    return _traverse_network(
        network,
        instructions,
        starting_node='AAA',
        stop_condition_func=lambda n: n == 'ZZZ',
    )


def task_2(instructions, network):
    starting_nodes = {node for node in network.keys() if node.endswith('A')}
    instruction_counters = [
        _traverse_network(
            network,
            instructions,
            starting_node=current_node,
            stop_condition_func=lambda n: n.endswith('Z'),
        )
        for current_node in starting_nodes
    ]
    return np.lcm.reduce(instruction_counters)


solution_function_01 = task_1
solution_function_02 = task_2
