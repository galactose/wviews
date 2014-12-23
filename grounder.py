import os, pprint, re, copy, math, elp
class grounding():
    """
        grounder():
            Generic Grounder object for elp.
            
        Summary
        Queue<string>& groundPredicates(Queue<string> &queue);
        Stack<int>& incrementString(Stack<int> &stack, int base, int length);
        Queue<int>& varPerRule(Queue<string>& queue, Queue<int>& varCQ);
        Queue<string>& varGroundQueue(Queue<string> &queue);
        string replaceVariable(string rule, Queue<string> &variable, Queue<string> & ground, Stack<int> &nBase);
        Queue<string>& copyPredicateRules(Queue<string>& queue, Queue<string>& predicates, bool ruleSwitch);
    """

    def __init__(self, fileName): pass

    def groundingSession(self, program):
        """
            groundPredicates :- This function takes the program input as argument and reduces all
            variables present in predicated rules and facts. This process is required as facts containing
            variable values will be considered dangerous reasoning by DLV's standards and will return without
            calculating the disjunctive answer set.

            grounding example :- 
            loves_coffee(ted). loves_tea(chip). loves_coffee(nancy).
            loves_hot_drinks(X) :- loves_coffee(X).

            ground :-
            loves_coffee(ted). loves_tea(chip). loves_coffee(nancy).
            loves_hot_drinks(ted) :- loves_coffee(ted).
            loves_hot_drinks(chip) :- loves_coffee(chip).
            loves_hot_drinks(nancy) :- loves_coffee(nancy).*/
        """
        groundingString = []
        varLit = buildVariableGroundingList(program)
        varCount = len(varlit[0])
        litCount = len(varlit[1])
        
        # -- separate predicated and non-predicated rules -- #

        # -- create list of variables in each predicated rule -- #
        
        # create a grounding string where:
            # length is the count of variables
            # instances are the base of the string
             
        for index in range(0, len(predicatedRules)):
            #push 0's on grounding string
            for count in range(0, varCount):
                groundingString.append(0)
            for count in range(0, math.pow(grnd.queueCount(), ruleLength)):
                self.replaceVariable(rule, var, ground, groundingString)
                groundingString = self.incString(groundingString, varCount, litCount)
        program = predicatedRules
        program.extend(unPredicatedRules)
        return program

    """
    Queue<string>& groundPredicates(Queue<string> &queue)
    {
        Queue<string> copy, var, grnd, qTemp, addPred, nonPred;
        Stack<int> nBase;
        Queue<int> varCount;
        bool flag = false;
        string dataOut, variable, ground, backup, dataString;
        int data = 0, temp = 0, length = 0, base = 0, operation = 0, count = 0, ruleLength = 0;
        copy = copyQueue(queue, copy);
        
        copy = varGroundQueue(copy); //make queue of variables
        while(copy.queueCount() > 0)
        {
            copy.dequeue(dataOut); //separating variables from ground instances in this queue
            if(isStringUpper(dataOut))
            {
                var.enqueue(dataOut);
            }
            else
            {
                grnd.enqueue(dataOut);
            }
        }

        length = var.queueCount();				//count of variables
        base = grnd.queueCount();				//get count of grounded atoms
        qTemp = copyQueue(queue, qTemp);	    //maintaining original queue, copying editable queue
        addPred = copyPredicateRules(qTemp, addPred, true);  //extracting rules containing predicates 
        nonPred = copyPredicateRules(qTemp, nonPred, false); //extracting non-predicated rules

        varCount = varPerRule(addPred, varCount); //determine how many unique variables exist in each line
        while(addPred.queueCount())
        {
            varCount.dequeue(temp);
            ruleLength = temp;
            while(temp)
            {
                nBase.pushStack(0);
                temp--;
            }
            addPred.dequeue(dataString);
            backup = dataString; 
            operation = pow((double)grnd.queueCount(), ruleLength);
            while(operation)
            {
                dataString = replaceVariable(backup, var, grnd, nBase);
                nonPred.enqueue(dataString);
                nBase = incrementString(nBase, base, ruleLength);
                operation--;
            }
        }
        queue = copyQueue(nonPred, queue);
        return queue;
    """

    def sepPredRules(self, program): pass
        #tempProgram = []
        #for line in program:
        #    if isinstance(line, type([])): pass
    
    def buildVariableGroundingList(self, program): pass
    
    def incString(self, nBase, base, length):
        """
            incrementString :- 
            increments the base n string up one value, if it has reached the highest value it
            will go back down to 0 and raise the next value up by one.
            stack: the number string, values are always accessed from the top of the stack
            base: the count of ground instances, e.g. ground instance of p(bob) would be bob
            length: the count of variables, identified by being all upper case
        """
        flag, carry = False, True
        if len(nBase) == 0 and base > 0 and length > 0:
            for count in range(0, length):
                nBase.append(0)
        for val in nBase:
            if val != base-1:
                flag = True
                break
        if flag == False or base == 0 or length == 0:
            return nBase
        count = length
        
        while count != 0 or carry == True:
            carry = True
            count = length
            while count and carry:
                if nBase[length - count] < base-1:
                    nBase[length - count] += 1
                    carry = False
                else:
                    nBase[length - count] = 0
                count -= 1
            yield nBase

    def replaceVariable(self, rule, variable, ground, nBase):
        pass
        
if __name__ == '__main__':
    session = elp.elp("worldviews\\interview.txt")
    grounder = grounding(session)
    base = []
    
    try:
        while 1:
            incObj = grounder.incString(base, 3, 4)
    except StopIteration:
        
    finally:
        print base
        os.system("pause")