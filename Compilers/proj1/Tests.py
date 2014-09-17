from STStack import *

input("Press ENTER to continue")
print()

print('~~~~~~~~~~ Creating STEs~~~~~~~~~~~')
ste1 = STE('a', '.', '.')
ste2 = STE('b', '.', '.')
ste3 = STE('a', '.', '.')
ste4 = STE('aleph', '.', '.')

ste1.printSTE()
ste2.printSTE()
ste3.printSTE()
ste4.printSTE()

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print()

input("Press ENTER to continue")
print()

print('~~~~~~~~~~~Creating STs~~~~~~~~~~~~')

st1 = symbolTable()
st2 = symbolTable()

st1.printTable()
st2.printTable()

print()
input("Press ENTER to continue")
print()

print('~~~~~~~~~~~Inserting STEs~~~~~~~~~~')

st1.addSymbol(ste1)
st1.addSymbol(ste2)
st2.addSymbol(ste3)
st2.addSymbol(ste4)

print()
print('~~~~~~~~st1~~~~~~~~~')
st1.printTable()
print()
print('~~~~~~~~st2~~~~~~~~~')
st2.printTable()

print()
input("Press ENTER to continue")
print()

print('~~~~~~~~~~~~Finding STEs~~~~~~~~~~~')

print('Finding "a" in st1: ' +str(st1.findSymbol('a')))
print('Finding "b" in st1: ' +str(st1.findSymbol('b')))
print('Finding "c" in st1: ' +str(st1.findSymbol('c')))
print()
print('Finding "aleph" in st2: ' +str(st2.findSymbol('aleph')))

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

print()
input("Press ENTER to continue")
print()

print('~~~~~~~~~~Creating Stack~~~~~~~~~~~')

sts1 = symbolStack()

print('Empty Symbol Table Stack: ' + str(sts1) )

print()
input("Press ENTER to continue")
print()

print('~~~~~~~~~Creating New STs~~~~~~~~~~')

sts1.stackNewTable()
print('Empty Symbol Table Stack w/ Empty Table: ' + str(sts1) )
print()

input("Press ENTER to continue")
print()

print('~~~~~~~Installing New STEs~~~~~~~~~')

sts1.stackInstall(ste1)
print(sts1)
print()

sts1.stackInstall(ste2)
print(sts1)
print()

input("Press ENTER to continue")
print()

print('~~~~~~~Installing New STs~~~~~~~~~~')

sts1.stackNewTable()
print(sts1)
print()

sts1.stackInstall(ste3)
print(sts1)
print()

sts1.stackInstall(ste4)
print(sts1)
print()

input("Press ENTER to continue")
print()

print('~~~~~~~~~~Finding STEs~~~~~~~~~~~~')

print('Reference Stack: ' + str(sts1))
print()

print('Finding "a" in st1: ' +str(sts1.stackFind('a')))
print()

print('Finding "b" in st1: ' +str(sts1.stackFind('b')))
print()

print('Finding "aleph" in st1: ' +str(sts1.stackFind('aleph')))
print()

print('Finding "z" in st1: ' +str(sts1.stackFind('z')))

print()
input("Press ENTER to continue")
print()

print('~~~~~~~~~~Adjust Levels~~~~~~~~~~~~')

sts1.stackNewTable()
print(sts1)
print()

print('Reference Stack: ' + str(sts1))
print()

print('Finding "a" in st1: ' +str(sts1.stackFind('a')))
print()

print('Finding "b" in st1: ' +str(sts1.stackFind('b')))
print()

print('Finding "aleph" in st1: ' +str(sts1.stackFind('aleph')))
print()

print('Finding "z" in st1: ' +str(sts1.stackFind('z')))

print()
input("Press ENTER to quit")

