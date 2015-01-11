"""
    optimisation.py: Optimisations for worldview solving

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

from atom import EpistemicModality, Atom
from rule import IndexedRule


class LogicProgram(object):
    def __init__(self, file_handle):
        self._label_id = 1
        self._label_set = set()
        self._label_cache = {}
        self._label_id_lookup = {}
        self._atom_id = 1
        self._atom_set = set()
        self._atom_cache = {}
        self._atom_id_lookup = {}
        self.epistemic_atom_cache = {}
        self.program = []
        self.epistemic_atom_id_to_valuation_index_map = None

    def get_program(self):
        """
            Returns the program as a list of strings that can be output to file.
        """
        return [str(rule) for rule in self.program]

    def index_atoms(self, program_handle):
        """
            index_epistemic_atoms: indexes atoms in program rules so that we can simplify rules and build atom
                and epistemic atom lookup tables, to speed up the process of applying epistemic valuations and determine
                if a coherent world view is possible from a disjunctive logic program.
            Returns:
             - atom_index_cache (dict) -
             - epistemic_atom_index_cache (dict) -
             - indexed_program (set) -
        """

        for rule in program_handle:  # loop over new rules
            new_rule = IndexedRule(head=set(), tail=set(), atom_dict=self._atom_cache)
            if rule.head:
                for atom_token in rule.head:  # check rule head
                    atom = self.get_atom_information(atom_token)
                    new_rule.head.add(atom.atom_id)
            if rule.tail:
                for atom_token in rule.tail:  # check rule body
                    atom = self.get_atom_information(atom_token)
                    new_rule.tail.add(atom.atom_id)
            self.program.append(new_rule)

        self.epistemic_atom_id_to_valuation_index_map = {
            epistemic_id: valuation_index
            for valuation_index, epistemic_id in enumerate(self.epistemic_atom_cache.keys())
        }

    def get_or_create_atom(self, atom):
        """
            Given a newly created logical atom, check to see if one exists of the given type. If it doesn't assign it a
            unique ID and add it to the atoms that exist for the program. If it is an epistemic atom add it to the
            epistemic atom cache. This allows fast access to atom information.
        """

        if str(atom) in self._atom_set:
            return False

        if atom.label not in self._label_id_lookup:
            atom.label_id = self._label_id
            self._label_cache[self._label_id] = atom.label
            self._label_id_lookup[atom.label] = self._label_id
            self._label_id += 1
        else:
            atom.label_id = self._label_id_lookup[atom.label]
        atom.atom_id = self._atom_id
        self._atom_set.add(str(atom))
        self._atom_id_lookup[str(atom)] = atom.atom_id
        self._atom_cache[atom.atom_id] = atom
        self._atom_id += 1

        if atom.modality:
            self.epistemic_atom_cache[atom.atom_id] = atom
        return True

    def get_atom_information(self, atom_token):
        """
        Given a logical atom represented as a string of characters, determine if it is an epistemic atom, if the atom
        has strong negation, what kind of epistemic modality is used and if it is negated, and whether or not negation
        as failure is used. Finally return an Atom instance which holds all this information and assign it an atom ID and
        if applicable an epistemic ID.

        Arguments:
         * atom_token (str) - a logical atom represented as a string.
        """

        atom_negation = False
        modality = None
        epistemic_negation = False
        negation_as_failure = False

        if atom_token.find('K') != -1 or atom_token.find('M') != -1:  # it's an epistemic atom
            modality = EpistemicModality.BELIEVE
            epistemic_modality_index = atom_token.find('M')
            label = atom_token[1:]
            if epistemic_modality_index == -1:
                epistemic_modality_index = atom_token.find('K')
                modality = EpistemicModality.KNOW
            if epistemic_modality_index != 0 and atom_token[epistemic_modality_index - 1] in ('-', '~'):
                epistemic_negation = True
                label = atom_token[epistemic_modality_index + 1:]
            if atom_token[epistemic_modality_index + 1] in ('-', '~'):
                atom_negation = True
                label = atom_token[epistemic_modality_index + 2:]
        else:
            label = atom_token
            if atom_token[0] in ('-', '~'):
                atom_negation = True
                label = atom_token[1:]
            if atom_token.startswith('not '):
                if '-' in atom_token or '~' in atom_token:
                    raise ValueError
                negation_as_failure = True
                label = atom_token[4:]

        atom = Atom(atom_id=None, label_id=None, label=label, modality=modality, epistemic_negation=epistemic_negation,
                    atom_negation=atom_negation, negation_as_failure=negation_as_failure)

        created = self.get_or_create_atom(atom)
        if not created:
            atom.atom_id = self._atom_id_lookup[str(atom)]
        return atom

    def get_evaluated_program_and_apply_valuation(self, valuation_tuple):
        evaluated_program = []
        for rule in self.program:
            evaluated_rule = self.get_evaluated_rule_and_apply_valuation(rule, valuation_tuple)
            if evaluated_rule:
                evaluated_program.append(evaluated_rule)
        return evaluated_program

    def get_evaluated_rule_and_apply_valuation(self, rule, valuation_tuple):
        false_valuation = False
        modal_atom_in_rule = False
        for atom_id in rule.tail:
            atom = self._atom_cache[atom_id]
            #apply the valuation
            if atom.modality:
                modal_atom_in_rule = True
                atom.valuation = valuation_tuple[self.epistemic_atom_id_to_valuation_index_map[atom_id]]
                if not atom.valuation:
                    false_valuation = True
        return rule.get_rule_string(apply_valuation=True) if not false_valuation or not modal_atom_in_rule else ''

    # def get_interpreted_program_and_apply_valuation(self, valuator_tuple):
    #     """
    #         showPossibleSet: Takes in the queue of rules,
    #                          the line locations of its modal operators,
    #                          the character locations of modal operators,
    #                          and the integer value which determines the truth valuation of each modal operator.
    #     """
    #
    #     count = 0
    #     flag = False
    #     mod_temp = len(stat_struct)
    #     if len(program) > 0 and not mod_temp:
    #         return stat_struct
    #     valuation = copy.deepcopy(program)
    #
    #     self.update_valuation(stat_struct, valuator_string)
    #
    #     for line in stat_struct:
    #         flag = False
    #         for epAtom in stat_struct[line]:
    #             if epAtom[4] == 0:
    #                 flag = True
    #                 break
    #         if flag:
    #             valuation[line].append(1)
    #         else:
    #             valuation[line][1] = self.remove_all_rule_epistemic_atoms(valuation[line][1])
    #             if not valuation[line][1]:
    #                 valuation[line] = valuation[line][0]
    #
    #     total = len(valuation)
    #     tempValuation = []
    #     for line in valuation:
    #         if line[-1] != 1:
    #             tempValuation.append(line)
    #
    #     return tempValuation
