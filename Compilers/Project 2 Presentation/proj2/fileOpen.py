

def file_input():
    '''
	function file_input()
	
	PRECONDITIONS: A valid file 'input.txt' must exist. 
	POSTCONDITIONS: Reads the file, and returns a string with '<eof>' 
			concatinated at the end.
    '''
    file = open("input.txt","r")
    inputString = file.read()

    return inputString + "<eof>"



if __name__ == "__main__":

    print(file_input())
