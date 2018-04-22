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
from itertools import product
from rule import Rule, Token


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


class Grounder(object):
    def __init__(self, parsed_program):
        self.parsed_program = parsed_program
        self.variables = list()
        self.ground_values = list()
        self.get_variables_and_domain()

    def get_variables_and_domain(self):
        for rule in self.parsed_program:
            for raw_token in rule.head:
                token = Token(raw_label=raw_token)
                self.variables.extend(token.variables)
                self.variables =  list(set(self.variables))
                self.ground_values.extend(token.ground_values)
                self.ground_values = list(set(self.ground_values))
            for raw_token in rule.tail:
                token = Token(raw_label=raw_token)
                self.variables.extend(token.variables)
                self.variables =  list(set(self.variables))
                self.ground_values.extend(token.ground_values)
                self.ground_values = list(set(self.ground_values))
        self.ground_values.sort()
        self.variables.sort()

    def ground_program(self, parsed_program):
        for rule in parsed_program:
            for grounded_rule in self.ground_rule(rule):
                yield grounded_rule

    def ground_rule(self, rule):
        val_product = product((self.ground_values * len(self.variables)))

        for ground_valuations in val_product:
            head = [str(token) for token in self.ground_tokens(rule.head, ground_valuations)]
            tail = [str(token) for token in self.ground_tokens(rule.tail, ground_valuations)]

            rule_string = ''
            if head and tail:
                rule_string = '%s :- %s' % (' v '.join(head), ', '.join(tail))
            elif tail:
                rule_string = ':- %s' % ', '.join(tail)
            else:
                rule_string = '%s' % (' v '.join(head))
            yield Rule(rule_string)

    def ground_tokens(self, tokens, valuation):
        for token in tokens:
            yield self.ground_token(token, valuation)

    def ground_token(self, raw_token, valuation):
        token = Token(raw_token)
        grounded_token = Token(raw_token)
        grounded_token.args = []
        for argument in token.args:
            if not argument.isupper():
                grounded_token.args.append(argument)
                continue
            try:
                var_index = self.variables.index(argument)
            except ValueError:
                print 'Parsing error with argument %s.' % argument
                exit(1)
            grounded_token.args.append(valuation[var_index])
        return grounded_token
