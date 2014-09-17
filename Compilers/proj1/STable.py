#from STE import *

'''
This is an implementation of a Sybmol Table using a dict. This class inherits
    all methods and properties from dict. This class has been designed to be
    used with a Symbol Table Stack for lexical / syntactical analyzer.

This Class will make extensive use of tuples, allowing for a flexible data
    type that will 
'''

class symbolTable(dict):

    def __init__(self, name = ''):
        self.name = name

    def addSymbol(self, tuple):

        ## Add a Symbol Table Entry to self

        ## PRECONDITIONS: User must provide a valid STE

        ## POSTCONDITIONS: Symbol is added to the table
    
        if tuple not in self:
            self[tuple[0]] = tuple
            
    def findSymbol(self, lexeme):

        ## Search for a STE in self

        ## PRECONDITIONS: A valid Symbol Table

        ## POSTCONDITIONS: Returns True if found, False otherwise
        
        return lexeme in self


    def replace(self, tuple):

        del self[tuple[0]]
        self[tuple[0]] = tuple
        

    def printTable(self):

        ## Test Method intended to print to screen all the elements of self

        for item in self:
            print(self[item].lexeme, self[item].ident, self[item].position)

        print(self.keys())

if __name__ == "__main__":

    testTable = symbolTable()
    testTable.addSymbol(('one','other'))
    print(testTable.findSymbol('one'))
    print(testTable.findSymbol('on'))
    print(testTable.findSymbol('1'))
    testTable.addSymbol(('on',))
    print(testTable.findSymbol('one'))
    print(testTable)
    testTable.replace(('one','thing'))
    print(testTable)
