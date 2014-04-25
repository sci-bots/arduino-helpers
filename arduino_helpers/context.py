from collections import OrderedDict
import re
from copy import deepcopy

from path_helpers import path
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


def nested_dict_iter(nested_dict, keys=None):
    if keys is None:
        keys = []
    for k, v in nested_dict.iteritems():
        if isinstance(v, dict):
            for nested_keys, nested_v in nested_dict_iter(v, keys=keys + [k]):
                yield nested_keys, nested_v
        else:
            yield keys + [k], v


def dump_nested_dict(nested_dict, depth=0, dump_values=False):
    for k, v in nested_dict.iteritems():
        print ('  ' * depth) + '-%s' % k,
        if isinstance(v, dict):
            print ''
            dump_nested_dict(v, depth=depth + 1)
        elif dump_values:
            print ':', v
        else:
            print ''


def resolve(config_dict, var, default_value=None, error_on_not_found=False):
    if not re.match(r'{[a-zA-Z_]+(\.[a-zA-Z_]+)*}', var):
        raise ValueError('Invalid variable "%s"' % var)
    keys = var[1:-1].split('.')
    value = config_dict
    for k in keys:
        if error_on_not_found:
            value = value[k]
        elif value is not None:
            value = value.get(k, default_value)
    return value


class ArduinoContext(object):
    def __init__(self, arduino_install_home):
        self.arduino_home_path = path(arduino_install_home)
        arduino_home = self.arduino_home_path
        # Check if the specified Arduino installation version is pre-1.5.
        self.pre_15 = not arduino_home.joinpath('revisions.txt').isfile()
        if not self.pre_15:
            # The Arduino installation version is 1.5+, which includes
            # information about the IDE run-time configuration.
            match = re.search(r'''
                ^ARDUINO \s+
                (?P<major>\d+) \. (?P<minor>\d+) \. (?P<micro>\d+)'''.strip(),
                              arduino_home.joinpath('revisions.txt').bytes(),
                              re.VERBOSE | re.MULTILINE)
            self.runtime_config = {'runtime':
                                   {'ide': {'path': arduino_home, 'version':
                                            '%s_%s_%s' %
                                            (match.group('major'),
                                             match.group('minor'),
                                             match.group('micro'))}}}
        else:
            # The Arduino installation version is pre-1.5, so there is no IDE
            # run-time configuration available.
            self.runtime_config = None

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
        if self.arduino_context.pre_15:
            self.platform = None
        else:
            self.platform = (self.arduino_context
                             .get_platform_config_by_family()[self.family])

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
        arduino_home = self.arduino_context.arduino_home_path
        self.build_config = {'build': {'arch': self.family.upper(), 'system':
                                       {'path':
                                        arduino_home.joinpath('hardware',
                                                              'arduino',
                                                              self.family
                                                              .lower(),
                                                              'system')}}}
        if self.arduino_context.runtime_config is not None:
            merge(self.combined_config, self.arduino_context.runtime_config)
        if self.platform is not None:
            merge(self.combined_config, self.platform)
        merge(self.combined_config, self.build_config)
        if self.resolve('{compiler.path}') is None:
            compiler_path = self.resolve_recursive('{runtime.ide.path}/'
                                                   'hardware/tools/%s/bin' %
                                                   self.family.lower())[0]
            if path(compiler_path).expand().isdir():
                self.combined_config['compiler']['path'] = compiler_path

    def resolve(self, var, extra_dicts=None):
        if extra_dicts is None:
            extra_dicts = []
        for config_dict in [self.combined_config] + list(extra_dicts):
            value = resolve(config_dict, var)
            if value is not None:
                return value

    def resolve_arduino_vars(self, pattern, extra_dicts=None):
        var_map = dict([(var, self.resolve(var, extra_dicts)) for var in
                        re.findall(r'{.*?}', pattern)])
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

    def resolve_recursive(self, config_str, extra_dicts=None):
        cre_var = re.compile(r'({[a-zA-Z_]+(\.[a-zA-Z_]+)*})')
        resolved_str = None

        resolved_str, unresolved = self.resolve_arduino_vars(config_str,
                                                             extra_dicts)

        most_recent_unresolved_matches = None
        unresolved_matches = cre_var.findall(resolved_str)

        # Since Arduino configuration values may contain `{...}`-style
        # replacement strings, retry resolving variables until all remaining
        # replacement strings cannot be resolved using the available
        # configuration data.
        while (resolved_str is None or most_recent_unresolved_matches !=
               unresolved_matches):
            resolved_str, unresolved = self.resolve_arduino_vars(resolved_str,
                                                                 extra_dicts)
            most_recent_unresolved_matches = unresolved_matches
            unresolved_matches = cre_var.findall(resolved_str)
        # Without the replacement below, some strings have extraneous escaped
        # quotes, _e.g._,
        #   \'-DUSB_MANUFACTURER="Unknown"\' \'-DUSB_PRODUCT="Arduino Due"\'
        resolved_str = resolved_str.replace("\'", '')
        return resolved_str, unresolved

    @property
    def mcu(self):
        return self.config['build']['mcu']


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

    @property
    def flags(self):
        return OrderedDict([
            ('-C', self.conf_path),
            ('-c', self.protocol),
            ('-p', self.board_context.mcu),
            ('-b', self.speed),
        ])

    @property
    def arduino_extra_flags(self):
        return OrderedDict([
            # Disable auto erase for flash memory.
            # __NB__ Enabled by default by Arduino IDE.
            ('-D', None),
        ])

    @property
    def protocol(self):
        return self.board_context.config['upload']['protocol']

    @property
    def speed(self):
        return int(self.board_context.config['upload']['speed'])

    @property
    def maximum_size(self):
        return int(self.board_context.config['upload']['maximum_size'])

    def bin(self):
        return (self.board_context.arduino_context.get_tools_dir_root()
                .joinpath(self.upload_tool))

    @property
    def conf_path(self):
        if self.upload_tool == 'avrdude':
            conf_path = self.tools_dir.joinpath('avr', 'etc', 'avrdude.conf')
            if not conf_path.isfile():
                conf_path = (self.board_context.arduino_context
                             .get_tools_dir_root().joinpath('avrdude.conf'))
            if not conf_path.isfile():
                raise IOError('`avrdude.conf` not found.')
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
