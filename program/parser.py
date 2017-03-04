"""
    parser.py: Parsing functionality for Wviews
    Copyright (C) 2014  Michael Kelly

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from rule import Rule


def parse_program(file_name):
    """
    parse_program - given a file path, parse a logic program of format:
        a :- b, c. OR
        a v d :- b, c. OR
        b v c. OR
        d.

    to the format:
        [[a], [b, c]] OR
        [[a, d], [b, c]] OR
        [[b, c]] OR
        [[d]] OR

    Arguments:
     - file_name (str) - the path to the logic program to be analysed
    """
    for line in get_program_lines(file_name):
        yield Rule(line)


def get_program_lines(file_name):
    for line in get_sanitised_lines(file_name):
        if '%' in line:
            line = line[:line.index('%')]
        # need to implement system such that rules can be staggered
        # over various lines or a line may have multiple rules.
        if line.index('.') != -1:
            for line_section in line.split('.'):
                raw_token = line_section.strip()
                if raw_token:
                    yield raw_token


def import_answer_set(file_name=''):
    for line in get_sanitised_lines(file_name):
        yield line.strip('\n')


def get_sanitised_lines(file_name=''):
    if not file_name:
        raise StopIteration

    try:
        # need to implement try/except block to catch exceptions
        input_file = file(file_name, 'r')
    except IOError:
        sys.stdout.write('\n<file does not exist.>\n')
        raise StopIteration

    for line in input_file:
        yield line
