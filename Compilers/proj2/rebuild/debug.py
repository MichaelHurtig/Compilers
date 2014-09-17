
DEBUG = True


def debug(mesg = 'I got here', *args):
    import inspect
    from sys import stderr
    frame = inspect.stack()[1]
    if 'DEBUG' not in globals().keys() or DEBUG:
##        print('IN PARSER @ ' + str(frame[3]))
        print('IN PARSER @ {} [ {} ]'.format(str(frame[3]), mesg))
 

