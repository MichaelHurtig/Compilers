# PLY Parser

from STStack import *
from mini_Lexer import *
import sys

'''
	This is a parser class, that takes the output of a lexer and attempts to 
	check langauge rules for PL0. 
'''
class parser():


    def __init__(self, instring, debug_mode = False):
        
        '''
        Method: __init__()

            Initializer to create a new parser with a pre-populated symbolTable
            and lexer.
        
        PRECONDITIONS: 'input.txt' must exist in the same file as the parser.
        POSTCONDITIONS: Parser will do a partial parsing of the input string
                no error checking is handled, as of yet.
        '''
        
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start a SymTab Manager~~~~~~~~~~~~~~~~~
        self.stack = symbolStack()
        self.stack.stackNewTable()
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Globals~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.s_indent = 0
        self.error_count = 0
        self.warning_count = 0
        self.DEBUG = debug_mode
        self.code = []
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start Lexical Analyser~~~~~~~~~~~~~~~~~
        self.lexer = Lexer(instring, self.stack)
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        

    '''
	Method: parse()

		Starts the parser
	
	PRECONDITIONS: A valid parser must have been declared
	POSTCONDITIONS: Starts the parse
    '''
    def parse(self):
    
        token = self.lexer.nextToken()
        while token != None:
            self.stack.stackInstall(token)
            token = self.lexer.nextToken()
            
        print(self.stack) 
       
#  Add one indent
    def indent(self):
        self.s_indent += 1
    
#  Sub one indent
    def dedent(self):
        self.s_indent -= 1

 # Print method that displays current method / error + line and column
    def debug(self, message = ''):
        import inspect
        from sys import stderr
        target = inspect.stack()[1]
        if self.DEBUG == True:
            print('{}{} [ {} ]'.format(self.s_indent*'   ', str(target[3]), message))

    def indent_table(self, table):
        self.indent()
        print(self.s_indent*'   ' + str(table).replace('\n', '\n' + self.s_indent*'   '))
        self.dedent()
        