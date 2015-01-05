import sys

from serial_device import get_serial_ports
from path_helpers import path
from arduino_helpers.context import auto_context, Board, Uploader


def parse_args():
    """Parses arguments, returns (options, args)."""
    from argparse import ArgumentParser

    available_ports = list(get_serial_ports())
    parser = ArgumentParser(description='Upload AVR `.hex` to '
                            'Arduino-compatible board.')
    parser.add_argument('board_name', help='Arduino board name (e.g., `uno`, '
                        '`mega2560`).')
    parser.add_argument('-V', '--disable-verify', action='store_true',
                        help='Disable automatic verify check when uploading '
                        'data.')
    parser.add_argument('hex', type=path, help='Path to `.hex` file.')
    parser.add_argument('port', help='Serial port.', nargs='+',
                        default=None, choices=available_ports)
    args = parser.parse_args()
    if args.port is None:
        # No serial port was specified.
        if len(available_ports) == 1:
            # There is only one serial port available, so select it
            # automatically.
            args.port = available_ports[0]
        else:
            parser.error('No serial port was specified.  Please select at '
                         'least one of the following ports: %s' %
                         available_ports)

    return args


if __name__ == '__main__':
    args = parse_args()

    print '# Upload `.hex` #'
    print ''
    print '    Board: `%s`' % args.board_name
    print '      Hex: `%s`' % args.hex
    print '     Port: `%s`' % args.port
    print ''
    context = auto_context()
    board = Board(context, args.board_name)
    uploader = Uploader(board)
    for p in args.port:
        uploader.upload(args.hex, p, verify=(not args.disable_verify))
