import random

# This CLI program should mimic the hacking minigame from the Fallout series. 
#
# It will be displayed in 2 columns of height 16 (32 total lines) in lines of 12 characters (total 32 * 12 = 384 characters),
# and consist of 16 words of a defined length placed randomly, with one of the words acting as the password (correct answer). 
# The player will have 4 guesses.
# Each time the user makes a guess, if the guess is incorrect, the guessed word should be removed and replaced with '.' characters. 
# Additionally, the user will be presented with a 'likeness score', which will show how many letters are in the correct position. 
# (Maybe on easier difficulties, the score should include 2 scores, correct letters in the correct and incorrect positions.)
# If the word is correct, the player wins and is presented the option to play again. 

# Besides the words, the playfield will be filled with random characters. If parentheses, curly or square brackets are
# within a single line in the correct order (enclosing something with their partner), the player should be able to select it, and
# 1 incorrect answer is removed. 
# Similarly, if <> is selected, the attempt counter is reset. 



# note: previously failed attempts show back up on the playfield
startNum= random.randint(256, 4095)
characters = ['(',')','{','}','[',']','!','?','^','&',';',':','%','/','<','>']
wordsList = []
baseString = ''
wordLen = 0
errorMessage = "Invalid input. Please try again."
coordinateList = []

class BadUserInputError(Exception):
    pass

def getDifficulty():
    level = input("Please choose your difficulty:\n(1) Novice\n(2) Advanced\n(3) Expert\n(4) Master\n(5) Impossible\n>")
    if level.isdigit():
        if 1 <= int(level) <= 5:
            return int(level)
        else:
            print("Choice out of range, please select again.\n")
            return getDifficulty()  # Return the result of the recursive call
    else:
        print("Please input the number only.\n")
        return getDifficulty()  # Return the result of the recursive call


# Accepts number from getDifficulty to determine how long the words should be.
def getWords(x):
    global wordsList
    allWords = []
    try:
        word = open('words.txt', 'r')
    except FileNotFoundError:
        print("The 'words.txt' file was not found.")

    match x:
        case 1:
            wordLen = random.choice([4,5])
        case 2:
            wordLen = random.choice([6,7])
        case 3:
            wordLen = random.choice([8,9])
        case 4:
            wordLen = random.choice([9,10])
        case 5:
            wordLen = random.choice([11,12])
        # case _: 
        #     raise BadUserInputError("Something went wrong with the difficulty setting.")
    # print("Your word length is: ", wordLen)
    # makes local list of all applicable words
    for i in word:
        if len(i) == (wordLen+1):
            allWords.append(i)
    
    # print("\nAll possible words: ", allWords, '\n')

    # selects 16 words randomly
    count = 0
    while count <= 15:
        temp = random.choice(allWords)
        newtemp = temp[:-1].upper()
        wordsList.append(newtemp)
        allWords.remove(temp)
        count += 1

    # print("\nWords to be printed in field: ", wordstoPrint)
    return wordLen

# Selects the password from the randomly generated list
def getPassword(list):
    password = random.choice(list)
    return str(password)

def generateString(wordList, wordLen):
    global characters
    tempList = []
    characterCount = wordLen*16
    numRandomCharacters = 384 - characterCount - 1

    tempList = wordList[:]
    count = 0
    # ensures that the first character is always a non-word. This will help in the adjacency test during shuffling.
    tempList.insert(0, random.choice(characters))
    while count < numRandomCharacters:
        tempList.append(random.choice(characters))
        count += 1
    
    # test for word adjacency
    # this section needs rethinking in the morning
    adjacent = True
    while adjacent:
        for index, item in enumerate(tempList):
            if len(item) == wordLen & len(tempList[index-1]) == wordLen:
                random.shuffle(tempList)
            else:
                adjacent = False
        
    tempString = ''.join(tempList)
    baseString = tempString
    

    return baseString

def splitString(baseString):
    chunks = [baseString[x:x + 12] for x in range(0, len(baseString), 12)]
    return chunks

def updatePlayField(baseString):
    
    # Split the input string into 32 lists of 12 items each
    chunks = splitString(baseString)
    chunkLeft = chunks[:16]
    chunkRight = chunks[16:]

    global startNum 
    columnID = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

    print("     ", end="")
    for identifier in columnID:
        print(f"{identifier:^3}", end="",)
    print("        ", end="")
    for identifier in columnID:
        print(f"{identifier:^3}", end="")
    print('\n')

    for i in range(16):
        left_formatted = ''.join([f"{item:^3}" for item in chunkLeft[i]])
        right_formatted = ''.join([f"{item:^3}" for item in chunkRight[i]])
        print(f"{hex(startNum + i)[2:].upper().zfill(2)}: {left_formatted}    {hex(startNum + i + 16)[2:].upper().zfill(2)}:{right_formatted}")

# replaces list item with period. To be used for incorrect guesses and removing duds.
def replace(word, baseString):
    if word in baseString:
        updatedString = baseString.replace(word, '.'*len(word))

    return updatedString

# selecting "(...)", "{...}", or "[...]" will remove one random non-password word from the field and updatePlayField()
def getDud(password, wordList):
    dud = password
    while dud == password:
        dud = random.choice(wordList)
    print(dud)
    return dud


def getChar(coordinate, baseString):
    global coordinateList
    column_identifiers = ['A','B','C','D','E','F','G','H','I','J','K','L']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    row_identifiers = [hex(i+startNum)[2:].upper().zfill(2) for i in range(32)]

    try:
        columnID = coordinate[3]
        rowID = coordinate[:3]

        if rowID not in row_identifiers or columnID not in column_identifiers:
            return 0

        # Convert rowID to an index
        row_index = row_identifiers.index(rowID)

        # Convert columnID to an index
        column_index = column_identifiers.index(columnID)

        # Split the input string into 32 lists of 12 items each
        chunks = splitString(baseString)

        # Extract the character at the specified coordinates
        chunk = chunks[row_index]
        character = chunks[row_index][column_index]

        if coordinate in coordinateList:
            return 4

        # Check if the character is an opening bracket and if there's a corresponding closing bracket in the same chunk
        elif character in '([{':
            if character == '(':
                closing_bracket = ')'
            elif character == '[':
                closing_bracket = ']'
            elif character == '{':
                closing_bracket = '}'
            else:
                closing_bracket = None

            # Iterate through the characters in the chunk
            for char in chunk[column_index:]:
                if char == closing_bracket:
                    coordinateList.append(coordinate)
                    return 1

        # Check if the character is an angle bracket and if there's a corresponding angle bracket in the same chunk
        elif character == '<':
            closing_bracket = '>'
            for char in chunk[column_index:]:
                if char == closing_bracket:
                    coordinateList.append(coordinate)
                    return 2

        # Check if the character is a lowercase alphabet letter
        elif character in alphabet.upper():
            return 3

        return 0  # Default case: Invalid input
    except Exception as e:
        raise BadUserInputError(str(e))

    


# accepts the correct word and the user attempt, outputs int  that represents number of letters in the correct place
def getLikeness(password, attempt):
    attempt = attempt.upper()
    count = 0
    for letters in zip(password, attempt):
        if letters[0] == letters[1]:
            count +=1
    return count

# User inputs either word or coordinate. If word is spelled incorrectly, 1 attempt is removed. 
# If coordinate is used, incorrect words will result in penalty: 1 attempt. 
# Coordinates that do not point to words will be tested for parentheses/brackets.
# Coordinates that lead to other characters (or brackets that don't close) will result in a thrown error.
def getAttempt():
    attempt = input(">")
    return attempt.upper()

def game():
    global baseString
    global wordsList
    global wordLen
    attempts = 4
    difficulty = getDifficulty()
    wordData = getWords(difficulty)
    wordLen += wordData
    password = getPassword(wordsList)
    # print("The password for this game is: ", password, '\n')
    wordsListTemp = wordsList
    
    baseString = generateString(wordsListTemp, wordLen)
    print('')
    print("Password Length: ", wordLen)
    print("Type \"--help\" at any time for instructions.\n")
    updatePlayField(baseString)
    while attempts > 0:
        attempt = getAttempt()
        test = getLikeness(password, attempt)
        if test == wordLen:
            print("SUCCESSFUL. WELL DONE.")
            exit()
        elif attempt == "--HELP":
            print("Instructions: \nType a word from the grid. Your attempt will be evaluated, and the number of letters \nin the correct position will be reported.")
            print("Remove an incorrect word by typing the coordinates of an opening parentheses, square \nor curly brackets which has an enclosing partner in the same section.")
            print("Reset your attempts by typing the coordinates of an opening angle bracket with \nan enclosing partner in the same section")
            print("You have ", attempts, " remaining attempts.\n")
        else:
            try:
                if attempt in wordsList:
                    attempts -= 1
                    baseString = replace(attempt, baseString)
                    updatePlayField(baseString)
                    wordsList.remove(attempt)
                    print("ENTRY DENIED.\nAttempts Remaining: ", attempts)
                    print("Likeness: ", test)
                elif attempt not in wordsList:
                    x = getChar(attempt, baseString)
                    match x:
                        case 0:             #coordinates lead to nothing and/or unclosed bracket
                            raise BadUserInputError(errorMessage)
                        case 1:             #coordinates lead to closed parentheses, square or squigly brackets -> dud removed
                            print("Removing dud...")
                            dud = getDud(password, wordsList)        #problem here <- wordlist is transformed somewhere into list of characters + words
                            print(dud)
                            wordsList.remove(dud)
                            baseString = replace(dud, baseString)
                            updatePlayField(baseString)
                        case 2:             #coordinates lead to angle brackets -> attempts reset
                            attempts = 4
                            print("Attempts reset to 4.")
                        case 3:             #coordinates lead to letter -> attempt check... on second thoughts I couldn't be bothered right now
                            print("Please type the word.")
                        case 4:             #User has already used parentheses set
                            print("Duplicate coordinates detected. Operation failure.")

                else:
                    raise BadUserInputError(errorMessage)
            except BadUserInputError as e:
                print(e)
    print("OUT OF ATTEMPTS. PROGRAM TERMINATED.")
    exit()

game()
