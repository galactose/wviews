/**************************************************************
University of Western Sydney - Penrith
School of Computing and Mathematics, Y Building.
Epistemic Answer Set Logic Parser
Author - Michael Kelly
Student Number - 15053927.

Summary: This program reads in programs containing lists of
	rules of the form:
		[a-z[a-z]*[(A-Z[A-Z]*)] [v a-z*]] :- [[~|-]K|M[a-z]*,]*[[not]a-z*]
	where a-z represents atoms, 
		  v represents disjunction,
		  "," represents conjunction,
		  K|M represents the modal operators,
			K: 'Knows' and
			B: 'Believes'
		  and ":-" which is best described as 
			"is true if the following is also true"

	and returns the applicable worldviews derived from the 
	rules.
**************************************************************/

#include <fstream>
#include <stdlib.h>
#include <iomanip>
#include <math.h>
#include "queue.cpp"
#include "stackADT.h"
#include <string>
#include <iostream>
#include <ctype.h>

using namespace std;

//Function prototypes
Queue<string>& build(Queue<string> &queue, char *filename);
void exportRules(Queue<string> &queue, char *filename);
Queue<string>& parseRules(Queue<string> &queue);
void showInstantiations(Queue<string> &queue, Queue<int> &rulePos, Queue<int> &charPos,  Queue<string> &copy);
Queue<string>& showPossibleSet(Queue<string> &queue, Queue<int> &rulePos, Queue<int> &charPos, long int binaryEval);
bool checkValidity(Queue<string> &model, Queue<string> &rules, long int binMod, Queue<int> &rulePos, Queue<int> &charPos);
string removeModOperators(string rule, int beginPos, int endPos);
int modalOpCount(Queue<int> &modalLines, int focus);
bool compareAtoms(Queue<string> &model, string data, bool modalOpType);
bool isRuleLit(string modRule);
Queue<string>& groundPredicates(Queue<string> &queue);

string removeSpaces(string data);
Stack<int>& incrementString(Stack<int> &stack, int base, int length);
Queue<string>& varGroundQueue(Queue<string> &queue);
Queue<string>& replaceVariable(Queue<string> &queue, Queue<string> &variable, Queue<string> & ground, Stack<int> &nBase);
Queue<string>& copyPredicateRules(Queue<string>& queue, Queue<string>& predicates);

//queue manipulating functions
void printQueue(Queue<string> &queue);
void printQueue(Queue<string> &queue, bool flag);
void printQueue(Queue<int> &queue);
Queue<string>& emptyQueue(Queue<string> &queue);
Queue<string>& copyQueue(Queue<string> &queue, 	Queue<string> &copy);
Queue<int>& copyQueue(Queue<int> &queue, Queue<int> &copy);
Queue<string>& appendQueue(Queue<string>& queue, Queue<string>& queue2);

//string manipulators
bool isStringUpper(string data);
int uniqueLines(Queue<int> &queue);

//entrypoint here.
int main(int argc, char *argv[])
{
	Queue<string> rules, copy; //contains lists of epistemic rules.
	Queue<int> modRulePos; //holds line numbers of rules containing modal operators.
	Queue<int> modCharPos; //holds character positions in a rule of where a modal operator is.
	int qLength = 0, tempLen = 0, relPos = 0, lastRule = 0, noModalOp = 0;
	string dataOut;
	int pos = 0, posAux = 0, count = 0;

	if(argc != 2)
	{
		printf("usage: elp filename");
		exit(1);
	}

	build(rules, argv[1]);
	rules = parseRules(rules);

	printQueue(rules);
	rules = groundPredicates(rules);
    
/*
	qLength = rules.queueCount();
	for(int rule = 0; rule < qLength; rule++)
	{
		rules.dequeue(dataOut);
		tempLen = dataOut.length();
		for(int pos = 0; pos < tempLen; pos++)
		{	
			if(((dataOut[pos])=='K')||((dataOut[pos])=='M'))
			{
				modRulePos.enqueue(rule+1);
				modCharPos.enqueue(pos);
			}
		}
		rules.enqueue(dataOut);	
		noModalOp = 0;
	}
	showInstantiations(rules, modRulePos, modCharPos, copy);	
*/
	return 0;
}

Queue<string>& groundPredicates(Queue<string> &queue)
{
	Queue<string> copy, var, grnd, qTemp, addPred;
	Stack<int> nBase;
	bool flag = false;
	string dataOut, variable, ground;
	int data = 0, temp = 0, length = 0, base = 0, operation = 0;
	copy = copyQueue(queue, copy);

	copy = varGroundQueue(copy); //make queue of variables
	while(copy.queueCount() > 0)
	{
		copy.dequeue(dataOut);
		if(isStringUpper(dataOut))
		{
			var.enqueue(dataOut);
		}
		else
		{
			grnd.enqueue(dataOut);
		}
	}
	//printQueue(var);
	//printQueue(grnd);

	length = var.queueCount(); 
	base = grnd.queueCount(); //get count of var/grnd
	operation = pow((double)var.queueCount(), grnd.queueCount()); //get how many ops will take place
	cout<<"operation: "<<operation<<"\n";
	temp = length;
	while(temp)
	{
		nBase.pushStack(0);
		temp--;
	}
	temp = length;

	qTemp = copyQueue(queue, qTemp);
	addPred = copyPredicateRules(qTemp, addPred);

	while(operation > 0)
	{	
		qTemp = replaceVariable(qTemp, var, grnd, nBase);
		if(operation > 1)
		{
			qTemp = appendQueue(qTemp, addPred);
		}
		nBase = incrementString(nBase, base, length);
		cout<<"operation: "<<operation<<"\n";
		operation--;
	}

	printQueue(qTemp);
	//exportRules(qTemp, "test.txt");
/*
	while(temp > 0)
	{
		nBase.popStack(data);
		printf("data: %d\n", data);
		temp--;
	}
*/
	return queue;
}

/*
	replaceVariable: replaces all instances of the variable indicated in parameters with the 
	ground instance also indicated in the parameters, 
*/
Queue<string>& replaceVariable(Queue<string> &queue, Queue<string> &variable, Queue<string> &ground, Stack<int> &nBase)
{
	int pos = 0, lastMark = 0, temp = queue.queueCount(), stackNo = 0, replace = 0;
	string dataOut, process, var, grnd, cycle;
	bool skip = false;
	Stack<int> sTemp;

	while(nBase.stackCount() > 0)
	{
		nBase.popStack(stackNo);
		sTemp.pushStack(stackNo);

		replace = (ground.queueCount() - stackNo)-1;

		while(stackNo >= 0)
		{
			ground.dequeue(grnd);
			ground.enqueue(grnd);
			stackNo--;
		}
		
		while(replace > 0)
		{
			ground.dequeue(cycle);
			ground.enqueue(cycle);
			replace--;
		}

		variable.dequeue(var);
		variable.enqueue(var);

		temp = queue.queueCount();

		while(temp > 0)
		{
			queue.dequeue(dataOut);
			pos = dataOut.size();
			for(int i = 0; i < pos; i++)
			{
				pos = dataOut.size();
				if(dataOut[i] == '(')
				{
					skip = false;
					lastMark = i+1;
					for(int j = i; (j < pos)&&(!skip); j++)
					{
						if(dataOut[j] == ',')
						{
							process = dataOut.substr(lastMark, (j-lastMark));
							process = removeSpaces(process);
							if(process == var)
							{
								dataOut.replace(lastMark, (j-lastMark), grnd);
							}

							lastMark = j+1;
						}
						if(dataOut[j] == ')')	
						{
							process = dataOut.substr(lastMark, (j-lastMark));
							process = removeSpaces(process);
							if(process == var)
							{
								dataOut.replace(lastMark, (j-lastMark), grnd);
							}

							lastMark = j+1;
							skip = true;
						}
					}
				}
			}
			temp--;
			queue.enqueue(dataOut);
		}
	}
	while(sTemp.stackCount() > 0)
	{
		sTemp.popStack(stackNo);
		nBase.pushStack(stackNo);
	}
	return queue;
}

//appends queue 2 to queue 1
Queue<string>& appendQueue(Queue<string>& queue, Queue<string>& queue2)
{
	int temp = queue2.queueCount();
	string data;
	while(temp > 0)
	{
		queue2.dequeue(data);
		queue2.enqueue(data);
		queue.enqueue(data);
		temp--;
	}
	return queue;
}

Queue<string>& copyPredicateRules(Queue<string>& queue, Queue<string>& predicates)
{
	int count = queue.queueCount(), pos = 0, lastMark = 0;
	string data, process;
	bool skip = true, lineDone = false;

	while(count > 0)
	{
		queue.dequeue(data);
		queue.enqueue(data);
		pos = data.size();
		lineDone = false;
		for(int i = 0; (i < pos)&&!lineDone; i++)
		{
			if(data[i] == '(')
			{
				skip = false;
				lastMark = i+1;
				for(int j = i; (j < pos)&&(!skip); j++)
				{
					if(data[j] == ',')
					{
						process = data.substr(lastMark, (j-lastMark));
						process = removeSpaces(process);
						if(isStringUpper(process)&&!lineDone)
						{
							predicates.enqueue(data);
							lineDone = true;
						}
						lastMark = j+1;
					}
					if(data[j] == ')')	
					{
						process = data.substr(lastMark, (j-lastMark));
						process = removeSpaces(process);
						if(isStringUpper(process)&&!lineDone)
						{
							predicates.enqueue(data);
							lineDone = true;
						}
						lastMark = j+1;
						skip = true;
					}
				}
			}
		}
		count--;
	}
	return predicates;
}

// stack: the number string
// base: the count of ground instances, e.g. ground instance of p(bob) would be bob
// length: the count of variables
Stack<int>& incrementString(Stack<int> &stackUse, int base, int length)
{
	bool flag = false, carry = true;
	Stack<int> sTemp;
	int temp = length, data = 0, no = 0;

	//detecting if the stack string is full
	while((stackUse.stackCount() > 0)&&(!flag))
	{
		stackUse.popStack(data);
		sTemp.pushStack(data);
		if(data != base-1)
		{
			flag = true;
		}
	}
	//if full return the stack without performing the operation
	if(flag == false)
	{
		return stackUse;
	}

	while(sTemp.stackCount() > 0)
	{
		sTemp.popStack(data);
		stackUse.pushStack(data);
	}

	temp = length;
	no = 0;
	while(temp&&carry) //temp so it doesnt carry over the length, carry so it ends when theres nothing to carry
	{
		stackUse.popStack(data); //remove next value to work with it
		//printf("data: %d\n", data);
		if(data+1 != base) //if this value isnt at the maximal possible value
		{
			data++;		   //increment it
			carry = false; //escape the loop
		}
		temp--; //decrement the loop
	}
	//printf("temp= %d, length = %d\n", temp, length);

	while(temp != length)
	{
		stackUse.pushStack(data);
		//printf("data= %d\n", data);
		data = 0;
		temp++;
	}

	return stackUse;
}

/*
	if varLit true return the number of variables
	if varLit false return the number of ground predicates
	variable is defined as being between brackets () and all upper case
	ground predicate being defined as a block of characters, not all of which are uppercase
*/
 Queue<string>& varGroundQueue(Queue<string> &queue)
{
	Queue<string> qTemp, lit;
	qTemp = copyQueue(queue, qTemp);
	int litCount = 0, varCount = 0, temp = queue.queueCount(), pos = 0, lastMark = 0, nextTemp = 0;
	string dataOut, process;
	bool skip = false;
	while(temp)
	{
		qTemp.dequeue(dataOut);
		pos = dataOut.size();
		for(int i = 0; i < pos; i++)
		{
			if(dataOut[i] == '(')
			{
				skip = false;
				lastMark = i+1;
				for(int j = i; (j < pos)&&(!skip); j++)
				{
					if(dataOut[j] == ',')
					{
						process = dataOut.substr(lastMark, (j-lastMark));
						process = removeSpaces(process);
	
						litCount++;
						lit.enqueue(process);

						lastMark = j+1;
					}
					if(dataOut[j] == ')')
					{
						process = dataOut.substr(lastMark, (j-lastMark));
						process = removeSpaces(process);

						litCount++;
						lit.enqueue(process);

						lastMark = j+1;
						skip = true;
					}
				}
			}
		}
		temp--;
	}

	temp = lit.queueCount();
	while(temp > 0)
	{
		lit.dequeue(dataOut);
		
		nextTemp = lit.queueCount();
		while(nextTemp > 0)
		{
			lit.dequeue(process);
			if(dataOut != process)
			{
				lit.enqueue(process);
			}
			else
			{
				--temp;
			}
			nextTemp--;
		}
		temp--;
		lit.enqueue(dataOut);
	}

	queue = copyQueue(lit, queue);

	return queue;
}

string removeSpaces(string data)
{
	int pos = data.size();
	for(int j = 0; j < pos; j++)
	{
		if(data[j] == ' ')
		{
			data.replace(j, 1, "");
			pos--;
		}
	}
	return data;
}

/*
int literalCount()
{
	return ;
}
*/
//build: builds data from file into a queue of blocks 
//	of incoherant strings
Queue<string>& build(Queue<string> &queue, char *filename)
{
	ifstream fp;
	string line;
	bool comment = false;
	int pos = 0;

	fp.open(filename, ios::in);
	
	if(!fp)
	{
		printf("\nCannot open %s",filename);
		exit(1);
	}
	
	while((!fp.eof())&&(!fp.fail()))
	{
		getline(fp, line);
		pos = line.size();
		comment = false;
		while(pos&&!comment)
		{
			if((line[pos-1] == '%')||(line[pos-1] == '#'))
			{
				line = line.substr(0 , pos-2);
				comment = true;
			}
			pos--;
		}
		if(!line.empty())
		{
			queue.enqueue(line);
		}
	}
	fp.close();
	
	return queue;
} // build

//isStringUpper: returns true if string passed to the function is completely uppercase
//	useful in the case of detecting a predicate variable
bool isStringUpper(string data)
{
	int temp = data.size();
	while(temp)
	{
		if(islower(data[temp]))
		{
			return false;
		}
		temp--;
	}
	return true;
}

//printQueue: prints out the queue as it stands.
void printQueue(Queue<string> &queue)
{
	string dataOut;
	int temp = queue.queueCount();
 	printf("Rules-------o\n");
	while(temp)
	{
		queue.dequeue(dataOut);
		cout<<dataOut<<"\n";
		queue.enqueue(dataOut);
		temp--;
	}
	printf("-------------\n");
	return;
}

void printQueue(Queue<string> &queue, bool flag)
{
	string dataOut;
	int temp = queue.queueCount();
 	printf("Rules-------o\n");
	if(flag)
		printf("WV = ");
	while(temp)
	{
		queue.dequeue(dataOut);
		cout<<dataOut<<"\n";
		queue.enqueue(dataOut);
		temp--;
	}
	printf("-------------\n");
	return;
}

void printQueue(Queue<int> &queue)
{
	int temp = queue.queueCount();
	int dataOut;
	cout<<"-------------\n";
	while(temp)
	{
		queue.dequeue(dataOut);
		cout<<dataOut<<"\n";
		queue.enqueue(dataOut);
		temp--;
	}
	cout<<"-------------\n";
	return;
}

//parseRules: takes character blocks from queue, collects them
// into coherant rules/facts put in the queue.
/*
	formatCheck: Takes in a coherant queue of rules and determines if
		all the rules fit the format of an epistemic/disjunctive/normal
		logic program. If not consistent, the value returned is false.
		
		The format of logic programs entered must fix the format:
			[a-z [v a-z*]] :- [[~|-]K|M[a-z]*,]*[[not]a-z*]
*/
Queue<string>& parseRules(Queue<string> &queue)
{
	string dataOut, newString;
	int temp = queue.queueCount();
	int tempLen = 0, npos = 0, entailLoc = 0;
	string::size_type pos, entailPos, check;

	bool or = false, entails = false, mod = false, end = false, error = false, and = false;
	bool not = false, comment = true;
	/*
	while(temp)
	{
		queue.dequeue(dataOut);
		tempLen = dataOut.length();

		newString+=dataOut;

		comment = false;
		for(int j = 0; j < tempLen; j++)
		{	
			if(dataOut[j] =='.')
			{
				queue.enqueue(newString);
				newString="\0";
			}
		}
		temp--;		
	}
	*/
	temp = queue.queueCount();
	while(temp)
	{
		entails = false;
		end = false;
		mod = false;
		or = false;
		and = false;
		not = false;

		queue.dequeue(dataOut);
		queue.enqueue(dataOut);
		pos = dataOut.find("not", 0);	
		if (pos != string::npos)
		{
			not = true;
			npos = pos;
		}
		entailPos = dataOut.find(":-", 0);
		if (entailPos != string::npos)
		{
			entails = true;
			entailLoc = entailPos;
		}

		check = dataOut.find(",,", 0);
		if (check != string::npos)
		{
			printf("error line %d: missing atom, ',,' found.\n", (queue.queueCount() - temp));
			error = true;
		}
		check = dataOut.find(", ,", 0);
		if (check != string::npos)
		{
			printf("error line %d: missing atom, ', ,' found.\n", (queue.queueCount() - temp));
			error = true;
		}
		tempLen = dataOut.length();
		for(int j = 0; j < tempLen; j++)
		{	
			switch(dataOut[j])
			{
				case '.':
					end = true;
				break;
				case ('K'||'M'):
					mod = true;
					if(end)
					{
						error = true;
						cout<<"K end";
					}
					if(entails)
					{
						if(entailLoc > j)
						{
							error = true;
							cout<<"entailment error";
						}
					}
					if(not)
					{
						if(npos < j)
						{
							error = true;
							cout<<"not error.";
						}
					}
				break;
				case ',':
					and = true;
					if(end)
					{
						cout<<", error";
						error = true;
					}
				break;
				case 'v':
					or = true;
					if(end||mod||and)
					{
						cout<<"v error.";
						error = true;
					}
					else if(entails)
					{
						if(entailLoc < j)
						{
							cout<<"disjunct entailment error.\n";
							error = true;
						}
					}
					else if(not)
					{
						if(npos < j)
						{
							printf("error line %d: negation as failure not allowed in head.\n", (queue.queueCount() - temp));
							error = true;
						}
					}
				break;
			}
		}
		temp--;
	}
	if(error)
	{
		exit(1);
	}
	return queue;
}

//parseAns: takes unformatted queue of answerset values and removes formatting, adds 
// sentinel value ENDSET to signify that a possible model has ended and if more are available the next one
//will start.
Queue<string>& parseAns(Queue<string> &queue)
{
	string dataOut, newString, endSet = "ENDSET ";
	int temp = queue.queueCount(), k = 0;
	while(temp)
	{
		queue.dequeue(dataOut);

		for(int j = 0; j < dataOut.size(); j++)
		{
			if((dataOut[j] == '{'))
			{
				k = j;
				while((dataOut[k] != ',')&&(dataOut[k] != '}'))
				{
					k++;
				}
				newString = dataOut.substr(j+1, k-1);
				queue.enqueue(newString);
			}
			if(dataOut[j] == ',')
			{
				k = j+2;
				while((dataOut[k] != ',')&&(dataOut[k] != '}'))
				{
					k++;
				}
				newString = dataOut.substr(j+2, (k-j)-2);
				queue.enqueue(newString);
			}
			if(dataOut[j] == '}')
			{
				queue.enqueue(endSet);
			}
		}
		temp--;
	}
	return queue;
}

//addBrackets, takes model sets and formats them in brackets, all model sets on one string.
Queue<string>& addBrackets(Queue<string> &queue)
{
	int temp = queue.queueCount();
	string dataOut, newString, dispose;
	if(temp == 0)
	{
		dataOut.replace(0,0, "{{}");
	}
	if(temp > 0)
	{
		queue.dequeue(dataOut);
		dataOut.replace(0, 0, "{{");
	}
	if(temp == 2)
	{
		dataOut.replace(dataOut.size()+1, 0, "}}");
		queue.dequeue(dispose);
		queue.enqueue(dataOut);
		return queue;
	}
	else
	{
		if(temp > 0)
		{
			dataOut.replace(dataOut.size(), 0, ", ");
		}
		newString = dataOut;
	}

	while(temp)
	{
		queue.dequeue(dataOut);
		if(dataOut == "ENDSET ")
		{
			newString.replace(newString.size()-2, 1, "}");
			if(queue.queueCount() > 0)
			{
				newString.replace(newString.size()-1, 1, ", {");
			}
		}
		else
		{
			dataOut.replace(dataOut.size(), 0, ", ");
			newString += dataOut;
		}
		
		temp--;
	}
	newString.replace(newString.size()-1,0,"}");
	queue.enqueue(newString);
	return queue;
}

/*
 showPossibleSet: Takes in the queue of rules, the line locations of its modal operators, the character locations
	of modal operators, and the integer value which determines the truth valuation of each modal operator.
*/
Queue<string>& showPossibleSet(Queue<string> &queue, Queue<int> &rulePos, Queue<int> &charPos, long int binaryEval)
{
	int modTemp = 0, modNoPrint = 0, ruleLoop = 1, tempPrint = 0, loopPrint = 0;
	int modVal = 0, value = 0, modNo = 0, modTestNo = 0, pos = 0, bPos = 0, ePos = 0, temp = 0;
	bool flag = false, ruleFlag = false, modEv = true;
	long int binBuf = 0;
	string dataOut;

	modTemp = uniqueLines(rulePos); //set modtemp as the number of unique modal operator rules

	while(modTemp) //loop while there are new lines to move to
	{
		flag = false;
		rulePos.dequeue(value); //cycle to new line
		rulePos.enqueue(value);

		modNo = modalOpCount(rulePos, value); //determine how many modal operators are on the current line
		modNoPrint = modNo;

		while(modNo > 1)
		{
			rulePos.dequeue(temp);
			if(temp != value)
			{
				rulePos.enqueue(temp);
			}
			modNo--;
		}

		ruleFlag = false;
		//value: tells the line number, determines whether to move to a new line or not
		while(!ruleFlag)
		{
			queue.dequeue(dataOut);
			if(ruleLoop == value)
			{
				binBuf = 0;
				modEv = true;
				tempPrint = modNoPrint;
				loopPrint = modNoPrint;
			
				while(loopPrint)
				{
					if((binaryEval&0x1) == 0)
					{
						modEv = false;
					}
					binBuf = binBuf|binaryEval&0x1;
					binBuf = binBuf<<1;
					binaryEval = binaryEval>>1;
					charPos.dequeue(pos);
					if((tempPrint-loopPrint)== 0)
					{
						bPos = pos;
					}
					ePos = pos;
					loopPrint--;
				}
				binBuf = binBuf>>1;
				if(modEv == true)
				{
					dataOut = removeModOperators(dataOut,bPos, ePos);
					queue.enqueue(dataOut);
				}
			
				ruleFlag = true;
			}
			else
			{
				queue.enqueue(dataOut);
			}
			ruleLoop++;
		}
		modTemp--;
	}
	return queue;
}

/* 
uniqueLines: returns a count of the number of unique lines in an integer queue.
*/
int uniqueLines(Queue<int> &queue)
{
	int modPos = queue.queueCount();
	int value = 0, checkLast = 0, uniq = 0;
	while(modPos) //this loop finds all unique lines containing modal operators
	{
		queue.dequeue(value);
		queue.enqueue(value);
		if(checkLast != value)
		{
			uniq++;
		}
		checkLast = value;
		modPos--;
	}
	return uniq;
}

int modalOpCount(Queue<int> &modalLines, int focus)
{
	Queue<int> copy;
	int count = 0, temp = modalLines.queueCount(), data = 0;
	copy = copyQueue(modalLines, copy);
	while(temp)
	{
		copy.dequeue(data);
		copy.enqueue(data);
		if(data == focus)
		{
			count++;
		}
		temp--;
	}
	return count;
}


/*removeModOperators: removes the modal operators present at the front of the rule,
	assumes rule format [a-z* [v a-z*]*] :- [[~|-]K|M[a-z]*,]*[[not]a-z*].
*/
string removeModOperators(string rule, int beginPos, int endPos)
{
	string temp;
				
	while((rule[endPos] != '.')&&(rule[endPos] != ','))
	{
		endPos++;
	}

	if((rule[beginPos-1] == '~')||(rule[beginPos-1] == '-'))
	{
		if(rule[endPos] == ',')
		{
			temp = rule.replace(beginPos-2, (endPos-(beginPos-3)), "");
		}
		else
		{
			temp = rule.replace(beginPos-2, (endPos-(beginPos-2)), "");
		}
	}
	else
	{
		if(rule[endPos] == ',')
		{
			temp = rule.replace(beginPos-1, (endPos-(beginPos-3)), "");
		}
		else
		{
			temp = rule.replace(beginPos-1, (endPos-(beginPos-2)), "");
		}
	}

	if((temp[temp.size()-2] == '-')&&(temp[temp.size()-3] == ':'))
	{
		temp = temp.substr(0, temp.size()-3);
		temp += '.';
	}
	if((temp[temp.size()-3] == '-')&&(temp[temp.size()-4] == ':'))
	{
		temp = temp.substr(0, temp.size()-4);
		temp += '.';
	}
	if((temp[temp.size()-2] == ' '))
	{
		temp.replace(temp.size()-2, 1, "");
	}
	return temp;
}

// show instantiations: removes modal operators in answer sets by assuming they are
// true or false, on the case they are true we remove the modal operator and its atom
// in the case it is false we move the entire rule from the answer set. once this is 
// done the answer set is sent to dlv for its stable model
void showInstantiations(Queue<string> &queue, Queue<int> &rulePos, Queue<int> &charPos, Queue<string> &copy)
{
	long int binModEval = 0, count = rulePos.queueCount(); 
	double binCount = pow((double)2, rulePos.queueCount());
	int value = 0, pos = 0, printCount = 0, position = 0;
	Queue<string> ansSet, ansCopy;
	Queue<int> intCopy, posCopy;
	bool check = false;
	if((count == 0)||(rulePos.queueCount() > 31))
	{
		return;
	}
	//printQueue(queue);
	while(binCount)
	{
		copy = copyQueue(queue, copy); //make duplicate copy to save original
		ansCopy = copyQueue(queue, ansCopy);
		intCopy = copyQueue(rulePos, intCopy);
		posCopy = copyQueue(charPos, posCopy);
		copy = showPossibleSet(copy, intCopy, posCopy, binModEval); //builds the instantiation of the modal set based on brute force.
		exportRules(copy, "temp");					//exports the instantiation set to a file
		system("dlv -silent temp > temp2");			//executes the set in dlv and returns the value to a text file
		build(ansSet, "temp2");						//builds the answer into a queue
		ansSet = parseAns(ansSet);
		intCopy = copyQueue(rulePos, intCopy);
		posCopy = copyQueue(charPos, posCopy);
		check = checkValidity(ansSet, ansCopy, binModEval, intCopy, posCopy);//checks returned set against original modal set.
		//if(check)
		//{
			ansSet = addBrackets(ansSet);
			printQueue(ansSet, true);	
		//}
		ansSet = emptyQueue(ansSet);
		//cout<<"binModEval: "<<binModEval<<"\n";
		binModEval++;								//increments the brute force binary value
		binCount--;									//one less possibility to check
	}
	return;
}

/*
	extractModAtom: extracts a modal operator and its corresponding atom.
		The position location of the modal operator is in pos.
*/
string extractModAtom(string rule, int pos)
{
	string modOp;
	int count = 0, tempPos = pos, initPos = pos;
	if((rule[tempPos-1] == '-')||(rule[tempPos-1] == '~'))
	{
		initPos = initPos-1;
	}
	while((rule[tempPos+1] != ',')&&(rule[tempPos+1] != '.'))
	{
		tempPos++;
	}
	modOp = rule.substr(initPos, (tempPos-(initPos-1)));
	return modOp;
}


bool checkValidity(Queue<string> &model, Queue<string> &rules, long int binMod, Queue<int> &rulePos, Queue<int> &charPos)
{
	int lines = uniqueLines(rulePos), modNo = 0, modNoPrint = 0, ruleLoop = 1, tempCheck = 0;
	int ansCount = rules.queueCount();
	int functBinMod = binMod, value = 0, pos = 0, temp = 0;
	string dataOut, data;
	long int binModTemp = 0;
	bool truth, ruleFlag = false, eval = true;

	while(lines)
	{
		truth = false;
		rulePos.dequeue(value);
		rulePos.enqueue(value);

		modNo = modalOpCount(rulePos, value); //determine how many modal operators are on the current line
		modNoPrint = modNo;		

		while(modNo > 1)
		{
			rulePos.dequeue(temp);
			if(temp != value)
			{
				rulePos.enqueue(temp);
			}
			modNo--;
		}

		ruleFlag = false;
		//value: tells the line number, determines whether to move to a new line or not
		while(!ruleFlag)
		{
			rules.dequeue(dataOut);
			if(ruleLoop == value)
			{
				tempCheck = modNoPrint;
				while(tempCheck)
				{
					binModTemp = binMod&0x1;
					binMod = binMod>>1;
					charPos.dequeue(pos);
					charPos.enqueue(pos);
					data = extractModAtom(dataOut, pos);
					truth = compareAtoms(model, data, binModTemp);
					if(truth)
					{
						cout<<"data:"<<data<<" valid truth assignment, true worldview\n";
					}
					else
					{
						cout<<"data:"<<data<<" invalid truth assignment, false worldview\n";
						eval = false;
					}
					tempCheck--;
				}
				ruleFlag = true;
			}
			else
			{
				rules.enqueue(dataOut);
			}
			ruleLoop++;
		}
		lines--;
	}
	return eval;
}

/*compareAtoms: *model: the returned disjunctive answer set from dlv
				*data: a modal operator and atom from the set
				*modalOpType: the truth valuation attached to the modal operator 
*/
bool compareAtoms(Queue<string> &model, string data, bool modalOpType)
{
	int count = model.queueCount(), allSetsCount = 0, endsetCount = 0;
	bool knows = false, negated = false; //if knows = true, K, if knows = false, M. 
	bool oneInstance = false, allSets = false;
	string dataOut, endset = "ENDSET";

	if((data[0] == '-')||(data[0] == '~'))
	{
		negated = true;
		if((data[1] == 'K'))
		{
			knows = true;
			data = data.substr(2, (data.size()-2));
		}
		else if(data[1] == 'M')
		{
			data = data.substr(2, (data.size()-2));
		}
		else
		{
			cout<<"error\n";
			exit(1);
		}
	}
	else if(data[0] == 'K')
	{
		knows = true;
		data = data.substr(1, (data.size()-1));
	}
	else if(data[0] == 'M')
	{
		data = data.substr(1, (data.size()-1));
	}
	else
	{
		cout<<"error\n";
		exit(1);
	}

	while(count)
	{
		model.dequeue(dataOut);
		model.enqueue(dataOut);
		dataOut = dataOut.substr(0,(dataOut.size()-1));
		if(dataOut == data)
		{
			allSetsCount++;
			oneInstance = true;
		}	
		if(dataOut == endset)
		{
			endsetCount++;
		}
		count--;
	}
	if(modalOpType)
		cout<<"modal block assumed true , 1\n";
	else
		cout<<"modal block assumed false , 0\n";

	if(knows) //applying logical 
	{
		if(negated)
		{
			if(allSetsCount == endsetCount)
			{
				if(modalOpType)
				{
					return false;
				}
				else
				{
					return true;
				}
			}
			else if((allSetsCount != endsetCount))
			{
				if(modalOpType)
				{
					return true;
				}
				else
				{
					return false;
				}
			}
			else
			{
				if(modalOpType)
				{
					return false;
				}
				else
				{
					return true;
				}
			}
		}
		else
		{
			if(allSetsCount == endsetCount)
			{
				if(modalOpType)
				{
					return true;
				}
				else
				{
					return false;
				}
			}
			else
			{
				if(modalOpType)
				{
					return false;
				}
				else
				{
					return true;
				}
			}
		}
	}
	else
	{
		if(negated)
		{
			if(oneInstance)
			{
				if(modalOpType)
				{
					return false;
				}
				else
				{
					return true;
				}
			}
			else
			{
				if(modalOpType)
				{
					return true;
				}
				else
				{
					return false;
				}
			}
		}
		else
		{
			if(oneInstance)
			{
				if(modalOpType)
				{
					return true;
				}
				else
				{
					return false;
				}
			}
			else
			{
				if(modalOpType)
				{
					return false;
				}
				else
				{
					return true;
				}
			}
		}
	}
}
/*
copyQueue: copies queue located in ADT "queue" to ADT "copy, works for strings"
*/
Queue<string>& copyQueue(Queue<string> &queue, 	Queue<string> &copy)
{
	string dataOut;
	int temp = queue.queueCount();
	int tempb = copy.queueCount();
	while(tempb)
	{
		copy.dequeue(dataOut);
		tempb--;		
	}
	
	while(temp)
	{
		queue.dequeue(dataOut);
		queue.enqueue(dataOut);
		copy.enqueue(dataOut);
		temp--;
	}
	return copy;
}

/*
copyQueue: copies queue located in ADT "queue" to ADT "copy, works for integers"
*/
Queue<int>& copyQueue(Queue<int> &queue, Queue<int> &copy)
{
	int dataOut;
	int temp = queue.queueCount();
	int tempb = copy.queueCount();
	while(tempb)
	{
		copy.dequeue(dataOut);
		tempb--;		
	}
	
	while(temp)
	{
		queue.dequeue(dataOut);
		queue.enqueue(dataOut);
		copy.enqueue(dataOut);
		temp--;
	}
	return copy;
}

/*
exportRules: exports values kept in queue "queue" to the file specified in "filename",
	if the file already exists it will be written over.
*/
void exportRules(Queue<string> &queue, char *filename)
{
	ofstream fp;
	string letter;
	fp.open(filename, ios::out);
	if(!fp)
	{
		printf("\nCannot open %s",filename);
		exit(1);
	}
	while(queue.queueCount() > 0)
	{	
		queue.dequeue(letter);
		fp<<letter<<"\n";
	}
	fp.close();	
	return;
}

/*
emptyQueue: Removes all enqueued values from the queue "queue" and returns the empty queue.
*/
Queue<string>& emptyQueue(Queue<string> &queue)
{
	string temp;
	while(queue.queueCount())
	{
		queue.dequeue(temp);
	}
	return queue;
}