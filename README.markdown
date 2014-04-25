Arduino configuration classes
=============================

The `arduino_helpers.context` module provides several helper classes, which
extract board and build configuration information from an Arduino installation
directory.

    >>> from pprint import pprint
    >>> from arduino_helpers.context import ArduinoContext, Board, Uploader
    >>> # In Ubuntu, the Arduino IDE is installed in `/usr/share/arduino`.
    >>> context = ArduinoContext('/usr/share/arduino/')

There are several methods to query various information, parsed from the Arduino
IDE configuration files.  For example:

    >>> context.
    context.arduino_home_path              context.get_libraries_dir_by_family
    context.get_arduino_dir_root           context.get_platform_config_by_family
    context.get_board_data_by_family       context.get_tools_dir_by_family
    context.get_board_names_by_family      context.get_tools_dir_root
    context.get_bootloaders_dir_by_family  context.get_variants_dir_by_family
    context.get_compiler_dir_by_family     context.pre_15
    context.get_cores_dir_by_family        context.runtime_config
    context.get_firmwares_dir_by_family

Now, let's print the list of available `avr`-based Arduino boards _(in Arduino
versions <1.5, `avr` is the only board family)_:

    >>> pprint(context.get_board_names_by_family()['avr'])
    ['mini',
     'pro',
     'lilypad',
     'lilypad328',
     'pro328',
     'nano',
     'atmega8',
     'robotMotor',
     'pro5v',
     'fio',
     'mega2560',
     'atmega168',
     'pro5v328',
     'atmega328',
     'bt328',
     'bt',
     'nano328',
     'esplora',
     'diecimila',
     'mega',
     'LilyPadUSB',
     'mini328',
     'micro',
     'robotControl',
     'ethernet',
     'leonardo',
     'uno']

Given an Arduino IDE context, we can create a board context, which provides an
API to query configuration details corresponding to a particular board.  For
example, let's query the configuration of the `uno` board:

    >>> board = Board(context, 'uno')
    >>> board.family
    'avr'
    >>> board.mcu
    'atmega328p'

Given our board context, we can create an uploader context, which provides an
API to query the uploader configuration for our board.  For example:

    >>> uploader = Uploader(board)
    >>> uploader.speed
    115200
    >>> uploader.conf_path
    path('/usr/share/arduino/hardware/tools/avrdude.conf')
    >>> uploader.protocol
    'arduino'
    >>> uploader.maximum_size
    32256

The uploader context provides a `flags` attribute, which returns a dictionary
containing the appropriate `avrdude` configuration flags for uploading.

    >>> pprint(uploader.flags.items())
    [('-C', path('/usr/share/arduino/hardware/tools/avrdude.conf')),
     ('-c', 'arduino'),
     ('-p', 'atmega328p'),
     ('-b', 115200)]

The flags can be used with the `upload_tool` and `tools_dir` to find the
`avrdude` path to form a command.

    >>> uploader.upload_tool
    'avrdude'
    >>> uploader.tools_dir
    path('/usr/share/arduino/hardware/tools/avr')

Note that we can reference any board included in the Arduino IDE configuration
files.  For example, let's look-up the configuration for the `mega2560` board:

    >>> board = Board(context, 'mega2560')
    >>> board.mcu
    'atmega2560'
    >>> uploader = Uploader(board)
    >>> pprint(uploader.flags.items())
    [('-C', path('/usr/share/arduino/hardware/tools/avrdude.conf')),
     ('-c', 'wiring'),
     ('-p', 'atmega2560'),
     ('-b', 115200)]

Note that the uploader flags now reflect the correct options for the
`mega2560`.


Board configurations
====================

The `arduino_helpers.hardware.boards` module provides functions for extracting
board configurations from an Arduino installation directory.

Example usage:

    >>> from arduino_helpers.hardware.boards import get_board_data_by_family
    >>> board_configs_by_family = get_board_data_by_family('~/local/opt/arduino-1.5.4')
    >>> board_configs_by_family.keys()
    ['avr', 'sam']
    >>> board_configs_by_family['avr'].keys()[:5]
    ['mini', 'nano', 'mega', 'micro', 'LilyPadUSB']
    >>> board_configs_by_family['avr']['uno'].keys()
    ['name', 'vid', 'pid', 'upload', 'build', 'bootloader']
    >>> board_configs_by_family['avr']['uno']['name']
    'Arduino Uno'
    >>> board_configs_by_family['avr']['uno']['bootloader']
    {'extended_fuses': '0x05', 'high_fuses': '0xDE', 'low_fuses': '0xFF',
     'lock_bits': '0x0F', 'tool': 'avrdude',
     'file': 'optiboot/optiboot_atmega328.hex', 'unlock_bits': '0x3F'}
    >>> board_configs_by_family['avr']['uno']['build']
    {'core': 'arduino', 'mcu': 'atmega328p', 'f_cpu': '16000000L',
     'board': 'AVR_UNO', 'variant': 'standard'}


Compatiblity
============

The `arduino_helpers.hardware.boards` module is confirmed compatible with
Arduino versions 1.0 and 1.5, but should also work with older Arduino versions.


Credits
=======

Copyright Christian Fobel 2013.
