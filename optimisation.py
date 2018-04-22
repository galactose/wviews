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

# def evaluation_skip(optimisation, stat_struct, valuator_string, debug=0):
#     """
#     Retrofitting for statistic structure
#     Evaluation Skip: Looks at possible optimisations from previous function
#         and sorts through epistemic atoms and the current valuation string
#         and determines if it is a valuation worth persuing, here valuations
#         containing conflicting values will be considered removable
#     Pre :-  * epistemic atoms and their negation status need to be processed.
#             * The valuation binary string must be calculated.
#             * An evaluation of optimisations to check for must also be looked
#               for.
#     Post :- * A binary value will be outputted deciding whether this set of
#               atoms is worth persuing as an interpretation of the original
#               subjective program.
#     """
#     temp = 0

#     if self.modal_operator_count(stat_struct) == 1 or \
#        not self.modal_operator_count(stat_struct):
#         return True

#     # make a copy of the original queue to not lose original value set
#     copysStat = copy.copy(stat_struct)
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
#             counta -= 1
#         countb -= 1

#     count = len(stat_struct)

#     while count:
#         if not stat_struct[stat_struct.keys()[count-1]]:
#             del stat_struct[count]
#         count -= 1

#     for linea in stat_struct:
#         for lineb in stat_struct:
#             comparison_modals = combinations(stat_struct[lineb] + stat_struct[linea], 2)
#             for modal_pair in comparison_modals:
#                 mod_a, mod_b = comparison_modals
#                 if mod_a.label != mod_b.label:
#                     continue
#                 if not check_optimisation(optimisation, mod_a, mod_b):
#                     return False
#     return True

# def check_optimisation(optimisation, mod_a, mod_b):
#     """
#     Analysing old code
#     0: epistemic negation
#     1: modality K|B
#     2: atom negation
#     """

#     if optimisation & 0x1 == 1:
#         if ((mod_a[1] & 0x2) != (mod_b[1] & 0x2)) and \
#            ((mod_a[1] & 0x1) != (mod_b[1] & 0x1)) and \
#            ((mod_a[1] & 0x4) == (mod_b[1] & 0x4)) and \
#            ((mod_a[1] & 0x4) == 0):
#             # if modal operators are different
#             # atom negation is different, and there is no atom negation
#             return False
#     elif (optimisation & 0x2) == 2:
#         if ((mod_a[1] & 0x6) == (mod_b[1] & 0x6)) and \
#            ((mod_a[1] & 0x2) == 1) and \
#            ((mod_a[1] & 0x4) == 0) and \
#            ((mod_a[1] & 0x1) != (mod_b[1] & 0x1)):
#             # if both mod negation and mod are the same (K and no negation)
#             return False
#     elif (optimisation & 0x4) == 4:
#         if ((mod_a[1] & 0x6) != (mod_b[1] & 0x6)) and \
#            ((mod_a[1] & 0x1) == (mod_b[1] & 0x1)) and \
#            ((mod_a[1] & 0x4) != (mod_a[1] & 0x2)) and \
#            ((mod_b[1] & 0x4) != (mod_b[1] & 0x2)):
#             return False
# elif (optimisation & 0x8) == 8:
#     # look for cases where the epistemic atoms are the same.
#     if (mod_a[1] == mod_b[1]):
#         return False
# elif (optimisation & 0x10) == 16:
#     if ((mod_a[1] & 0x2) != (mod_b[1] & 0x2)) and \
#        ((mod_a[1] & 0x2) == 1) and \
#        ((mod_a[1] & 0x1) == (mod_b[1] & 0x1)) and \
#        ((mod_a[1] & 0x4) == (mod_b[1] & 0x4)) and \
#        ((mod_a[1] & 0x4) == 0):
#         return False
# elif (optimisation & 0x20) == 32:
#     if ((mod_a[1] & 0x3) == (mod_b[1] & 0x3)) and \
#        ((mod_b[1] & 0x4) != (mod_a[1] & 0x4)):
#         return False

# def optimisation_present(e_atom_a, e_atom_b):
#     if e_atom_a == e_atom_b:
#         return True
#     # if different modality but same negations on same label
#     # optimisation exists
#     if not e_atom_a.same_modal_token(e_atom_b) and e_atom_a.know() and \
#        e_atom_b.same_atom_negation(e_atom_b) and \
#        e_atom_b.same_epistemic_negation(e_atom_b)
#        not e_atom_a.atom_negation:
#        return True

#     if e_atom_a.same_modal(e_atom_b) and \
#        not e_atom_a.same_atom_negation(e_atom_b):
#        return True

#     if e_atom_a.same_modal(e_atom_b) and e_atom_a.know()
#     elif (optimisation & 0x2) == 2:
#         if ((mod_a[1] & 0x6) == (mod_b[1] & 0x6)) and \
#            ((mod_a[1] & 0x2) == 1) and \
#            ((mod_a[1] & 0x4) == 0) and \
#            ((mod_a[1] & 0x1) != (mod_b[1] & 0x1)):
