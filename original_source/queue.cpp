//#include <iostream.h>

//node declaration
template <class TYPE>
struct NODE
{
       TYPE data;
       NODE<TYPE> *next;
};

//class declaration
template <class TYPE>
class Queue
{
      private:
              NODE<TYPE> *front;
              int        count;
              NODE<TYPE> *rear;
      
      public:
             Queue (void);
             ~Queue (void);
             bool dequeue (TYPE& dataOut);
             bool enqueue (TYPE dataIn);
             bool queueFront (TYPE& dataOut);
             bool queueRear (TYPE& dataOut);
             int queueCount (void);
             bool emptyQueue (void);
             bool fullQueue (void);          
};//class queue

template <class TYPE>
inline Queue<TYPE> :: Queue (void)
{
            //statements
            front = NULL;
            rear = NULL;
            count = 0;
}

template <class TYPE>
inline bool Queue<TYPE>::enqueue (TYPE dataIn)
{
     NODE<TYPE> *newPtr;
     if(!(newPtr = new NODE<TYPE>))
                 return false;
                 
     newPtr->data = dataIn;
     newPtr->next = NULL;
     
     if(count == 0)
              front = newPtr;
     else
              rear->next = newPtr;
              
     count++;
     rear = newPtr;
     return true;
}//enqueue

template <class TYPE> 
inline bool Queue<TYPE>::dequeue (TYPE& dataOut)
{
     NODE<TYPE> *deleteLoc;
     if(count == 0)
              return false;
     
     dataOut = front->data;
     deleteLoc = front;
     if(count == 1)
              //delete the only item in queue
              rear = front = NULL;
     else
              front = front->next;
     count--;
     delete deleteLoc;
     return true;
}//dequeue

template <class TYPE>
inline bool Queue<TYPE>::queueFront (TYPE& dataOut)
{
     if(count == 0)
              return false;
     else
     {
         dataOut = front->data;
         return true;
     }//else
}//queue front

template <class TYPE>
inline bool Queue<TYPE>::queueRear (TYPE& dataOut)
{
     if(count == 0)
              return false;
     else
     {
         dataOut = rear->data;
         return true;
     }//else
}//queue rear

template <class TYPE>
inline bool Queue<TYPE>::emptyQueue (void)
{
     return (count == 0);
}

template <class TYPE>
inline bool Queue<TYPE>::fullQueue (void)
{
     NODE<TYPE> *temp;
     temp = new NODE<TYPE>;
     if (temp != NULL)
     {
              delete temp;
              return false;
     }     //if
     //Heap full
     return true;
} //full queue

template <class TYPE>
inline int Queue<TYPE>::queueCount (void)
{
    return count;
}//queueCount

template <class TYPE>
inline Queue<TYPE>::~Queue (void)
{
     NODE<TYPE> *deletePtr;
     
     while(front != NULL)
     {
                 deletePtr = front;
                 front = front->next;
                 delete deletePtr;
     }//while       
} //destructor
