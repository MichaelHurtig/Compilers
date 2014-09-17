

def file_input(fileString):
    '''
	function file_input()
	
	PRECONDITIONS: A valid file 'input.txt' must exist. 
	POSTCONDITIONS: Reads the file, and returns a string with '<eof>' 
			concatinated at the end.
    '''
    file = open(fileString,"r")
    inputString = file.read()

    return inputString + "<eof>"





