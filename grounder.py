import os
import math
import elp


class Grounder(object):
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

    def __init__(self, file_name):
        pass

    def ground_predicates(self, program):
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
        grounding_string = []
        varLit = self.build_variable_grounding_list(program)
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
                self.replaceVariable(rule, var, ground, grounding_string)
                grounding_string = self.increment_string(grounding_string, varCount, litCount)
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

    def sepPredRules(self, program):
        pass
        #tempProgram = []
        #for line in program:
        #    if isinstance(line, type([])): pass
    
    def build_variable_grounding_list(self, program):
        pass

    @staticmethod
    def increment_string(base_n_string, string_base, string_length):
        """
            incrementString :- 
            increments the base n string up one value, if it has reached the highest value it
            will go back down to 0 and raise the next value up by one.
            stack: the number string, values are always accessed from the top of the stack

            Arguments:
             * string_base (int) - the count of ground instances, e.g. ground instance of p(bob) would be bob
             * string_length (int): the count of variables, identified by being all upper case
        """
        not_max_value_flag = False
        if not base_n_string and string_base > 0 and string_length > 0:
            base_n_string = [0] * string_length

        for val in base_n_string:
            if val != string_base - 1:
                not_max_value_flag = True
                break

        if not not_max_value_flag or not string_base or not string_length:
            # return the string value if we've reached the largest value for the incrementer
            # possibly raise stop iteration here instead
            raise StopIteration

        iteration_count = string_length

        carry = True
        while iteration_count or carry:
            carry = True
            iteration_count = string_length
            while iteration_count and carry:
                # going from the bottom, if a value is less than it's max, increment it and indicate that carry isn't
                # necessary, otherwise set to zero and move to next value up in string
                if base_n_string[string_length - iteration_count] < string_base - 1:
                    base_n_string[string_length - iteration_count] += 1
                    carry = False
                else:
                    base_n_string[string_length - iteration_count] = 0
                iteration_count -= 1
            yield base_n_string

    def replace_variable(self, rule, variable, ground, base_n_string):
        pass

# /*
# 	replaceVariable: replaces all instances of the variable indicated in parameters with the
# 	ground instance also indicated in the parameters,
# */
# Queue<string>& replaceVariable(Queue<string> &queue, Queue<string> &variable, Queue<string> &ground, Stack<int> &nBase)
# {
# 	int pos = 0, lastMark = 0, temp = queue.queueCount(), stackNo = 0, replace = 0;
# 	string dataOut, process, var, grnd, cycle;
# 	bool skip = false;
# 	Stack<int> sTemp;
#
# 	while(nBase.stackCount() > 0)
# 	{
# 		nBase.popStack(stackNo);
# 		sTemp.pushStack(stackNo);
#
# 		replace = (ground.queueCount() - stackNo)-1;
#
# 		while(stackNo >= 0)
# 		{
# 			ground.dequeue(grnd);
# 			ground.enqueue(grnd);
# 			stackNo--;
# 		}
#
# 		while(replace > 0)
# 		{
# 			ground.dequeue(cycle);
# 			ground.enqueue(cycle);
# 			replace--;
# 		}
#
# 		variable.dequeue(var);
# 		variable.enqueue(var);
#
# 		temp = queue.queueCount();
#
# 		while(temp > 0)
# 		{
# 			queue.dequeue(dataOut);
# 			pos = dataOut.size();
# 			for(int i = 0; i < pos; i++)
# 			{
# 				pos = dataOut.size();
# 				if(dataOut[i] == '(')
# 				{
# 					skip = false;
# 					lastMark = i+1;
# 					for(int j = i; (j < pos)&&(!skip); j++)
# 					{
# 						if(dataOut[j] == ',')
# 						{
# 							process = dataOut.substr(lastMark, (j-lastMark));
# 							process = removeSpaces(process);
# 							if(process == var)
# 							{
# 								dataOut.replace(lastMark, (j-lastMark), grnd);
# 							}
#
# 							lastMark = j+1;
# 						}
# 						if(dataOut[j] == ')')
# 						{
# 							process = dataOut.substr(lastMark, (j-lastMark));
# 							process = removeSpaces(process);
# 							if(process == var)
# 							{
# 								dataOut.replace(lastMark, (j-lastMark), grnd);
# 							}
#
# 							lastMark = j+1;
# 							skip = true;
# 						}
# 					}
# 				}
# 			}
# 			temp--;
# 			queue.enqueue(dataOut);
# 		}
# 	}
# 	while(sTemp.stackCount() > 0)
# 	{
# 		sTemp.popStack(stackNo);
# 		nBase.pushStack(stackNo);
# 	}
# 	return queue;

    def var_ground_queue(self):
        """
            if varLit true return the number of variables
            if varLit false return the number of ground predicates
            variable is defined as being between brackets () and all upper case
            ground predicate being defined as a block of characters, not all of which are uppercase
        """
        pass

# /*
# 	if varLit true return the number of variables
# 	if varLit false return the number of ground predicates
# 	variable is defined as being between brackets () and all upper case
# 	ground predicate being defined as a block of characters, not all of which are uppercase
# */
#  Queue<string>& varGroundQueue(Queue<string> &queue)
# {
# 	Queue<string> qTemp, lit;
# 	qTemp = copyQueue(queue, qTemp);
# 	int litCount = 0, varCount = 0, temp = queue.queueCount(), pos = 0, lastMark = 0, nextTemp = 0;
# 	string dataOut, process;
# 	bool skip = false;
# 	while(temp)
# 	{
# 		qTemp.dequeue(dataOut);
# 		pos = dataOut.size();
# 		for(int i = 0; i < pos; i++)
# 		{
# 			if(dataOut[i] == '(')
# 			{
# 				skip = false;
# 				lastMark = i+1;
# 				for(int j = i; (j < pos)&&(!skip); j++)
# 				{
# 					if(dataOut[j] == ',')
# 					{
# 						process = dataOut.substr(lastMark, (j-lastMark));
# 						process = removeSpaces(process);
#
# 						litCount++;
# 						lit.enqueue(process);
#
# 						lastMark = j+1;
# 					}
# 					if(dataOut[j] == ')')
# 					{
# 						process = dataOut.substr(lastMark, (j-lastMark));
# 						process = removeSpaces(process);
#
# 						litCount++;
# 						lit.enqueue(process);
#
# 						lastMark = j+1;
# 						skip = true;
# 					}
# 				}
# 			}
# 		}
# 		temp--;
# 	}
#
# 	temp = lit.queueCount();
# 	while(temp > 0)
# 	{
# 		lit.dequeue(dataOut);
#
# 		nextTemp = lit.queueCount();
# 		while(nextTemp > 0)
# 		{
# 			lit.dequeue(process);
# 			if(dataOut != process)
# 			{
# 				lit.enqueue(process);
# 			}
# 			else
# 			{
# 				--temp;
# 			}
# 			nextTemp--;
# 		}
# 		temp--;
# 		lit.enqueue(dataOut);
# 	}
#
# 	queue = copyQueue(lit, queue);
#
# 	return queue;
# }


if __name__ == '__main__':
    session = elp.elp('worldviews\\interview.txt')
    grounder = Grounder(session)
    base = []
    
    try:
        while 1:
            incObj = grounder.increment_string(base, 3, 4)
    except StopIteration:
        pass

    print base
    os.system('pause')
