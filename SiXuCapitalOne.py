'''
Solution Overview
========================
For this assignment, I was only familiar with the two commenting styles:
Python #, and C-style /* */, //. 

My quick search through various programming languages indicates that these are 
sufficient to cover the majority of popular languages. That is, one case where
the single line comment and multiline comments are identical, and one case
where the multiline comment has different symbols.

The CStyleFSM is capable of handling any programming language with both single
line and multi-line comments. The symbol set of //, /* */ seems to apply quite
broadly. 

CStyleFSM can also handle languages with only multi-line 
comments like HTML. In this case I made the assumption that all comments here 
should be treated as multiline comments as given in the example.

The PythonFSM will handle cases where there are only single line comments.

Edge Cases
========================
Case 1)
// /* */
In this situation, there is a single line comment and a multiline comment on 
the same line. My system counts the multi-line first, this is for compatibility
with languages like HTML which do not have single line comments. 

Case 2)
A string containing a comment symbol on the same line as a comment
string = "#" #"commentnotstr




'''

class CommentCounter:
    def __init__(self): 
        self.FSMType = True
        self.PythonFSM = 0 #Represents the FSM state
        self.CStyleFSM = 0 #Represents the FSM state
        self.lineCount = 0
        self.commentCount = 0
        self.singleLineCount = 0
        self.multilineCount = 0
        self.linesInMultiline = 0
        self.numToDo = 0
        self.singleLineComment = ""
        self.multiLineCommentStart = ""
        self.multiLineCommentEnd = ""
        self.TODO = "TODO"

    def reset(self):
        self.PythonFSM = 0
        self.CStyleFSM = 0
        self.lineCount = 0
        self.commentCount = 0
        self.singleLineCount = 0
        self.multilineCount = 0
        self.linesInMultiline = 0
        self.numToDo = 0

    def useMultilineFSM(self,input):
        '''
        Tell class to use the multiline FSM or singleline FSM
        True = Multiline FSM
        False = SingleLine FSM
        '''
        self.FSMType = input
        
    def loadSingleLineComment(self, input):
        '''
        String which represents the start of a single line comment
        '''
        self.singleLineComment = input
    
    def loadMultiLineComment(self, start_symbol, end_symbol):
        '''
        String which represents the start/end of a multi line comment
        '''
        self.multiLineCommentStart = start_symbol
        self.multiLineCommentEnd = end_symbol
        
    def loadCustomSymbols(self, singleLineSymbol, multiLineStart, multiLineEnd):
        '''
        Load a set of symbols for your favourite programming language
        '''
        self.loadSingleLineComment(singleLineSymbol)
        self.loadMultiLineComment(multiLineStart, multiLineEnd)
    
    def loadTODO(self, input):
        '''
        Load a different string to represent the TODO
        '''
        self.TODO = input
    
    def loadPythonCommentPreset(self):
        '''
        Sample comment symbols for Python
        '''
        self.loadSingleLineComment("#")
        self.loadMultiLineComment("#","#")

    def loadCPPCommentPreset(self):
        '''
        Sample comment symbols for C++, Java etc.
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

    def contextFSM(self,line):
        '''
        Return the type of the first comment encountered in the string
        -1 : No comment present
         0 : Single line comment
         1 : Multi-line start
        and the index at which it is encountered
        
        This search assumes that strings are defined by either ' or "
        and we must ensure that the comment is not actually part of a string
        '''
        for i in range(0,len(line)):
            if line[i]=='"':
                i = line.find('"',i+1)
            elif line[i]=="'":
                i = line.find("'",i+1)
            if line[i]==self.singleLineComment[0]:
                temp = line.find(self.singleLineComment,i)
                if(temp>=0):
                     return 0,temp
            if line[i]==self.multiLineCommentStart[0]:
                temp = line.find(self.multiLineCommentStart,i)
                if(temp>=0):
                     return 1,temp
        return -1,-1

    def checkPythonComment(self, line):
        '''
        Use this to compute comments where the single line comment and multiline
        comments use identical identifiers, ie Python
        '''
        if self.PythonFSM == 0:
            #Base Case
            if self.singleLineComment not in line:
                return
            else:
                if line[0]==self.singleLineComment:
                    self.PythonFSM = 1
                    self.checkPythonComment(line)
                else:
                    self.PythonFSM = 5
                    self.checkPythonComment(line)

        elif self.PythonFSM == 5:
            #Single line only
            self.singleLineCount += 1
            self.commentCount += 1
            if self.TODO in line:
                self.numToDo += 1
            self.PythonFSM = 0
        
        elif self.PythonFSM == 1:
            # If line[0] is comment symbol
            self.singleLineCount += 1
            self.commentCount += 1
            if self.TODO in line:
                self.numToDo += 1
            self.PythonFSM = 2
        
        elif self.PythonFSM == 2:
            #Waiting to see if single line comment becomes multiline
            if self.singleLineComment not in line:
                self.PythonFSM = 0
            else:
                if line[0]==self.singleLineComment:
                    self.PythonFSM = 3
                    self.checkPythonComment(line)
                else:
                    self.PythonFSM = 5
                    self.CheckPythonComment(line)
                if self.TODO in line:
                    self.numToDo += 1
        
        elif self.PythonFSM == 3:
            #Single line turned into multiline
            self.singleLineCount -= 1
            self.commentCount += 1
            self.multilineCount += 1
            self.linesInMultiline += 2
            self.PythonFSM = 4
            if self.TODO in line:
                self.numToDo += 1
        
        elif self.PythonFSM == 4:
            #Inside a multiline, waiting to end
            if self.singleLineComment in line:
                if line[0]==self.multiLineCommentStart:
                    self.commentCount+=1
                    self.linesInMultiline += 1
                    if self.TODO in line:
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
        
        This uses an FSM with two states:
        CStyleFSM = 0 means we are not inside a multiline comment, normal search
        CStyleFSM = 1 we are in a multiline comment, increment accordingly
        '''
        if self.CStyleFSM==0:
            commentType, index = self.contextFSM(line)
            if commentType == 1: #Multiline comment starter found
                self.commentCount += 1
                self.multilineCount += 1
                self.linesInMultiline += 1
                if self.TODO in line:
                    self.numToDo += 1
                if self.multiLineCommentEnd not in line:
                    self.CStyleFSM = 1
                    
            elif commentType== 0: #Singleline comment found
                self.commentCount += 1
                self.singleLineCount += 1
                if self.TODO in line:
                    self.numToDo += 1
            
        elif self.CStyleFSM==1:
            #We are inside a multiline comment, just keep incrementing until
            #we find a multiLineEnder
            if self.TODO in line:
                self.numToDo += 1
            if self.multiLineCommentEnd in line:
                self.commentCount += 1
                self.linesInMultiline += 1
                self.CStyleFSM = 0
            else:
                self.commentCount += 1
                self.linesInMultiline += 1

    def runFSM(self,filename):
        '''
        Main function for file parsing
        '''
        with open(filename, "r") as file:
            for line in file:
                line.strip()
                self.lineCount += 1
                if self.FSMType == False:
                    self.checkPythonComment(line)
                else:
                    self.checkOtherComment(line)
        self.printAll()
    
    def checkFile(self, filename):
        '''
        Entry point into the algorithm
        '''
        self.reset()
        if filename[0] == ".":
            print("This file starts with . ?")
            return
        filename_info = filename.split(".")
        if len(filename_info)<2:
            print("This file has no extension ?")
            return
        self.runFSM(filename)
        
        
        
if __name__ == "__main__":
    javaChecker = CommentCounter() #initialize the class
    javaChecker.loadCPPCommentPreset() #load the symbols for this language
    #I've also included two other options:
    #javaChecker.loadPythonCommentPreset()
    #javaChecker.loadCustomSymbols(str,str,str) #add your own!
    javaChecker.useMultilineFSM(True) 
    filename = "test2.txt"
    javaChecker.checkFile(filename)
