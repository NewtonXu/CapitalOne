'''
Here I give some examples

commentChecker = CommentCounter() #load the comment counter class

commentChecker.loadCustomSymbols("<!--","<!--","-->") #load the symbols which
represent comments. For a language like HTML, put the multiline case for single

commentChecker.useMultilineFSM(True) #Set to True if there are multiline 
comments in this programming language. Set to False if there are only single
line comments. 

filename = "test.html"
commentChecker.checkFile(filename) #Launch algorithm
'''

from commentcount import CommentCounter

from timeit import default_timer as timer #just for timing 

def pythonExample():
    commentChecker = CommentCounter()
    commentChecker.loadPythonCommentPreset()
    commentChecker.useMultilineFSM(False)
    filename = "test.py"
    commentChecker.checkFile(filename)

def javaExample():
    commentChecker = CommentCounter()
    commentChecker.loadCPPCommentPreset()
    commentChecker.useMultilineFSM(True)
    filename = "test.txt"
    commentChecker.checkFile(filename)
    
def javaExample2():
    commentChecker = CommentCounter()
    commentChecker.loadCPPCommentPreset()
    commentChecker.useMultilineFSM(True)
    filename = "test2.txt"
    commentChecker.checkFile(filename)
    
def HTMLExample():
    commentChecker = CommentCounter()
    commentChecker.loadCustomSymbols("<!--","<!--","-->")
    commentChecker.useMultilineFSM(True)
    filename = "test.html"
    commentChecker.checkFile(filename)
    
def bigTestExample():
    '''
    Testing runtime on a regular size file
    '''
    start = timer()
    commentChecker = CommentCounter()
    commentChecker.loadCPPCommentPreset()
    commentChecker.useMultilineFSM(True)
    filename = "bigtest.txt"
    commentChecker.checkFile(filename)
    end = timer()
    print("Elapsed time: ")
    print(end-start)

if __name__ == "__main__":
    print("Python Example 1")
    pythonExample()
    print("\n")
    
    print("Java Example 1")
    javaExample()
    print("\n")
    
    print("Java Example 2")
    javaExample2()
    print("\n")
    
    print("HTML Example 1")
    HTMLExample()
    print("\n")
    
    print("Big Java Example")
    bigTestExample()
    print("\n")
