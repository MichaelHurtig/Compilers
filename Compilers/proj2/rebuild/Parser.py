from STStack import *
from Lexer import *
from fileOpen import *
##from debug import *

'''
	This is a parser class, that takes the output of a lexer and attempts to 
	check langauge rules for PL0. 
'''
class parser():

    '''
	Method: __init__()

		Initializer to create a new parser with a prepopulated symbolTable
		and lexer.
	
	PRECONDITIONS: 'input.txt' must exist in the same file as the parser.
	POSTCONDITIONS: Parser will do a partial parsing of the input string
			no error checking is handled, as of yet.
    '''
    def __init__(self, instring):

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start a SymTab Manager~~~~~~~~~~~~~~~~~
        self.stack = symbolStack()
        self.stack.stackNewTable()
        
        keys = ['BEGIN', 'CALL', 'CONST', 'DO', 'ELSE', 'END', 'IF', 'ODD',
                'PRINT', 'PROCEDURE', 'READ', 'THEN', 'VAR', 'WHILE', 'WRITE',
                'WRITELN']

        for item in keys:
            self.stack.stackInstall((item, item.upper()))
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Get File Input~~~~~~~~~~~~~~~~~~~~~~~~~
        string = instring
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start Lexical Analyzer~~~~~~~~~~~~~~~~~
        self.LA = lexer(self.stack, string)
        self.pos = self.LA.tokenize()
        self.current_token = next(self.pos)
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        

    '''
	Method: match( string )

		A method used to check the current token and advance to the next
	
	PRECONDITIONS: Valid input string and generator provided by a lexer

	POSTCONDITIONS: Checks and advances the current token, or prints bad
			comparison on failure
    '''
    def match(self, st):
        print( "Comparing: " +str(self.current_token[1])+ " to " + st)
        try:
            if self.current_token[1] == st:
                self.stack.stackInstall(self.current_token)
                self.current_token = next(self.pos)

            else:
                print("ERROR :: Expected {0}, Found {1} instead on LINE {2}".format( st, self.current_token[1],self.current_token[2]))
##                self.current_token = next(self.pos)
                
        except StopIteration:
            pass


    '''
	Method: parse()

		Starts the parser
	
	PRECONDITIONS: A valid parser must have been declared
	POSTCONDITIONS: Starts the parse
    '''
    def parse(self):
        self.program()
##        print("A GREAT SUCCESS!")

    '''
	Method: program()

		A method used internally to handle PL0 programs
    '''
    def program(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("PROG~~~~~~~~~~~~~~~~")
        self.block()
        self.match("BLCKEND")
        self.match("FEND")

##        print("ENDPROG~~~~~~~~~~~~~")

    '''
	Method: block()

		an method used internally to handle PL0 blocks
    '''
    def block(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("BLOCK~~~~~~~~~~~~~~~")
        self.stack.stackNewTable()
        self.const_declaration()
        self.var_declaration()
        self.procedure_declaration()
        self.statement()
        print(self.stack)
        self.stack.pop()
##        print("ENDBLOCK~~~~~~~~~~~~")

    '''
	Method: const_declaration

		A method used internally to handle PL0 constant declarations
    '''
    def const_declaration(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("CONST~~~~~~~~~~~~~~~")
        if self.current_token[1] == "CONST":
            self.match("CONST")
            tempToken = self.current_token
##            print(self.current_token)
            self.match("ID")
            #need to look at current to make sure it is '=', otherwise invalid
            self.match("RELOP")
            valueReplace = (tempToken[0], tempToken[1], 'CONST', self.current_token[0])
##            print(valueReplace)
            self.match("NUM")
            self.stack.stackReplace(valueReplace)
            while self.current_token[1] == "COMMA":
                self.match("COMMA")
                self.match("ID")
                #need to look at current to make sure it is '=', otherwise invalid
                self.match("RELOP")
                self.match("NUM")
                self.match("ENDSTMT")
            self.match("ENDSTMT")
##        print("ENDCONST~~~~~~~~~~~~")   

    '''

	Method: var_declaration()

		A method used internally to handle PL0 variable declarations

    '''
    def var_declaration(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("VAR~~~~~~~~~~~~~~~~~")
        if self.current_token[1] == "VAR":
            self.match("VAR")
            self.match("ID")
            while self.current_token[1] == "COMMA":
                self.match("COMMA")
                self.match("ID")
            self.match("ENDSTMT")
##        print("ENDVAR~~~~~~~~~~~~~~")

    '''
	Method: procedure_declaration

		A method used internally to handle PL0 procedure declarations
    '''
    def procedure_declaration(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("PROC~~~~~~~~~~~~~~~~")
        while self.current_token[1] == "PROCEDURE":
            self.match("PROCEDURE")
            self.match("ID")
            self.match("ENDSTMT")
            self.block()
            self.match("ENDSTMT")
##        print("ENDPROC~~~~~~~~~~~~~")

    '''
	Method: statement

		A method used internally to handle PL0 statements
    '''     
    def statement(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("STMT~~~~~~~~~~~~~~")
        if self.current_token[1] == "ID":
            self.match("ID")
            self.match("ASN")
            self.expression()
            
        elif self.current_token[1] == "CALL":
            self.match("CALL")
            self.match("ID")
            
        elif self.current_token[1] == "BEGIN":
            self.match("BEGIN")
            self.statement()
            while self.current_token[1] == "ENDSTMT":
                self.match("ENDSTMT")
                self.statement()
            self.match("END")

        elif self.current_token[1] == "IF":
            self.match("IF")
            self.condition()
            self.match("THEN")
            self.statement()
            if self.current_token[1] == "ELSE":
                self.match("ELSE")
                self.statement()
            
        elif self.current_token[1] == "WHILE":
            self.match("WHILE")
            self.condition()
            self.match("DO")
            self.statement()
            
        elif self.current_token[1] == "READ":
            self.match("READ")
            self.match("LPAREND")
            self.match("ID")
            self.match("RPAREND")
            
        elif self.current_token[1] == "WRITE":
            self.match("WRITE")
            self.match("LPAREND")
            self.expression()
            self.match("RPAREND")
            
        elif self.current_token[1] == "WRTLN":
            self.match("WRTLN")
            self.match("LPAREND")
            self.expression()
            self.match("RPAREND")
##        print("ENDSTMT~~~~~~~~~~~")

    '''
	Method: condition()

		A method used internally to handle PL0 conditions
    '''       
    def condition(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("COND~~~~~~~~~~~~~~")
        if self.current_token[1] == "ODD":
            self.match("ODD")
            self.expression()
        else:
            self.expression()
            self.match("RELOP")
            self.expression()
##        print("ENDCOND~~~~~~~~~~~")

    '''
	Method: expression

		A method used internally to handle PL0 expressions
    '''    
    def expression(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("EXPR~~~~~~~~~~~~~~")
        if self.current_token[1] == "ADDOP":
            self.match("ADDOP")
        self.term()
        while self.current_token[1] == "ADDOP":
            self.match("ADDOP")
            self.term()
##        print("ENDEXPR~~~~~~~~~~~")

    '''
	Method: term()

		A method used internally to handle PL0 terms
    '''
    def term(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("TERM~~~~~~~~~~~~~~")
        self.factor()
        while self.current_token[1] == "MULOP":
            self.match("MULOP")
            self.factor()
##        print("ENDTERM~~~~~~~~~~~")

    '''
	Method: factor()

		A method used internally to handle PL0 factors
    '''
    def factor(self):
        debug('line: ' + str(self.current_token[2]),self)
##        print("FACT~~~~~~~~~~~~~~")
        if self.current_token[1] == "ID":
            self.match("ID")
        elif self.current_token[1] == "NUM":
            self.match("NUM")
        else:
            self.match("LPAREND")
            self.expression()
            self.match("RPAREND")
##        print("ENDFACT~~~~~~~~~~~")



    
