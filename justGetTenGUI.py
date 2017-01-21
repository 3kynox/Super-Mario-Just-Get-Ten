"""
@ToDo Python
- Missing animations at startup / modification / gravity -> not enough time
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
    global gameArea, gameBoard, mapSize, surface, start_time, timeOver
    mapSize = 5
    cellSize = 32
    xPos = 289
    yPos = 231
    frame_count = 0
    frame_rate = 60
    start_time = 0
    numTurns = 0
    play_again = 1
    proba=(0.05,0.30,0.6)
    clockMode = False
    savePushed = False
    loadPushed = False
    timeOver = False
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
    musicChanged = False
    pygame.mixer.music.load('sounds/music1.ogg')
    oneUp = pygame.mixer.Sound('sounds/smb_1-up.wav')
    noAdj = pygame.mixer.Sound('sounds/smb_fireworks.wav')
    fuseUp = pygame.mixer.Sound('sounds/smb_jump.wav')
    newGame = pygame.mixer.Sound('sounds/smb_powerup.wav')
    gameOver = pygame.mixer.Sound('sounds/smb_mariodie.wav')
    wonGame = pygame.mixer.Sound('sounds/smb_stage_clear.wav')

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
    # Display the new cell gris
    def drawGrid(gameArea):
        for col in range(mapSize):
            for row in range(mapSize):
                # Prepare to display correct numeric image according gameArea cell value in the correct position
                surface.blit(cells[gameArea[col][row]], (yPos + row*cellSize, xPos + col*cellSize, cellSize, cellSize))

    # Set startup vars and buttons
    def startupDisplay():
        scoreTitle = font.render('CURRENT SCORE :', True, Black)
        numTurnsTitle = font.render('NUMTURN COUNT :', True, Black)
        surface.blit(scoreTitle, (650, 100, 50, 50))
        surface.blit(numTurnsTitle, (650, 120, 50, 50))

        # Draw buttons
        global timeButton, fourButton, fiveButton, sixButton, loadButton, saveButton, mainQuitButton
        timeButton = pygame.draw.rect(surface, Grey, (815,220,85,23))
        timeText = font.render("Time Limit", True, White)
        surface.blit(timeText, (816,217,100,20))
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

    # Display score and maxValue of the game area    
    def displayScore():
        maxScore = maxValue(mapSize, gameArea)
        gameScore = font.render(str(maxScore), True, Black)
        numTurnsScore = font.render(str(numTurns), True, Black)
        surface.fill(White, (820, 100, 50, 50))
        surface.blit(gameScore, (820, 100, 50, 50))
        surface.fill(White, (820, 120, 50, 50))
        surface.blit(numTurnsScore, (820, 120, 50, 50))

    # Occult screen and show win or lost game status
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
        file = 'save/' + file
        if len(file)<3 :
            file = "save/save.txt"
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

    # Load grid according to chosen file
    def loadGrid():
        file = choose()
        try:
            gameArea = []
            i = 0
            with open(file, 'r') as openfile:
                for line in openfile:
                    gameArea.append([])
                    gameArea[i] = [int(n) for n in line.split(',')]
                    i += 1
            openfile.close()
            return gameArea
        except:
            print("The file does not exists!")
            loadGrid()

    # When timer is near to be over music changing
    def changeMusic():
        pygame.mixer.music.load('sounds/music2.ogg')
    
    # Startup draw
    drawGrid(gameArea)
    startupDisplay()
    # Play music
    pygame.mixer.music.play(-1)

    # Main Loop
    while play_again:
        # Calculate mousePos based on gameArea grid
        mouseX = (pygame.mouse.get_pos()[1] - xPos) // cellSize
        mouseY = (pygame.mouse.get_pos()[0] - yPos) // cellSize

        # Game Over
        if not stillMoves(mapSize, gameArea) and gameFinished == False or timeOver == True :
            pygame.mixer.music.stop()
            gameOver.play()
            gameFinished = True
            timeOver = False
            gameWonOrOver('Game Over !')

        # Game Won
        if maxValue(mapSize, gameArea) == 10 and gameFinished == False:
            pygame.mixer.music.stop()
            wonGame.play()
            gameFinished = True
            gameWonOrOver('You Win !')

        # Displaying score& timer since while game not finished
        if not gameFinished:
            displayScore()

            # Normal timer mode
            if clockMode == False:
                # Display timer while game is on
                total_seconds = frame_count // frame_rate
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                surface.fill(White, (740, 183, 60, 20))
                output_string = "{0:02}:{1:02}".format(minutes, seconds)
                timer = font.render(output_string, True, Black)
                surface.blit(timer, [740, 180])
            else:
                # Display countdown on clock game mode
                total_seconds = start_time - (frame_count // frame_rate)
                if total_seconds < 0:
                    total_seconds = 0
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                surface.fill(White, (740, 183, 60, 20))
                output_string = "{0:02}:{1:02}".format(minutes, seconds)
                if minutes < 1: # Time almost done
                    if musicChanged == False:
                        pygame.mixer.music.stop()
                        musicChanged = True
                        changeMusic()
                        pygame.mixer.music.play(-1)
                    text = font.render(output_string, True, Red)

                    if minutes == 0 and seconds == 0: timeOver = True # Game over
                else:
                    text = font.render(output_string, True, Black)
                
                surface.blit(text, [740, 180])

            frame_count += 1
            clock.tick(frame_rate)

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
            elif event.type == MOUSEBUTTONDOWN and gameFinished:
                # Game finished quit button
                if quitButton.collidepoint(pygame.mouse.get_pos()):
                    print('See u soon !')
                    pygame.quit()
                    sys.exit()

                # Reload whole game (main function)
                elif retryButton.collidepoint(pygame.mouse.get_pos()):
                    main()

            elif event.type == MOUSEBUTTONDOWN:
                # Time limit mode
                if timeButton.collidepoint(pygame.mouse.get_pos()):
                    clockMode = True
                    frame_count = 0
                    gameArea = gameBoard(mapSize, proba)
                    drawGrid(gameArea)
                    if mapSize == 4:
                        start_time = 300
                    elif mapSize == 5:
                        start_time = 480
                    elif mapSize == 6:
                        start_time = 600

                # 4x4 Grid
                if fourButton.collidepoint(pygame.mouse.get_pos()):
                    clockMode = False
                    frame_count = 0
                    mapSize = 4
                    gameArea = gameBoard(mapSize, proba)
                    surface = pygame.image.load("images/surface-4x4.png")
                    drawGrid(gameArea)
                    startupDisplay()
                    newGame.play()

                # 5x5 Grid
                elif fiveButton.collidepoint(pygame.mouse.get_pos()):
                    clockMode = False
                    frame_count = 0
                    mapSize = 5
                    gameArea = gameBoard(mapSize, proba)
                    surface = pygame.image.load("images/surface-5x5.png")
                    drawGrid(gameArea)
                    startupDisplay()
                    newGame.play()

                # 6x6 Grid
                elif sixButton.collidepoint(pygame.mouse.get_pos()):
                    clockMode = False
                    frame_count = 0
                    mapSize = 6
                    gameArea = gameBoard(mapSize, proba)
                    surface = pygame.image.load("images/surface-6x6.png")
                    drawGrid(gameArea)
                    startupDisplay()
                    newGame.play()

                # Same game to file
                elif saveButton.collidepoint(pygame.mouse.get_pos()):
                    saveGrid()

                # Load game from file
                elif loadButton.collidepoint(pygame.mouse.get_pos()):
                    gameArea = loadGrid()
                    frame_count = 0
                    clockMode = False
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

                # Main quit button
                elif mainQuitButton.collidepoint(pygame.mouse.get_pos()):
                    print('See u soon !')
                    pygame.quit()
                    sys.exit()

            # First selection on grid
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
            
            # Second selection ...
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
