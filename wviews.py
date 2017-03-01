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

import sys

from subprocess import Popen, PIPE, STDOUT
from itertools import product
from answer_set import parse_answer_sets, NO_MODEL_FOR_EVALUATED_PROGRAM
from program.program import LogicProgram
from program import parser
from program.atom import EpistemicModality


class WorldViews(object):
    """
        This program reads in programs containing lists of rules of the form:
                [a-z+[a-z]*[(A-Z+[A-Z]*)] [v a-z*]] :- [[~|-]K|M[a-z]*,]*[[not]a-z*]
            where a-zA-Z represents atoms, v represents disjunction,
            ',' represents conjunction, K and M are modal operators,
            K 'Knows' and M 'Believes'
            and ':-' representing implication (is true if the following is also true)

            Returns:
                - worldviews - the applicable worldviews derived from the rules.
    """

    def __init__(self, file_name):
        self.program_info = LogicProgram(None)
        self.program_info.index_atoms(parser.parse_program(file_name))

    @staticmethod
    def check_atom_valuation(possible_world_view, atom):
        """
            Given a possible world view and an epistemic atom which has an applied valuation, return True if the
            valuation against the atom was correct given the occurrences of the atom in the possible world view and
            the modal operator associated with the atom.

            Arguments:
             * possible_world_view (set(str)) - a returned answer set, {a_1, ..., a_n }
             * atom (Atom) - an atom label, also containing its valuation
        """
        universal_count = 0
        answer_set_count = 0
        one_instance = False

        for answer_set in possible_world_view:
            if atom.valuation_string() in answer_set:
                universal_count += 1
                one_instance = True
                if atom.modality == EpistemicModality.BELIEVE:
                    break
            answer_set_count += 1

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

    def check_valuation_validity(self, possible_world_view):
        """
            #goal: extract the current evaluation on the modal atom
            #     - with the given binary evaluation, the epistemic atom and the found worldview
            #     - if the evaluation is satisfied by the worldview return true
            #     - otherwise for any given epistemic atom and its evaluation, if one fails the whole
            #       evaluation fails.
        """

        for _, epistemic_atom in self.program_info.epistemic_atom_cache.iteritems():
            if not self.check_atom_valuation(possible_world_view, epistemic_atom):
                return False
        return True

    @staticmethod
    def get_valuation_string(epistemic_atom_count):
        """
        Arguments:
         * epistemic_atom_count (int) - How many epistemic atoms exist in the program
        """
        for valuation in product((True, False), repeat=epistemic_atom_count):
            yield valuation

    def generate_worldview(self):
        # posOpt = self.optimisation_feasibilty(stat_struct)
        for valuation in self.get_valuation_string(len(self.program_info.epistemic_atom_cache)):
            # if self.evaluation_skip(posOpt, stat_struct, binModEval)
            #     continue
            evaluated_program = self.program_info.get_evaluated_program_and_apply_valuation(valuation)
            raw_worldview = self.get_possible_worldview(evaluated_program)
            world_view = parse_answer_sets(raw_worldview)
            # checks returned set against original set.
            if world_view != NO_MODEL_FOR_EVALUATED_PROGRAM and self.check_valuation_validity(world_view):
                yield world_view


    @staticmethod
    def get_possible_worldview(evaluated_program):
        dlv_response = Popen(['dlv', '-silent', '--'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        for line in dlv_response.communicate(input='\n'.join(evaluated_program))[0].split('\n'):
            if line:
                yield line

    @staticmethod
    def translate_modality(atom_details):
        """
            transModality:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
        """
        mod = ''
        if (atom_details & 0x1) == 1:
            mod = '-'  # 0x1 is atom negation
        if (atom_details & 0x2) == 2:
            mod = 'K' + mod  # 0x2 is epistemic modality, if true its knows, false if believes
        else:
            mod = 'M' + mod
        if (atom_details & 0x4) == 4: # 0x4 is epistemic negation
            mod = '-' + mod
        return mod


if __name__ == '__main__':
    WORLD_VIEW_SESSION = WorldViews('examples/interview_grounded.elp')
    WORLDVIEWS = []
    for worldview in WORLD_VIEW_SESSION.generate_worldview():
        WORLDVIEWS.append(worldview)

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
