"""Parse Arguments.

All the special stuff needed to parse arguments like validating colors and
intensity.
"""
from argparse import ArgumentParser, ArgumentTypeError, Action


def range_type(astr, minimum=1, maximum=10):
    value = int(astr)
    if minimum <= value <= maximum:
        return value
    else:
        raise ArgumentTypeError(f'value not in range [{min}-{max}]')


def parse_args():
    p = ArgumentParser(description="Creates a rainfall effect in the CLI.")

    p.add_argument('COLORS', nargs='*',
                   default=["blue", "b_blue"],
                   help="Choose which COLORS to use.")
    p.add_argument('--monochrome', '-m', action='store_true',
                   help="Enables monochrome mode.")

    p.add_argument('--intensity', '-i', type=range_type,
                   default=1,
                   help="Intensity of the rainfall in the range of "
                        "[%(minimum)d-%(maximum)d]. Default is %(default).")
    return p.parse_args()
