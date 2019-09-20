'''
For this assignment, I was only familiar with the two commenting styles:
Python #, and C-style /* */, //. 

My quick search through various programming languages indicates that these are 
sufficient to cover the majority of popular languages. That is, one case where
the single line comment and multiline comments are identical, and one case
where the multiline comment has different symbols.

The main edge case I encountered was comment symbols inside strings. 

'''

class commentCounter:
    def __init__(self): 
        self.PythonFSM = 0
        self.CStyleFSM = 0
        self.lineCount = 0
        self.commentCount = 0
        self.singleLineCount = 0
        self.multilineCount = 0
        self.linesInMultiline = 0
        self.numToDo = 0
        self.singleLineComment = ""
        self.multiLineCommentStart = ""
        self.multiLineCommentEnd = ""

    def reset(self):
        self.PythonFSM = 0
        self.CStyleFSM = 0
        self.lineCount = 0
        self.commentCount = 0
        self.singleLineCount = 0
        self.multilineCount = 0
        self.linesInMultiline = 0
        self.numToDo = 0
        self.singleLineComment = ""
        self.multiLineCommentStart = ""
        self.multiLineCommentEnd = ""
    
    def loadSingleLineComment(self, input):
        self.singleLineComment = input
    
    def loadMultiLineComment(self, start_symbol, end_symbol):
        self.multiLineCommentStart = start_symbol
        self.multiLineCommentEnd = end_symbol
       
    def loadPythonCommentPreset(self):
        '''
        Sample comment symbols for Python
        '''
        self.loadSingleLineComment("#")
        self.loadMultiLineComment("#","#")

    def loadCPPCommentPreset(self):
        '''
        Sample comment symbols for C++
        '''
        self.loadSingleLineComment("//")
        self.loadMultiLineComment("/*","*/")
        
    def printAll(self):
        print("Total # of lines: %d" % self.lineCount)
        print("Total # of comment lines: %d" % self.commentCount)
        print("Total # of single line comments: %d" % self.singleLineCount)
        print("Total # of comment lines within block comments: %d" % self.linesInMultiline)
        print("Total # of block line comments: %d" % self.multilineCount)
        print("Total # of TODO's: %d" % self.numToDo)

    def checkIfCommentIsBetweenQuotes(line, symbol):
        '''
        Checking for comment symbols inside a string. For simplicity, I have 
        assumed that 
        '''
        singleQuoteIndex = line.find("'")
        doubleQuoteIndex = line.find('"')
        if singleQuoteIndex==-1 and doubleQuoteIndex==-1:
            return False
        else:
            if singleQuoteIndex > 0:
                pass
        return 0
                

    def checkPythonComment(self, line):
        '''
        Use this to compute comments where the single line comment and multiline
        comments use identical identifiers, ie Python, HTML
        '''
        if self.PythonFSM == 0:
            #Base Case
            if "#" not in line:
                return
            else:
                if line[0]=="#":
                    self.PythonFSM = 1
                    self.checkPythonComment(line)
                else:
                    self.PythonFSM = 5
                    self.checkPythonComment(line)

        elif self.PythonFSM == 5:
            #Single line only
            self.singleLineCount += 1
            self.commentCount += 1
            if "TODO" in line:
                self.numToDo += 1
            self.PythonFSM = 0
        
        elif self.PythonFSM == 1:
            # If line[0] is hash
            self.singleLineCount += 1
            self.commentCount += 1
            if "TODO" in line:
                self.numToDo += 1
            self.PythonFSM = 2
        
        elif self.PythonFSM == 2:
            #Waiting to see if single line becomes multiline
            if "#" not in line:
                self.PythonFSM = 0
            else:
                if line[0]=="#":
                    self.PythonFSM = 3
                    self.checkPythonComment(line)
                else:
                    self.PythonFSM = 5
                    self.CheckPythonComment(line)
                if "TODO" in line:
                    self.numToDo += 1
        
        elif self.PythonFSM == 3:
            #Single line turned into multiline
            self.singleLineCount -= 1
            self.commentCount += 1
            self.multilineCount += 1
            self.linesInMultiline += 2
            self.PythonFSM = 4
            if "TODO" in line:
                self.numToDo += 1
        
        elif self.PythonFSM == 4:
            #Inside a multiline, waiting to end
            if "#" in line:
                if line[0]=="#":
                    self.commentCount+=1
                    self.linesInMultiline += 1
                    if "TODO" in line:
                        self.numToDo += 1
                else:
                    self.PythonFSM = 5
                    self.checkPythonComment(line)
            else:
                self.PythonFSM = 0

    def checkOtherComment(self, line):
        '''
        Use this to compute comments where the multiline and single line
        comments are different EG: C++, Java 
        '''
        if self.CStyleFSM==0:
            if "/*" in line:
                self.commentCount += 1
                self.multilineCount += 1
                self.linesInMultiline += 1
                if "TODO" in line:
                    self.numToDo += 1
                if "*/" not in line:
                    self.CStyleFSM = 1
                    
            elif "//" in line:
                self.commentCount += 1
                self.singleLineCount += 1
                if "TODO" in line:
                    self.numToDo += 1
            
        elif self.CStyleFSM==1:
            if "TODO" in line:
                self.numToDo += 1
            if "*/" in line:
                self.commentCount += 1
                self.linesInMultiline += 1
                self.CStyleFSM = 0
            else:
                self.commentCount += 1
                self.linesInMultiline += 1

    def runPythonFSM(self,filename):
        with open(filename, "r") as file:
            for line in file:
                line.strip()
                if(line!="\n"):
                    self.lineCount += 1
                self.checkPythonComment(line)
        self.printAll()
    
    def runCStyleFSM(self, filename):
        with open(filename, "r") as file:
            for line in file:
                line.strip()
                if(line!="\n"):
                    self.lineCount += 1
                self.checkOtherComment(line)
        self.printAll()
        
    def checkFile(self, filename):
        self.reset()
        if filename[0] == ".":
            return
        name, extension = filename.split(".")
        if extension == "py":
            self.runPythonFSM(filename)
        else:
            self.runCStyleFSM(filename)
        
        
        
if __name__ == "__main__":
    javaChecker = commentCounter()
    javaChecker.reset()
    filename = "test.txt"
    javaChecker.checkFile(filename)