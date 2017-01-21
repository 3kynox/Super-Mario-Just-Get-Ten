"""
@ToDo Python
- Laura : Put save file on save folder
- Documentation of the code (fully done)
- Timer game modes
- Rewrite part 4 function as explained in course subject
- Music (at start game and in timer game mode, when timer almost done)
- Functions game sounds
- Some animations at cells startup placement and on cells fusion
"""

# -*- coding: utf-8 -*-
import sys, pygame
from bases import *
from merge import *
from possible import *
from pygame.locals import *

pygame.init()

def main():
    # Init vars
    global gameArea, gameBoard, mapSize, surface
    mapSize = 5
    cellSize = 32
    xPos = 289
    yPos = 231
    numTurns = 0
    play_again = 1
    proba=(0.05,0.30,0.6)
    savePushed = False
    loadPushed = False
    gameFinished = False
    firstSelection = False
    clock = pygame.time.Clock()
    size = width, height = 1088, 607
    gameArea = gameBoard(mapSize, proba)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Super Mario Get Ten")
    fontSmall = pygame.font.Font('fonts/impress-bt-42347.ttf', 18)
    font = pygame.font.Font('fonts/impress-bt-42347.ttf', 20)
    fontBig = pygame.font.Font('fonts/impress-bt-42347.ttf', 40)

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

    # Sounds loading
    pygame.mixer.music.load('sounds/music1.ogg')
    oneUp = pygame.mixer.Sound('sounds/smb_1-up.wav')
    noAdj = pygame.mixer.Sound('sounds/smb_fireworks.wav')
    fuseUp = pygame.mixer.Sound('sounds/smb_jump.wav')
    newGame = pygame.mixer.Sound('sounds/smb_powerup.wav')

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
    
    # Colors
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Green = (0, 205, 0)
    Red = (255, 0, 0)
    Grey = (110, 128, 145)

    # Functions
    def drawGrid(gameArea):
        for col in range(mapSize):
            for row in range(mapSize):
                # Prepare to display correct numeric image according gameArea cell value in the correct position
                surface.blit(cells[gameArea[col][row]], (yPos + row*cellSize, xPos + col*cellSize, cellSize, cellSize))

    def startupDisplay():
        scoreTitle = font.render('CURRENT SCORE :', True, Black)
        numTurnsTitle = font.render('NUMTURN COUNT :', True, Black)
        surface.blit(scoreTitle, (650, 100, 50, 50))
        surface.blit(numTurnsTitle, (650, 120, 50, 50))

        # Draw buttons
        global fourButton, fiveButton, sixButton, loadButton, saveButton, mainQuitButton
        fourButton = pygame.draw.rect(surface, Grey, (637,245,85,23))
        fourText = font.render("4x4 Grid", True, White)
        surface.blit(fourText, (642,243,100,20))
        fiveButton = pygame.draw.rect(surface, Grey, (726,245,85,23))
        fiveText = font.render("5x5 Grid", True, White)
        surface.blit(fiveText, (731,243,100,20))
        sixButton = pygame.draw.rect(surface, Grey, (815,245,85,23))
        sixText = font.render("6x6 Grid", True, White)
        surface.blit(sixText, (820,243,100,20))
        loadButton = pygame.draw.rect(surface, Grey, (643,270,50,23))
        loadText = font.render("Load", True, White)
        surface.blit(loadText, (648,268,100,20))
        saveButton = pygame.draw.rect(surface, Grey, (698,270,50,23))
        saveText = font.render("Save", True, White)
        surface.blit(saveText, (703,268,100,20))
        mainQuitButton = pygame.draw.rect(surface, Grey, (810,270,50,23))
        mainQuitText = font.render("Quit", True, White)
        surface.blit(mainQuitText, (817,268,100,20))
        consoleText = fontSmall.render("Load / Save filename in console!", True, Red)
        surface.blit(consoleText, (6402,302,100,20))
        
    def displayScore():
        maxScore = maxValue(mapSize, gameArea)
        gameScore = font.render(str(maxScore), True, Black)
        numTurnsScore = font.render(str(numTurns), True, Black)
        surface.fill(White, (820, 100, 50, 50))
        surface.blit(gameScore, (820, 100, 50, 50))
        surface.fill(White, (820, 120, 50, 50))
        surface.blit(numTurnsScore, (820, 120, 50, 50))

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

    # Choose file name at saving/loading file
    def choose():
        file = input('Enter file name : ')
        if len(file)<3 :
            file = "save.txt"
        else:
            try:
                i = file.index('.')
            except:
                file += '.txt'
                
        return file

    # Save the current grid
    def saveGrid():
        file = choose()
        save = open(file, "w")
        output = ''
        i = 0
        for col in range(mapSize):
            if i > 0:
                output += '\n'
            for row in range(mapSize):
                if col > 0 or row > 0:
                    if i == 0:
                        output += ','
                    if i > 0 and row != 0:
                        output += ','
                output += str(gameArea[col][row])
            
            i += 1
        
        save.write(output)
        save.close()

    def loadGrid():
        file = choose()
        gameArea = []
        i = 0
        with open(file, 'r') as openfile:
            for line in openfile:
                gameArea.append([])
                gameArea[i] = [int(n) for n in line.split(',')]
                i += 1
        openfile.close()

        return gameArea
    
    # Startup draw
    drawGrid(gameArea)
    startupDisplay()
    # Play music
    pygame.mixer.music.play(-1)

    # Main Loop
    while play_again:
        clock.tick(30)
        
        # Calculate mousePos based on gameArea grid
        mouseX = (pygame.mouse.get_pos()[1] - xPos) // cellSize
        mouseY = (pygame.mouse.get_pos()[0] - yPos) // cellSize

        # Game Over
        if not stillMoves(mapSize, gameArea) and gameFinished == False:
            gameFinished = True
            gameWonOrOver('Game Over !')

        # Game Won
        if maxValue(mapSize, gameArea) == 10 and gameFinished == False:
            gameFinished = True
            gameWonOrOver('You Win !')

        if not gameFinished:
            displayScore()

        # Events loop
        for event in pygame.event.get():
            # Manage quit / closing window event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

            # Buttons actions
            elif event.type == MOUSEBUTTONDOWN:
                if fourButton.collidepoint(pygame.mouse.get_pos()):
                    mapSize = 4
                    gameArea = gameBoard(mapSize, proba)
                    surface = pygame.image.load("images/surface-4x4.png")
                    drawGrid(gameArea)
                    startupDisplay()
                    newGame.play()
                elif fiveButton.collidepoint(pygame.mouse.get_pos()):
                    mapSize = 5
                    gameArea = gameBoard(mapSize, proba)
                    surface = pygame.image.load("images/surface-5x5.png")
                    drawGrid(gameArea)
                    startupDisplay()
                    newGame.play()
                elif sixButton.collidepoint(pygame.mouse.get_pos()):
                    mapSize = 6
                    gameArea = gameBoard(mapSize, proba)
                    surface = pygame.image.load("images/surface-6x6.png")
                    drawGrid(gameArea)
                    startupDisplay()
                    newGame.play()
                elif saveButton.collidepoint(pygame.mouse.get_pos()):
                    saveGrid()
                elif loadButton.collidepoint(pygame.mouse.get_pos()):
                    gameArea = loadGrid()
                    if len(gameArea) == 4:
                        mapSize = 4
                        surface = pygame.image.load("images/surface-4x4.png")
                        drawGrid(gameArea)
                        startupDisplay()
                        newGame.play()
                    if len(gameArea) == 5:
                        mapSize = 5
                        surface = pygame.image.load("images/surface-5x5.png")
                        drawGrid(gameArea)
                        startupDisplay()
                        newGame.play()
                    if len(gameArea) == 6:
                        mapSize = 6
                        surface = pygame.image.load("images/surface-6x6.png")
                        drawGrid(gameArea)
                        startupDisplay()
                        newGame.play()
                elif mainQuitButton.collidepoint(pygame.mouse.get_pos()):
                    print('See u soon !')
                    pygame.quit()
                    sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN and gameFinished:
                if quitButton.collidepoint(pygame.mouse.get_pos()):
                    print('See u soon !')
                    pygame.quit()
                    sys.exit()
                elif retryButton.collidepoint(pygame.mouse.get_pos()):
                    main()
            
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
                                noAdj.play()  
            elif firstSelection == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouseX >= 0 and mouseY >= 0:
                        if mouseX < mapSize and mouseY < mapSize:
                            if adjCells(mapSize, gameArea, mouseX, mouseY):
                                maxBefore = maxValue(mapSize, gameArea)
                                numTurns += 1
                                firstSelection= False
                                myTuple = (mouseX, mouseY)
                                tupleList = [myTuple]
                                propagation(mapSize, gameArea, myTuple, tupleList)
                                modification(mapSize, gameArea, tupleList)
                                gravity(mapSize, gameArea, proba)
                                fuseUp.play()
                                if maxValue(mapSize, gameArea) > maxBefore: oneUp.play()
                                drawGrid(gameArea)

        screen.blit(surface, (0, 0))
        pygame.display.flip()

if __name__ == '__main__': main()
