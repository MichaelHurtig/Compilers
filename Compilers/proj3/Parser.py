from STStack import *
from PLY_Lexer import *
from Lexer import *
from fileOpen import *
from debug import *
import sys

'''
	This is a parser class, that takes the output of a lexer and attempts to 
	check langauge rules for PL0. 
'''
class parser():

    '''
	Method: __init__()

		Initializer to create a new parser with a pre-populated symbolTable
		and lexer.
	
	PRECONDITIONS: 'input.txt' must exist in the same file as the parser.
	POSTCONDITIONS: Parser will do a partial parsing of the input string
			no error checking is handled, as of yet.
    '''
    def __init__(self, instring, debug_mode = False):

        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start a SymTab Manager~~~~~~~~~~~~~~~~~
        self.stack = symbolStack()
        self.stack.stackNewTable()
        
        # keys = ['BEGIN', 'CALL', 'CONST', 'DO', 'ELSE', 'END', 'IF', 'ODD',
                # 'PRINT', 'PROCEDURE', 'READ', 'THEN', 'VAR', 'WHILE', 'WRITE',
                # 'WRITELN']

        # for item in keys:
            # self.stack.stackInstall((item, item.upper()))
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Globals~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.s_indent = 0
        self.error_count = 0
        self.warning_count = 0
        self.DEBUG = debug_mode
        self.factorflag = False
        self.code = []
        self.linecount = 0
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start Lexical Analyser~~~~~~~~~~~~~~~~~
        self.LA = Tokenizer( instring, self.stack )
        # self.pos = self.LA.tokenize()
        self.current_token = self.LA.t_next()
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        

    '''
	Method: match( string )

		A method used to check the current token and advance to the next
	
	PRECONDITIONS: Valid input string and generator provided by a lexer

	POSTCONDITIONS: Checks and advances the current token, or prints bad
			comparison on failure
    '''
    def match( self, target):
        try: 
            self.indent()
            if (self.current_token['value'] == target):
                if self.current_token['type'] == "ID":
                    self.debug('{:<10} {}'.format(str(target)+ " -> ", str(self.current_token) ))
                    # {:<7} 
                                                          # ' L: ' + str(self.current_token[2].get('line')) + \
                                                          # ' C: ' + str(self.current_token[2].get('column'))))
                else:
                    self.debug('{:<10} {}'.format(str(target)+ " -> ", str(self.current_token['value']) ))
                self.current_token = self.LA.t_next()
            else:
                sys.stderr.write("MISMATCH: Found ({}), Expected ({}) on Line ({})\n"\
                                         .format(self.current_token['value'], \
                                         target,\
                                        self.current_token['line']))
                self.current_token = self.LA.t_next()
                self.error_count += 1
                
            self.dedent()
        except StopIteration:
            pass
            
        # except:
            # print('Unexpected Exception: ',sys.exc_info()[0], self.current_token)
            # exit()
    '''
	Method: parse()

		Starts the parser
	
	PRECONDITIONS: A valid parser must have been declared
	POSTCONDITIONS: Starts the parse
    '''
    def parse(self):
        self.program()
        for i in self.code:
            print(i)



    # '''
	# Method: program()

		# A method used internally to handle PL0 programs
    # '''
    def program(self):
        
        self.debug(str('line: ' + str(self.current_token['line'])))
        self.code.append(str(self.linecount) + '\tJMP\t' + '0\t1\t# Main program JMP\n')
        self.linecount += 1
        # self.block('__main')
        self.match("BLCKEND")
        # self.code.append(str(self.linecount) + '\tOPR\t' + '0\t0\t# Exit Main\n')
        self.match("FEND")



    # '''
	# Method: block()

		# an method used internally to handle PL0 blocks
    # '''
    # def block(self, name = ''):
        # self.indent()
        # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
        
        # offset = 3
        
        # self.stack.stackNewTable(name)
        # self.const_declaration()
        # offset += self.var_declaration(offset)
        # self.procedure_declaration(offset)
        # self.statement()
        # if self.DEBUG:
            # self.indent_table(self.stack)
        # self.stack.pop()
        # self.dedent()

    # '''
    # if the current token is a const, return true, else return false
    # '''
    # def isConst(self):
        # return self.current_token[1] == "CONST"
    # '''
	# Method: const_declaration

		# A method used internally to handle PL0 constant declarations
        
        # A pl0 CONST may be used from the current or any parent scope
        # A pl0 CONST may only be defined once per scope
        # A pl0 CONST may not be modified
    # '''
    # def const_declaration(self):
        # self.indent()
        # tempID = ''
        # tempNUM = ''
        # flag = False
        # if the current token is a keyword CONST
        # if self.isConst() == True:
            # print debug statement 
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # match const and move on
            # self.match("CONST")
            # search for the current token and save the search
            # tempToken = self.stack.stackFind(self.current_token[0])
            ## test the current table name, if it is the same, issue warning
            # if self.current_token[0] == self.stack.topTableName():
                # print("WARNING: CONST{} declared in PROCEDURE {}"\
                # .format(self.current_token[0],self.stack.topTableName())) 
                # self.warning_count += 1
            # redefinition of an existing local constant
            # if ( tempToken != -1 and tempToken[0] == 0):
                # print( "ERROR: Redefinition of {}".format(tempToken[1]))
                # self.error_count += 1
                # self.current_token = next(self.pos)
                # flag = True
            # get the ID Value and store it
            # if self.current_token[1] == 'ID':
                # tempID = self.current_token[0]
                # self.match("ID")
            # Check the relop
            # if (self.current_token[0] != "=" ): ## try to use := as a warning case, need to do something with token
                # print("WARNING: Incorrect relational operator: '{}'".format(self.current_token[0]))
                # self.warning_count += 1
            # self.match("RELOP")
            # Get the value
            # if self.current_token[1] == "NUM":
                # tempNUM = self.current_token[0]
                # self.match("NUM")
            # make a new token and put it in the table
            # if flag == False:
                # self.stack.stackInstall((tempID, tempNUM, {'type': 'CONST'}))
                # self.code.append(str(self.linecount) + '\tLIT\t' + '0\t' + str(tempNUM)+ '\t# Push literal number ' + str(tempNUM) + '\n')
                # self.linecount += 1
                # self.code.append(str(self.linecount) + '\tSTO\t' + '0\t' + str(tempNUM) + '\t# Store in const ' + tempID + '\n')
                # self.linecount += 1
            # if (self.current_token[1] != "COMMA" and self.current_token[1] != "ENDSTMT"):
                # self.panicMode([',', ';'])
            # while self.current_token[1] == "COMMA":
                # self.match("COMMA")
                # get the ID Value and store it
                # tempToken = self.stack.stackFind(self.current_token[0])
                ##test to make sure declaration is not obscuring top table
                # if self.current_token[0] == self.stack.topTableName():
                    # print("WARNING: CONST{} declared in PROCEDURE {}"\
                    # .format(self.current_token[0],self.stack.topTableName())) 
                    # self.warning_count += 1
                # if (  tempToken != -1 and tempToken[0] == 0):
                    # self.error_count += 1
                    # print( "ERROR: Redefinition of {}".format(tempToken[1]))
                # if self.current_token[1] == 'ID':
                    # tempID = self.current_token[0]
                    # self.match("ID")
                # Check the relop for '='
                # if self. current_token[0] != "=" :
                    # print("WARNING: Incorrect relational operator: '{}'".format(self.current_token[0]))
                    # self.warning_count += 1
                # self.match("RELOP")
                # Get the value
                # if self.current_token[1] == "NUM":
                    # tempNUM = self.current_token[0]
                    # self.match("NUM")
                # make a new token and put it in the table
                # self.stack.stackInstall((tempID, tempNUM, {'type': 'CONST'}))
                # self.code.append(str(self.linecount) + '\tLIT\t' + '0\t' + str(tempNUM)+ '\t# Push literal number ' + str(tempNUM) + '\n')
                # self.linecount += 1
                # self.code.append(str(self.linecount) + '\tSTO\t' + '0\t' + str(tempNUM) + '\t# Store in const ' + tempID + '\n')
                # self.linecount += 1
                # if (self.current_token[1] != "COMMA" and self.current_token[1] != "ENDSTMT"):
                    # self.panicMode([',', ';'])                

            # self.match("ENDSTMT")

        # self.dedent()

        
    # def isVar(self):
        # return self.current_token[1] == "VAR"
    # '''

	# Method: var_declaration()

		# A method used internally to handle PL0 variable declarations

    # '''
    # def var_declaration(self, offset):
        # v_offset = offset
        # self.indent()
        # tempID = ''
        # tempNUM = ''
        
        # if self.isVar() == True:
            ##print debug statement
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            ##match VAR
            # self.match("VAR")
            ##if self.current_token[1] == 'ID':
                ##tempID = self.current_token[0]
            # if it already exists in current scope, ERROR
            # tempToken = self.stack.stackFind(self.current_token[0])
            ##if same came as current table, throw warning
            # if self.current_token[0] == self.stack.topTableName():
                # print("WARNING: {} declared in PROCEDURE {}"\
                # .format(self.current_token[0],self.stack.topTableName())) 
                # self.warning_count += 1
            ##if found in the current table, throw redeclaration error
            # if ( tempToken != -1 and tempToken[0] == 0):
                # print( "ERROR: Redefinition of {}".format(tempToken[1]))
            ##insert a token and increase the offset
            # self.token_ins((self.current_token[0], 'ID', {'type': 'VAR', 'offset': v_offset}))
            # v_offset += 1   
            # self.match("ID")
            # if (self.current_token[1] != "COMMA" and self.current_token[1] != "ENDSTMT"):
                # self.panicMode([',', ';']) 
            # while self.current_token[1] == "COMMA":
                # self.match("COMMA")
                # tempToken = self.stack.stackFind(self.current_token[0])
                ##if same came as current table, throw warning
                # if self.current_token[0] == self.stack.topTableName():
                    # print("WARNING:{} declared in PROCEDURE {}"\
                    # .format(self.current_token[0],self.stack.topTableName())) 
                    # self.warning_count += 1
                ##if found in the current table, throw redeclaration error
                # if ( tempToken != -1 and tempToken[0] == 0):
                    # print( "ERROR: Redefinition of {}".format(tempToken[1]))
                ##insert a token and increase the offset
                # self.token_ins((self.current_token[0], 'ID', {'type': 'VAR', 'offset': v_offset}))
                # v_offset += 1   
                # self.match("ID")
                # if (self.current_token[1] != "COMMA" and self.current_token[1] != "ENDSTMT"):
                    # self.panicMode([',', ';'])
            # self.match("ENDSTMT")
        # return v_offset
        # self.dedent()

        
    # def isProc(self):
        # return self.current_token[1] == "PROCEDURE"
    # '''
	# Method: procedure_declaration

		# A method used internally to handle PL0 procedure declarations
    # '''
    # def procedure_declaration(self, offset):
        ##p_offset = offset
        # self.indent()
        # tempID = ''
        # tempName = ''
        # while self.isProc() == True:
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # self.match("PROCEDURE")
            # tempToken = self.stack.stackFind(self.current_token[0])
            ##temps for inserting
            # tempID = self.current_token[1]
            # tempName = self.current_token[0]
            ##If ID exists, redefinition error
            # if tempToken != -1:
                # print("ERROR: Redefinition of {}".format(tempToken[1]))
                # self.error_count += 1
                
            ##If ID value == top table name, throw a warning
            # if self.current_token[0] == self.stack.topTableName():
                # print("WARNING: PROCEDURE {} declared in PROCEDURE {}"\
                # .format(self.current_token[0],self.stack.topTableName())) 
                # self.warning_count += 1
                
            ##Else add PROC ID to table
            # else:
                # self.token_ins((tempName, tempID, {'type':'PROCEDURE', 'addr': 0}))
                
            # self.match("ID")
            ##p_offset += 1
            # self.match("ENDSTMT")
            # self.block(tempName)
            # self.match("ENDSTMT")
        ##return p_offset
        # self.dedent()

    # '''
	# Method: statement

		# A method used internally to handle PL0 statements
    # '''

#===============================================================
            
#===============================================================
    # def statement(self):
        # self.indent()
        # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
        
        ##TEST for declarations: if found throw error, don't belong here
        ##if self.current_token[1] == 'CONST':
            ##print("ERROR: Can't be CONST")
            ##self.error_count += 1
        ##elif self.current_token[1] == 'VAR':
            ##print("ERROR: Can't be VAR")
        ##else:
            ##pass
        ##print("I")
        # self.s_ID()
        ##print("II")
        # self.s_CALL()
        ##print("III")
        # self.s_BEGIN()
        ##print("IV")
        # self.s_IF()
        ##print("IV")
        # self.s_WHILE()
        ##print("V")
        # self.s_READ()
        ##print("VI")
        # self.s_WRITE()
        ##print("VII")
        # self.s_WRTLN()
        ##print("VIII")
        
        # self.factorflag = False
        # self.dedent()
    # '''
	# Method: condition()

		# A method used internally to handle PL0 conditions
    # '''       
    # def condition(self):
        # self.indent()
        # self.debug(str('line: ' + str(self.current_token[2].get('line'))))

        
        # if self.current_token[1] == "ODD":
            # self.match("ODD")
            # self.expression()
        # else:
            # self.expression()
            # self.code.append(str(self.linecount) + '\tJMP\t0\t' + str(self.linecount + 1) + \
                  # '\t# Cal & Andy\'s NO-OP instruction :-)\n')
            # self.linecount += 1
            # if self.current_token[1] == '=':
                # self.code.append(str(self.linecount) + '\tOPR\t0\t8\t# =\n')
            # if self.current_token[1] == '!=':
                # self.code.append(str(self.linecount) + '\tOPR\t0\t9\t# !=\n')
            # if self.current_token[1] == '<':
                # self.code.append(str(self.linecount) + '\tOPR\t0\t10\t# <\n')
            # if self.current_token[1] == '<=':
                # self.code.append(str(self.linecount) + '\tOPR\t0\t13\t# <=\n')
            # if self.current_token[1] == '>':
                # self.code.append(str(self.linecount) + '\tOPR\t0\t12\t# >\n')
            # if self.current_token[1] == '>=':
                # self.code.append(str(self.linecount) + '\tOPR\t0\t11\t# >=\n')
            # self.linecount += 1
# lincount
            # self.match("RELOP")
            # self.expression()
        # self.dedent()


    # '''
	# Method: expression

		# A method used internally to handle PL0 expressions
    # '''    
    # def expression(self):
        # self.indent()
        # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
        # if self.current_token[1] == "ADDOP":
            # temp = self.current_token[0]
            # self.match("ADDOP")
            # self.term()
            # if temp == '-':
                # pass
        # else:
            # self.term()
            
        # while self.current_token[1] == "ADDOP":
            # temp = self.current_token[0]
            # self.match("ADDOP")
            # code generatation
            # linecount
            # self.term()
            # if temp == '+':
                # pass
            # else:
                # pass
            #linecount
        # self.dedent()


    # '''
	# Method: term()

		# A method used internally to handle PL0 terms
    # '''
    # def term(self):
        # self.indent()
        # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
        ##keep value for code generation
        # temp = self.current_token[0]
        # self.factor()
        # while (self.current_token[1] == "MULOP" and self.factorflag == True):
            # self.match("MULOP")
            # code generation
            # lincount
            # self.factor()
            # if temp == '*':
                # pass
            # if temp == '/':
                # pass
            # lincount
        # self.dedent()
        
        # if self.factorflag == False:
            # print("ERROR: MULOP")


    # '''
	# Method: factor()

		# A method used internally to handle PL0 factors
    # '''
    # def factor(self):
        # self.indent()
        # tempToken = self.stack.stackFind(self.current_token[0])

        # if (self.current_token[1] == "ID" and tempToken != -1):
            # self.factorflag = True
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # code generatation
            #linecount
            # self.match("ID")

        # if the ID does not exist, should move on
        # if tempToken == -1:
            # print("ERROR: {} does not exist".format(self.current_token[0]))
            # self.current_token = next(self.pos)
            # return
            
        # if self.current_token[1] == "NUM":
            # self.factorflag = True
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # code generatation
            # linecount
            # self.match("NUM")

            
        # if self.current_token[1] == "LPAREND":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))

            # self.match("LPAREND")
            # self.expression()
            # self.match("RPAREND")

            
        # self.dedent()

    # def s_ID(self):
        # self.indent()
        
        # if self.current_token[1] == "ID":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # if self.stack.stackFind(self.current_token[0]) == -1:
                # print('ERROR: ' + str(self.current_token[0]) + ' not found')
            # tempToken = self.stack.stackFind(self.current_token[0])
            ##if token is in table, and token is CONST or VAR, throw error
            # if ( tempToken != -1 and tempToken[1][2]['type'] != "VAR" ):
                # print("ERROR: {} must be a VAR".format(tempToken))
                # self.error_count += 1
            # self.match("ID")
            ##If we get = instead of :=, throw warning, move on
            # if self.current_token[0] == '=':
                # print("WARNING: got '=' instead of ':='")
                # self.warning_count += 1
                # self.current_token = next(self.pos)
            ##otherwise carry out match
            # else:
                # self.match("ASN")
            # self.expression()
        # self.dedent()

    # def s_CALL(self):
        # self.indent()
        
        # if self.current_token[1] == "CALL":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # self.match("CALL")
            # tempToken = self.stack.stackFind(self.current_token[0])
            # if (tempToken != -1 and tempToken[1][2]['type'] != "PROCEDURE"):
                # print("ERROR: {} must be a PROCEDURE".format(self.current_token))
                # self.error_count += 1
                
            ##check to see if ID exists
            # if tempToken == -1:
                # print("ERROR: PROCEDURE {} must exist".format(self.current_token[0]))
                # self.error_count += 1
            # self.match("ID")


            
        # self.dedent()

    # def s_BEGIN(self):
        # self.indent()
        # if self.current_token[1] == "BEGIN":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))

            # self.match("BEGIN")
            # self.statement()
            # while self.current_token[1] == "ENDSTMT":
                # self.match("ENDSTMT")
                # self.statement()
            # self.match("END")

        # self.dedent()

    # def s_IF(self):
        # self.indent()
        
        # if self.current_token[1] == "IF":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))

            # self.match("IF")
            # self.condition()
            # self.match("THEN")
            # self.statement()

            
            # if self.current_token[1] == "ELSE":
                # self.debug(str('line: ' + str(self.current_token[2].get('line'))))

                # self.match("ELSE")
                # self.statement()

                
        # self.dedent()

    # def s_WHILE(self):
        # self.indent()
        # if self.current_token[1] == "WHILE":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))

            # self.match("WHILE")
            # self.condition()
            # self.match("DO")
            # self.statement()

        # self.dedent()

    # def s_READ(self):

        # self.indent()
        # if self.current_token[1] == "READ":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # self.match("READ")
            # self.match("LPAREND")
            # tempToken = self.stack.stackFind(self.current_token[0])
            # if self.current_token[1] == "ID":
                # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
                # if self.stack.stackFind(self.current_token[0]) == -1:
                    # print('ERROR: ' + str(self.current_token[0]) + ' not found')
                # tempToken = self.stack.stackFind(self.current_token[0])
                ##if token is in table, and token is CONST or VAR, throw error
                # if ( tempToken != -1 and tempToken[1][2]['type'] != "VAR" ):
                    # print("ERROR: {} must be a VAR".format(tempToken))
                    # self.error_count += 1 
            # self.match("ID")
            # self.match("RPAREND")


        # self.dedent()

    # def s_WRITE(self):
        # self.indent()
        # if self.current_token[1] == "WRITE":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # self.match("WRITE")
            # self.match("LPAREND")
            # self.expression()
            # self.match("RPAREND")
        # self.dedent()

    # def s_WRTLN(self):

        # self.indent()
        # if self.current_token[1] == "WRTLN":
            # self.debug(str('line: ' + str(self.current_token[2].get('line'))))
            # self.match("WRITELN")
            # self.match("LPAREND")
            # self.expression()
            # self.match("RPAREND")  
        # self.dedent()
    
       
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
        
    # def token_ins(self, item):
        # if self.stack.stackFind(item[0]) == -1:
            # self.stack.stackInstall(item)
        # elif (self.stack.stackFind(item[0]))[0] != 0:
            # self.stack.stackInstall(item)
        # else:
            # print("ERROR: Redefinition of {}".format(self.stack.stackFind(item[0])))
            # self.error_count += 1
            
    # def token_exists(self, token):
        # if self.stack.stackFind(token) == -1:
            # return False    
        # elif (self.stack.stackFind(token))[0] == 0:
            # return True

    # def panicMode(self, target):
        # try:
            # while (self.current_token[0] not in target and self.current_token[1] != "FEND"):
                # self.current_token = next(self.pos)
            # print("Panic Mode") ## make a better statement
            # print("{} found, continuing:".format(self.current_token[1]))
            # if self.current_token[1] == "FEND":
                # print("End of Program: Terminating")
                # sys.exit()
        # except StopIteration:
            # pass
            
if __name__ == "__main__":

    string = '''

.'''
    parser = parser(string)
    parser.parse()
    
