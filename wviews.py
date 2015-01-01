"""
    Wviews: Worldview Solver for Epistemic Logic Programs
        Build 1.0 - Port from C++ -> Python.
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

import os
import re
import copy
import math
import sys

from answer_set import parse_answer_sets
from optimisation import LogicProgram
from program import parser
from program.atom import EpistemicModality


class WorldViews(object):
    """
    **************************************************************************
        Author - Michael Kelly BSc CompSci (Hons.), PhD Candidate.

        Summary: This program reads in programs containing lists of
            rules of the form:
                [a-z+[a-z]*[(A-Z+[A-Z]*)] [v a-z*]] :- [[~|-]K|M[a-z]*,]*[[not]a-z*]
            where a-zA-Z represents atoms,
                  v represents disjunction,
                  ',' represents conjunction,
                  K|M represents the modal operators,
                    K: 'Knows' and
                    M: 'Believes'
                  and ':-' representing implication
                    'is true if the following is also true'

            and returns the applicable worldviews derived from the rules.
    **************************************************************************
    """

    def __init__(self, file_name):
        self.program = []
        self.stats = {}
        parser_handle = parser.parse_program(file_name)
        self.stats = LogicProgram(parser_handle)

    @staticmethod
    def check_atom_valuation(possible_world_view, atom, debug=False):
        """
            Given a possible world view and an epistemic atom which has an applied valuation, return True if the
            valuation against the atom was correct given the occurrences of the atom in the possible world view and
            the modal operator associated with the atom.

            - world_view: a returned answer set
            - data, epAtom Position
            - modalOpType - represents modality and negation

        """
        universal_count = 0
        answer_set_count = 0
        one_instance = False

        for answer_set in possible_world_view:
            if atom.valuation_string in answer_set:
                universal_count += 1
                one_instance = True
                if atom.modality == EpistemicModality.BELIEVE:
                    break
            answer_set_count += 1

        if debug:
            sys.stdout.write(
                'wView: %s,\natom: %s,\nvaluation: %s,\nuniversalCount: %s,\nendsetCount: %s,\noneInstance: %s' %
                (possible_world_view, atom, atom.valuation, universal_count, answer_set_count, one_instance)
            )

        if atom.modality == EpistemicModality.KNOW:
            if atom.epistemic_negation and universal_count == answer_set_count:
                return not atom.valuation
            elif not atom.epistemic_negation and universal_count == answer_set_count:
                return atom.valuation
            elif not atom.epistemic_negation and universal_count != answer_set_count:
                return not atom.valuation
            elif atom.epistemic_negation and universal_count != answer_set_count:
                return atom.valuation

        elif atom.modality == EpistemicModality.BELIEVE:
            if atom.epistemic_negation and one_instance:  # NEGATED BELIEF
                return not atom.valuation
            elif atom.epistemic_negation and not one_instance:  # NEGATED BELIEF
                return atom.valuation
            if not atom.epistemic_negation and one_instance:  # POSITIVE BELIEF
                return atom.valuation
            if not atom.epistemic_negation and not one_instance:  # POSITIVE BELIEF
                return not atom.valuation

    def check_valuation_validity(self, possible_world_view, epistemic_program):
        """
            #goal: extract the current evaluation on the modal atom
            #     - with the given binary evaluation, the epistemic atom and the found worldview
            #     - if the evaluation is satisfied by the worldview return true
            #     - otherwise for any given epistemic atom and its evaluation, if one fails the whole
            #       evaluation fails.
        """
        for _, epistemic_atom in epistemic_program.epistemic_atom_cache.iteritems():
            if not self.check_atom_valuation(possible_world_view, epistemic_atom):
                return False
        return True

    @staticmethod
    def translate_modality(eval):
        """
            transModality:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
        """
        mod = ''
        if (eval & 0x1) == 1:
            mod = '-'  # 0x1 is atom negation
        if (eval & 0x2) == 2:
            mod = 'K' + mod  # 0x2 is epistemic modality, if true its knows, false if believes
        else:
            mod = 'M' + mod
        if (eval & 0x4) == 4: # 0x4 is epistemic negation
            mod = '-' + mod
        return mod

    @staticmethod
    def modal_operator_count(stat_struct):
        return sum([len(stat_struct[key]) for key in stat_struct])

    def generate_worldview(self, program, stat_struct):
        """
            show instantiations: removes modal operators in answer sets by assuming they are
            true or false, on the case they are true we remove the modal operator and its atom
            in the case it is false we move the entire rule from the answer set. once this is
            done the answer set is sent to dlv for its stable model
        """

        binary_count = math.pow(2, len(program.epistemic_atom_cache))
        binary_modal_valuation = 0
        good_int_count = 0

        if len(program.epistemic_atom_cache) > 31:
            return

        # posOpt = self.optimisation_feasibilty(stat_struct)

        while binary_count:
            # passCheck = self.evaluation_skip(posOpt, stat_struct, binModEval)
            # if passCheck:
            good_int_count += 1
            program_copy = self.build_interpreted_program(program, stat_struct, binary_modal_valuation)
            parser.export_rules(program_copy, 'ans.elp')
            os.system('./dlv -silent ans.elp > temp2')
            raw_answer_sets = parser.import_answer_set('temp2')  # builds the answer into a queue
            answer_sets = parse_answer_sets(raw_answer_sets)
            # os.system('pause')

            if self.check_valuation_validity(answer_sets, program):  # checks returned set against original set.
                yield answer_sets
            # else:
                # contraCount += 1
            binary_modal_valuation += 1
            binary_count -= 1

    @staticmethod
    def print_opt(opt_type, mod_a, mod_b, debug=False):
        if debug:
            sys.stdout.write('%s mod: %s, atom: %s, modCompare: %s, atom: %s' %
                             (opt_type, mod_a[1], mod_a[2], mod_b[1], mod_b[2]))

    @staticmethod
    def remove_modal_operators(body, rule, epistemic_atom, begin_position):  # NOT COMPLETE
        """
            remove_modal_operators: removes the modal operators present at the front of the rule,
            assumes rule format [a-z* [v a-z*]*] :- [[~|-]K|M[a-z]*,]*[[not]a-z*].
        """
        if len(rule) < begin_position or begin_position == 0:
            return 0
        if rule[begin_position - 1] == '-' or rule[begin_position - 1] == '~':
            begin_position -= 1

        for count in range(begin_position, len(rules)):
            end_position = 0
            if rule[count] == '.' or rule[count] == ',':
                end_position = count

        if rule[end_position] == '.':
            rule = rule[:begin_position - 1] + rule[end_position:len(rule)]
        else:
            rule = rule[:begin_position - 1] + rule[end_position+1:len(rule)]
        for count in range(0, len(body)):
            if body[count].find(epistemic_atom) != -1:
                pass
        return rule

    @staticmethod
    def update_valuation(stat_struct, valuation_string):
        """

        update_valuation: runs through valuation string and the optimisation structure and
        """
        count_b = len(stat_struct)
        while count_b:
            count_a = len(stat_struct[stat_struct.keys()[count_b - 1]])
            while count_a:
                temp = valuation_string & 0x1
                valuation_string >>= 1
                if len(stat_struct[stat_struct.keys()[count_b - 1]][count_a - 1]) == 5:
                    stat_struct[stat_struct.keys()[count_b - 1]][count_a - 1][4] = temp
                elif len(stat_struct[stat_struct.keys()[count_b - 1]][count_a - 1]) < 5:
                    stat_struct[stat_struct.keys()[count_b-1]][count_a-1].append(temp)
                count_a -= 1
            count_b -= 1

    def update_index(self, line_index, dictionary):
        tempDict = {}
        for index in range(0, line_index):
            tempDict[dictionary.keys()[index]] = copy.copy(dictionary[dictionary.keys()[index]])
        for index in range(line_index, len(dictionary.keys())):
            tempDict[dictionary.keys()[index]-1] = copy.copy(dictionary[dictionary.keys()[index]])
        return tempDict

    @staticmethod
    def remove_all_rule_epistemic_atoms(line):
        temp = []
        if isinstance(line, list):
            for index in range(0, len(line)):
                if not line[index].find('K') != -1 and not line[index].find('M') != -1:
                    temp.append(line[index])
        if not len(temp):
            return
        else:
            return temp

    def build_interpreted_program(self, program, stat_struct, valuator_string):
        """
            showPossibleSet: Takes in the queue of rules,
                             the line locations of its modal operators,
                             the character locations of modal operators,
                             and the integer value which determines the truth valuation of each modal operator.
        """

        count = 0
        flag = False
        mod_temp = len(stat_struct)
        if len(program) > 0 and not mod_temp:
            return stat_struct
        valuation = copy.deepcopy(program)

        self.update_valuation(stat_struct, valuator_string)

        for line in stat_struct:
            flag = False
            for epAtom in stat_struct[line]:
                if epAtom[4] == 0:
                    flag = True
                    break
            if flag:
                valuation[line].append(1)
            else:
                valuation[line][1] = self.remove_all_rule_epistemic_atoms(valuation[line][1])
                if not valuation[line][1]:
                    valuation[line] = valuation[line][0]

        total = len(valuation)
        tempValuation = []
        for line in valuation:
            if line[-1] != 1:
                tempValuation.append(line)

        return tempValuation

    def run_session(self):
        world_view_count = 0
        try:
            world_view = self.generate_worldview(self.program, self.stats)
            while True:
                world_view_count += 1
                sys.stdout.write(world_view.next())
        except StopIteration:
            del self

# if __name__ == '__main__':
#     file_path = os.getcwd() + '\\worldviews'
#     files = os.listdir('worldviews')
#     session = WorldViews('worldviews\\interview.txt')
#     worldview_grounder = grounder.grounding(session)
#     countString = []
#     length = 5
#     base = 4
#
#     for count in range(0, length):
#         countString.append(0)
#
#     while 1:
#         countString = worldview_grounder.incString(countString, base, length)
#         os.system('pause')

    # 'worldviews\\interview.txt'
    # for inst in files:
    #    session = elp('worldviews\\' + inst)
    #    session.run_session()
    #    os.system('pause')
    #    os.system('cls')
    #    del session
