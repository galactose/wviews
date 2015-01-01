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

from program.atom import EpistemicModality, Atom


class LogicProgram(object):
    def __init__(self, file_handle):
        self._atom_id = 1
        self._epistemic_id = 1
        self._atom_set = set()
        self._atom_cache = {}
        self._epistemic_atom_cache = {}
        self.program = []

    def get_evaluated_program(self):
        """
            Returns the program as a list of strings that can be output to file.
        """
        return [str(rule) for rule in self.program]

    def index_epistemic_atoms(self, program_handle):
        """
            index_epistemic_atoms: indexes atoms in program rules so that we can simplify rules and build atom
                and epistemic atom lookup tables, to speed up the process of applying epistemic valuations and determine
                if a coherent world view is possible from a disjunctive logic program.
            Returns:
             - atom_index_cache (dict) -
             - epistemic_atom_index_cache (dict) -
             - indexed_program (set) -
        """

        for line in program_handle:  # loop over new rules
            if len(line) == 0:
                continue

            head = []
            for atom_token in line[0]:  # check rule head
                _, atom = self.get_atom_information(atom_token)
                head.append(atom.atom_id)
            tail = []
            if len(line) > 1:
                for atom_token in line[1]:  # check rule body
                    _, atom = self.get_atom_information(atom_token)
                    tail.append(atom.atom_id)
            self.program.append([head, tail])

    def get_or_create_atom(self, atom):
        """
            Given a newly created logical atom, check to see if one exists of the given type. If it doesn't assign it a
            unique ID and add it to the atoms that exist for the program. If it is an epistemic atom add it to the
            epistemic atom cache. This allows fast access to atom information.
        """

        if str(atom) in self._atom_set:
            return False

        atom.atom_id = self._atom_id
        self._atom_set.add(str(atom))
        self._atom_cache[atom.atom_id] = atom
        self._atom_id += 1
        if atom.modality:
            atom.epistemic_id = self._epistemic_id
            self._epistemic_atom_cache[atom.epistemic_id] = atom
            self._epistemic_id += 1
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

        atom = Atom(atom_id=None, epistemic_id=None, label=label, modality=modality,
                    epistemic_negation=epistemic_negation, atom_negation=atom_negation,
                    negation_as_failure=negation_as_failure)

        created = self.get_or_create_atom(atom)

        return created, atom


# def optimisation_feasibility(stat_struct, debug=0):
#     """
#         Optimisation Feasibility:
#             Determines if a program is feasible for optimisation, if there is no way
#             speed it up then going through the extra process of attempting it.
#             Valuation optimisation requires at least 2 atoms to be identical in label (not including negation)
#             Pre :- The processing and attainment of subjective atoms and their negation status
#             Post :- A string of bits will be returned determining which optimisations should be
#             checked for in the optimisation process
#     """
#     ops = 0
#     stop_optimisation = False
#
#     for line_a in stat_struct:
#         for mod_a in range(0, len(stat_struct[line_a])):
#             for line_b in stat_struct:
#                 for mod_b in range(0, len(stat_struct[line_b])-1):
#                     if stat_struct[line_b][mod_a][2] == stat_struct[line_b][mod_b][2] and \
#                             (line_b != line_a and mod_a != mod_b):
#                         if debug:
#                             print 'stat_struct[line_b][mod_a][2]:', stat_struct[line_b][mod_a][2]
#                             print 'stat_struct[line_b][mod_b][2]:', stat_struct[line_b][mod_b][2]
#                             print 'line_b:', line_b
#                             print 'line_a:', line_a
#                             print 'mod_a:', mod_a
#                             print 'mod_b:', mod_b
#                         stop_optimisation = True
#                         break
#
#     if not stop_optimisation:
#         return False
#
#     for line_a in stat_struct:
#         for epa in stat_struct[line_a]:
#             for line_b in stat_struct:
#                 for epb in stat_struct[line_b]:
#                     if line_b != line_a and epa != epb:
#                         if debug:
#                             print 'linea: %s\nlineb: %s\n, epa: %s\n, epb: %s\n', (line_a, line_b, epa, epb)
#                         if ((epa[1] & 0x5) == (epb[1] & 0x5)) and ((epa[1] & 0x2) != (epb[1] & 0x2)) and \
#                            ((epa[1] & 0x4) == 0):  # for opt TF2
#                             if debug:
#                                 print 'opt TF2'
#                             ops |= 0x10
#                         if (epa[1] & 0x2) == (epb[1] & 0x2):  # for opt TT2
#                             if debug:
#                                 print 'opt TT2'
#                             ops |= 0x2
#                         if ((epa[1] & 0x1) == (epb[1] & 0x1)) and ((epa[1] & 0x4) != (epb[1] & 0x4)):
#                             # for opts TT3/4 FF1
#                             if (epa[1] & 0x2) == (epb[1] & 0x2):
#                                 if debug:
#                                     print 'opt TT3 FF1\n'
#                                 ops |= 0x20
#                             if (epa[1] & 0x2) != (epb[1] & 0x2):
#                                 if debug:
#                                     print 'opt TT4\n'
#                                 ops |= 0x4
#                         if epa[1] == epb[1]:  # for opts TF1
#                             if debug:
#                                 print 'opt TF1\n'
#                             ops |= 0x8
#                         if ((epa[1] & 0x2) != (epb[1] & 0x2)) and ((epa[1] & 0x1) != (epb[1] & 0x1)) and \
#                                 ((epa[1] & 0x4) == (epb[1] & 0x4)) and ((epa[1] & 0x4) == 0):
#                             # for opt TT1
#                             if debug:
#                                 print 'opt TT1'
#                             ops |= 0x1
#     return ops
#
#
# def evaluation_skip(optimisation, stat_struct, valuator_string, debug=0):
#     """
#         Retrofitting for statistic structure
#         Evaluation Skip: Looks at possible optimisations from previous function and sorts through
#         epistemic atoms and the current valuation string and determines if it is a valuation worth
#         persuing, here valuations containing conflicting values will be considered removable
#         Pre :-  *epistemic atoms and their negation status need to be processed.
#                 *The valuation binary string must be calculated.
#                 *An evaluation of optimisations to check for must also be looked for.
#         Post :- *A binary value will be outputted deciding whether this set of atoms is worth persuing
#                  as an interpretation of the original subjective program.
#     """
#     temp = 0
#
#     if self.modal_operator_count(stat_struct) == 1 or not self.modal_operator_count(stat_struct):
#         return True
#
#     # make a copy of the original queue to not lose original value set
#     copysStat = copy.copy(stat_struct)
#     # print 'valuator_string:',valuator_string
#     count = self.modOpCount(stat_struct)
#     countb = len(stat_struct.keys())
#     while countb:
#         counta = len(stat_struct[stat_struct.keys()[countb-1]])
#         while counta:
#             temp = valuator_string & 0x1
#             valuator_string >>= 1
#             if not temp:
#                 remove_item = stat_struct[stat_struct.keys()[countb-1]][counta-1]
#                 stat_struct[stat_struct.keys()[countb-1]].remove(remove_item)
#                 # print stat_struct[stat_struct.keys()[countb-1]]
#             counta -= 1
#         countb -= 1
#
#     count = len(stat_struct)
#
#     while count:
#         if len(stat_struct[stat_struct.keys()[count-1]]) == 0:
#             del stat_struct[count]
#         count -= 1
#
#     for linea in stat_struct:
#         for mod_a in stat_struct[linea]:
#             for lineb in stat_struct:
#                 for mod_b in stat_struct[lineb]:
#                     if mod_a != mod_b:
#                         print 'mod_a:', mod_a
#                         print 'mod_b:', mod_b
#                         if optimisation & 0x1 == 1:
#                             if ((mod_a[1] & 0x2) != (mod_b[1] & 0x2)) and ((mod_a[1] & 0x1) != (mod_b[1] & 0x1)) and \
#                                     (mod_a[2] == mod_b[2]) and ((mod_a[1] & 0x4) == (mod_b[1] & 0x4)) and \
#                                     ((mod_a[1] & 0x4) == 0):
#                                 # if modal operators are different
#                                 # atom negation is different, and there is no atom negation
#                                 self.print_opt('TT1', mod_a, mod_b, debug)
#                                 return False
#                         elif (optimisation & 0x2) == 2:
#                             if ((mod_a[1] & 0x6) == (mod_b[1] & 0x6)) and ((mod_a[1] & 0x2) == 1) and \
#                                ((mod_a[1] & 0x4) == 0) and ((mod_a[1] & 0x1) != (mod_b[1] & 0x1)) and \
#                                (mod_a[2] == mod_b[2]):
#                                 # if both mod negation and mod are the same (K and no negation)
#                                 self.print_opt('TT2', mod_a, mod_b, debug)
#                                 return False
#                         elif (optimisation & 0x4) == 4:
#                             if ((mod_a[1] & 0x6) != (mod_b[1] & 0x6)) and (mod_a[2] == mod_b[1]) and \
#                                ((mod_a[1] & 0x1) == (mod_b[1] & 0x1)) and \
#                                ((mod_a[1] & 0x4) != (mod_a[1] & 0x2)) and \
#                                ((mod_b[1] & 0x4) != (mod_b[1] & 0x2)):
#                                 self.print_opt('TT4', mod_a, mod_b, debug)
#                                 return False
#                         if (optimisation & 0x20) == 32:
#                             if ((mod_a[1] & 0x3) == (mod_b[1] & 0x3)) and (mod_a[2] == mod_b[2]) and \
#                                ((mod_a[1] & 0x4) != (mod_b[1] & 0x4)):
#                                 self.print_opt('TT3', mod_a, mod_b, debug)
#                                 return False
#                         if (optimisation & 0x8) == 8:
#                             if (mod_a[1] == mod_b[1]) and (mod_a[2] == mod_b[2]):
#                                 if debug:
#                                     print 'TF1 1 nMod = modCompare, ', mod, ' = ', modCompare, \
#                                         '\n atom = atomCompare, ', atom, ' = ', atomCompare
#                                 return False
#                         if (optimisation & 0x10) == 16:
#                             if ((mod_a[1] & 0x2) != (mod_b[1] & 0x2)) and ((mod_a[1] & 0x2) == 1) and \
#                                (mod_a[2] == mod_b[2]) and ((mod_a[1] & 0x1) == (mod_b[1] & 0x1)) and \
#                                ((mod_a[1] & 0x4) == (mod_b[1] & 0x4)) and ((mod_a[1] & 0x4) == 0):
#                                 self.print_opt('TF2', mod_a, mod_b, debug)
#                                 return False
#                         if (optimisation & 0x20) == 32:
#                             if ((mod_a[1] & 0x3) == (mod_b[1] & 0x3)) and (mod_b[2] == mod_a[2]) and \
#                                     ((mod_b[1] & 0x4) != (mod_a[1] & 0x4)):
#                                 return False
#     return True
