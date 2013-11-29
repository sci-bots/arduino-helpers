import re
from copy import deepcopy

from path import path
from .hardware import merge
from .hardware.platform import get_platform_config_by_family
from .hardware.boards import get_board_data_by_family
from .hardware.tools import (get_tools_dir_root, get_tools_dir_by_family,
                             get_compiler_dir_by_family)
from .hardware.arduino import (get_libraries_dir_by_family,
                               get_variants_dir_by_family,
                               get_firmwares_dir_by_family,
                               get_bootloaders_dir_by_family,
                               get_cores_dir_by_family, get_arduino_dir_root)


class ArduinoContext(object):
    def __init__(self, arduino_install_home):
        self.arduino_home_path = path(arduino_install_home)

    def get_platform_config_by_family(self):
        return get_platform_config_by_family(self.arduino_home_path)

    def get_variants_dir_by_family(self):
        return get_variants_dir_by_family(self.arduino_home_path)

    def get_bootloaders_dir_by_family(self):
        return get_bootloaders_dir_by_family(self.arduino_home_path)

    def get_cores_dir_by_family(self):
        return get_cores_dir_by_family(self.arduino_home_path)

    def get_firmwares_dir_by_family(self):
        return get_firmwares_dir_by_family(self.arduino_home_path)

    def get_libraries_dir_by_family(self):
        return get_libraries_dir_by_family(self.arduino_home_path)

    def get_arduino_dir_root(self):
        return get_arduino_dir_root(self.arduino_home_path)

    def get_tools_dir_root(self):
        return get_tools_dir_root(self.arduino_home_path)

    def get_tools_dir_by_family(self):
        return get_tools_dir_by_family(self.arduino_home_path)

    def get_compiler_dir_by_family(self):
        return get_compiler_dir_by_family(self.arduino_home_path)

    def get_board_data_by_family(self):
        return get_board_data_by_family(self.arduino_home_path)

    def get_board_names_by_family(self):
        return dict([(k, v.keys()) for k, v in
                     self.get_board_data_by_family().iteritems()])


class Board(object):
    def __init__(self, arduino_context, board_name):
        self.arduino_context = arduino_context
        board_configs_by_family = (self.arduino_context
                                   .get_board_data_by_family())
        self.family = None
        for family, board_configs in board_configs_by_family.iteritems():
            for name in board_configs:
                if board_name == name:
                    self.family = family
        assert(self.family is not None)
        self.name = board_name
        self.config = board_configs_by_family[self.family][board_name]
        self.platform = (self.arduino_context.get_platform_config_by_family()
                          [self.family])
        self.cores_dir = (self.arduino_context.get_cores_dir_by_family()
                          [self.family])
        self.libraries_dir = (self.arduino_context
                              .get_libraries_dir_by_family()[self.family])
        self.variants_dir = (self.arduino_context.get_variants_dir_by_family()
                             [self.family])
        self.firmwares_dir = (self.arduino_context
                              .get_firmwares_dir_by_family()[self.family])
        self.bootloaders_dir = (self.arduino_context
                                .get_bootloaders_dir_by_family()[self.family])
        self.combined_config = deepcopy(self.config)
        merge(self.combined_config, self.platform)

    def resolve(self, var):
        if not re.match(r'{[a-zA-Z_]+(\.[a-zA-Z_]+)*}', var):
            raise ValueError, 'Invalid variable "%s"' % var
        keys = var[1:-1].split('.')
        value = self.combined_config
        for k in keys:
            value = value.get(k, None)
        return value

    def resolve_arduino_vars(self, pattern):
        var_map = dict([(var, self.resolve(var))
                         for var in re.findall(r'{.*?}', pattern)])
        cmd = pattern[:]
        unresolved = []
        resolved = []

        for var, value in var_map.iteritems():
            if value is None:
                unresolved.append(var)
            else:
                cmd = cmd.replace(var, value)
                resolved.append((var, value))
        return cmd, unresolved


class Uploader(object):
    def __init__(self, board_context):
        self.board_context = board_context
        upload_tool = self.board_context.config['upload'].get('tool', None)
        if upload_tool is None:
            self.upload_tool = 'avrdude'
        else:
            self.upload_tool = upload_tool
        self.tools_dir = (self.board_context.arduino_context
                          .get_tools_dir_by_family()
                          [self.board_context.family])

    def bin(self):
        return (self.board_context.arduino_context.get_tools_dir_root()
                .joinpath(self.upload_tool))

    def get_conf(self):
        if self.upload_tool == 'avrdude':
            conf_path = self.tools_dir.joinpath('avr', 'etc', 'avrdude.conf')
            if not conf_path.isfile():
                conf_path = (self.board_context.arduino_context
                             .get_tools_dir_root().joinpath('avrdude.conf'))
            if not conf_path.isfile():
                raise IOError, '`avrdude.conf` not found.'
            return conf_path


class Compiler(object):
    def __init__(self, board_context):
        self.board_context = board_context
        self.bin_dir = (self.board_context.arduino_context
                        .get_compiler_dir_by_family()
                        [self.board_context.family])
        bin_prefix = {'avr': 'avr-', 'sam':
                      'arm-none-eabi-'}[self.board_context.family]
        self.bin_prefix = self.bin_dir.joinpath(bin_prefix)
