
import inspect

def debug(mesg = 'I got here', indent = 0, *args ):
    string = ''
    for x in range(0, indent):
        string += '   '
    import inspect
    from sys import stderr
    frame = inspect.stack()[1]
    #if 'DEBUG' not in globals().keys() or DEBUG:
    print("{:15s}:: ".format(frame[3]+':'+str(frame[2])), mesg, *args, file=stderr)
    print(  string + "[1 " + str(frame[0]) +" ]\n" +\
             string + "[2 " + str(frame[1]) +" ]\n" +\
             string + "[3 " + str(frame[2]) +" ]\n" +\
             string + "[4 " + str(frame[3]) +" ]\n" +\
             string + "[5 " + str(frame[4]) +" ]\n" +\
             string + "[6 " + str(frame[5]) +" ]\n" \
            )

    

    


class testClass():


    def function1(self):

        debug('blah blah',4, self )

        print("function1")

    def function2(self):
        debug(self)

        self.function1()

        print("function2")

    
if __name__ == "__main__":

    new = testClass()

    new.function2()

    
