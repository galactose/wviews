import os
import re
import copy
import math
import grounder
import parser
import sys


class WorldViewsOptimisation(object):
    def __init__(self, file_name):
        pass


class WorldViews(object):
    """
    **************************************************************************
        elp: Epistemic Answer Set Logic Program Interpreter
        Build 1.1 - Port from C++ -> Python.

        School of Computing and Mathematics,
          Intelligent Systems Laboratory,
           University of Western Sydney,
                  Penrith Campus.

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
        parser.parse_program(file_name)
        self.stats = self.system_statistics(self.program)

    def __del__(self):
        del self.program
        del self

    def system_statistics(self, program):
        """
            system_statistics:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
        """
        statistics = {}
        for index in range(0, len(program)):  # loop over rules
            rule_tokens = []
            if isinstance(program[index], type([])):
                word_count = 0
                for word in program[index][1]:
                    atom_tokens = []
                    mod_neg = 0
                    # word = word.strip()
                    if word.find('K') != -1 or word.find('M') != -1:
                        check = word.find('M')
                        if check == -1:
                            check = word.find('K')
                            mod_neg |= 0x2
                        atom_tokens.append(word_count)  # appending atomCount
                        word_count = -1
                        atom_tokens.append(check)  # appending epistemic atom to list
                        if check != 0:
                            if word[check-1] == '-' or word[check-1] == '~':
                                mod_neg |= 0x4
                        if word[check + 1] == '-' or word[check + 1] == '~':
                            mod_neg |= 0x1
                        atom_tokens.append(mod_neg)
                        if not (word[check + 1] == '-' or word[check + 1] == '~'):
                            atom_tokens.append(word[check+1:len(word)])
                        else:
                            atom_tokens.append(word[check+2:len(word)])
                        rule_tokens.append(atom_tokens)
                    word_count += 1
            if len(rule_tokens):
                statistics[index] = rule_tokens
        return copy.copy(statistics)

    def parse_rules(self, program):
        """
            parse_rules:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
        """
        for curPos in range(0, len(program)):
            pass

    def groundPredicates(self):
        pass

    def printRules(self, prog):
        pass

    def elpSession(self, program):
        pass

    def findFacts(self, program):
        pass

    @staticmethod
    def compare_atoms(world_view, modal_operation_type, atom, valuation, debug=0):
        """
            compare_atoms:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
                - wView a returned answer set
                - data, epAtom Position
                - modalOpType - represents modality and negation
                -
        """
        universal_count = 0
        answer_set_count = 0
        one_instance = False
        if modal_operation_type & 0x1 == 0x1:
            atom = '-' + atom

        for answer_set in world_view:
            if atom in answer_set:
                universal_count += 1
                one_instance = True
            answer_set_count += 1

        if debug:
            print 'wView: %s,\n modalOpType: %s,\natom: %s,\nvaluation: %s,\nuniversalCount: %s,\nendsetCount: %s,\noneInstance: %s' % \
                  (world_view, modal_operation_type, atom, valuation, universal_count, answer_set_count, one_instance)

        if modal_operation_type & 0x2 == 0x2:  # KNOWS
            if modal_operation_type & 0x4 == 0x4:  # NEGATED KNOWLEDGE
                if universal_count == answer_set_count:  # IF atom present in all answer sets
                    return not valuation
                else:  # IF NOT present in all answer sets
                    return valuation
            else:  # POSITIVE KNOWLEDGE
                if universal_count == answer_set_count:
                    return valuation
                else:
                    return not valuation
        else:  # BELIEVES
            if modal_operation_type & 0x4 == 0x4:  # NEGATED BELIEF
                if one_instance:
                    return not valuation
                else:
                    return valuation
            else:  # POSITIVE BELIEF
                if one_instance:
                    return valuation
                else:
                    return not valuation

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
            mod = '-'
        if (eval & 0x2) == 2:
            mod = 'K' + mod
        else:
            mod = 'M' + mod
        if (eval & 0x4) == 4:
            mod = '-' + mod
        return mod

    def check_validity(self, answer_set, stat_struct, debug=0):
        """
            #goal: extract the current evaluation on the modal atom
            #     - with the given binary evaluation, the epistemic atom and the found worldview
            #     - if the evaluation is satisfied by the worldview return true
            #     - otherwise for any given epistemic atom and its evaluation, if one fails the whole
            #       evaluation fails.
        """
        for line in stat_struct.keys():
            for mod in stat_struct[line]:
                if not self.compare_atoms(answer_set, mod[2], mod[3], mod[4]):
                    return False
        return True

    @staticmethod
    def parse_answer_set(queue):
        """
            parse_answer_set: takes unformatted queue of answerset values and removes formatting, making a list of lists
        """
        answer_set_regex = re.compile(r'{([\W\w]*)}')
        temp_list = []
        return_list = []
        for line in queue:
            if answer_set_regex.search(line):
                counter = answer_set_regex.search(line)
                line = counter.group(1)
                temp_list = line.split(',')
                for index in range(0, len(temp_list)):
                    temp_list[index] = temp_list[index].strip()
            return_list.append(temp_list)
        return return_list

    def modal_operator_count(self, stat_struct):
        count = 0
        for key in stat_struct.keys():
            count += len(stat_struct[key])
        return count

    def generate_worldview(self, program, stat_struct):
        """
            show instantiations: removes modal operators in answer sets by assuming they are
            true or false, on the case they are true we remove the modal operator and its atom
            in the case it is false we move the entire rule from the answer set. once this is
            done the answer set is sent to dlv for its stable model
        """
        binary_count = math.pow(2, self.modal_operator_count(stat_struct))
        binary_modal_valuation = 0
        good_int_count = 0

        if self.modal_operator_count(stat_struct) > 31:
            return

        # posOpt = self.optimisation_feasibilty(stat_struct)

        while binary_count:
            # passCheck = self.evaluation_skip(posOpt, stat_struct, binModEval)
            # if passCheck:
            good_int_count += 1
            program_copy = self.build_interpreted_program(program, stat_struct, binary_modal_valuation)
            # print ''
            # print 'iterpreted program ->'
            # pprint.pprint(copy)
            # print ''
            self.export_rules(program_copy, 'ans.elp')
            os.system('dlv -silent ans.elp > temp2')
            answer_set = parser.import_answer_set('temp2')  # builds the answer into a queue
            answer_set = self.parse_answer_set(answer_set)
            # print answer_set
            # os.system('pause')

            if self.check_validity(answer_set, stat_struct):  # checks returned set against original modal set.
                yield answer_set
                # answer_set = emptyQueue(answer_set);
            # else:
                # contraCount += 1
            binary_modal_valuation += 1
            binary_count -= 1

    @staticmethod
    def optimisation_feasibility(stat_struct, debug=0):
        """
            Optimisation Feasibility:
                Determines if a program is feasible for optimisation, if there is no way
                speed it up then going through the extra process of attempting it.
                Valuation optimisation requires at least 2 atoms to be identical in label (not including negation)
                Pre :- The processing and attainment of subjective atoms and their negation status
                Post :- A string of bits will be returned determining which optimisations should be
                checked for in the optimisation process
        """
        ops = 0
        stop_optimisation = False

        for line_a in stat_struct:
            for mod_a in range(0, len(stat_struct[line_a])):
                for line_b in stat_struct:
                    for mod_b in range(0, len(stat_struct[line_b])-1):
                        if stat_struct[line_b][mod_a][2] == stat_struct[line_b][mod_b][2] and \
                                (line_b != line_a and mod_a != mod_b):
                            if debug:
                                print 'stat_struct[line_b][mod_a][2]:', stat_struct[line_b][mod_a][2]
                                print 'stat_struct[line_b][mod_b][2]:', stat_struct[line_b][mod_b][2]
                                print 'line_b:', line_b
                                print 'line_a:', line_a
                                print 'mod_a:', mod_a
                                print 'mod_b:', mod_b
                            stop_optimisation = True
                            break

        if not stop_optimisation:
            return False

        for line_a in stat_struct:
            for epa in stat_struct[line_a]:
                for line_b in stat_struct:
                    for epb in stat_struct[line_b]:
                        if line_b != line_a and epa != epb:
                            if debug:
                                print 'linea: %s\nlineb: %s\n, epa: %s\n, epb: %s\n', (line_a, line_b, epa, epb)
                            if ((epa[1] & 0x5) == (epb[1] & 0x5)) and ((epa[1] & 0x2) != (epb[1] & 0x2)) and \
                               ((epa[1] & 0x4) == 0):  # for opt TF2
                                if debug:
                                    print 'opt TF2'
                                ops |= 0x10
                            if (epa[1] & 0x2) == (epb[1] & 0x2):  # for opt TT2
                                if debug:
                                    print 'opt TT2'
                                ops |= 0x2
                            if ((epa[1] & 0x1) == (epb[1] & 0x1)) and ((epa[1] & 0x4) != (epb[1] & 0x4)):
                                # for opts TT3/4 FF1
                                if (epa[1] & 0x2) == (epb[1] & 0x2):
                                    if debug:
                                        print 'opt TT3 FF1\n'
                                    ops |= 0x20
                                if (epa[1] & 0x2) != (epb[1] & 0x2):
                                    if debug:
                                        print 'opt TT4\n'
                                    ops |= 0x4
                            if epa[1] == epb[1]:  # for opts TF1
                                if debug:
                                    print 'opt TF1\n'
                                ops |= 0x8
                            if ((epa[1] & 0x2) != (epb[1] & 0x2)) and ((epa[1] & 0x1) != (epb[1] & 0x1)) and \
                                    ((epa[1] & 0x4) == (epb[1] & 0x4)) and ((epa[1] & 0x4) == 0):
                                # for opt TT1
                                if debug:
                                    print 'opt TT1'
                                ops |= 0x1
        return ops

    def evaluation_skip(self, optimisation, stat_struct, valuator_string, debug=0):
        """
            Retrofitting for statistic structure
            Evaluation Skip: Looks at possible optimisations from previous function and sorts through
            epistemic atoms and the current valuation string and determines if it is a valuation worth
            persuing, here valuations containing conflicting values will be considered removable
            Pre :-  *epistemic atoms and their negation status need to be processed.
                    *The valuation binary string must be calculated.
                    *An evaluation of optimisations to check for must also be looked for.
            Post :- *A binary value will be outputted deciding whether this set of atoms is worth persuing
                     as an interpretation of the original subjective program.
        """
        temp = 0

        if self.modal_operator_count(stat_struct) == 1 or not self.modal_operator_count(stat_struct):
            return True

        # make a copy of the original queue to not lose original value set
        copysStat = copy.copy(stat_struct)
        # print 'valuator_string:',valuator_string
        count = self.modOpCount(stat_struct)
        countb = len(stat_struct.keys())
        while countb:
            counta = len(stat_struct[stat_struct.keys()[countb-1]])
            while counta:
                temp = valuator_string & 0x1
                valuator_string >>= 1
                if not temp:
                    remove_item = stat_struct[stat_struct.keys()[countb-1]][counta-1]
                    stat_struct[stat_struct.keys()[countb-1]].remove(remove_item)
                    # print stat_struct[stat_struct.keys()[countb-1]]
                counta -= 1
            countb -= 1

        count = len(stat_struct)

        while count:
            if len(stat_struct[stat_struct.keys()[count-1]]) == 0:
                del stat_struct[count]
            count -= 1

        for linea in stat_struct:
            for mod_a in stat_struct[linea]:
                for lineb in stat_struct:
                    for mod_b in stat_struct[lineb]:
                        if mod_a != mod_b:
                            print 'mod_a:', mod_a
                            print 'mod_b:', mod_b
                            if optimisation & 0x1 == 1:
                                if ((mod_a[1] & 0x2) != (mod_b[1] & 0x2)) and ((mod_a[1] & 0x1) != (mod_b[1] & 0x1)) and \
                                        (mod_a[2] == mod_b[2]) and ((mod_a[1] & 0x4) == (mod_b[1] & 0x4)) and \
                                        ((mod_a[1] & 0x4) == 0):
                                    # if modal operators are different
                                    # atom negation is different, and there is no atom negation
                                    self.print_opt('TT1', mod_a, mod_b, debug)
                                    return False
                            elif (optimisation & 0x2) == 2:
                                if ((mod_a[1] & 0x6) == (mod_b[1] & 0x6)) and ((mod_a[1] & 0x2) == 1) and \
                                   ((mod_a[1] & 0x4) == 0) and ((mod_a[1] & 0x1) != (mod_b[1] & 0x1)) and \
                                   (mod_a[2] == mod_b[2]):
                                    # if both mod negation and mod are the same (K and no negation)
                                    self.print_opt('TT2', mod_a, mod_b, debug)
                                    return False
                            elif (optimisation & 0x4) == 4:
                                if ((mod_a[1] & 0x6) != (mod_b[1] & 0x6)) and (mod_a[2] == mod_b[1]) and \
                                   ((mod_a[1] & 0x1) == (mod_b[1] & 0x1)) and \
                                   ((mod_a[1] & 0x4) != (mod_a[1] & 0x2)) and \
                                   ((mod_b[1] & 0x4) != (mod_b[1] & 0x2)):
                                    self.print_opt('TT4', mod_a, mod_b, debug)
                                    return False
                            if (optimisation & 0x20) == 32:
                                if ((mod_a[1] & 0x3) == (mod_b[1] & 0x3)) and (mod_a[2] == mod_b[2]) and \
                                   ((mod_a[1] & 0x4) != (mod_b[1] & 0x4)):
                                    self.print_opt('TT3', mod_a, mod_b, debug)
                                    return False
                            if (optimisation & 0x8) == 8:
                                if (mod_a[1] == mod_b[1]) and (mod_a[2] == mod_b[2]):
                                    if debug:
                                        print 'TF1 1 nMod = modCompare, ', mod, ' = ', modCompare, \
                                            '\n atom = atomCompare, ', atom, ' = ', atomCompare
                                    return False
                            if (optimisation & 0x10) == 16:
                                if ((mod_a[1] & 0x2) != (mod_b[1] & 0x2)) and ((mod_a[1] & 0x2) == 1) and \
                                   (mod_a[2] == mod_b[2]) and ((mod_a[1] & 0x1) == (mod_b[1] & 0x1)) and \
                                   ((mod_a[1] & 0x4) == (mod_b[1] & 0x4)) and ((mod_a[1] & 0x4) == 0):
                                    self.print_opt('TF2', mod_a, mod_b, debug)
                                    return False
                            if (optimisation & 0x20) == 32:
                                if ((mod_a[1] & 0x3) == (mod_b[1] & 0x3)) and (mod_b[2] == mod_a[2]) and \
                                        ((mod_b[1] & 0x4) != (mod_a[1] & 0x4)):
                                    return False
        return True

    @staticmethod
    def print_opt(opt_type, mod_a, mod_b, debug=0):
        if debug:
            print '%s mod: %s, atom: %s, modCompare: %s, atom: %s' % (opt_type, mod_a[1], mod_a[2], mod_b[1], mod_b[2])

    def export_rules(self, queue, filename='ans.elp', debug=0):
        if debug:
            print 'export_rules(self, queue, filename = "ans.elp") -> queue\n', queue, '\n'
        output = file(filename, 'w')
        for line in queue:
            if debug:
                print 'export_rules(self, queue, filename = "ans.elp") -> line\n', line, '\n'
            if isinstance(line[0], list):  # STILL WORKING HERE
                for head in range(0, len(line[0])):
                    output.write(line[0][head])
                    # print 'line[0][head]:', line[0][head]
                    # print 'head:', head, 'len(line)-2:', len(line[0])-2, 'len(line):', len(line[0])
                    # print ''
                    if head != len(line[0])-1:
                        # print 'IM WRITING DISJUNCTION'
                        output.write(' v ')

                output.write(' :- ')
                for tail in range(0, len(line[1])):
                    output.write(line[1][tail])
                    # print 'tail:', tail, 'len(line):', len(line[1])
                    if tail != len(line[1])-1:
                        output.write(', ')

            elif isinstance(line[0], str):
                for head in range(0, len(line)):
                    output.write(line[head])

                    if head != len(line)-1:
                        output.write(' v ')
            output.write('.\n')
        output.close()
        return True

    def remove_modal_operators(self, body, rule, epAtom, beginPos):  # NOT COMPLETE
        """
            removeModOperators: removes the modal operators present at the front of the rule,
            assumes rule format [a-z* [v a-z*]*] :- [[~|-]K|M[a-z]*,]*[[not]a-z*].
        """
        if len(rule) < beginPos or beginPos == 0:
            return 0
        if rule[beginPos-1] == '-' or rule[beginPos-1] == '~':
            beginPos -= 1

        for count in range(beginPos, len(rules)):
            if rule[count] == '.' or rule[count] == ',':
                endPos = count

        if rule[endPos] == '.':
            rule = rule[0:beginPos-1] + rule[endPos:len(rule)]
        else:
            rule = rule[0:beginPos-1] + rule[endPos+1:len(rule)]
        for count in range(0, len(body)):
            if body[count].find(epAtom) != -1:
                pass
        return rule

    @staticmethod
    def update_valuation(stat_struct, valuation_string):
        count_b = len(stat_struct)
        while count_b:
            count_a = len(stat_struct[stat_struct.keys()[count_b-1]])
            while count_a:
                temp = valuation_string & 0x1
                valuation_string >>= 1
                if len(stat_struct[stat_struct.keys()[count_b-1]][count_a-1]) == 5:
                    stat_struct[stat_struct.keys()[count_b-1]][count_a-1][4] = temp
                elif len(stat_struct[stat_struct.keys()[count_b-1]][count_a-1]) < 5:
                    stat_struct[stat_struct.keys()[count_b-1]][count_a-1].append(temp)
                count_a -= 1
            count_b -= 1

    def update_index(self, line_index, dictionary):
        tempDict = {}
        for index in range(0, line_index):
            tempDict[dictionary.keys()[index]] = copy.copy(dictionary[dictionary.keys()[index]])
        for index in range(line_index, len(dictionary.keys())):
            tempDict[dictionary.keys()[index]-1] = copy.copy(dictionary[dictionary.keys()[index]])
        # print 'tempDict:', tempDict
        return tempDict

    @staticmethod
    def remove_all_epistemic_atoms(line):
        temp = []
        # print 'remove_all_epistemic_atoms(', line, ')'
        if isinstance(line, type([])):
            for index in range(0, len(line)):
                # print 'remove_all_epistemic_atoms(line) -> index:', index
                # print 'remove_all_epistemic_atoms(line) -> line[index]:', line[index]
                if not line[index].find('K') != -1 and not line[index].find('M') != -1:
                    temp.append(line[index])
        if not len(temp):
            return
        else:
            return temp

    def build_interpreted_program(self, program, stat_struct, valuator_string):
        """
            showPossibleSet: Takes in the queue of rules, the line locations of its modal operators,
                the character locations of modal operators, and the integer value which determines the truth valuation
                of each modal operator.
        """

        valuation = copy.deepcopy(program)
        mod_temp = 0
        count = 0
        flag = 0
        if len(program) > 0 and not len(stat_struct):
            return queue

        mod_temp = len(stat_struct)
        self.update_valuation(stat_struct, valuator_string)

        for line in stat_struct:
            flag = 0
            for epAtom in range(0, len(stat_struct[line])):
                if stat_struct[line][epAtom][4] == 0:
                    flag = 1
                    # print 'found 0, breaking'
                    break
            # os.system('pause')
            # print 'flag:', flag
            if flag == 1:
                valuation[line].append(1)
            else:
                valuation[line][1] = self.remove_all_epistemic_atoms(valuation[line][1])
                if not valuation[line][1]:
                    valuation[line] = valuation[line][0]

        # pprint.pprint(valuation)
        total = len(valuation)
        tempValuation = []
        for line in valuation:
            # print 'line[-1]:', line[-1]
            if line[-1] != 1:
                tempValuation.append(line)

        # pprint.pprint(tempValuation)
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

if __name__ == '__main__':
    file_path = os.getcwd() + '\\worldviews'
    files = os.listdir('worldviews')
    session = WorldViews('worldviews\\interview.txt')
    worldview_grounder = grounder.grounding(session)
    countString = []
    length = 5
    base = 4

    for count in range(0, length):
        countString.append(0)
    print countString

    while 1:
        countString = worldview_grounder.incString(countString, base, length)
        print countString
        os.system('pause')

    # 'worldviews\\interview.txt'
    # for inst in files:
    #    session = elp('worldviews\\' + inst)
    #    session.run_session()
    #    print 'im here!'
    #    os.system('pause')
    #    os.system('cls')
    #    del session
