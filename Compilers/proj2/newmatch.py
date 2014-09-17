





def match( a_list, target ):
    try:
        if self.current_token[1] == target:
            self.debug('{:<20} {:>10}'.format(str(self.current_token[1])+ " --> " + st, \
                                                  ' L: ' + str(self.current_token[2].get('line')) + \
                                                  ' C: ' + str(self.current_token[2].get('column'))))
            self.current_token = next(self.pos)

        elif self.current_token[1] in a_list:
            while self.current_token[1] != a_list[0]:
                a_list.pop(0)
                sys.stderr.write("ERROR: MISMATCH - {}".format(self.current_token[1])
            self.debug('{:<20} {:>10}'.format(str(self.current_token[1])+ " --> " + st, \
                                                  ' L: ' + str(self.current_token[2].get('line')) + \
                                                  ' C: ' + str(self.current_token[2].get('column'))))
            self.current_token = next(self.pos)

        else:
            a_list = []

    
