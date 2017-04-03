#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#   rchar.py
#
#   Copyright (C) 2017 Andrew Moe
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
from io import StringIO
from contextlib import redirect_stdout
import unittest

from rchar import main, parse_args

DEFAULT_LENGTH = 256

ERR_RCHAR_YIELD = "`rchar {}` ⊢ '{}' ∉ {}"


def rchar_output_string(*args):
    """
    Execute the program with the provided arguments and capture the STDOUT.
    :param args: The arguments passed to the program.
    :return: The string captured from STDOUT.
    :rtype: str
    """
    result = StringIO()
    with redirect_stdout(result):
        main(parse_args(*args))
    return str(result.getvalue()).rstrip('\n')


class BasicCharacterVerification(unittest.TestCase):

    def test_verify_ctrl33(self):
        """
        Verify that rchar will generate only the 33 ASCII control characters when selected.
        """
        # Execute rchar and re-direct output to buffer
        args = ('--ctrl33', str(DEFAULT_LENGTH))
        rstring = rchar_output_string(args)

        # Verify result
        self.assertEqual(len(rstring), DEFAULT_LENGTH,
                         msg="Generated string length {} != {}".format(len(rstring), DEFAULT_LENGTH))
        for character in rstring:
            int_ord = ord(character)  # Convert char to int
            self.assertTrue(int_ord == 127 or (0 <= int_ord <= 31),
                            msg=ERR_RCHAR_YIELD.format(' '.join(args),
                                                       "ctrl({})".format(int_ord),
                                                       "ASCII[0:31], or 127]"))

    def test_verify_print95(self):
        """
        Verify that rchar will generate only the standard printable 95 ASCII characters when selected.
        """
        # Execute rchar and retrieve
        args = ['--print95', str(DEFAULT_LENGTH)]
        rstring = rchar_output_string(args)

        # Verify result
        self.assertEqual(len(rstring), DEFAULT_LENGTH,
                         msg="Generated string length {} != {}".format(len(rstring), DEFAULT_LENGTH))
        for character in rstring:
            int_ord = ord(character)  # Convert char to int
            self.assertGreaterEqual(int_ord, 32, msg=ERR_RCHAR_YIELD.format(' '.join(args), character, "ASCII[32:126]"))
            self.assertLessEqual(int_ord, 126, msg=ERR_RCHAR_YIELD.format(' '.join(args), character, "ASCII[32:126]"))

    def test_verify_extprint223(self):
        """
        Verify that rchar will generate only the standard+extended printable 223 ASCII characters when selected.
        """
        # Execute rchar and re-direct output to buffer
        args = ['--extprint223', str(DEFAULT_LENGTH)]
        rstring = rchar_output_string(args)

        # Verify result
        self.assertEqual(len(rstring), DEFAULT_LENGTH,
                         msg="Generated string length {} != {}".format(len(rstring), DEFAULT_LENGTH))
        for character in rstring:
            int_ord = ord(character)
            self.assertTrue((32 <= int_ord <= 126) or (128 <= int_ord <= 255),
                            msg=ERR_RCHAR_YIELD.format(' '.join(args), character, "ASCII[32:126], or 128:255]"))

    def test_verify_charscope(self):
        """
        Verify that rchar will generate only the characters from the provided charscope.
        """
        # Generate a random charscope with rchar
        args = ['--full256', str(DEFAULT_LENGTH)]
        charscope = rchar_output_string(args)

        # Execute rchar and re-direct output to buffer
        args = ['--charscope', charscope, str(DEFAULT_LENGTH)]
        rstring = rchar_output_string(args)

        # Verify result
        self.assertEqual(len(rstring), DEFAULT_LENGTH,
                         msg="Generated string length {} != {}".format(len(rstring), DEFAULT_LENGTH))
        for character in rstring:
            self.assertTrue(character in charscope,
                            msg="`rchar {}` ⊢ {} ∉ CHARSCOPE[]".format(' '.join(args), character)),


if __name__ == '__main__':
    unittest.main()
