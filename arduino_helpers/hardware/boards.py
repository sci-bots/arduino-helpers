from path_helpers import path

from . import parse_config


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
        boards_by_family = {'avr': parse_config(pre_1_5_boards_path)}
    else:
        hardware_family_directory = arduino_home_path.joinpath('hardware',
                                                               'arduino')
        boards_by_family = dict([(str(d.name),
                                  parse_config(d.joinpath('boards.txt'))) for d
                                 in hardware_family_directory.dirs()])
    return boards_by_family
