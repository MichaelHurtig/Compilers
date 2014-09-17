
'''
A class that implements a Symbol Table Entry, for use in a lexical / syntactical
    analyzer.
'''

class STE(list):

    def __init__(self, lexeme, ident, position):

        ## INITIALIZER: This defines and creates the STE from list.

        ## PRECONDITIONS: String inputs for 'lexeme', 'ident', and 'position'

        ## POSTCONDITION: Creates a new instance of STE
        
        self.lexeme = lexeme
        self.ident = ident
        self.position = position

    def printSTE(self):

        ## Test Method that prints the contents of of an STE

        ## POSTCONDITIONS: Print to screen STE
        print(self.lexeme, self.ident, self.position)
