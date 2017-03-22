"""
    grounder.py: Grounding functionality for logic programs.
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

import math
import re
from itertools import product
import wviews


class Predicate(object):
    def __init__(self, label, arguments=None):
        self.label = label
        self.arguments = arguments
        self.indexed_arguments = []

    def ground_predicate(self):
        pass

    def variables(self):
        pass

    def constants(self):
        pass

    def __str__(self):
        return '%s(%s)' % (self.label, ','.join(self.arguments))

    def __hash__(self):
        return hash(self.__str__())


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

    def __init__(self, tokenised_rules):
        self.tokenised_rules = tokenised_rules
        self.variables = set()
        self.constants = set()
        self.label_id = 1
        self.predicate_id = 1
        self.constant_id = 1
        self.variable_id = 1
        self.variable_id_lookup = {}
        self.constant_id_lookup = {}
        self.predicate_arg_regex = re.compile(r'\(([\W\w]*)\)')

    @staticmethod
    def get_variable_instantiation(variable_pool, constant_pool):
        for ground_instantiation in product(tuple(variable_pool), len(constant_pool)):
            yield ground_instantiation

    def get_variables_and_constants(self):
        for tokenised_rule in self.tokenised_rules:
            if tokenised_rule.head:
                self.process_rule_section(tokenised_rule.head)
            if tokenised_rule.tail:
                self.process_rule_section(tokenised_rule.tail, head=False)

    def process_rule_section(self, section, head=True):
        section_separator = 'v' if head else ','
        for unground_predicate in section:
            predicate_arguments_token = self.predicate_arg_regex.search(unground_predicate)
            if predicate_arguments_token:
                self.process_predicate_arguments(unground_predicate[:unground_predicate.find('(')],
                                                 predicate_arguments_token.group(1).split(section_separator))

    def process_predicate_arguments(self, label, raw_argument_list):
        """
        Given the arguments of a predicate, divide them into variables and values to be ground later.

        Arguments:
         * label (str) - label for the predicate
         * raw_argument_list (str) - the list containing raw argument strings that are potentially values or variables
        """
        for raw_argument in raw_argument_list:
            argument = raw_argument.strip()
            if argument.isupper():
                if argument not in self.variables:
                    self.variables.add(argument)
                    self.variable_id_lookup[self.variable_id] = argument
                    self.variable_id += 1

            else:
                if argument not in self.constants:
                    self.constants.add(argument)
                    self.constant_id_lookup[self.variable_id] = argument
                    self.constant_id += 1

            Predicate(label)

    def ground_predicates(self, tokenised_rules):
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


        for rule in tokenised_rules:
            pass

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

    def separate_predicate_rules(self, program):
        pass
        #tempProgram = []
        #for line in program:
        #    if isinstance(line, type([])): pass

    def build_variable_grounding_list(self, program):
        pass

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
    session = wviews.elp('worldviews\\interview.txt')
    grounder = Grounder(session)
    base = []

    try:
        while 1:
            incObj = grounder.increment_string(base, 3, 4)
    except StopIteration:
        pass
