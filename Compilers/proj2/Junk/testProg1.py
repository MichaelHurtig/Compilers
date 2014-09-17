
from Parser import *
from fileOpen import *

file = file_input("test1.txt")
print(file)
print("=================TEST 1=================")
testParse = parser(file)
testParse.parse()
##
##file2 = file_input("test2.txt")
##print(file2)
##print("=================TEST 2=================")
##testParse2 = parser(file2)
##testParse2.parse()
##
##
##file3 = file_input("test3.txt")
##print(file3)
##print("=================TEST 3=================")
##testParse3 = parser(file3)
##testParse3.parse()
##
##file4 = file_input("test4.txt")
##print(file4)
##print("=================TEST 4=================")
##testParse4 = parser(file4)
##testParse4.parse()
