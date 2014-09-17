
class symbolTableStack:
        def __init__(self):
                self.stack = []

        def stackEmpty(self):
                return self.stack == []

        def stackNewTable(self, tableID):
                self.stack.append( tableID = [])
'''                
	def __init__(self):
		self.items = []
		
	def stackEmpty(self):
		return self.items == []
		
	def stackPush(self, tableID):
                pass

	def stackPop(self):
                pass

        def stackSymbolFind(self, lexeme):
                pass

        def stackSymbolPush(self, symbol):
                pass

        def stackSymbolRemove(self, symbol):
                pass

        def stackSymbolReplace(self, entry):
                pass

        def __str__(self):
                pass

'''
if __name__ == "__main__":

        symTabStack = symbolTableStack()
        
