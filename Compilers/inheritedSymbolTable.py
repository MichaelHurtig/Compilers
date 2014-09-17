

class symbolTableStack(list):

    def newTable(self, tableName):
        tableName = {}
        self.append(tableName)

    def newSymbol(self, entry):
        # Find index '0'
        top = len(self) - 1
        self[top] = entry

    def replaceSymbol(self, entry):
        pass

    def searchSymbol(self, lexeme):
        # Use 'top' table first
        print( (item for item in self) )
        
if __name__ == "__main__":
    pass
