SYMBOL TABLE STACK

I.   STable - Python implementation of a Symbol Table

	- symbolTable(): Create a symbol table and put it on the stack
	
	- addSymbol(STE): Add a symbol to current table
	
	- findSymbol(string): Find a lexeme in current table
	
	- printTable(): TEST METHOD - print current table
	
	- hashMethod(STE,int=0) HELPER METHOD (OUTDATED) - returns a has of STE.lexeme

II.  (DEFUNCT) STE - Python implementation of a Symbol Table Entry

	- STE(lexeme, ident, position): Create an STE

	- __init__(string, string, string): initialize a STE
	
	- printSTE(): prints the fields of the STE

III. STSTack - Python implementation of a Symbol Table Stack

	- symbolStack(): Create a symbol table stack

	- stackFind(string)
	
	- stackNewTable()
	
	- stackInstall(STE)
	
	- stackReplace(STE) NON-FUNCTIONAL (FIX)
	
IV. KNOWN BUGS:
	
	a. The stackInstall(STE) method from STStack handles collisions awkwardly. 
	   Revision of STE and stackInstall Methods will be needed. (9-11-13)
	   
	   RESOLVED: used built-in hashing for python dict objects. (9-11-13)
	   
	b. The stackFind(string) method from STStack appears to have been 
	   accidentally reverted to a earlier, incorrect version. Will need to be
	   corrected to return correct 'level' or index of the stack. Method does
	   find desired lexeme if it exists, however
	   
	   RESOLVED: found corrected methods and restored them
	   
	