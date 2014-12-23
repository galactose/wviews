import os, re, copy, math, grounder


class WviewsOptimisation():
    def __init__(self, fileName):
        pass


class Wviews():
    """
    **************************************************************************
        elp: Epistemic Answer Set Logic Program Interpreter
        Build 1.5 - Port from C++ -> Python.

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
                  "," represents conjunction,
                  K|M represents the modal operators,
                    K: 'Knows' and
                    M: 'Believes'
                  and ":-" representing implication
                    "is true if the following is also true"

            and returns the applicable worldviews derived from the rules.
    **************************************************************************
    """
    
    def __init__(self, file_name):
        self.program = []
        self.stats = {}
        self.build_program(file_name)
        self.stats = self.sysStat(self.program)
        
    def __del__(self):
        del self.program
        del self
        
    def build_program(self, fileName):
        """
            buildProgram:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED: incomplete
        """
        """
        body, rule, head, tail, tempProgram = [], [], [], [], []
        if fileName != '':
            try:
                
                input = file(fileName, "r") #need to implement try/except block to catch exceptions
            except IOError:
                print "<file doesnt exist.>"
                os.system("pause")
                exit(1)
            for line in input.readlines():
                try:
                    if '#' in line:
                        line = line[0: line.index('#')]
                    if not line.index('.') == -1: #need to implement system such that rules can be staggered over various lines or a line may have multiple rules.
                        tempProgram.append(line[0:line.index('.')+1].strip())
                except ValueError: pass
            for line in tempProgram:
                body, rule, head, tail = [], [], [], []
                line = line.replace('.', '')
                body = line.split(":-")
                if len(body) == 1:
                    body[0] = body[0].strip()
                    rule = body[0].split(" v ")
                    for count in range(0, len(rule)):
                        rule[count] = rule[count].strip()
                elif len(body) == 2:
                    head = body[0].split(' v ')
                    for count in range(0, len(head)):
                        head[count] = head[count].strip()
                    tail = body[1].split(',')
                    for count in range(0, len(tail)):
                        tail[count] = tail[count].strip()
                    rule.append(head)
                    rule.append(tail)
                self.program.append(rule)"""

    def sysStat(self, program):
        """
            sysStat:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
        """
        line, atomTokens, ruleTokens, statistics = [], [], [], {}
        check, modNeg = 0, 0
        for index in range(0, len(program)): #loop over rules
            ruleTokens = []
            if isinstance(program[index], type([])):
                wordCount = 0
                for word in program[index][1]:
                    atomTokens = []
                    modNeg = 0
                    #word = word.strip()
                    if word.find('K') != -1 or word.find('M') != -1:
                        check = word.find('M')
                        if check == -1:
                            check = word.find('K')
                            modNeg = modNeg|0x2
                        atomTokens.append(wordCount) #appending atomCount
                        wordCount = -1
                        atomTokens.append(check) #appending epistemic atom to list
                        if check != 0:
                            if word[check-1] == '-' or word[check-1] == '~':
                                modNeg = modNeg|0x4
                        if word[check + 1] == '-' or word[check + 1] == '~':
                            modNeg = modNeg|0x1
                        atomTokens.append(modNeg)
                        if not (word[check + 1] == '-' or word[check + 1] == '~'):
                            atomTokens.append(word[check+1:len(word)])
                        else:
                            atomTokens.append(word[check+2:len(word)])
                        ruleTokens.append(atomTokens)
                    wordCount += 1
            if len(ruleTokens) != 0:
                statistics[index] = ruleTokens
        return copy.copy(statistics)

    def parseRules(self, program):
        """
            parseRules:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
        """
        for curPos in range(0, len(program)): pass

    def groundPredicates(self):
        pass

    def printRules(self, prog):
        pass

    def elpSession(self, program):
        pass

    def findFacts(self, program):
        pass
    
    def compare_atoms(self, world_view, modal_operation_type, atom, valuation, debug = 0):
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
        if modal_operation_type&0x1 == 0x1:
            atom = '-' + atom

        for answer_set in world_view:
            if atom in answer_set:
                universal_count += 1
                one_instance = True
            answer_set_count += 1

        if debug:
            print 'wView: %s,\n modalOpType: %s,\natom: %s,\nvaluation: %s,\nuniversalCount: %s,\nendsetCount: %s,\noneInstance: %s' % \
                  (world_view, modal_operation_type, atom, valuation, universal_count, answer_set_count, one_instance)

        if modal_operation_type&0x2 == 0x2:  # KNOWS
            if modal_operation_type&0x4 == 0x4:  # NEGATED KNOWLEDGE
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
            if modal_operation_type&0x4 == 0x4:  # NEGATED BELIEF
                if one_instance:
                    return not valuation
                else:
                    return valuation
            else:  # POSITIVE BELIEF
                if one_instance:
                    return valuation
                else:
                    return not valuation

    def translate_modality(self, eval):
        """
            transModality:
            PRE:
            POST:
            COMPLEXITY:
            COMPLETED:
        """
        mod = ''
        if (eval&0x1) == 1:
            mod = '-'
        if (eval&0x2) == 2:
            mod = 'K' + mod
        else:
            mod = 'M' + mod
        if (eval&0x4) == 4:
            mod = '-' + mod
        return mod
        
    def checkValidity(self, answer_set, stat_struct, debug = 0):
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
        answer_set_regex = re.compile('{([\W\w]*)}')
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
    
    def modal_operator_count(self, statStruct):
        count = 0
        for key in statStruct.keys():
            count += len(statStruct[key])
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
            
        #posOpt = self.optFeasibilty(stat_struct)
        
        while binary_count:
            # passCheck = self.evaluation_skip(posOpt, stat_struct, binModEval)
            # if passCheck:
            good_int_count += 1
            program_copy = self.build_interpreted_program(program, stat_struct, binary_modal_valuation)
            # print ""
            # print "iterpreted program ->"
            # pprint.pprint(copy)
            # print ""
            self.export_rules(program_copy, "ans.elp")
            os.system("dlv -silent ans.elp > temp2")
            answer_set = self.ImportAnsSet("temp2")  # builds the answer into a queue
            answer_set = self.parse_answer_set(answer_set)
            # print answer_set
            # os.system("pause")
            
            if self.checkValidity(answer_set, stat_struct):  # checks returned set against original modal set.
                yield answer_set
                # answer_set = emptyQueue(answer_set);
            # else:
                # contraCount += 1
            binary_modal_valuation += 1
            binary_count -= 1

    @staticmethod
    def optimisation_feasibility(stat_struct, debug = 0):
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
                        if stat_struct[line_b][mod_a][2] == stat_struct[line_b][mod_b][2] and (line_b != line_a and mod_a != mod_b):
                            if debug == 1:
                                print 'statStruct[line_b][mod_a][2]:', stat_struct[line_b][mod_a][2]
                                print 'statStruct[line_b][mod_b][2]:', stat_struct[line_b][mod_b][2]
                                print 'line_b:', line_b
                                print 'line_a:', line_a
                                print 'mod_a:', mod_a
                                print 'mod_b:', mod_b
                            stop_optimisation = True
                            break 
         
        if not stop_optimisation:
            return False

        for line_a in stat_struct.keys():
            for epa in stat_struct[line_a]:
                for line_b in stat_struct.keys():
                    for epb in stat_struct[line_b]:
                        if line_b != line_a and epa != epb:
                            if debug:
                                print "lineb:", line_b
                                print "linea:", line_a
                                print "epa:", epa
                                print "epb:", epb
                            if ((epa[1]&0x5) == (epb[1]&0x5)) and ((epa[1]&0x2) != (epb[1]&0x2)) and \
                               ((epa[1]&0x4) == 0):  # for opt TF2
                                if debug:
                                    print "opt TF2"
                                ops |= 0x10
                            if (epa[1]&0x2) == (epb[1]&0x2):  # for opt TT2
                                if debug:
                                    print "opt TT2"
                                ops |= 0x2
                            if ((epa[1]&0x1) == (epb[1]&0x1)) and ((epa[1]&0x4) != (epb[1]&0x4)):  # for opts TT3/4 FF1
                                if (epa[1]&0x2) == (epb[1]&0x2):
                                    if debug:
                                        print "opt TT3 FF1\n"
                                    ops |= 0x20
                                if (epa[1]&0x2) != (epb[1]&0x2):
                                    if debug:
                                        print "opt TT4\n"
                                    ops |= 0x4
                            if epa[1] == epb[1]:  # for opts TF1
                                if debug:
                                    print "opt TF1\n"
                                ops |= 0x8
                            if ((epa[1]&0x2) != (epb[1]&0x2)) and ((epa[1]&0x1) != (epb[1]&0x1)) and ((epa[1]&0x4) == (epb[1]&0x4)) and ((epa[1]&0x4) == 0):
                                #for opt TT1
                                if debug:
                                    print "opt TT1"
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

        #make a copy of the original queue to not lose original value set
        copysStat = copy.copy(stat_struct)
        #print "valuator_string:",valuator_string
        count = self.modOpCount(stat_struct)
        countb = len(stat_struct.keys())
        while countb:
            counta = len(stat_struct[stat_struct.keys()[countb-1]])
            while counta:
                temp = valuator_string & 0x1
                valuator_string = valuator_string >> 1
                if not temp:
                    stat_struct[stat_struct.keys()[countb-1]].remove(stat_struct[stat_struct.keys()[countb-1]][counta-1])
                    #print stat_struct[stat_struct.keys()[countb-1]]
                counta -= 1
            countb -= 1
            
        count = len(stat_struct)
        while count:
            if len(stat_struct[stat_struct.keys()[count-1]]) == 0:
                del stat_struct[count]
            count -= 1

        for linea in stat_struct.keys():
            for moda in stat_struct[linea]:
                for lineb in stat_struct.keys():
                    for modb in stat_struct[lineb]:
                        if moda != modb:
                            print "moda:", moda
                            print "modb:", modb
                            if optimisation & 0x1 == 1:
                                if(((moda[1]&0x2) != (modb[1]&0x2)) and ((moda[1]&0x1) != (modb[1]&0x1)) and (moda[2] == modb[2]) and ((moda[1]&0x4) == (modb[1]&0x4)) and ((moda[1]&0x4) == 0)):
                                    #if modal operators are different, atom negation is different, and there is no atom negation
                                    if debug:
                                        print "TT1 mod: ", moda[1], ", atom: ", moda[2], ", modCompare: ", modb[1], ", atom:", moda[2]
                                    return False
                            elif((optimisation&0x2) == 2):
                                if(((moda[1]&0x6) == (modb[1]&0x6)) and ((moda[1]&0x2) == 1) and ((moda[1]&0x4) == 0)
                                   and ((moda[1]&0x1) != (modb[1]&0x1)) and (moda[2] == modb[2])):
                                    #if both mod negation and mod are the same (K and no negation)
                                    print "TT2 mod: ", moda[1], ", atom: ", moda[2], ", modCompare: ", modb[1], ", atom:", moda[2]
                                    return False
                            elif((optimisation&0x4) == 4):
                                if(((moda[1]&0x6) != (modb[1]&0x6)) and (moda[2] == modb[1]) and
                                       ((moda[1]&0x1) == (modb[1]&0x1)) and ((moda[1]&0x4) != (moda[1]&0x2)) and
                                       ((modb[1]&0x4) != (modb[1]&0x2))):
                                    print "TT4 mod: ", moda[1], ", atom: ", moda[2], ", modCompare: ", modb[1], ", atom:", moda[2]
                                    return False
                            if((optimisation&0x20) == 32):
                                if(((moda[1]&0x3) == (modb[1]&0x3)) and (moda[2] == modb[2]) and
                                       ((moda[1]&0x4) != (modb[1]&0x4))):
                                    print "TT3 mod: ", moda[1], ", atom: ", moda[2], ", modCompare: ", modb[1], ", atom:", moda[2]
                                    return False
                            if(optimisation&0x8) == 8:
                                if(moda[1] == modb[1]) and (moda[2] == modb[2]):
                                    if debug:
                                        print "TF1 1 nMod = modCompare, ", mod, " = ", modCompare, "\n atom = atomCompare, ", atom, " = ", atomCompare
                                    return False
                            if (optimisation&0x10) == 16:
                                if(((moda[1]&0x2) != (modb[1]&0x2)) and ((moda[1]&0x2) == 1) and
                                       (moda[2] == modb[2]) and ((moda[1]&0x1) == (modb[1]&0x1)) and
                                       ((moda[1]&0x4) == (modb[1]&0x4)) and ((moda[1]&0x4) == 0)):
                                    if debug:
                                        print "TF2 mod: ", moda[1], ", atom: ", moda[2], ", modCompare: ", modb[1], ", atom:", moda[2]
                                    return False
                            if (optimisation&0x20) == 32:
                                if((moda[1]&0x3) == (modb[1]&0x3)) and (modb[2] == moda[2]) and \
                                        ((modb[1]&0x4) != (moda[1]&0x4)):
                                    print "TT FF mod: ", moda[1], ", atom: ", moda[2], ", modCompare: ", modb[1], ", atom:", moda[2]
                                    return False
        return True

    def export_rules(self, queue, filename='ans.elp', debug=0):
        if debug == 1:
            print "export_rules(self, queue, filename = 'ans.elp') -> queue"
            print queue
            print ""
        output = file(filename, "w")
        for line in queue:
            if debug == 1:
                print "export_rules(self, queue, filename = 'ans.elp') -> line"
                print line
                print ""
            #print line
            if isinstance(line[0], list): #STILL WORKING HERE
                for head in range(0, len(line[0])):
                    output.write(line[0][head])
                    #print "line[0][head]:", line[0][head]
                    #print "head:", head, "len(line)-2:", len(line[0])-2, "len(line):", len(line[0])
                    #print ""
                    if head != len(line[0])-1:
                        #print "IM WRITING DISJUNCTION"
                        output.write(" v ")

                output.write(" :- ")
                for tail in range(0, len(line[1])):
                    output.write(line[1][tail])
                    #print "tail:", tail, "len(line):", len(line[1])
                    if tail != len(line[1])-1:
                        output.write(", ")
            
            elif isinstance(line[0], str):
                for head in range(0, len(line)):
                    output.write(line[head])

                    if head != len(line)-1:
                        output.write(" v ")    
            output.write(".\n")
        output.close()          
        return True

    def build_program(self, fileName):
        body, rule, head, tail, tempProgram = [], [], [], [], []
        if fileName != '':
            try:
                print "fileName:", fileName
                input = file(fileName, "r") #need to implement try/except block to catch exceptions
            except IOError:
                print "<file doesnt exist.>"
                os.system("pause")
                exit(1)
            for line in input.readlines():
                try:
                    if '%' in line:
                        line = line[0: line.index('%')]
                    if not line.index('.') == -1: #need to implement system such that rules can be staggered over various lines or a line may have multiple rules.
                        tempProgram.append(line[0:line.index('.')+1].strip())
                except ValueError: pass
            for line in tempProgram:
                body, rule, head, tail = [], [], [], []
                line = line.replace('.', '')
                body = line.split(":-")
                if len(body) == 1:
                    body[0] = body[0].strip()
                    rule = body[0].split(" v ")
                    for count in range(0, len(rule)):
                        rule[count] = rule[count].strip()
                elif len(body) == 2:
                    head = body[0].split(' v ')
                    for count in range(0, len(head)):
                        head[count] = head[count].strip()
                    tail = body[1].split(',')
                    for count in range(0, len(tail)):
                        tail[count] = tail[count].strip()
                    rule.append(head)
                    rule.append(tail)
                self.program.append(rule)
        print self.program

    def ImportAnsSet(self, fileName = ''):
        queue = []
        if fileName != '':
            try:
                input = file(fileName, "r") #need to implement try/except block to catch exceptions
            except IOError:
                print "<file doesnt exist.>"
                os.system("pause")
                exit(1)
        for line in input.readlines():
            try:
                queue.append(line.strip('\n'))
            except ValueError: pass
        #print queue
        return queue


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

    def updateValuation(self, statStruct, valuatorString):
        countb = len(statStruct.keys())
        while countb:
            counta = len(statStruct[statStruct.keys()[countb-1]])
            while counta:
                temp = valuatorString&0x1
                valuatorString = valuatorString>>1
                if len(statStruct[statStruct.keys()[countb-1]][counta-1]) == 5:
                    statStruct[statStruct.keys()[countb-1]][counta-1][4] = temp
                elif len(statStruct[statStruct.keys()[countb-1]][counta-1]) < 5:
                    statStruct[statStruct.keys()[countb-1]][counta-1].append(temp)                             
                counta -= 1
            countb -= 1

    def updateIndex(self, lineIndex, dict):
        tempDict = {}
        for index in range(0, lineIndex):
            tempDict[dict.keys()[index]] = copy.copy(dict[dict.keys()[index]])
        for index in range(lineIndex, len(dict.keys())):            
            tempDict[dict.keys()[index]-1] = copy.copy(dict[dict.keys()[index]])
        # print "tempDict:", tempDict
        return tempDict

    def remAllEpAtoms(self, line):
        temp = []
        #print "remAllEpAtoms(", line, ")"
        if isinstance(line, type([])):
            for index in range(0, len(line)):
                #print "remAllEpAtoms(line) -> index:", index
                #print "remAllEpAtoms(line) -> line[index]:", line[index]
                if not line[index].find('K') != -1 and not line[index].find('M') != -1:
                    temp.append(line[index])
        if not len(temp): return
        else: return temp
            
            
    def build_interpreted_program(self, program, statStruct, valuatorString):
        """
            showPossibleSet: Takes in the queue of rules, the line locations of its modal operators, the character locations
                of modal operators, and the integer value which determines the truth valuation of each modal operator.
        """
        
        valuation = copy.deepcopy(program)
        modTemp, count, flag = 0, 0, 0
        if len(program) > 0 and len(statStruct.keys()) == 0:
            return queue

        modTemp = len(statStruct.keys())
        self.updateValuation(statStruct, valuatorString)
        
        for line in statStruct.keys():
            flag = 0
            for epAtom in range(0, len(statStruct[line])):
                if statStruct[line][epAtom][4] == 0:
                    flag = 1
                    #print "found 0, breaking"
                    break
            #os.system("pause")
            #print "flag:", flag
            if flag == 1:
                valuation[line].append(1)
            else:
                valuation[line][1] = self.remAllEpAtoms(valuation[line][1])
                if valuation[line][1] == None:
                    valuation[line] = valuation[line][0]
        
        #pprint.pprint(valuation)
        total = len(valuation)
        count = 0
        tempValuation = []
        for line in valuation:
            #print "line[-1]:", line[-1]
            if line[-1] != 1:
                tempValuation.append(line)
                
        #pprint.pprint(tempValuation)
        return tempValuation
        
    def runSession(self):
        count = 0
        try:
            wvObj = self.generate_worldview(self.program, self.stats)
            while 1:
                count += 1
                print wvObj.next()
        except StopIteration:
            del self
                
if __name__ == '__main__':
    path = os.getcwd() + "\\worldviews"
    files = os.listdir("worldviews")
    session = Wviews("worldviews\\interview.txt")
    wview_grounder = grounder.grounding(session)
    countString = []
    length = 5
    base = 4

    for count in range(0, length):
        countString.append(0)
    print countString

    while 1:
        countString = wview_grounder.incString(countString, base, length)
        print countString
        os.system("pause")

    #"worldviews\\interview.txt"
    #for inst in files:
    #    session = elp("worldviews\\" + inst)
    #    session.runSession()
    #    print "im here!"
    #    os.system("pause")
    #    os.system("cls")
    #    del session
