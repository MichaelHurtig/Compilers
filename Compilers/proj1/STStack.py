from STable import *
'''
This project is an implementation of a Symbol Table Stack to hand the management
    of a symbol table stack, for use with a lexical / syntactical analyzer. 

This file implements the Symbol Table Stack. The stack is implemented using a
    list, inheriting all class member of list.

This file includes the Symbol Table. The Symbol Table is implemented using a
    dict data class. This class inherits all of dict's members.

This File includes the Symbol Table Entry class, and is implemended using a
    list. This class enforces a limited number of arguments.
'''

class symbolStack(list):
    
    def stackFind(self, lexeme):

        ## Search for the first occurance of a 'lexeme', and returns the index
        ## of the stack location.

        ## PRECONDITION: User must provide a lexeme as a string input

        ## POSTCONDITION: Returns the first top-down occurance of 'lexeme' as
        ##                an int. If no instance is found method will return -1

        ## enumerate
        
        rList = list(reversed(self))
        for index, table in enumerate(rList):
            if table.findSymbol(lexeme):
                return index, table
        return -1
##        for table in range(0,len(rList)):
##            if rList[table].findSymbol(lexeme):
##                return table
##        return -1
            

    def stackNewTable(self, name = ''):

        ## Create a new Symbol Table with a name and push it onto the top of
        ## the stack as a tuple (name, table)

        ## POSTCONDITION: New Symbol table will be added to the top of the stack
        
        new = symbolTable(name)
        self.append(new)

    def stackInstall(self, STE):

        ## Add an existing Symbol Table Entry to the topmost table in the stack.

        ## PRECONDITIONS: Valid STE needs to exist

        ## POSTCONDITIONS: Adds the STE to the topmost table in the stack.

        self[len(self)-1].addSymbol(STE)


    def stackReplace(self, STE):

        self[len(self)-1].replace(STE)
        
    
if __name__ == "__main__":

    symbol = ("a","b","c")

    symbol2 = ("asfd", "asdfasgasfg", "asdfqwaerasfg")
    
    symbol3 = ("a","c","b")

    testTable = symbolTable()
    testTable.addSymbol(symbol)
    testTable.addSymbol(symbol3)

    testTable.addSymbol(symbol2)
    ## testTable.printTable()

    ## print(testTable.hashMethod(symbol2))

    print(testTable.findSymbol("a"))
    print(testTable.findSymbol("T"))

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    stack = symbolStack()
    stack.stackNewTable()
    stack.stackInstall(symbol2)

    print(stack)
    
    stack.stackNewTable()
    print(stack)

    stack.stackInstall(symbol3)
    print(stack)

    stack.stackInstall(symbol)
    print(stack)

    print(stack.stackFind("asfd"))

    print(stack.stackFind("a"))
