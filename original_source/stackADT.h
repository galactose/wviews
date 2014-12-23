/* file : stackADT.h */
/* Stack ADT Type Defintions */
// Node Declaration

//template <class TYPE>
//struct NODE
//{
//	TYPE data;
//	NODE<TYPE> *next;
//};

// Class Declaration
template <class TYPE>
class Stack
{
	private:
		NODE<TYPE> *front;
		int count;
		NODE<TYPE> *rear;
	public:
		Stack (void);
		~Stack (void);
		bool popStack (TYPE& dataOut);
		bool pushStack (TYPE dataIn);
		bool queueFront (TYPE& dataOut);
		bool stackTop (TYPE& dataOut);
		int stackCount (void);
		bool emptyStack (void);
		bool fullQueue (void);
}; // class Queue


/* ================== Constructor =================
Instantiates a queue and initializes private data.
Pre queue being defined
Post queue created and initialized
*/
template <class TYPE>
Stack<TYPE> :: Stack (void)
{
	// Statements
	front = NULL;
	rear = NULL;
	count = 0;
} // Constructor


/* ================== enqueue =================
This algorithm inserts data into a queue.
Pre dataIn contains data to be enqueued
Post data have been inserted
Return true if successful, false if overflow
*/
template <class TYPE>
bool Stack<TYPE> :: pushStack (TYPE dataIn)
{
	// Local Definitions
	NODE<TYPE> *newPtr;
	// Statements
	if (!(newPtr = new NODE<TYPE>))
	return false;
	newPtr->data = dataIn;
	newPtr->next = rear;
	rear = newPtr;
	count ++;

	return true;
} //enqueue


/* ================= dequeue ==================
This algorithm deletes a node from the queue.
Pre dataOut variable to receive data
Post front data placed in dataOut and front deleted
Return true if successful, false if underflow
*/
template<class TYPE>
bool Stack<TYPE> :: popStack (TYPE& dataOut)
{
	// Local Definitions
	NODE<TYPE> *deleteLoc;
	// Statements
	if (count == 0)
	return false;
	dataOut = rear->data;
	deleteLoc = rear;
	
	rear = rear->next;
	count--;
	delete deleteLoc;
	return true;
} // dequeue


/*
 ================== queueFront ==================
Retrieves data at the front of the queue
without changing the queue contents.
Pre dataOut is variable for data
Post data in dataOut
Return true if successful, false if underflow*/

template <class TYPE>
bool Stack<TYPE> :: queueFront (TYPE& dataOut)
{
	// Statements
	if (count == 0)
		return false;
	else
	{
		dataOut = front->data;
		return true;
	} //else
} // queueFront


/* =============== stackTop ==============
Retrieves data at the rear of the queue
without changing the queue contents.
Pre dataOut is variable to receive data
Post dataOut contains data at rear of queue
Return true if successful, false if underflow
*/
template <class TYPE>
bool Stack<TYPE> :: stackTop (TYPE& dataOut)
{
	// Statements
	if (count == 0)
		return false;
	else
	{
		dataOut = rear->data;
		return true;
	} // else
} // queueRear


/* =================== emptyStack ==================
This algorithm checks to see if a queue is empty.
Pre nothing
Return true if empty, false if queue has data
*/
template <class TYPE>
bool Stack<TYPE> :: emptyStack (void)
{
	// Statements
	return (count == 0);
} // emptyQueue


/* =================== fullQueue ===================
This algorithm checks to see if a queue is full.
The queue is full if memory cannot be allocated
for another node.
Pre nothing
Return true if full, false if room for a node*/

template <class TYPE>
bool Stack<TYPE> :: fullQueue (void)
{
	// Local Definitions
	NODE<TYPE> *temp;
	// Statements
	temp = new NODE<TYPE>;
	if (temp != NULL)
	{
		delete temp;
		return false;
	} // if
	// Heap full
	return true;
} // fullQueue



/* =============== stackCount ==============
Returns the number of elements in the queue.
Pre nothing
Return queue count
*/
template <class TYPE>
int Stack<TYPE> :: stackCount(void)
{
	// Statements
	return count;
} // queueCount

/* =================== Destructor ==================
Deletes all data from a queue and recycles
its memory.
Pre queue is being destroyed
Post all data have been deleted and recycled
*/
template <class TYPE>
Stack<TYPE> :: ~Stack (void)
{
	// Local Definitions
	NODE<TYPE> *deletePtr;
	// Statements
	while (front != NULL)
	{
		deletePtr = front;
		front = front->next;
		delete deletePtr;
	} // while
} // Destructor