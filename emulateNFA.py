import NFA as automaton
import sys
import os

# python3 emulateNFA.py NFAfile inputFile OPTIONAL(1/0) 
#                                           1 - all intermediate steps printed to the output
#                                           0 - only accepted/rejected printed to the screen
class NFAFileNotFoundError(Exception):
    pass

class NotEnoughArgummentsError(Exception):
    pass

class DirectoryNotFoundError(Exception):
    pass

def changeDirectory(directoryPath):
    # safely changes the current working directory to the specified target directory.

    if os.path.isdir(directoryPath):
        os.chdir(directoryPath)
        # print(f"Successfully changed directory to: {os.getcwd()}")
        return True
    else:
        raise DirectoryNotFoundError(f"Error: Directory '{directoryPath}' does not exist.")

# support for IDE running script
# easily modifiable to make more modular -
# currently we are using two subfolders to be more organised - one with all the .nfa files
# and one with all of the input files to feed into the NFA
nfaDefinitionFolder = "NFA Definition Files"
inputFolder = "Input Files"
if len(sys.argv) == 1:
    try:
        changeDirectory(nfaDefinitionFolder)
        inputNfaFile = open(input("Give NFA Definition file name: "), "r")
        os.chdir("..")
        changeDirectory(inputFolder)
        inputStringFile = open(input("Give input file name: "), "r")
        os.chdir("..")
        allowVerbosity = bool(int(input("Want to output all steps taken by the NFA? (Input 1/0) ")))
        stringInput = input("What separator is used between the symbols in the input file? (Space -> ' ', NoSeparator -> '', ; -> ';', etc.) ")
        if stringInput.upper() == "SPACE":
            stringSeparator = " "
        elif stringInput.upper() == "NOSEPARATOR":
            stringSeparator = ""
        else:
            stringSeparator = stringInput
    except FileNotFoundError:
        raise NFAFileNotFoundError(f"NFA file not found in current directory {os.getcwd()}") 

# support for CLI running script
#         
elif len(sys.argv) == 2:
    raise NotEnoughArgummentsError("You need to also give input file name as an argument, and optionally if you want to output all steps taken by the NFA (1/0 as third argument) ")

else:     
    try:
        changeDirectory(nfaDefinitionFolder)
        inputNfaFile = open(sys.argv[1], "r")
        os.chdir("..")
        changeDirectory(inputFolder)
        inputStringFile = open(sys.argv[2], "r")
        os.chdir("..")
        if len(sys.argv) == 4: 
            allowVerbosity = bool(int(sys.argv[3])) # 1 or 0 if i want all intermediate steps printed to the output or not
        else:
            allowVerbosity = False # verbosity disabled by default
        if len(sys.argv) >= 4: 
            allowVerbosity = bool(int(sys.argv[3])) # 1 or 0 if i want all intermediate steps printed to the output or not
        else:
            allowVerbosity = False # verbosity disabled by default
        if len(sys.argv) == 5:
            if (sys.argv[4]).upper() == "SPACE":
                stringSeparator = " "
            elif (sys.argv[4]).upper() == "NOSEPARATOR":
                stringSeparator = ""
            else:
                stringSeparator = sys.argv[4] 
        else:
            stringSeparator = ""

    except FileNotFoundError:
        raise NFAFileNotFoundError(f"NFA input file not found in current directory {os.getcwd()}") 
    
    
nfa = automaton.parseFile(inputNfaFile)
inputNfaFile.close()
# automaton.printNfaDataStructures(nfa)
# print()
inputString = inputStringFile.read()
inputStringFile.close()

if automaton.runNfa(nfa, inputString, stringSeparator, allowVerbosity) == True:
    print("Accepted")
else:
    print("Rejected")

# automaton.generateDefinitionNFAFile(nfa)
# automaton.convertNFAtoDFA(nfa)
# automaton.generateDefinitionNFAFile(nfa)