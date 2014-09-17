from STable import *
'''
This project is an implementation of a Symbol Table Stack to hand the management
    of a symbol table stack, for use with a lexical / syntactical analyser. 

This file implements the Symbol Table Stack. The stack is implemented using a
    list, inheriting all class member of list.

This file includes the Symbol Table. The Symbol Table is implemented using a
    dict data class. This class inherits all of dict's members.

This File includes the Symbol Table Entry class, and is implemented using a
    list. This class enforces a limited number of arguments.
'''

class symbolStack(list):

    '''
	Method: stackFind( string ) 

		Search for the first occurrence of a 'lexeme', and returns the index
		of the stack location.
	
	PRECONDITIONS: User must provide a lexeme as a string input

	POSTCONDITIONS: Returns the first top-down occurrence of 'lexeme' as
			an int. If no instance is found method will return -1
    '''   
    def stackFind(self, lexeme):

        rList = list(reversed(self))
        for index, table in enumerate(rList):
            if table.findSymbol(lexeme) != -1:
                return index, table.findSymbol(lexeme)
        return -1

    '''
	Method: stackNewTable( string )

		Create a new Symbol Table with a name and push it onto the top of
		the stack as a tuple (name, table)
	
	PRECONDITIONS: A valid stack must exist
	POSTCONDITIONS: New Symbol table will be added to the top table of the stack
    '''
    def stackNewTable(self, name = ''):
        
        new = symbolTable(name)
        self.append(new)

    '''
	Method: stackInstall( tuple )
		
		Add an existing Symbol Table Entry to the topmost table in the stack.
	
	PRECONDITIONS: Valid STE needs to exist
	POSTCONDITIONS: Adds the STE to the topmost table in the stack.
    '''
    def stackInstall(self, STE):

        self[len(self)-1].addSymbol(STE)

    '''
	Method: stackReplace( tuple )
		
		A method to replace an existing topmost table entry with another
	
	PRECONDITIONS: A tuple must exist that can be replaced
	POSTCONDITIONS: Topmost target tuple with be replaced with the provided tuple
    '''
    def stackReplace(self, dictionary):

        rList = list(reversed(self))
        for index, table in enumerate(rList):
            if self[index].findSymbol(dictionary['value']) != -1:
                self[index].replace(dictionary)
                
    def topTableName(self):
        return self[len(self)-1].name
        


    '''
	Method: __str__()

		Provided to string method for clear formatting 
	
	PRECONDITIONS: A valid stack must exist
	POSTCONDITIONS: Self will be formatted and returned as a string
    '''
    def __str__(self):

        outstr = ''
        for index in range(0, len(self)):
            rList = list(reversed(self))
            outstr += 'LEVEL: %s \n' % index + str(rList[index]) + '\n'
    
        return outstr
        
        
    
if __name__ == "__main__":
    stack = symbolStack()
    stack.stackNewTable('bob')
    
    dict1 = {'value':1}
    dict2 = {'value':2}
    dict3 = {'value':3}
    dict4 = {'value':1, 'type': 'a test'}
    
    stack.stackInstall(dict1)
    stack.stackInstall(dict2)
    stack.stackInstall(dict3)
    
    print(stack.stackFind(1))
    print(stack.stackFind(3))
    
    stack.stackNewTable('otherbob')
    
    print( stack.topTableName() )
    
    print (stack)
    
    stack.stackReplace(dict4)
    
    print( stack )
    
    stack.stackInstall(dict1)
    
    print( stack )
    
    print(stack.stackFind(1))
    print(stack.stackFind(3))
    
    stack.stackReplace(dict4)
    
    print( stack )