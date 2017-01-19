import sys, pygame
from bases import *
from merge import *
from possible import *
from pygame.locals import *

pygame.init()

def main():
    # Init vars
    global gameBoard
    mapSize = 5
    cellSize = 32
    xPos = 289
    yPos = 231
    play_again = 1
    proba=(0.05,0.30,0.6)
    gameFinished = False
    firstSelection = False
    size = width, height = 1088, 607
    gameArea = gameBoard(mapSize, proba)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Super Mario Get Ten")
    font = pygame.font.Font('fonts/impress-bt-42347.ttf', 20)
    fontBig = pygame.font.Font('fonts/impress-bt-42347.ttf', 40)

    # Colors
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Green = (0, 204, 0)
    Red = (255, 0, 0)

    # Images loading
    surface = pygame.image.load("images/surface-5x5.png")
    mask = pygame.image.load("images/mask.png").convert_alpha()
    numOne = pygame.image.load("images/1.png")
    numTwo = pygame.image.load("images/2.png")
    numThree = pygame.image.load("images/3.png")
    numFour = pygame.image.load("images/4.png")
    numFive = pygame.image.load("images/5.png")
    numSix = pygame.image.load("images/6.png")
    numSeven = pygame.image.load("images/7.png")
    numEight = pygame.image.load("images/8.png")
    numNine = pygame.image.load("images/9.png")
    numTen= pygame.image.load("images/10.png")
    selectedCellEffect = pygame.image.load("images/selected.png")

    # Images object
    cells = {
        1: numOne,
        2: numTwo,
        3: numThree,
        4: numFour,
        5: numFive,
        6: numSix,
        7: numSeven,
        8: numEight,
        9: numNine,
        10: numTen
    }

    # Functions
    def drawGrid():
        for col in range(mapSize):
            for row in range(mapSize):
                # Prepare to display correct numeric image according gameArea cell value in the correct position
                surface.blit(cells[gameArea[col][row]], (yPos + row*cellSize, xPos + col*cellSize, cellSize, cellSize))

    def displayScore():
        maxScore = maxValue(mapSize, gameArea)
        gameScore = font.render(maxScore, True, Black)
        surface.fill(White, (820, 100, 50, 50))
        surface.blit(gameScore, (820, 100, 50, 50))

    def gameWonOrOver(msg):
        # Draw end game screen
        text = fontBig.render(msg, True, White)
        textRect = text.get_rect()
        textX = surface.get_width() / 2 - textRect.width / 2
        textY = surface.get_height() / 2 - textRect.height / 2
        surface.blit(mask, (0,0))
        surface.blit(text, [textX, textY])

        # Display end game buttons
        global retryButton, quitButton
        retryButton = pygame.draw.rect(surface, Green, (430,330,100,23))
        retryText = font.render("Retry", True, White)
        surface.blit(retryText, (455,328,100,20))
        quitButton = pygame.draw.rect(surface, Red, (550,330,100,23))
        quitText = font.render("Quit", True, White)
        surface.blit(quitText, (580,328,100,20))

    def imageNumber(myPicture):
        for i in range(1,11,1):
            if cells[i] == myPicture :
                if i>1 :
                    return "," + i
                else:
                    return i
        return 0

    def choose():
        fichier = input("Entrer le nom du fichier :")
        if len(fichier)<3 :
            fichier = "save.txt"

    def saveGrid():
        fichier = choose()
        sauvegarde = open(fichier, "w")
        for col in range(mapSize):
            for row in range(mapSize):
                sauvegarde.write(imageNumber(gameArea[col][row]))
        sauvegarde.close()
        
    def replay():
        fichier = choose()
        sauvegarde = open(fichier, "r")
        chaine = sauvegarde.read()
        numberList = chaine.split(",")
        for col in range(mapSize):
            for row in range(mapSize):
                surface.blit(cells[numberList[row*mapSize + col]], (yPos + row*cellSize, xPos + col*cellSize, cellSize, cellSize))
        sauvegarde.close()
        
    # Startup draw
    drawGrid()
    scoreTitle = font.render('CURRENT SCORE :', True, Black)
    surface.blit(scoreTitle, (650, 100, 50, 50))

    # Main Loop
    while play_again:
        # Calculate mousePos based on gameArea grid
        mouseX = (pygame.mouse.get_pos()[1] - xPos) // cellSize
        mouseY = (pygame.mouse.get_pos()[0] - yPos) // cellSize

        # Game Over
        if not stillMoves(mapSize, gameArea) and gameFinished == False:
            gameFinished = True
            gameWonOrOver('Game Over !')

        # Game Won
        if maxValue(mapSize, gameArea) == 10:
            gameFinished = True
            gameWonOrOver('You Win !')

        if not gameFinished:
            displayScore()

        # Events loop
        for event in pygame.event.get():
            # Manage quit / closing window event
            if event.type == pygame.QUIT: sys.exit()

            # Display mousePos on window title bar
            elif event.type == pygame.MOUSEMOTION:
                if mouseX >= 0 and mouseY >= 0:
                    if mouseX < mapSize and mouseY < mapSize:
                        text = "mouseX: {0} - mouseY: {1}".format(mouseX, mouseY)
                        pygame.display.set_caption("Super Mario Get Ten - " + text)
                    else:
                        pygame.display.set_caption("Super Mario Get Ten")
                else:
                    pygame.display.set_caption("Super Mario Get Ten")

            elif event.type == MOUSEBUTTONDOWN and gameFinished:
                if quitButton.collidepoint(pygame.mouse.get_pos()):
                    print('See u soon !')
                    sys.exit()
                elif retryButton.collidepoint(pygame.mouse.get_pos()):
                    play_again = False
                    return main()
            
            if firstSelection == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouseX >= 0 and mouseY >= 0:
                        if mouseX < mapSize and mouseY < mapSize:
                            if adjCells(mapSize, gameArea, mouseX, mouseY):
                                firstSelection = True
                                myTuple = (mouseX, mouseY)
                                tupleList = [myTuple]
                                propagation(mapSize, gameArea, myTuple, tupleList)
                                for item in range(len(tupleList)):
                                    currentPos = tupleList[item]
                                    surface.blit(selectedCellEffect, (yPos + currentPos[1]*cellSize, xPos + currentPos[0]*cellSize, cellSize, cellSize))
                            else:
                                # play error sound, no adjacent cells
                                print('No Adj Cells')  
            elif firstSelection == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouseX >= 0 and mouseY >= 0:
                        if mouseX < mapSize and mouseY < mapSize:
                            if adjCells(mapSize, gameArea, mouseX, mouseY):
                                firstSelection= False
                                myTuple = (mouseX, mouseY)
                                tupleList = [myTuple]
                                propagation(mapSize, gameArea, myTuple, tupleList)
                                modification(mapSize, gameArea, tupleList)
                                gravity(mapSize, gameArea, proba)
                                drawGrid()
                          

        screen.blit(surface, (0, 0))
        pygame.display.update()

main()
