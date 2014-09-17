from collections import *

'''
This is an implementation of a Sybmol Table using a dict. This class inherits
    all methods and properties from dict. This class has been designed to be
    used with a Symbol Table Stack for lexical / syntactical analyzer.

This Class will make extensive use of tuples, allowing for a flexible data
    type that will 
'''

class symbolTable(OrderedDict):

    '''
	Method: __init__()

		Initialize a new instance of symbolTable()
		Inherits OrderedDict from collections
	
	PRECONDITIONS: none

	POSTCONDITIONS: A named OrderedDict will be initialized, default name
			will be '' empty string
    '''
    def __init__(self, name = ''):
        OrderedDict.__init__(self)
        self.name = name

    '''
	Method: addSymbol( tuple ) 

		Add a new symbol to the topmost table in the stack
	
	PRECONDITIONS: A valid table must exist, and must be provided a valid tuple

	POSTCONDITIONS:The symbol is added to the  table
    '''
    def addSymbol(self, dictionary):
    
        if type( dictionary.value ) == dict:
            self[dictionary.value['value']] = dictionary
        else:
            self[dictionary.value] = dictionary
    '''
	Method: findSymbol( string )

		Find the topmost tuple instance with 'string'
	
	PRECONDITIONS: A valid table must exist
	POSTCONDITIONS: Returns a tuple (level, (target, tuple)) if found
			other wise returns -1
    '''           
    def findSymbol(self, lexeme):

        return self.get(lexeme, -1)

    '''
	Method: replace( tuple )

		Replace topmost tuple with provided tuple
	
	PRECONDITIONS: Valid table must exist, tuple must be valid.

	POSTCONDITIONS: Topmost instance of tuple will be removed and replaced
    '''
    def replace(self, dictionary):

        del self[dictionary.value]
        self.addSymbol(dictionary)

    '''
	Method: __str__()

		Formats and returns table as a string
	
	PRECONDITIONS:  A valid table must exist

	POSTCONDITIONS: Returns table as a formatted string
    '''
    def __str__(self):

        outstr = ''
        if self.name == '':
            outstr = 'TABLE: ______ \n'
            
        else:
            outstr = 'TABLE: %s \n' % (self.name)
            
        for dict in self:
            token = self.findSymbol(dict)
            outstr += '  ' + str(token) + '\n'

        return outstr


# if __name__ == "__main__":

    
    # dict1 = {'value':1}
    # dict2 = {'value':2}
    # dict3 = {'value':3}
    
    # table = symbolTable('bob')
    
    # table.addSymbol(dict1)
    # table.addSymbol(dict2)
    # table.addSymbol(dict3)
    # print( table.findSymbol(1))
    # print( table.findSymbol(2))
    # print( table.findSymbol(3))
    # print( table.findSymbol(4))
    # table.replace({'value':1, 'type': 'a test'})
    
    # print()
    # print( table.findSymbol(1))
    
    # print( table )

