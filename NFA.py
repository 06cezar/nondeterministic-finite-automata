# NFA stands for nondeterministic finite automaton  
# M is a 5-tuple, (Q, Σ, δ, q0, F), consisting of:  
# a finite set of states Q  
# a finite set of input symbols called the alphabet Σ  
# a transition function δ : Q × Σ → P(Q), where P(Q) is the power set of Q  
# an initial (or start) state q0 ∈ Q  
# a set of accepting (or final) states F ⊆ Q  

class NFAError(Exception): # exception is a class that all built-in Python errors (like ValueError, TypeError) inherit from.
    pass                   # defining a custom error that behaves like a normal Python exception with subclasses that 
                           # help categorize different types of NFA errors

class UndefinedStartStateError(NFAError):
    # raised when the NFA doesn't have a start state
    pass

class UndefinedAcceptStatesError(NFAError):
    # raised when the nFA doesn't have any accept states
    pass

class UndefinedAlphabetError(NFAError):
    # raised when the nFA doesn't have an alphabet
    pass
class InvalidStateError(NFAError):
    # raised when an invalid/undefined state is encountered.
    pass

class InvalidSymbolError(NFAError):
    # raised when an invalid/undefined symbol is encountered.
    pass

class EpsilonTransitionError(NFAError):
    # raised when you find
    pass 

class InputStringError(Exception):
    # raised when there isn't an error with the NFA, but with the input string fed into it (it contains characters not present in the NFA's alphabet)
    pass

# duplicate rule error seen in NFA's no longer found - the NFA transition function allow for multiple destination states for the same source state and symbol

def isComment(string):
    return string.startswith("#")
    # return string[0] == "#" would raise an IndexError for an empty string ""

def stringWithoutComments(string):
    return string[0 : string.index("#")] # does not raise an exception, as function is only called 
                                         # when character "#" exists in the string, and everything after
                                         # the first "#" shouldn't be processed
def isEmptyLine(string):
    return string == ""

def fixUtf8Corruption(possiblyCorruptedString):
    try:
        # attempt to fix the corrupted string:
        # 1. first, interpret the string as if it were encoded in Latin-1 (a single-byte encoding).
        # 2. then, decode it properly as UTF-8 (which may fix misinterpreted characters).
        # example: 'Îµ' (Windows-1252 corruption) should become 'ε' (UTF-8 character).
        return possiblyCorruptedString.encode("latin1").decode("utf-8") 
        # if any error is found exception will be caught and return clause will not be triggered
    
    except (UnicodeEncodeError, UnicodeDecodeError):
        # if either encoding or decoding fails:
        # - an UnicodeEncodeError could occur if the string can't be encoded to Latin-1.
        # - an UnicodeDecodeError could occur if the byte sequence can't be decoded to UTF-8.
        # in either case, the string is returned as it is (uncorrupted or irreparably corrupted).
        return possiblyCorruptedString  # return the original string if no fix was possible

def parseFile(inputNfaFile):
    lines = inputNfaFile.readlines()
    currentSection = "None"
    states = []
    sigma = [] # sigma = alphabet
    rules = {} # rules[sourceState] = {symbol : destinationState}
               # tules[sourceState][symbol] = destinationState
    start = "None" # a nfa can only have one start state
    accept = [] # a nfa can have multiple accept states
    inMultipleLineComment = False # boolean variable to allow multiple line comments starting with /* and ending with */
                               # is true if we are currently inside a multi line comment and we need to skip all lines until */
    for line in lines:
        line = line.strip() # eliminating whitespace
        
        # continue statements go to next iteration (next line) and are used for readability purposes,
        # could be replaced by elif statements
        
        if isComment(line) or isEmptyLine(line):
            continue # skipping lines that are comments
            
        if "#" in line: # filtering lines that contain comments
            line = stringWithoutComments(line) # only text before the comment is processed 
            line = line.strip() # eliminating possible whitespace before first "#" character
            
        if not inMultipleLineComment:
            
            if "/*" in line:
                
                inMultipleLineComment = True # we are inside a multiple line comment
                # even though we are now in a multiple line comment, it can still be used as a one-liner
                # and this needs to be checked
                multipleLineCommentStartIndex = line.find("/*") # gives the position of the first comment opener
                
                if "*/" in line:

                    multipleLineCommentLastStartIndex = line.rfind("/*") # more /* can be used in a line, checks for the last one
                    multipleLineCommentLastEndIndex = line.rfind("*/") # gives the position of the last ending comment symbol
                    
                    if multipleLineCommentLastStartIndex < multipleLineCommentLastEndIndex:
                        # then this is actually a one liner comment
                        inMultipleLineComment = False
                        line = line[:multipleLineCommentStartIndex] + line[multipleLineCommentLastEndIndex + 2:] # concatenates string before the comment and after the comment
                        line = line.strip()
                        # checks if there is anything to parse before and after the comment
                        
                else:   # not a one-liner comment - only need to check before the /* 
                    
                    line = line[:multipleLineCommentStartIndex] # checks if there is anything to parse before the comment
                    line = line.strip()
                    
                if isEmptyLine(line):
                    continue
            
            
            
        elif inMultipleLineComment: # this means that it's not the first line in the comment
                                    # elif statement ensures that the parser won't skip lines that are before the start of a multiple line comment
                                    # for example, q1, 1, q0 /* some text - would be skipped by the continue statement if not for the elif statement
            if "*/" in line:
                
                multipleLineCommentEndIndex = line.rfind("*/")
                line = line[multipleLineCommentEndIndex + 2:] # the string after the */ (is not a comment)
                inMultipleLineComment = False
                line = line.strip()
                if isEmptyLine(line):
                    continue
                
            else:
                continue # skip line that is completely within the multiple line comment
        
        if line[0] == "[": # new section starts here, filtering opening and closing pharantesis
            currentSection = line[1:-1]
            continue
        if line == "End":
            currentSection = "None" # searching for new section tag ([SectionName])
            continue
        
        if currentSection == "None":
            continue # skipping line, still searching for section tags ([SectionName])
        if currentSection == "States":
            states.append(line) 
            continue
        if currentSection == "Sigma":
            sigma.append(line)
            continue 
        if currentSection == "Rules":
            sourceState, symbol, destinationState = line.split(",")
            sourceState = sourceState.strip()
            symbol = symbol.strip() 
            symbol = fixUtf8Corruption(symbol) # fixing any possible corruption that can be caused by file in different encoding from utf-8
            destinationState = destinationState.strip()
            if sourceState not in rules:        
                rules[sourceState] = {} # initialising with a hashmap
                
                                                                      # a transition function 
                                                                      # δ  :  Q    ×   Σ    →  P(Q)
                                                                      #     srcSt    symbol  destStates
            if symbol == "ε" or symbol.lower() == "epsilon":
                symbol = "epsilon" # will be the symbol present in the dictionary for all epsilon transitions
                                   # ε looks prettier and more formal - but some older text editors without UTF-8 or 
                                   # with weirder font styles may not display it correctly
                                   # or make it too similar with an 'e'
                                                                                             
            if symbol not in rules[sourceState]:
                rules[sourceState][symbol] = set() # initialising with a set

            rules[sourceState][symbol].add(destinationState) # updating the hashset
        if currentSection == "Start":
            start = line
            continue
        if currentSection == "Accept":
            accept.append(line)
            continue

    inputNfaFile.close()
    
    NFA = states, sigma, rules, start, accept
    if not isNfaValid(NFA):
        return False 
    else:
        # returning 5-tuple
        return NFA
    
def isNfaValid(NFA):
    states, sigma, rules, start, accept = NFA # getting values from 5-tuple
    if len(sigma) == 0:
        raise UndefinedAlphabetError("Alphabet is not defined")
        return False
    
    if start == "None":
        raise UndefinedStartStateError("Start state is not defined")
        return False 
    
    elif start not in states:
        raise InvalidStateError(f"Start state {start} is not defined")
        return False
    
    if accept == []:
        raise UndefinedAcceptStatesError("Accept state is not defined")
        return False 
    
    else:
        for acceptState in accept:
            if acceptState not in states:
                raise InvalidStateError(f"Accept state {acceptState} is not defined")
                return False
            
            
    for sourceState in rules: # rules dict key is the source state of the rule
    
        if sourceState not in states:
            raise InvalidStateError(f"Source state {sourceState} is not defined in the states list for the NFA")
            return False
        
        for symbol in rules[sourceState]:
            if symbol not in sigma and symbol not in ["epsilon", "ε"]: # epsilon doesn't need to be defined in the alphabet
                raise InvalidSymbolError(f"Symbol {symbol} is not defined in the alphabet for the NFA")
                return False
            elif symbol in ["epsilon", "ε"] and symbol in sigma:
                raise EpsilonTransitionError("Epsilon doesn't need to be defined in the alphabet for the NFA (it includes it by default). You can use 'epsilon' or 'ε' in your rules without defining epsilon or ε.")
            
            # for destinationState in rules[sourceState][symbol]: not for, as there is only one destinationState, this for would split the destinationState
            # string character by character
            for destinationState in list(rules[sourceState][symbol]): # all possible destination states from that source state, symbol tuple
                if destinationState not in states:
                    raise InvalidStateError(f"Destination state {destinationState} {rules} is not defined in the states list for the NFA")
                    # print(sourceState, symbol, destinationState)
                    return False
                    # traverses all rules in the dictionary, looking for source states, destination states and symbols
    return True

def printNfaDataStructures(NFA):
    states, sigma, rules, start, accept = NFA # getting values from 5-tuple

    print(f"States : {states}")
    print(f"Alphabet : {sigma}")
    print(f"Rules : {rules}")
    print(f"Start state : {start}")

    if len(accept) != 1:
        print(f"Accept states : {accept}") 
    else:
        print(f"Accept state: {accept[0]}") # to show singular form if needed and not a list with only one element

def isStringValid(string, stringSeparator, sigma):
    # searches if any element in the string is not included in the alphabet
    for symbol in splitIncludingNoSeparator(string, stringSeparator):
        if symbol not in sigma:
            return False
    return True

def getNextStates(currentState, currentSymbol, rules):
    if currentState not in rules:
        return set([currentState]) # considered by default for every state, if a rule is not specified, the NFA stays in the same state
                                   # here we have no rule with the source state = the current state of the NFA
    elif currentSymbol not in rules[currentState]:
        return set([currentState]) # same case, but in the NFA we have a rule defined with the current state as the source state
                                   # but no rule with the corresponding symbol, so we stay in the same state (by convention)
    else:
        return rules[currentState][currentSymbol] # the NFA goes to the states specified by the rule
        # function returns a set
    
def splitIncludingNoSeparator(string, separator):
    if separator == "" : # if not for this function, ValueError: empty separator
        return string    # would need an if-else statement within the runnfa function
    else:                # removes redudant code, by calling getNextStates only once
        return string.split(separator)
# def onlyEpsilonTransitions(state, rules):

def getEpsilonStatesSetMaxDepth(epsilonDepth1StatesSet, rules):
    epsilonStates = set() # set of states reached with epsilon transitions - without consuming any input symbol
    epsilonStates.update(epsilonDepth1StatesSet) # initialise it with the epsilon states with depth = 1 from current states
    addedEpsilonState = True
    while addedEpsilonState:
        addedEpsilonState = False # at first while loop when no new epsilon transition state is added, it means we have reached all possible states
                                  # with any depth of epsilon transition at this iteration, so we can exit this loop
        newEpsilonStates = set()  # epsilon states reached in the last iteration
        for state in epsilonStates:
            if state in rules and 'epsilon' in rules[state]:
                newEpsilonStates.update(rules[state]['epsilon']) # adding epsilon transitions first - by using sets we allow no duplicates

        newStates = newEpsilonStates - epsilonStates
        if newStates: # is not an empty set - we have added a new state from the previous iteration, we need 
                      # to continue searching for posible new states reached from epsilon transitions
            epsilonStates.update(newStates) # update the main set
            addedEpsilonState = True
        epsilonStates.update(newEpsilonStates)
    return epsilonStates
# currentStates.update(newEpsilonStates) # when reaching a possible epsilon transition, the NFA branch can either take it or not
                                                    # in this set we will have all the branches - with epsilon transitions and without
def runNfa(NFA, inputString, stringSeparator, printNFASteps = True):

    states, sigma, rules, start, accept = NFA  # unpack the NFA

    # NFA validity is looked upon when processing the file
    # if the functions are arranged in different files/modules, code like this is preferrable
    if not isNfaValid(NFA):
        raise NFAError("NFA not valid")
    
    inputString = inputString.strip() # removes whitespace, \n, from left and right
    if not isStringValid(inputString, stringSeparator, sigma):
        raise InputStringError("Input string contains symbols not in the given alphabet of the NFA")
    
    
    currentStates = {start} # first state is the start state of the NFA
    if printNFASteps == True: 
        # printNFASteps - boolean parameter - if it is true all the states and symbols the NFA encounters
        # will be printed to the screen - if not, only if the input string is valid will be printed to the screen
        print(currentStates) # printing starting state
    
    for currentSymbol in splitIncludingNoSeparator(inputString, stringSeparator):
            if printNFASteps == True:
                print(currentSymbol) # printing every symbol in the string

            nextStates = set()
            epsilonDepth1States = set()
            for state in currentStates:
                if state in rules and 'epsilon' in rules[state]:
                    epsilonDepth1States.update(rules[state]['epsilon']) # adding epsilon transitions first - by using sets we allow no duplicates
            
            epsilonStates = getEpsilonStatesSetMaxDepth(epsilonDepth1States, rules)
            currentStates.update(epsilonStates) # when reaching a possible epsilon transition, the NFA branch can either take it or not
                                                # in this set we will have all the branches - with epsilon transitions and without

            for state in currentStates: # now we can iterate across all possible current states, including the epsilon paths
                destinationStates = getNextStates(state, currentSymbol, rules) # all destination states for one of the current possible states
                nextStates.update(destinationStates)
            # function searches through the rules and finds the correct one 
            # improved time efficiency wise by using two hashmaps - dictionaries, for O(1) search time
            currentStates = nextStates
            if printNFASteps == True:
                print(currentStates)  # printing the new state of the NFA after every symbol

    epsilonStates = getEpsilonStatesSetMaxDepth(currentStates, rules) # seperate check needed for states after last symbol from the input string is set
    currentStates.update(epsilonStates)
    if printNFASteps == True:
        print(currentStates, "<- all final states after final epsilon transition search")
    for endState in currentStates: # after the for loop exits the currentStates variable stores the last states 
        if endState in accept: # of the NFA, if one state in it is valid return true
            return True
    
    return False # if all final states are rejected

def getSortedSetString(statesSubset):
    if not statesSubset: # empty set
        return fixUtf8Corruption("∅") 
    
    statesList = list(statesSubset)
    statesList.sort() 

    sortedSetString = "{"
    for state in statesList[:-1]: # adding all set elements except last one
        sortedSetString += state + ", "
    sortedSetString += statesList[-1] + "}" # adding last set element
    return sortedSetString

def getPowerSet(states): # by using bitwise operators method
    powerSet = [] 
    n = len(states)
    # iterate through all numbers from 0 to 2^n - 1
    for i in range(1 << n):  # 1 << n is the same as 2**n
        subset = {states[j] for j in range(n) if (i & (1 << j)) > 0}  # select elements where the j-th bit is 1 
                                                                      # (indicating that the j-th element of Q should be in the subset).\
        # example: - 3 states
        # 000 - empty set
        # 001 - first element is in the set
        # ...
        # 100 - third element is in the set
        # 101 - first and third element are in the set
        # 111 - all elements are in the set
        # bits in binary numbers are read from right to left - so the first bit is the one in the most right
        #         
        powerSet.append(subset)
    return powerSet
'''
def addIdentifierToStates(states, identifier):
    modifiedStates = []
    for state in states:
        modifiedStates.append(state + identifier)
    return modifiedStates

def addIdentifierToRules(rules, identifier):
    # this function will modify the sourceState and destinationState by adding identifiers
    modifiedRules = {}
    for sourceState in rules:
        modifiedRules[sourceState + identifier] = {}  # Add identifier to the source state
        for symbol in rules[sourceState]:
            modifiedRules[sourceState + identifier][symbol] = set()

            # Add identifier to the destination states
            for destinationState in rules[sourceState][symbol]:
                modifiedRules[sourceState + identifier][symbol].add(destinationState + identifier)

    return modifiedRules

    for sourceState in rules:
        modifiedRules[sourceState + identifier] = {} # add the identifier to the source states
        for symbol in rules[sourceState]:
            modifiedRules[sourceState + identifier][symbol] = set()
            
            # add the identifier to the destination states
            for destinationState in rules[sourceState][symbol]:
                modifiedRules[sourceState + identifier][symbol].add(destinationState + identifier)

    return modifiedRules

def union(NFA1, NFA2):
    # performs the union operation to 2 NFAs that are equivalent to 2 regular expressions
    states1, sigma1, rules1, start1, accept1 = NFA1
    states2, sigma2, rules2, start2, accept2 = NFA2 
    
    for stateIndex in range(len(states1)):
        states1[stateIndex] += "_1" # adding identifier to end of state name
    for stateIndex in range(len(states2)):
        states2[stateIndex] += "_2" # adding identifier to end of state name
    for sourceState in rules:
        for symbol in rules[sourceState]:
            for destinationState in list(rules[sourceState][symbol]):

    states1 = addIdentifierToStates(states1, "_1")
    states2 = addIdentifierToStates(states2, "_2")
    rules1 = addIdentifierToRules(rules1, "_1")
    rules2 = addIdentifierToRules(rules2, "_2")
    unionStates = states1 + states2 + ["0"]
    unionSigma = set(sigma1).update(set(sigma2))
    unionSigma = list(unionSigma) 
    unionRules = rules1 
    unionRules.update(rules2) # merging 2 hashmaps
    newEpsilonRules = {"0": {"epsilon" : set([start1 + "_1", start2 + "_1"]) } }
    unionRules.update(newEpsilonRules)
    accept1 = 
    unionAccept =
    unionStart = "0"
    unionNFA = (unionStates, unionSigma, unionRules, unionStart, unionAccept)
    return unionNFA



# getCurrentState - modularitate cod - enter next move
# editor harti joc
#     
def concatenation(NFA1, NFA2):
    # concatenates 2 NFAs that are equivalent to 2 regular expressions

def star(NFA):
    # performs the star operation on a NFA - equivalent to a regular expression

def convertRegextoNFA(regularExpression):
    # regular expression will contain paranthesis, unions, concatenations and star operations




def convertNFAtoDFA(NFA): # using powerset construction
    states, sigma, rules, start, accept = NFA # getting values from 5-tuple
    # first of all we will compute the start state for the new DFA, which will be the subset
    # formed by the previous start state and all the epsilon transitions from it
    startSet = set([start]) # set containing just the NFA’s start state - the getEpsilonStatesSetMaxDepth function requires a set as it's first argument
    epsilonTransitionsFromStartState = getEpsilonStatesSetMaxDepth(startSet, rules) 
    print(getSortedSetString(epsilonTransitionsFromStartState))
    DFAStates = []
    powerSet = getPowerSet(states)
    for subset in powerSet:
        DFAStates.append(getSortedSetString(subset))
        print(getSortedSetString(subset))
'''
def generateDefinitionNFAFile(NFA, file_name="nfa_definition.txt"):
    states, sigma, rules, start, accept = NFA  # unpack the NFA components
    
    # open the file in write mode - does NOT raise an error if file does not exist - it creates the file!
    # if the file exists - it overwrites the file contents
    with open(file_name, "w") as file:

        file.write("[States]\n")
        for state in states:
            file.write(f"{state}\n")
        file.write("End\n\n")
        

        file.write("[Sigma]\n")
        for symbol in sigma:
            file.write(f"{symbol}\n")
        file.write("End\n\n")
        

        file.write("[Rules]\n")
        for sourceState in rules:
            for symbol in rules[sourceState]:
                for destinationState in rules[sourceState][symbol]:
                    # write each transition in the format "q0, epsilon, q1"
                    file.write(f"{sourceState}, {symbol}, {destinationState}\n")
        file.write("End\n\n")
        
        file.write("[Start]\n")
        file.write(f"{start}\n")
        file.write("End\n\n")
        
        file.write("[Accept]\n")
        for acceptState in accept:
            file.write(f"{acceptState}\n")
        file.write("End\n")

    print(f"NFA definition written to {file_name}")
 
