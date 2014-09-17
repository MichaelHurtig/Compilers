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
    def addSymbol(self, tuple):
    
        if tuple not in self:
            self[tuple[0]] = tuple

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
    def replace(self, tuple):

        #print("HELPER: %s" % str(tuple[0]) + str(self[tuple[0]]))
        del self[tuple[0]]
        self[tuple[0]] = tuple
        #print("HELPER: %s" % str(tuple[0]) + str(self[tuple[0]]))
        

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
        for item in self.items():
            outstr += '  ' +  'KEY: ' + '{:<8}'.format (str(item[0])) \
                      + "||  " + "STE:" + str(item[1]) + '\n' 

        return outstr


if __name__ == "__main__":

    testTable = symbolTable('test')
    testTable.addSymbol(('one','other'))
    print("Finding 'one'")
    print(testTable.findSymbol('one'))
    print("Finding 'on' (not in table)")
    print(testTable.findSymbol('on'))
    print("Finding '1' (not in table)")
    print(testTable.findSymbol('1'))
    testTable.addSymbol(('on',))
    print("Finding 'on' after insert)")
    print(testTable.findSymbol('one'))
    print('--------01---------------')
    print(testTable)
    print('--------02---------------')
    print("testing replace on 'one'")
    testTable.replace(('one','thing'))
    print('--------03---------------')
    print(testTable)

