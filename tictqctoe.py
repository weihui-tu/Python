import math
import random

size = 4


def myTicTacToe(grille, monSymbole):
    # x = int(input('please enter the row number:'))
    # y = int(input('please enter the column number:'))
    # check lines
    for i in range(4):
        sum = 0
        for j in range(4):
            sum = sum + grille[i][j]
        if sum == -3:
            for j in range(4):
                if grille[i][j] == 0:
                    return (i, j)
    # check columns
    for i in range(4):
        sum = 0
        for j in range(4):
            sum = sum + grille[j][i]
        if sum == -3:
            for j in range(4):
                if grille[j][i] == 0:
                    return (j, i)
    # check diags
    sum = 0
    for i in range(4):
        sum = sum + grille[i][i]
    if sum == -3:
        for i in range(4):
            if grille[i][i] == 0:
                return (i, i)
    sum = 0
    for i in range(4):
        sum = sum + grille[i][3 - i]
    if sum == -3:
        for i in range(4):
            if grille[3 - i][i] == 0:
                return (3 - i, i)
    # check squares
    sum = 0
    for i in range(2):
        for j in range(2):
            sum = grille[i][j] + grille[i][j + 1] + grille[i + 1][j] + grille[i + 1][j + 1]
            if sum == -3:
                if grille[i][j] == 0:
                    return (i, j)
                elif grille[i][j + 1] == 0:
                    return (i, j + 1)
                elif grille[i + 1][j] == 0:
                    return (i + 1, j)
                elif grille[i + 1][j + 1] == 0:
                    return (i + 1, j + 1)
    # if grille[3-m][3-n]==0:
    #     return (3-m,3-n)
    # else:
    ini_distance = 10
    pre_j = pre_i = 4
    for i in range(1, 3):
        for j in range(1, 3):
            distance = abs((i + j) - (m + n))
            if distance < ini_distance and grille[i][j] == 0:
                ini_distance = distance
                pre_i, pre_j = i, j
    if not (pre_i == 4 and pre_j == 4):
        return pre_i, pre_j
    if grille[0][0] == 0:
        return (0, 0)
    if grille[0][3] == 0:
        return (0, 3)
    if grille[3][0] == 0:
        return (3, 0)
    if grille[3][3] == 0:
        return (3, 3)
    for i in range(4):
        for j in range(4):
            if grille[i][j] == 0:
                return (i, j)
                # return (x, y)


def check(tab):
    global sum
    sum = 0
    motif = 0

    global finished
    finished = False
    global winner
    winner = -1

    # check lines
    for i in range(0, 4):
        sum = 0
        for j in range(0, 4):
            sum = sum + tab[i][j]
        # print("lines" + str(sum))
        if math.fabs(sum) == 4:
            motif = sum

    # check columns
    for i in range(0, 4):
        sum = 0
        for j in range(0, 4):
            sum = sum + tab[j][i]
        # print("columns" + str(sum))
        if math.fabs(sum) == 4:
            motif = sum

    # check diags
    sum = 0
    for j in range(0, 4):
        sum = sum + tab[j][j]
    if math.fabs(sum) == 4:
        motif = sum

    sum = 0
    for j in range(0, 4):
        sum = sum + tab[j][3 - j]
    if math.fabs(sum) == 4:
        motif = sum

    # check squares
    for i in range(0, 2):
        for j in range(0, 2):
            sum = tab[i][j] + tab[i + 1][j] + tab[i][j + 1] + tab[i + 1][j + 1]
            if math.fabs(sum) == 4:
                motif = sum

    if motif == 4:
        finished = True
        winner = 1
    elif motif == -4:
        finished = True
        winner = -1
    else:
        finished = True
        winner = 0
        for i in range(0, 4):
            if tab[i][j] == 0:
                finished = False

    # print(str(winner)+" "+str(finished))
    return (winner, finished)


def tictactoeRandom(grille, monSymbole):
    x = random.randint(0, (size - 1))
    y = random.randint(0, (size - 1))

    # print(grille[x][y])

    while (grille[x][y] == monSymbole or (grille[x][y] + monSymbole) == 0):
        x = random.randint(0, (size - 1))
        y = random.randint(0, (size - 1))

    return (x, y)


def affecterSymbole(grille, monSymbole, x, y):
    # print(grille)
    # print(x, y)
    grille[x][y] = monSymbole
    # print(grille)


def affichage(grille):
    for i in range(0, size):
        ch = ""
        for j in range(0, size):
            ch += str(grille[i][j]) + " "
        print(ch)
    print()


grille = [0] * size
for i in range(size):
    grille[i] = [0] * size

affichage(grille)

winner = 0
finished = False

while (winner == 0 or finished == False):
    monSymbole = -1
    # print(grille)
    (x, y) = tictactoeRandom(grille, monSymbole)

    affecterSymbole(grille, monSymbole, x, y)
    # print(grille)
    global m, n
    m, n = x, y

    print("Dummy player")
    affichage(grille)
    (winner, finished) = check(grille)

    if (winner == 0 or finished == False):
        monSymbole = 1
        (x, y) = myTicTacToe(grille, monSymbole)
        affecterSymbole(grille, monSymbole, x, y)
        (winner, finished) = check(grille)

        print("Student player")
        affichage(grille)
