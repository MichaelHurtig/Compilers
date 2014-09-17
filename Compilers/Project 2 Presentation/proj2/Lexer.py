import re
from STStack import *

'''
        The lexer class provides the methods required to take an input string 
        and tokenize it. This particular implementation uses re to find 
        patterns in the string, and then yields a generator object that will
        allow the user to advance through a provided string, token by token
'''

class lexer:

    '''
	Method: __init__(symbolTable, string) 

		Initializer for the lexer class. 
	
	PRECONDITIONS: There must exist a valid symbolTable and input string

	POSTCONDITIONS: A new instance of lexer will be created.
    '''
    def __init__(self, symbolTable, s):

        self.symbolTable = symbolTable
        self.s = s

    '''
	Method: tokenize()

		Tokenizes a string and yeilds a generator object for iteration
	
	PRECONDITIONS: valid input string, valid symbol table

	POSTCONDITIONS: yeilds a generator that may be advanced token by token
    '''
    def tokenize(self):
       
        define_tokens = [
            ('FEND',    r'\<eof>'),                  # Appended End of File
            ('NUM',     r'[0-9]+'),                  # Ints
            ('ID',      r'[A-Za-z][A-Za-z0-9_]*'),   # IDs, starting with a letter
            ('ADDOP',   r'[+-]'),                    # Math Operations '+' '-'
            ('MULOP',   r'[\*/]'),                   # Math Operations '*' '/'
            ('RELOP',   r'=|!=|<|<=|>|>='),          # Math Operations "=" "!=" "<" "<=" ">" ">="
            ('ASN',     r':='),                      # Assignment Operator
            ('COMMENT', r'\{[^\}]*\}'),              # Comments, comment cannot contain '}'
            ('ENDSTMT', r';'),                       # End of a Statment
            ('LPAREND', r'\('),                      # Left Parend
            ('RPAREND', r'\)'),                      # Right Parend
            ('BLCKEND', r'\.'),                      # End of program block
            ('COMMA',   r','),                       # Comma sperator of declarations
            ('SKIP',    r'[ \t]'),                   # Skip over spaces and tabs
            ('NEWLINE', r'\n'),                      # Line endings
            ]

        regTokens = '|'.join('(?P<%s>%s)' % pair for pair in define_tokens)
        getToken = re.compile(regTokens).match
        
        lineCount = 1
        position = line_start = 0
        
        thing = getToken(self.s)
        while thing is not None:
            typ = thing.lastgroup
            if typ == 'NEWLINE':
                line_start = position
                lineCount += 1
                print("----Newline----")

            elif typ == 'COMMENT':
                newlines = len(re.findall(r'\n', thing.group(typ)))
                lineCount += newlines

            elif typ != 'SKIP':
                value = thing.group(typ)

                if typ != 'ID' :
                    yield ( value, typ, lineCount, thing.start()-line_start)
               
                else:
                    if self.symbolTable.stackFind(value.upper()) != -1:
                        temp = self.symbolTable.stackFind(value.upper())
                        yield (temp[1][0],temp[1][1],temp[0])
                    else:
                        yield ( value, typ, lineCount, thing.start()-line_start)
             
            
            position = thing.end()
            thing = getToken(self.s, position)

        if position != len(self.s):
            raise RuntimeError('Unexpected character %r on line %d' %(self.s[position], lineCount))

if __name__ == "__main__":

    statements = '''const z = 56;
var x, y;
begin	
  	read(y)
	x := y + z;
	write(x)
end.

begin
	read (w);
   	x:= 4;
   	if w > x then
			w:= w + 1
   	else
			w:= x;
	write (w);
end.

<eof>'''
    
    stack = symbolStack()
    stack.stackNewTable()

    keys = ['BEGIN', 'CALL', 'CONST', 'DO', 'ELSE', 'END', 'IF', 'ODD', 'PRINT',
        'PROCEDURE', 'READ', 'THEN', 'VAR', 'WHILE', 'WRITE', 'WRITELN']

    for item in keys:
        stack.stackInstall((item, item.upper()))
    
    alexer = lexer(stack, statements)
    a = alexer.tokenize()
##    print(next(a))
    for item in a:
        print(item)

