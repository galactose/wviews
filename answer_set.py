"""
    answer_set.py: functionality for handling answer sets.
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

import re


NO_MODEL_FOR_EVALUATED_PROGRAM = -1


def parse_answer_sets(raw_worldview):
    """
        parse_answer_set: takes unformatted queue of answerset values and
        removes formatting, making a list of lists.

        Arguments:
         * answer_sets (list(str)) - a list of unformatted strings
    """
    answer_set_regex = re.compile(r'{([\W\w]*)}')
    worldview = []
    one_model = False
    for line in raw_worldview:
        one_model = True
        regex_object = answer_set_regex.search(line)
        if regex_object:
            answerset = set()
            for worldview_token in regex_object.group(1).split(','):
                answer_set.add(worldview_token.strip())
            worldview.append(answer_set)
    return worldview if one_model else NO_MODEL_FOR_EVALUATED_PROGRAM
