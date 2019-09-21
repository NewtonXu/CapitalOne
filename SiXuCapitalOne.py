'''
Solution Overview
========================
I implemented two finite state machines to handle the two styles of commenting
from the example.

The CStyleFSM is capable of handling any programming language with both single
line and multi-line comments. The symbol set of //, /* */ seems to apply quite
broadly, C++ / Java. Here I assume multiple consecutive single comments are not 
treated as a block

CStyleFSM can also handle languages with only multi-line 
comments like HTML. In this case I made the assumption that all comments here 
should be treated as multiline comments as given in the example. 

The PythonFSM will handle cases where there are only single line comments. And
multiple consecutive single line comments count as blocks. 

Handling strings
========================
I have added a search which will identify if a comment symbol is a 
comment or part of a string. 

I have assumed that all strings will use single or double quotes. 
There are some languages which don't use this, and my system can be expanded
to handle this if needed. 

I have also included a way to detect multiline strings, this is necessary to 
ensure that comment symbols can be used in multi-line strings without breaking
the counter. 

I made the assumption that two multiline strings will not end and begin on the 
same line. This is necessary because multiline strings and single line strings
share characters sometimes, such as in Python. Multiline and single line strings
are treated seperately because of this, if I wanted to be able to detect
them together, it would require loading more than one line at a time into memory
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
        
        self.multiLineStringStart = None
        self.multiLineStringEnd = None
        self.insideMultiLineString = False

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
        
    def loadTODO(self, input):
        '''
        Load a different string to represent the TODO
        '''
        self.TODO = input
    
    def loadMultiLineStrings(self, start, end):
        self.multiLineStringStart = start
        self.multiLineStringEnd = end
    
    def loadCustomSymbols(self, singleLineSymbol, multiLineStart, multiLineEnd):
        '''
        Load a set of symbols for your favourite programming language
        '''
        self.loadSingleLineComment(singleLineSymbol)
        self.loadMultiLineComment(multiLineStart, multiLineEnd)
        
    def loadPythonCommentPreset(self):
        '''
        Sample comment symbols for Python
        '''
        self.loadSingleLineComment("#")
        self.loadMultiLineComment("#","#")
        self.loadMultiLineStrings("'''","'''")

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
        
    def commentSearch(self,line):
        '''
        Return the type of the first comment encountered in the string
        -1 : No comment present
         0 : Single line comment
         1 : Multi-line start
        and the index at which it is encountered
        
        This search assumes that strings are defined by either ' or "
        We have to add in additional checks to ensure the comment symbol is
        not part of a string
        '''
        i = 0
        while i < len(line):
            if line[i]==self.singleLineComment[0]:
                temp = line.find(self.singleLineComment,i)
                if(temp>=0):
                    if line.find(self.TODO,temp) != -1:
                        self.numToDo += 1
                    return 0,temp
            if line[i]==self.multiLineCommentStart[0]:
                temp = line.find(self.multiLineCommentStart,i)
                if(temp>=0):
                    if line.find(self.TODO,temp) != -1:
                        self.numToDo += 1
                    return 1,temp
            if line[i]=='"':
                i = line.find('"',i+1)
            elif line[i]=="'":
                i = line.find("'",i+1)
            i += 1
        return -1,-1
        
    def checkPythonComment(self, line):
        '''
        Use this to compute comments where the single line comment and multiline
        comments use identical identifiers and the multiline is just 
        consecutive single line comments. ie Python
        '''
        if self.PythonFSM == 0:
            commentType, index = self.commentSearch(line)
            if commentType==-1: #No comment in this line
                return
            else:
                if index==0: #Single line comment
                    self.PythonFSM = 1
                    self.checkPythonComment(line)
                else:
                    self.PythonFSM = 5
                    self.checkPythonComment(line)
        
        elif self.PythonFSM == 5:
            #Just a single line comment
            self.singleLineCount += 1
            self.commentCount += 1
            self.PythonFSM = 0
        
        elif self.PythonFSM == 1:
            #Single line comment but could potentially be multiline
            self.singleLineCount += 1
            self.commentCount += 1
            self.PythonFSM = 2
        
        elif self.PythonFSM == 2:
            #Check to see if the single line should be promoted to multiline
            commentType, index = self.commentSearch(line)
            if commentType==-1: #No comment present
                self.PythonFSM = 0
            else:
                if index==0:
                    self.PythonFSM = 3
                    self.checkPythonComment(line)
                else:
                    self.PythonFSM = 5
                    self.CheckPythonComment(line)
        
        elif self.PythonFSM == 3:
            #Single line turned into multiline
            self.singleLineCount -= 1
            self.commentCount += 1
            self.multilineCount += 1
            self.linesInMultiline += 2
            self.PythonFSM = 4
        
        elif self.PythonFSM == 4:
            #Inside a multiline, waiting to end
            commentType, index = self.commentSearch(line)
            if commentType!=-1: #Contains comment
                if index==0: #Comment is at beginning of line, still multiline
                    self.commentCount+=1
                    self.linesInMultiline += 1
                else: #Comment is not at beginning, no longer multiline
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
            commentType, index = self.commentSearch(line)
            if commentType == 1: #Multiline comment starter found
                self.commentCount += 1
                self.multilineCount += 1
                self.linesInMultiline += 1
                if self.multiLineCommentEnd not in line:
                    self.CStyleFSM = 1
                    
            elif commentType== 0: #Singleline comment found
                self.commentCount += 1
                self.singleLineCount += 1
            
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
    
    def checkForMultiLineString(self,line):
        '''
        Return true if this line contains an unclosed multi-line string
        Also sets the class variable insideMultiLineString if we are
        '''
        if self.multiLineStringStart == None:
            return False
        idx = line.find(self.multiLineStringStart)
        if idx != -1:
            if line.find(self.multiLineStringEnd, idx+len(self.multiLineStringStart))==-1:
                self.insideMultiLineString = True
                return True
        return False
        
    def runFSM(self,filename):
        '''
        Main function for file parsing
        '''
        with open(filename, "r") as file:
            for line in file:
                line.strip()
                self.lineCount += 1
                
                #This section is specifically for dealing with multiline strings
                #If a multiline string is encountered, skip lines until the end
                if self.insideMultiLineString:
                    idx = line.find(self.multiLineStringEnd)
                    if idx!=-1:
                        #We've found the end, slice off the end of the multiline
                        #Then search as usual.
                        self.insideMultiLineString = False
                        line = line[idx+len(self.multiLineStringEnd):len(line)]
                    else:
                        continue
                else:
                    if self.checkForMultiLineString(line):
                        continue
                        
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
    #javaChecker.loadCPPCommentPreset() #load the symbols for this language
    #I've also included two other options:
    javaChecker.loadPythonCommentPreset()
    #javaChecker.loadCustomSymbols(str,str,str) #add your own!
    javaChecker.useMultilineFSM(False) 
    filename = "test.py"
    javaChecker.checkFile(filename)
