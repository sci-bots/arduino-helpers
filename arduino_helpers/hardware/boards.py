from path import path
from itertools import groupby


def traverse(data):
    results = {}
    if data[0][0]:
        for key, group in groupby([d for d in data if d[0]], lambda x: x[0][0]):
            group_data = list(group)
            results[key] = traverse([(item[0][1:], item[1])
                                     for item in group_data])
        return results
    else:
        return data[0][1]


def get_board_data_dict(boards_path):
    '''
    Return a nested dictionary containing configuration from Arduino-formatted
    `boards.txt` file.
    '''
    boards_data = sorted([line.strip() for line in path(boards_path).lines()
                          if line.strip() and not line.startswith('#')])
    boards_cleaned_data = [(k.split('.'), v) for k, v in [d.split('=') for d in
                                                          boards_data]]
    return traverse(boards_cleaned_data)


def get_board_data_by_family(arduino_home_path):
    '''
    Return a nested dictionary containing configuration from all boards
    supported by an Arduino installation home directory.
    '''
    arduino_home_path = path(arduino_home_path).expand()
    pre_1_5_boards_path = arduino_home_path.joinpath('hardware', 'arduino',
                                                     'boards.txt')
    if pre_1_5_boards_path.isfile():
        # The provided Arduino home is pre-1.5.
        boards_by_family = {'avr': get_board_data_dict(pre_1_5_boards_path)}
    else:
        hardware_family_directory = arduino_home_path.joinpath('hardware',
                                                               'arduino')
        boards_by_family = dict([(str(d.name),
                                  get_board_data_dict(d
                                                      .joinpath('boards.txt')))
                                 for d in hardware_family_directory.dirs()])
    return boards_by_family
