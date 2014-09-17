
def match( self, target, exp_tokens ):
    try: 
        self.indent()
        if self.current_token[1] == a_list[0]:
            self.debug('{:<20} {:>10}'.format(str(self.current_token[1])+ " --> " + a_list[0],\
                                                      ' L: ' + str(self.current_token[2].get('line')) + \
                                                      ' C: ' + str(self.current_token[2].get('column'))))
            self.current_token = next(self.pos)
            
        elif self.current_token[1] in exp_tokens:
            sys.stderr.write("MISMATCH: Found ({}), Expected ({}) Line ({})\n"\
                                     .format(self.current_token[1], \
                                    a_list[0], \
                                    self.current_token[2].get('line')))
            self.error_count += 1
            
        else: 
            sys.stderr.write("MISMATCH: Found ({}), Expected ({}) Line ({})\n"\
                                     .format(self.current_token[1], \
                                    a_list[0], \
                                    self.current_token[2].get('line')))
            self.current_token = next(self.pos)
            self.error_count += 1
            
    except StopIteration:
        pass
        
    except:
        print('Unexpected Exception: ',sys.exc_info()[0], 'Line: ', self.current_token[2].get('line'))
        exit()
        
    def match(self, a_list, exp_tokens):
        if self.error_count == 8:
            sys.exit()
        try:
            self.indent()

            while a_list != []:
                if self.current_token[1] == a_list[0]:
                    self.debug('{:<20} {:>10}'.format(str(self.current_token[1])+ " --> " + a_list[0],\
                                                      ' L: ' + str(self.current_token[2].get('line')) + \
                                                      ' C: ' + str(self.current_token[2].get('column'))))
                    self.current_token = next(self.pos)

                    a_list.pop(0)

## We will want to have an elif to test when it is in the table and an else if it is not

                elif self.current_token[1] in a_list:
                    sys.stderr.write("MISMATCH: Found ({}), Expected ({}) Line ({})\n"\
                                     .format(self.current_token[1], a_list[0], self.current_token[2].get('line')))
                    a_list.pop(0)
                    self.error_count += 1
                    
                else:
##rewrite this so that we advnace the token and discard teh current list
                    sys.stderr.write("MISMATCH: Found ({}), Expected ({}) Line ({})\n"\
                                     .format(self.current_token[1], a_list[0], self.current_token[2].get('line')))
##                    self.error_count += len(a_list)
##                    a_list = []
                    self.current_token = next(self.pos)


            self.dedent()
                                 
        except StopIteration:
            pass

        except:
            print('Unexpected Exception: ',sys.exc_info()[0], 'Line: ', self.current_token[2].get('line'))
            exit()