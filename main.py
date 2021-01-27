import random
#import time

print("\n")

def game():
    points = 0
    shufword = nineLettersBoard()
    print(shufword)
    print(printBoard(box(shufword.copy())))
    print("If you need to see the board again, please type \"reprint board\" and press enter. "
          "If you wish to end the game, please type \"end game\" and press enter. Please have fun."
          "It is mandatory.")
    print("Please type a word using the letters in the grid: \n")
    count = 5
    attempted_words = []
    while count > 0:
        attempt = guess()
        if attempt == "reprint board":
            print(printBoard(box(shufword.copy())))
        elif attempt == "end game":
            break
        elif attempt in attempted_words:
            print("You have already guessed that word. Please try again.")
        elif check1(shufword.copy(), attempt) and check2(attempt):
            print("Correct!")
            points += len(attempt)
            attempted_words.append(attempt)
        else:
            count -= 1
    print("Your score: ", points)


def box(a):
    boxes = []
    for i in range(3):
        row = []
        for j in range(3):
            x = a.pop()
            row.append(x)
        boxes.append(row)
    return boxes

def printBoard(boxes):
    to_print = ""
    to_print += " " + boxes[0][0] + " | " + boxes[0][1] + " | " + boxes[0][2] + " \n"
    to_print += "---+---+---\n"
    to_print += " " + boxes[1][0] + " | " + boxes[1][1] + " | " + boxes[1][2] + " \n"
    to_print += "---+---+---\n"
    to_print += " " + boxes[2][0] + " | " + boxes[2][1] + " | " + boxes[2][2] + " \n"

    return to_print


def nineLettersList():
    word = open('words.txt', 'r')
    list = open('list.txt', 'w')
    for line in word:
        if len(line) == 10:
            print(line)
            list.write(line)
    word.close()
    list.close()


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
      if random.randrange(num): continue
      line = aline
    return line

def split(s):
    return [char for char in s]


def countlines():
    list = open('list.txt', 'r')
    count = 0
    for line in list:
        line.strip('\n')
        count += 1
    return count

def nineLettersBoard():
    x = open('list.txt', "r")
    y = random_line(x)
    x.close()
    word = split(y)[:-1]
    print(y)
    shufword = random.sample(word, len(word))
    return shufword


def guess():
    attempt = str(input())
    return attempt.lower()

def check1(shufword, attempt):
    x = attempt
    y = split(x)
    #print(y, type(y))
    count = 0
    while count != 9:
        for i in y:
            for j in shufword:
                try:
                    if i == j:
                        y.remove(i)
                        shufword.remove(j)
                except ValueError:
                    print("VE")
                    continue
        count += 1
    if len(y) != 0:
        print("Please use only the characters in the grid.")
        return False
    else:
        return True


def check2(attempt):
    x = open('words.txt', 'r')
    #print(attempt)
    for line in x:
        word = line.strip()
        #print(word)
        if word == attempt:
            x.close()
            return True
    return False


game()

