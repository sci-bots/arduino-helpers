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
