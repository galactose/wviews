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
        yield Rule(head=None, tail=None).parse_rule_string(line)


def get_program_lines(file_name):
    for line in get_sanitised_lines(file_name):
        if '%' in line:
            line = line[:line.index('%')]
        # need to implement system such that rules can be staggered over various lines or
        # a line may have multiple rules.
        if not line.index('.') == -1:
            yield line[:line.index('.') + 1].strip().replace('.', '')


def import_answer_set(file_name=''):
    for line in get_sanitised_lines(file_name):
        yield line.strip('\n')


def get_sanitised_lines(file_name=''):
    if not file_name:
        raise StopIteration

    try:
        input_file = file(file_name, 'r')  # need to implement try/except block to catch exceptions
    except IOError:
        sys.stdout.write('\n<file does not exist.>\n')
        raise StopIteration

    for line in input_file:
        try:
            yield line
        except ValueError:
            pass


def export_rules(queue, filename='ans.elp', debug=0):
    if debug:
        sys.stdout.write('export_rules(self, queue, filename = "ans.elp") -> queue\n%s\n' % queue)
    output = file(filename, 'w')
    for line in queue:
        if debug:
            sys.stdout.write('export_rules(self, queue, filename = "ans.elp") -> line\n%s\n' % line)
        if isinstance(line[0], list):  # STILL WORKING HERE
            for head_token_index in range(0, len(line[0])):
                output.write(line[0][head_token_index])
                if head_token_index != len(line[0]) - 1:
                    output.write(' v ')

            output.write(' :- ')
            for tail in range(0, len(line[1])):
                output.write(line[1][tail])
                if tail != len(line[1])-1:
                    output.write(', ')

        elif isinstance(line[0], str):
            for head_token_index in range(0, len(line)):
                output.write(line[head_token_index])
                if head_token_index != len(line)-1:
                    output.write(' v ')
        output.write('.\n')
    output.close()
    return True
