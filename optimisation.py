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
