#include "stackADT.h"
#include "queue.cpp"

int class baseNString
{
	private:
		Stack<int> intStack;
		int base;
		int length;
	public:
		bool baseNString(int qlength, int qbase);
		void ~baseNString(int qlength, int qbase);
		bool incrementString();
}

inline bool baseNString :: baseNString(int slength, int sbase)
{
	int count = slength;
	length = slength;
	base = qbase;
	if((length <= 0)||(base <= 0))
	{
		return false;
	}
	while(count)
	{
		intStack.pushStack(0);
		count--;
	}
	return true;
}

inline bool baseNString :: incrementString()
{
	bool flag = false, carry = true;
	Queue<int> queue;
	int temp = length, data = 0;

	while(temp)
	{
		intStack.popStack(data);
		queue.enqueue(data);
		temp--;
	}
	temp = length;
	while(temp)
	{
		queue.dequeue(data);
		queue.enqueue(data);
		intStack.pushStack(data);
		queue.enqueue(data);
		temp--;
	}
	temp = length;
	while(temp)
	{
		queue.dequeue(data);
		if(data != base-1)
		{
			flag = true;
		}
		temp--;
	}
	if(flag == false)
	{
		return false;
	}
	temp = length;
	while(temp&&carry)
	{
		intStack.popStack(data);
		data++;
		if(data == base)
		{
			data = 0;
		}
		else
		{
			carry = false;
		}
		temp--;
	}
	while(temp != length)
	{
		intStack.pushStack(data);
		data = 0;
		temp++;
	}
	return true;
}