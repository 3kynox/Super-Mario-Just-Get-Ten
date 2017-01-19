# Comments
def adjCells(n, myList, i, j):
    if i-1 != -1:
        if myList[i][j] == myList[i-1][j]:
            return True
    if j-1 != -1:
        if myList[i][j] == myList[i][j-1]:
            return True
    if i+1 != n:
        if myList[i][j] == myList[i+1][j]:
            return True
    if j+1 != n:
        if myList[i][j] == myList[i][j+1]:
            return True
        
    return False

def stillMoves(n, myList):
    for j in range(n):
        for i in range(n):
            if i-1 != -1:
                if myList[i][j] == myList[i-1][j]:
                    return True
            if j-1 != -1:
                if myList[i][j] == myList[i][j-1]:
                    return True
            if i+1 != n:
                if myList[i][j] == myList[i+1][j]:
                    return True
            if j+1 != n:
                if myList[i][j] == myList[i][j+1]:
                    return True
                
    return False # Game Over

def maxValue(n, myList):
    maxValue = 0
    for j in range(n):
        for i in range(n):
            if myList[i][j] > maxValue:
                maxValue = myList[i][j]
    return str(maxValue)

