#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#   rchar.py
#
#   Copyright (C) 2015 - 2019 Andrew Moe
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. Or, see
#   <http://www.gnu.org/licenses/gpl-2.0.html>.
# -----------------------------------------------------------------------------

import argparse
import itertools
import logging
import random
import sys

__ERR_SYS_RAND_NOT_FOUND = "SystemRandom not supported, defaulting to Python random."
__ERR_STRING_LENGTH = "String length must be greater than zero!"
__ERR_CHARSCOPE_IS_EMPTY = "Charscope is empty."
__ERR_ASCII_RANGE_INVALID = "Input ASCII range out of bounds (0 <= r <= 255)."
__ERR_INTERFACE_FUNC_NOT_CALLABLE = "Interface function not callable."
__ERR_INVALID_PARAMETERS = "Invalid parameters in function!"

# Set default verbosity
verbosity = 0

# Attempt to set SystemRandom as global random class
_randclass = random
try:
    randclass = random.SystemRandom()
except (NotImplementedError, Exception):
    print(__ERR_SYS_RAND_NOT_FOUND, file=sys.stderr)

__version__ = '1.2'
__all__ = ['__version__', 'parse_args', 'main', 'generate_ctrl33', 'generate_print95', 'generate_extprint223',
           'generate_full256', 'generate_string_from_charscope']


def generate_ctrl33(length):
    """Generate a pseudo-random string from the 33 ASCII control characters.
    :param length: The quantity of characters to generate in string.
    :return: The generated string of ASCII control characters
    :rtype: str
    """
    logging.debug("Generating random string from the 33 ASCII control characters. (length = {})".format(length))
    return generate_string_from_charscope(length, "{}{}".format(__range2charscope(0, 31), chr(127)))


def generate_print95(length):
    """Generate a pseudo-random string from the standard printable 95 ASCII characters.
    :param length: The quantity of characters to generate in string.
    :return: The generated string of printable ASCII characters.
    :rtype: str
    """
    logging.debug("Generating random string from the standard printable 95 ASCII characters. (length = {})".format(length))
    return generate_string_from_charscope(length, __range2charscope(32, 126))


def generate_extprint223(length):
    """Generate a pseudo-random string from the standard+extended printable 223 ASCII characters.
    :param length: The quantity of characters to generate in string.
    :return: The generated string from the extended set of printable ASCII characters.
    :rtype: str
    """
    logging.debug("Generating random string from the standard+extended printable 223 ASCII characters. (length = {})".format(length))
    return generate_string_from_charscope(length, "{}{}".format(__range2charscope(32, 126), __range2charscope(128, 255)))


def generate_full256(length):
    """Generate a pseudo-random string from all 256 ASCII characters.
    :param length: The quantity of characters to generate in string.
    :return: The generated string from all 256 ASCII characters.
    :rtype: str
    """
    logging.debug("Generating random string from all 256 ASCII characters. (length = {})".format(length))
    return generate_string_from_charscope(length, __range2charscope(0, 255))


def generate_string_from_charscope(length, charscope):
    """Generate a pseudo-random string from a provided scope of characters.
    :param length: The quantity of characters to generate in string.
    :param charscope: The scope of characters from which to select.
    :return: The generated string from a select set of characters.
    :rtype: str
    """
    assert charscope is not None and charscope is not "", __ERR_CHARSCOPE_IS_EMPTY
    logging.debug("Generating random string from the provided charscope. (length = {}, charscope = {})".format(length, charscope))
    return ''.join(itertools.islice(_RandomCharacter(charscope), length))


def __range2charscope(lobound, hibound):
    """Convert an (int, int) range representing ASCII characters into a string
    containing that full scope of characters.
    :param lobound: The low-range boundary of characters to select.
    :param hibound: The high-range boundary of characters to select.
    :return: A set of characters corresponding to a range of indicies within the ASCII table.
    :rtype: str
    """
    return ''.join(map(chr, range(lobound, hibound + 1)))


def __unit_test():
    """Perform a unit test on this program.
    :return rc: The return code that is a sum of errors experienced in unit test.
    :rtype: int
    """
    rc = 0
    rc += __unit_breakdown(5, generate_ctrl33)
    rc += __unit_breakdown(6, generate_print95)
    rc += __unit_breakdown(7, generate_extprint223)
    rc += __unit_breakdown(8, generate_full256)
    return rc


def __unit_breakdown(length, _func_str):
    """Breakdown the output of a generated string function.
    :param length: The quantity of characters to generate in string.
    :param _func_str: The function to generate a particular random string.
    :return: The return code that is a sum of errors experienced in unit test breakdown.
    :rtype: int
    """
    # Generate string data
    outstr = _func_str.__call__(length)
    len_outstr = len(outstr)

    # Print string analysis
    print("test: %s(%d)" % (_func_str.__name__, length))
    print("len   = %d" % len_outstr)
    print("code  = %s" % outstr.encode())
    print("repr  = %s" % repr(outstr))
    print("print = %s" % outstr)
    print()

    # Validate breakdown
    rc = 0
    if length is not len_outstr:
        rc += 1
    return rc


class _RandomCharacter(object):
    def __init__(self, charscope):
        self.charscope = charscope

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def set_charscope(self, charscope):
        self.charscope = charscope

    def next(self):
        return _randclass.choice(self.charscope)


def parse_args(*args, **kwargs):
    """Parse the arguments received from STDIN.
    :return: The parameters parsed from the input arguments.
    :rtype: Namespace
    """
    # Constructing argument parser
    parser = argparse.ArgumentParser(prog="rchar", description="A handy tool to generate (pseudo-)random ASCII strings.")

    parser.add_argument("length", type=int, nargs='?', default=8,
                        help="The quantity of characters to generate in string.")
    strchoice_group = parser.add_mutually_exclusive_group()
    strchoice_group.add_argument("-c", "--charscope", nargs='?', type=str, const='',
                                 help="A pseudo-random string generated by this charscope.")
    strchoice_group.add_argument("-C", "--ctrl33", action='store_true',
                                 help="A pseudo-random string generated from the 33 ASCII control characters.")
    strchoice_group.add_argument("-P", "--print95", action='store_true',
                                 help="A pseudo-random string generated from the 95 standard ASCII characters "
                                      "(default=True).")
    strchoice_group.add_argument("-E", "--extprint223", action='store_true',
                                 help="A pseudo-random string generated from the 223 standard+extended ASCII "
                                      "characters.")
    strchoice_group.add_argument("-A", "--full256", action='store_true',
                                 help="A pseudo-random string generated from all 256 ASCII characters.")
    strchoice_group.add_argument("--unittest", action='store_true', help=argparse.SUPPRESS)
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Display rchar.py debug output during runtime.")
    parser.add_argument("--version", action='version', version='rchar.py %s' % __version__)

    # Process arguments
    return parser.parse_args(*args, **kwargs)


def main(params):
    """
    Execute the main function of the program.
    :param params: The parameters that dictate the functionality of the program.
    :return: The return code of the main function.
    :rtype: int
    """
    # Set up logging
    if params.verbose > 0:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    # Display program variables
    logging.debug("rchar.py input arguments")
    logging.debug("\tlength \t\t{}".format(params.length))
    logging.debug("\t--charscope \t'{}'".format(params.charscope))
    logging.debug("\t--ctrl33 \t{}".format(params.ctrl33))
    logging.debug("\t--print95 \t{}".format(params.print95))
    logging.debug("\t--extprint223 \t{}".format(params.extprint223))
    logging.debug("\t--full256 \t{}".format(params.full256))
    logging.debug("\t--unittest \t{}".format(params.unittest))
    logging.debug("\t--verbose \t{}".format(params.verbose))

    # Generate string based on parameters
    if params.unittest:
        sys.exit(__unit_test())

    elif params.ctrl33:
        print(generate_ctrl33(params.length))

    elif params.print95:
        print(generate_print95(params.length))

    elif params.extprint223:
        print(generate_extprint223(params.length))

    elif params.full256:
        print(generate_full256(params.length))

    elif params.charscope == '':
        raise Exception("Charscope is undefined.")

    elif params.charscope is not None:
        print(generate_string_from_charscope(params.length, params.charscope))

    else:  # Print
        logging.debug("No options selected. Defaulting to --print95.")
        print(generate_print95(params.length))

    return 0


# Program execution start
if __name__ == "__main__":
    sys.exit(main(parse_args()))
