"""
    program.py: Program structures for worldview solving

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
from itertools import combinations

from collections import defaultdict

from atom import EpistemicModality, Atom, EpistemicAtom, NegationAsFailureAtom
from rule import IndexedRule


class LogicProgram(object):
    def __init__(self, file_handle):
        self._label_id = 1
        self._label_set = set()
        self._label_cache = {}
        self._label_id_lookup = {}
        self.label_to_epistemic_atom_id = defaultdict(list)
        self._atom_id = 1
        self._atom_set = set()
        self._atom_cache = {}
        self._atom_id_lookup = {}
        self.epistemic_atom_cache = {}
        self.program = []
        self.epistemic_atom_id_to_valuation_index_map = None

    def get_program(self):
        """
        Returns the program as a list of strings that can be output to
        file.
        """
        return [str(rule) for rule in self.program]

    def index_atoms(self, program_handle):
        """
        index_epistemic_atoms: indexes atoms in program rules so that
        we can simplify rules and build atom and epistemic atom lookup tables,
        to speed up the process of applying epistemic valuations and determine
        if a coherent world view is possible from a disjunctive logic program.
        Returns:
          - atom_index_cache (dict) -
          - epistemic_atom_index_cache (dict) -
          - indexed_program (set) -
        """

        for rule in program_handle:  # loop over new rules
            new_rule = IndexedRule(head=set(), tail=set(),
                                   atom_dict=self._atom_cache)
            if rule.head:
                for atom_token in rule.head:  # check rule head
                    atom = self.get_atom_information(atom_token)
                    new_rule.head.add(atom.atom_id)
            if rule.tail:
                for atom_token in rule.tail:  # check rule body
                    atom = self.get_atom_information(atom_token)
                    new_rule.tail.add(atom.atom_id)
            self.program.append(new_rule)

        # here we map each epistemic id to a number in an order so that when we
        # apply a valuation it's consistent and unique so we're not testing the
        # same set of valuations twice
        self.epistemic_atom_id_to_valuation_index_map = {
            epistemic_id: valuation_index
            for valuation_index, epistemic_id in
            enumerate(self.epistemic_atom_cache.keys())
        }

    def get_or_create_atom(self, atom):
        """
        Given a newly created logical atom, check to see if one exists of the
        given type. If it doesn't assign it a unique ID and add it to the atoms
        that exist for the program. If it is an epistemic atom add it to the
        epistemic atom cache. This allows fast access to atom information.
        Also identify unique labels and index them here.

        Arguments:
          * atom (Atom/EpistemicAtom/NegationAsFailureAtom)
              an object representing an atom in an epistemic logic program
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

        if isinstance(atom, EpistemicAtom):
            self.epistemic_atom_cache[atom.atom_id] = atom
            self.label_to_epistemic_atom_id[atom.label].append(atom.atom_id)
        return True

    def get_atom_information(self, atom_token):
        """
        Given a logical atom represented as a string of characters, determine
        if it is an epistemic atom, if the atom has strong negation, what
        kind of epistemic modality is used and if it is negated, and whether
        or not negation as failure is used. Finally return an Atom instance
        which holds all this information and assign it an atom ID and if
        applicable an epistemic ID.

        Arguments:
         * atom_token (str) - a logical atom represented as a string.
        """

        atom_negation = False
        epistemic_negation = False
        negation_as_failure = False
        # it's an epistemic atom
        if atom_token.find('K') != -1 or atom_token.find('M') != -1:
            modality = EpistemicModality.BELIEVE
            epistemic_modality_index = atom_token.find('M')
            label = atom_token[1:]
            if epistemic_modality_index == -1:
                epistemic_modality_index = atom_token.find('K')
                modality = EpistemicModality.KNOW
            if epistemic_modality_index != 0 and \
               atom_token[epistemic_modality_index - 1] in ('-', '~'):
                epistemic_negation = True
                label = atom_token[epistemic_modality_index + 1:]
            if atom_token[epistemic_modality_index + 1] in ('-', '~'):
                atom_negation = True
                label = atom_token[epistemic_modality_index + 2:]
            atom = EpistemicAtom(label, modality, atom_negation=atom_negation,
                                 epistemic_negation=epistemic_negation)
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
            if negation_as_failure:
                atom = NegationAsFailureAtom(label, atom_negation)
            else:
                atom = Atom(label, atom_negation)
        created = self.get_or_create_atom(atom)
        if not created:
            atom.atom_id = self._atom_id_lookup[str(atom)]
        return atom

    def get_evaluated_program_and_apply_valuation(self, valuation_tuple):
        """
        Given a tuple of valuations to apply to the epistemic atoms, run
        through each rule, apply the valuations and determine the consequences
        of the valuations to each rule. Here, if a valuation is true for an
        epistemic atom it is removed from the rule meaning that we're
        considering true for the purposes of determining if it leads to a
        valid worldview. If a valuation is false for an epistemic atom the
        entire rule is removed, indicating that since one atom is false in the
        body of a rule its whole rule is unsatisfiable.

        If a rules entire body is true we take the head and say that the head
        is therefore true for the evaluated program.

        Arguments:
         * valuation_tuple (tuple(bool))
           - a tuple of boolean values representing valuations to apply to the
             epistemic atoms in the program.
        """
        evaluated_program = []
        for rule in self.program:
            evaluated_rule = self.get_evaluated_rule_and_apply_valuation(rule, valuation_tuple)
            if evaluated_rule:
                evaluated_program.append(evaluated_rule)
        return evaluated_program

    def get_evaluated_rule_and_apply_valuation(self, rule, valuation_tuple):
        """
        At a rule level go through the rule and check for epistemic atoms, if
        you find one find its index number in the valuation string. Apply it's
        valuation in the atom and work out what that means to the rule in the
        evaluated program. If True remove the atom from the rule body,
        otherwise remove the rule from the program.
        Return the rule string if all True valuations for the epistemic atoms.

        Arguments:
         * valuation_tuple (tuple(bool))
           - a tuple of boolean values representing valuations to apply to the
             epistemic atoms in the program.
        """
        false_valuation = False
        modal_atom_in_rule = False
        for atom_id in rule.tail:
            atom = self._atom_cache[atom_id]
            if not isinstance(atom, EpistemicAtom):
                continue
            # apply the valuation
            modal_atom_in_rule = True
            valuation_index = self.epistemic_atom_id_to_valuation_index_map[atom_id]
            atom.valuation = valuation_tuple[valuation_index]
            if not atom.valuation:
                false_valuation = True
        if not false_valuation or not modal_atom_in_rule:
            return rule.get_rule_string(apply_valuation=True)
        return ''

    def check_optimisations(self):
        """
        Search the label to epistemic atom dictionary and identify any labels
        which appear in an epistemic atom more than once. If they have
        negations or modalities which conflict valuations can be simplified
        to not process these cases.

        """
        optimisation_atom_pairs = []
        for label, e_atom_id_list in self.label_to_epistemic_atom_id:
            if not e_atom_id_list or len(e_atom_id_list) == 1:
                continue
            e_combinations = combinations(e_atom_id_list, 2)
            for e_atom_id_a, e_atom_id_b in e_combinations:
                e_atom_a = self._atom_cache[e_atom_id_a]
                e_atom_b = self._atom_cache[e_atom_id_b]
                if self.check_optimisation(e_atom_a, e_atom_b):
                    optimisation_atom_pairs.append(e_atom_a, e_atom_b)
        return optimisation_atom_pairs

    def check_optimisation(e_atom_a, e_atom_b):
        """
        """
        return (
            self.check_conflicts(e_atom_a, e_atom_b) and
            self.check_conflicts(e_atom_b, e_atom_a)
            ) or \
            self.check_conflicting_negation(e_atom_a, e_atom_b) or \
            self.check_different_modality(e_atom_a, e_atom_b) or \
            self.check_different_modality(e_atom_b, e_atom_a)

    @staticmethod
    def check_conflicts(atom_a, atom_b):
        """
        Given two epistemic atoms, if one is K and doesnt have epistemic
        negation and the other is M and doesnt have epistemic negation
        and their atom negations do not agree we can safely say that any
        valuation where they are both true or both false can't be satisfied.

        Argument:
         * atom_a (EpistemicAtom) - an epistemic atom
         * atom_b (EpistemicAtom) - another epistemic atom
        """
        return (atom_a.modality == EpistemicModality.KNOW and
                atom_b.modality == EpistemicModality.BELIEVE and
                not atom_a.epistemic_negation and
                not atom_b.epistemic_negation and
                atom_a.atom_negation != atom_b.atom_negation)

    @staticmethod
    def check_different_modality(atom_a, atom_b):
        """
        Given two epistemic atoms, if one is K and has epistemic negation and
        the other is M and hasn't and their atom negation is equal we can say
        that any valuation that agrees for both of them cannot be true.

        Argument:
         * atom_a (EpistemicAtom) - an epistemic atom
         * atom_b (EpistemicAtom) - another epistemic atom
        """
        return (atom_a.modality == EpistemicModality.KNOW and
                not atom_a.epistemic_negation and
                atom_b.modality == EpistemicModality.BELIEVE and
                atom_b.epistemic_negation and
                atom_a.atom_negation == atom_b.atom_negation)

    @staticmethod
    def check_conflicting_negation(atom_a, atom_b):
        """
        Given two epistemic atoms, if they have the same modality
        (rather K or M) but they have a conflicting negation status for their
        modality or for their atom (but not both) then we can safely say that
        any valuation which say both of these things are true will be false
        valuations.

        Argument:
         * atom_a (EpistemicAtom) - an epistemic atom
         * atom_b (EpistemicAtom) - another epistemic atom
        """
        return (atom_a.modality == atom_b.modality and
                ((atom_a.atom_negation != atom_b.atom_negation and
                  atom_a.epistemic_negation == atom_b.epistemic_negation) or
                 (atom_a.atom_negation == atom_b.atom_negation and
                  atom_a.epistemic_negation != atom_b.epistemic_negation)))
