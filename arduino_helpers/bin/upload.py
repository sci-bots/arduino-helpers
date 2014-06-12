from path_helpers import path
from arduino_helpers.context import auto_context, Board, Uploader


def parse_args():
    """Parses arguments, returns (options, args)."""
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Upload AVR `.hex` to '
                            'Arduino-compatible board.')
    parser.add_argument('board_name', help='Arduino board name (e.g., `uno`, '
                        '`mega2560`).')
    parser.add_argument('hex', type=path, help='Path to `.hex` file.')
    parser.add_argument('port')
    args = parser.parse_args()

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
    uploader.upload(args.hex, args.port)
