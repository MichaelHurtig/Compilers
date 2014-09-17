'''
Author - Cory Hagen
Date - Sept/28/13
Class - Compilers
'''

from lex import *
from symbol import *
import sys

class Parser():
     
   def __init__(self, sourceCode, bug, theFile):
      self.STM = symbolTableManager()
      self.LA = lexicalAnalyzer(self.STM,sourceCode)
      self.debug = int(bug)
      self.theProgram = theFile
      
      self.bpFlag = False
      #self.code = ''
      self.offset = 0
            
      self.statementFlag = False
      self.factorFlag = False
      
      self.linecount = 0
      self.code = []
      
      self.warnings = 0
      self.errors = 0
      
      self.myIndent = ''
      
      #preloading the symbol table
      self.STM.newSymbolTable('RESERVED')
      t = ('begin','BEGIN','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('call','CALL','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('const','CONST','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('do','DO','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('else','ELSE','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('end','END','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('if','IF','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('odd','ODD','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('print','PRINT','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('procedure','PROCEDURE','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('read','READ','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('then','THEN','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('var','VAR','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('while','WHILE','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('write','WRITE','KEYWORD',0)
      self.STM.insertEntry(t)
      t = ('writeln','WRITELN','KEYWORD',0)
      self.STM.insertEntry(t)
       
       
   #Start of the program
   def parse(self):
      self.currentTok = self.LA.scan()
      self.program()
      print ('Parse complete with', self.warnings, 'Warnings and', self.errors,'Errors')
      print ('Parse Complete')
      if (self.errors == 0):
         self.emit()
         print ('target code was written to:', self.string)
    
   #program -> block '.' FEND
   def program(self):
      if (self.debug == 1):
         print (self.myIndent + 'Program ->')
      self.code.append(str(self.linecount) + '\tJMP\t' + '0\t1\t# Main program JMP\n')
      self.linecount += 1
      self.block('_main')
      self.match('.')
      self.code.append(str(self.linecount) + '\tOPR\t' + '0\t0\t# Exit main\n')
      self.match('FEND')
      
   #block -> const-declaration var-declaration procedure-declaration statement
   #creater newsymboltabel in block and print in block
   def block(self,entry):
      self.offset = 3
      if (self.debug == 1):
         print (self.myIndent + 'block ->')
      self.STM.newSymbolTable(entry)
      tok = self.getCurrTok()
      if (tok == 'CONST'):
         self.constDec()
      tok = self.getCurrTok()
      if (tok == 'VAR'):
         self.varDec()
      tok = self.getCurrTok()
      if (tok == 'PROCEDURE'):
         self.procDec() 
      tok = self.getCurrTok()
      self.stmt()
      #if (self.debug == 1):
      #   print (self.STM)
      self.STM.kpop()
      
   #Checks to see if ID is in the symbol table
   #if not ingore it
   def checkConst(self):
      if (self.currentTok[2][0] != 0):
         self.entry = self.currentTok[2][1]
         self.match('ID')
      else:
         self.error('RedefVar')
      if (self.currentTok[0] == '='):
         self.match('RELOP')
      else:
         print ('Warning at line:',self.LA.getLine(),'saw', self.currentTok[0],'expected =')
         self.warnings += 1
         self.match('ASN')
      temp = list(self.entry)
      temp[2] = 'CONST'
      temp[3] = self.currentTok[0]
      self.entry = tuple(temp)
      if (self.getCurrTok() == 'NUM'):
         self.match('NUM')
      else:
         self.error('Num')
      self.STM.insertEntry(self.entry)
      self.code.append(str(self.linecount) + '\tLIT\t' + '0\t' + str(temp[3]) + '\t# Push literal number ' + str(temp[3]) + '\n')
      self.linecount += 1
      self.code.append(str(self.linecount) + '\tSTO\t' + '0\t' + str(temp[3]) + '\t# Store in const ' + temp[0] + '\n')
      self.linecount += 1
         
   #Checks to see if ID is in the symbol table
   #if not ingore it
   def checkVar(self):
      if (self.currentTok[2][0] != 0 or self.currentTok[2][1][2] == 'CONST'):
         entry = self.currentTok[2][1]
         temp = list(entry)
         temp[2] = 'VAR'
         temp[3] = self.offset
         entry = tuple(temp)
         self.STM.insertEntry(entry)
         self.match('ID')
         self.offset += 1
      else:
         self.error('RedefVar')
         
        
   def indent(self):
      self.myIndent += '\t'
      
   def dedent(self):
      self.myIndent = self.myIndent[:-1]
   
   #const-declaration -> [CONST ID '=' NUM {',' ID '=' NUM} ';']
   def constDec(self):
      if (self.debug == 1):
         print (self.myIndent + 'const_dec ->')
      self.indent()
      self.match('CONST')
      self.checkConst()      
      while (self.getCurrTok() != ';'):
         self.match(',')
         self.checkConst()
      self.match(';')
      self.dedent()
      
   #var-declaration -> [VAR ID {',' ID} ';']
   def varDec(self):
      if (self.debug == 1):
         print (self.myIndent + 'var_dec -> ')
         self.indent()
      self.match('VAR')
      self.checkVar()      
      while (self.getCurrTok() != ';'):
         self.match(',')
         self.checkVar()
      self.match(';')
      self.dedent()
      
   #Procedure-Declaration -> [PROC ID ';' block ';'}
   def procDec(self):
      self.match('PROCEDURE')
      self.indent()
      ID = self.currentTok[0]
      if (self.currentTok[2][1][2] != 'PROCEDURE'):
         self.entry = self.currentTok[2][1]
         temp = list(self.entry)
         temp[2] = 'PROCEDURE'
         self.entry = tuple(temp)
         self.STM.insertEntry(self.entry)
         temp = self.currentTok[0]
         self.STM.newSymbolTable(temp)
         self.match('ID')
      else:
         self.error('Redef')       
      self.match(';')
      self.indent()
      self.block(ID)
      self.dedent()
      self.match(';')
      self.dedent()
         
      
   #gets my current token value
   def getCurrTok(self):
      return self.currentTok[1]
      
   def stmt(self):
      '''
      statement -> [ID ASN expr
                  | CALL ID
                  |BEGIN stmt { ';' stmt } END
                  |IF cond THEN stmt [ELSE stmt]
                  |WHILE cond DO stmt
                  |READ '(' ID ')'
                  |WRITE '(' expr ')'
                  |WRITELN '(' expr ')'
                  |e]
      '''
      self.statementFlag = True
      if (self.debug == 1):
         print (self.myIndent + 'stmt ->')
         self.indent()
      tok = self.getCurrTok()
      if (tok == 'ID'):
         if (self.currentTok[2][1][2] == 'CONST'):
            self.error('Const')
         elif (self.currentTok[2][1][2] != 'VAR'):
            self.error('Var')
         else:
            self.var = self.currentTok
            self.match('ID')
         if (self.currentTok[0] == '='):
            print ('Warning at line:',self.LA.getLine(),'Saw \''+self.currentTok[0]+'\' expecting :=')
            self.errors += 1
            self.match(self.currentTok[1])
         else:
            self.match('ASN')
         self.expr()
         self.code.append(str(self.linecount) + '\tSTO\t' + '0\t' \
               + str(self.var[2][1][3]) + '\t# Store in variable ' + self.var[0] + '\n')
         self.linecount += 1
      if (tok == 'CALL'):
         self.match('CALL')
         if (self.currentTok[2][1][2] == 'PROCEDURE'):
            self.match('ID')
         else:
            self.error('Call')
      if (tok == 'BEGIN'):
         self.match('BEGIN')
         self.stmt()         
         while (self.getCurrTok() == ';'):
            self.match(';')
            self.stmt()
         self.match('END')
      if (tok == 'IF'):
         self.match('IF')
         self.cond()
         temp = self.linecount
         self.code.append(str(self.linecount) + '\tJPC\t0\t'+ str(temp) + '\t# Backpatching over IF\n')
         self.linecount += 1
         self.match('THEN')
         self.stmt()
         self.code[temp] = str(temp) + '\tJPC\t0\t'+ str(self.linecount+1) + '\t# Backpatching over IF\n'
         if (self.getCurrTok() == 'ELSE'):
            self.match('ELSE')
            temp = self.linecount
            self.code.append(str(self.linecount) + '\tJPC\t0\t'+ str(temp) + '\t# Backpatching over ELSE\n')
            self.linecount += 1
            self.stmt()
            self.code[temp] = str(temp) + '\tJPC\t0\t'+ str(self.linecount) + '\t# Backpatching over Else\n'
      if (tok == 'WHILE'):
         self.match('WHILE')
         tempDo = self.linecount
         self.cond()
         temp = self.linecount
         self.code.append(str(self.linecount) + '\tJPC\t0\t'+ str(temp) + '\t# Backpatching over WHILE\n')
         self.linecount += 1
         self.match('DO')
         self.stmt()
         self.code[temp] = str(temp) + '\tJPC\t0\t'+ str(self.linecount+1) + '\t# Backpatching over WHILE\n'
         
         self.code.append(str(self.linecount) + '\tJMP\t0\t'+ str(tempDo) + '\t# Jump back to WHILE expr\n')
         self.linecount += 1
      if (tok == 'READ'):
         self.match('READ')
         self.match('(')
         if (self.currentTok[2][1][2] == 'VAR'):
            self.code.append(str(self.linecount) + '\tLOD\t0\t' \
                  + str(self.currentTok[2][1][3]) + '\t# Load Variable ' + str(self.currentTok[0]) + '\n')
            self.linecount += 1
            self.code.append(str(self.linecount) + '\tOPR\t0\t14\t# Read Variable ' + self.currentTok[0] + '\n')
            self.linecount += 1
            self.match('ID')
         else:
            self.error('Read')
         self.match(')')
      if (tok == 'WRITE'):      
         self.match('WRITE')
         self.match('(')
         self.expr()
         self.code.append(str(self.linecount) + '\tOPR\t0\t15\t# Write Line\n')
         self.linecount += 1
         self.code.append(str(self.linecount) + '\tOPR\t0\t17\t# Write Character\n')
         self.linecount += 1   
         self.match(')')
      if (tok == 'WRITELN'):
         self.match('WRITELN')
         self.match('(')
         self.expr()
         self.code.append(str(self.linecount) + '\tOPR\t0\t15\t# Write Line\n')
         self.linecount += 1
         self.code.append(str(self.linecount) + '\tLIT\t0\t10\t# Write Newline\n')
         self.linecount += 1
         self.code.append(str(self.linecount) + '\tOPR\t0\t17\t# Write Character\n')
         self.linecount += 1
         self.match(')')
      if (tok == ';'):
         self.match(';')
      self.dedent()
      self.statementFlag = False
      self.factorFlag = False
      
   #expression -> [ADDOP] term { (ADDOP) term}
   def expr(self):
      if (self.debug == 1):
         print (self.myIndent + 'expr ->')
         self.indent()
      tok = self.getCurrTok()
      if (tok == 'ADDOP'):
         temp = self.currentTok[0]
         self.match('ADDOP')
         self.term()
         if (temp == '-'):
            self.code.append(str(self.linecount) + '\tOPR\t0\t1' + \
                  '\t# Unary INT negate\n')
            self.linecount += 1
         #else:
         #   self.code = (self.code + str(self.linecount) + '\tOPR\t0\t1') + \
         #         '\t# Operator +\n')
         #   self.linecount += 1
      else:
         self.term()
      while (self.getCurrTok() == 'ADDOP'):
         temp = self.currentTok[0]
         self.match('ADDOP')
         self.code.append(str(self.linecount) + '\tJMP\t0\t' + str(self.linecount + 1) + \
                  '\t# Cal & Andy\'s NO-OP instruction :-)\n')
         self.linecount += 1
         self.term()
         if (temp == '+'):
            self.code.append(str(self.linecount) + '\tOPR\t0\t2\t#ADD\n')
         else:
            self.code.append(str(self.linecount) + '\tOPR\t0\t3\t#SUBTRACT\n')
         self.linecount += 1
      self.dedent()
         
   #Term factor {(MULOP) factor }
   def term(self):  
      if (self.debug == 1):
         print (self.myIndent + 'term ->')
         self.indent()
      self.factor()
      while (self.getCurrTok() == 'MULOP' and self.factorFlag == True):
         temp = self.currentTok[0]
         self.match('MULOP')
         self.code.append(str(self.linecount) + '\tJMP\t0\t' + str(self.linecount + 1) + \
                  '\t# Cal & Andy\'s NO-OP instruction :-)\n')
         self.linecount += 1
         self.factor()
         if (temp == '*'):
            self.code.append(str(self.linecount) + '\tOPR\t0\t4\t# MULTIPLY\n')
         else:
            self.code.append(str(self.linecount) + '\tOPR\t0\t5\t# DIVIDE\n')
         self.linecount += 1

      if (self.factorFlag == False):
         self.error('MOLOP')
      self.dedent()
         
   #Factor  ID | NUM | "(" expression ")"
   def factor(self):
      if (self.debug == 1):
         print (self.myIndent + 'factor ->')
         self.indent()
      tok = self.getCurrTok()
      if (tok == 'ID'):
         self.factorFlag = True
         self.code.append(str(self.linecount) + '\tSTO\t' + '0\t' + \
               str(self.currentTok[2][1][3]) + '\t# Load variable ' + str(self.currentTok[0]) + '\n')
         self.linecount += 1
         self.match('ID')
      if (tok == 'NUM'):
         self.factorFlag = True
         self.code.append(str(self.linecount) + '\tLIT\t' + '0\t' + \
               str(self.currentTok[0]) + '\t# Push literal number ' + str(self.currentTok[0]) + '\n')
         self.linecount += 1
         self.match('NUM')
      if (tok == '('):
         self.match('(')
         self.expr()
         self.match(')')
      
      self.dedent()
      
   
   #condition -> ODDexpr
               #|expr RELOP expr
   def cond(self):
      if (self.debug == 1):
         print (self.myIndent + 'cond ->')
         self.indent()
      tok = self.getCurrTok()
      if (tok == 'ODD'):
         self.match('ODD')
         #self.code = self.code + str(self.linecount) + '\tOPR\t' + '0\t' + \
         #      '1' + '\t#Unary INT negative\n'
         #self.linecount += 1
         self.expr()
      else:        
         self.expr()
         self.code.append(str(self.linecount) + '\tJMP\t0\t' + str(self.linecount + 1) + \
                  '\t# Cal & Andy\'s NO-OP instruction :-)\n')
         self.linecount += 1 
         temp = self.currentTok[0]
         self.match('RELOP')
         self.expr()
         if (temp == '='):
            self.code.append(str(self.linecount) + '\tOPR\t0\t8\t# =\n')
         if (temp == '!='):
            self.code.append(str(self.linecount) + '\tOPR\t0\t9\t# !=\n')
         if (temp == '<'):
            self.code.append(str(self.linecount) + '\tOPR\t0\t10\t# <\n')
         if (temp == '<='):
            self.code.append(str(self.linecount) + '\tOPR\t0\t13\t# <=\n')
         if (temp == '>'):
            self.code.append(str(self.linecount) + '\tOPR\t0\t12\t# >\n')
         if (temp == '>='):
            self.code.append(str(self.linecount) + '\tOPR\t0\t11\t# >=\n')
         self.linecount += 1
      self.dedent()
         
   #Checks tokens 
   def match(self,token):
      if (self.debug == 1):
         print (self.myIndent + 'match ', token, '->', self.currentTok[0])
         if (token == 'ID'):
            print (self.myIndent + 'level:',self.currentTok[2][0],'Entry:',self.currentTok[2][1])
      if (token == self.currentTok[1]):
         self.currentTok = self.LA.scan()
      else:
         self.error('Panic')
         
   def panicMode(self):
      print ('PanicMode searching for \';\' token')
      while (self.currentTok[1] != ';' and self.currentTok[1] != 'FEND'):
         self.currentTok = self.LA.scan()
      print ('found \''+self.currentTok[1]+'\' token continuing.')
      if (self.currentTok[1] == 'FEND'):
         sys.exit()
      if (self.statementFlag == False):
         self.match(';')
      
         
   def emit(self):
      string = self.theProgram.split('.')
      string = string[0]
      self.string = string+'.fsti'
      f = open(self.string,'w')
      finalcode = ''
      for i in self.code:
         f.write(i)
      f.close()
      
   def backpatching(self, check):
      if (check == 'IF'):
         self.code.append(str(self.linecount) + '\tJPC\t'+ self.linecount + '\t# Backpatching over IF\n')
         self.linecount += 1
         self.code = self.code + self.string
      
   def error(self,theError):
      if (theError == 'Panic'):
         print ('Syntax error, at line:',self.LA.line()-1,'entering Panic Mode')
      if (theError == 'MOLOP'):
         print ('Syntax error at line:',self.LA.getLine()-1,'Expecting an ID before the MOLOP')
      if (theError == 'RedefVar'):
         print ('RedefineError at line:',self.LA.getLine()-1,'Ignoring',self.currentTok[0])
         
      if (theError == 'Read'):
         print ('ReadError at line:',self.LA.getLine(),'Ignoring',self.currentTok[0],'must read a VAR')
      if (theError == 'Call'):
         print ('CallError at line:',self.LA.getLine(),'Ignoring',self.currentTok[0],'Must call a procedure')
      if (theError == 'Cosnt'):
         print ('ConstError at line:',self.LA.getLine(), 'Ignoring',self.currentTok[0],'cannot change value of a const')
      if (theError == 'Var'):
         print ('VarError at line:',self.LA.getLine()-1,'expecting a VAR ID')
      if (theError == 'Redef'):
         print ('RedefineError at line:',self.LA.getLine(),'Ignoring',self.currentTok[0])
      if (theError == 'Num'):
         print ('Error at line:',self.LA.getLine(),'Ignoring',self.currentTok[0],'Expecting a NUM') 
         
         
      if (theError is 'Panic' or theError is 'MOLOP' or theError is 'RedefVar'):
         self.panicMode()
      else:
         self.match(self.currentTok[1])
      
      self.errors += 1
      
      
      
if __name__ == '__main__':
   source = open('test5.txt')
   test = source.read()
   source.close()
   
   p = Parser(test)
   
   p.parse()
   print ('Finished')
      