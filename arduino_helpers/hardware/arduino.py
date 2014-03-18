from path_helpers import path


def get_dir_by_family(arduino_home_path, dir_name):
    '''
    Return a dictionary containing the specified directory path for each
    processor family supported by an Arduino installation home directory.
    '''
    return dict([(family, d.joinpath(dir_name)) for family, d in
                 get_arduino_dir_by_family(arduino_home_path).iteritems()])


def get_variants_dir_by_family(arduino_home_path):
    return get_dir_by_family(arduino_home_path, 'variants')


def get_bootloaders_dir_by_family(arduino_home_path):
    return get_dir_by_family(arduino_home_path, 'bootloaders')


def get_cores_dir_by_family(arduino_home_path):
    return get_dir_by_family(arduino_home_path, 'cores')


def get_firmwares_dir_by_family(arduino_home_path):
    return get_dir_by_family(arduino_home_path, 'firmwares')


def get_libraries_dir_by_family(arduino_home_path):
    return get_dir_by_family(arduino_home_path, 'libraries')


def get_arduino_dir_by_family(arduino_home_path):
    '''
    Return a dictionary containing the `hardware/arduino` directory path for
    each processor family supported by an Arduino installation home directory.
    '''
    arduino_dir = get_arduino_dir_root(arduino_home_path)
    if arduino_dir.joinpath('cores').isdir():
        # This is Arduino < 1.5
        return {'avr': arduino_dir}
    else:
        # Assume this is Arduino 1.5+
        return dict([(str(d.name), d) for d in arduino_dir.dirs()])


def get_arduino_dir_root(arduino_home_path):
    '''
    Return the root `hardware/arduino` directory, which contains the cores,
    etc. for each processor family.
    '''
    return path(arduino_home_path).expand().joinpath('hardware', 'arduino')
