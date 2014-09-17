import sys
import argparse
from mini_Parser import *

def main():

    inputString = ''

    cmd_line = argparse.ArgumentParser(description = 'A PL0 Language Compiler')

    cmd_line.add_argument('source', help = 'Target PL0 source file')
    cmd_line.add_argument('-d', '--debug', help = 'Enable Debug Mode', action = 'store_true')

    flags = cmd_line.parse_args()

    global DEBUG
    DEBUG = flags.debug

    target_file = flags.source



    try:
        with open(target_file, 'r') as file:
            inputString = file.read()
            inputString += '<eof>'

    except:
        print( target_file + ' is not a valid vile' )
        sys.exit()

    new_parser = parser(inputString, DEBUG)
    new_parser.parse()

        

if __name__ == "__main__":
    main()
