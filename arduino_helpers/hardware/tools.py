from path_helpers import path


def get_compiler_dir_by_family(arduino_home_path):
    '''
    Return a dictionary containing the directory containing the `gcc` compiler
    binaries for each processor family supported by an Arduino installation
    home directory.
    '''
    return dict([(f, d.joinpath('bin')) for f, d in
                 get_tools_dir_by_family(arduino_home_path).iteritems()])


def get_tools_dir_by_family(arduino_home_path):
    '''
    Return a dictionary containing the root directory path for each processor
    family supported by an Arduino installation home directory.
    '''
    arduino_home_path = path(arduino_home_path).expand()
    tools_directory = arduino_home_path.joinpath('hardware', 'tools')
    toolchain_by_family = {'avr': 'avr'}
    if tools_directory.joinpath('g++_arm_none_eabi').isdir():
        # This is Arduino 1.5+
        toolchain_by_family['sam'] = 'g++_arm_none_eabi'
    return dict([(f, tools_directory.joinpath(toolchain_by_family[f]))
                 for f in toolchain_by_family])


def get_tools_dir_root(arduino_home_path):
    '''
    Return the root tools directory, which contains the uploading program for
    all processor families, including `avrdude`, and `bossac`.
    '''
    return path(arduino_home_path).expand().joinpath('hardware', 'tools')
