
DEBUG = True


def debug(mesg = 'I got here', *args):
    import inspect
    from sys import stderr
    frame = inspect.stack()
##    string = ''
##    for i in frame:
##        string += '-->' + i[3]

    target = inspect.stack()[1]

    if 'DEBUG' not in globals().keys() or DEBUG:
        print('IN PARSER @ {} [ {} ]'.format(str(target[3]), mesg))

 

