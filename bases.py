import random

# Take a t-uple as parameter
# Compare random number with t-uple value
# Return an integer (depends of the comparison)
def realNumber(proba):
    randomNumber = random.random()

    x1, x2, x3 = proba[0], proba[1], proba[2]

    if randomNumber < x1:
        return 4
    if x1 < randomNumber and randomNumber < x2:
        return 3
    if x2 < randomNumber and randomNumber < x3:
        return 2
    else:
        return 1

def returnListContent(myList):
    for x in range(len(myList)):
        return x
    
def gameBoard(n, proba):
    matrix = [[realNumber(proba) for x in range(n)] for y in range(n)] 
    return matrix

def display(matrix):
    end = " "
    for row in matrix:
        for val in row:
            print(val, end)
        print()

    


