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

class BadUserInputError(Exception):
    pass

def getDifficulty():
    level = input("Please choose your difficulty:\n(1) Novice\n(2) Advanced\n(3) Expert\n(4) Master\n(5) Impossible\n")
    if level.isdigit():
        if 1 <= int(level) <= 5:
            return int(level)
        else:
            print("Choice out of range, please select again.\n")
            getDifficulty()
    else:
        print("Please input the number only.\n")
        getDifficulty()

# Accepts number from getDifficulty to determine how long the words should be.
def getWords(x):
    allWords = []
    wordstoPrint = []
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
        wordstoPrint.append(newtemp)
        allWords.remove(temp)
        count += 1

    # print("\nWords to be printed in field: ", wordstoPrint)
    return wordstoPrint, wordLen

# Selects the password from the randomly generated list
def getPassword(list):
    password = random.choice(list[0])
    return str(password)

def generateString(wordList):
    characters = ['(',')','{','}','[',']','!','?','^','&',';',':','%','/','\\']
    tempList = []
    characterCount = wordList[1]*16
    numRandomCharacters = 384 - characterCount - 1

    tempList = wordList[0]
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
            if len(item) == wordList[1] & len(tempList[index-1]) == wordList[1]:
                random.shuffle(tempList)
            else:
                adjacent = False
        
    tempString = ''.join(tempList)
    finalString = tempString
    

    return finalString


def updatePlayField(playData):
    
    # Split the input string into 32 lists of 12 items each
    chunks = [playData[x:x + 12] for x in range(0, len(playData), 12)]

    chunkLeft = chunks[:15]
    chunkRight = chunks[16:]

    for i in range(15):
        left_formatted = ''.join([f"{item:^3}" for item in chunkLeft[i]])
        right_formatted = ''.join([f"{item:^3}" for item in chunkRight[i]])
        print(f"{left_formatted}    {right_formatted}")

# selecting "(...)", "{...}", or "[...]" will remove one random non-password word from the field and updatePlayField()
def removeDud():
    return

# selecting "<...>" in a single section will reset attempts back to 5
def resetAttempts():
    return



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
    return attempt

def game():
    attempts = 4
    difficulty = getDifficulty()
    wordList = getWords(difficulty)
    password = getPassword(wordList)
    print("The password for this game is: ", password, '\n')
    
    baseString = generateString(wordList)
    # print(baseString)
    # print('')
    updatePlayField(baseString)
    while attempts > 0:
        attempt = getAttempt()
        test = getLikeness(password, attempt)
        if test == wordList[1]:
            print("SUCCESSFUL. WELL DONE.")
            exit()
        else:
            print("ENTRY DENIED.\nLikeness: ", test)
            attempts -= 1
    print("OUT OF ATTEMPTS. PROGRAM TERMINATED.")
    exit()


game()



