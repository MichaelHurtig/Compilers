import sys, getopt
import fileOpen

def main(argv = None):
    DEBUG = False
    inputfile = ''
    parseString = ''

    try:
        options, args = getopt.getopt(argv, "d:")

    except getopt.GetoptError:
        print("Malformated command")
        sys.exit(2)

    for opt, arg in options:

        if opt == '-d':
            DEBUG = True

            inputfile = arg
            parseString = file_input(inputFile)

        else:
            inputfile = arg
            parseString = file_input(inputFile)

    print(parseString)
    
if __name__ == "__main__":

    main()
