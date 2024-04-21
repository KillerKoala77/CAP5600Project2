import pygame
import random
import json
import argparse
import sys
import time


################################################################################
# SnakeGame Class
#
# Handles setting up the game, processing the move to make and running the game
################################################################################
class SnakeGame:
    def __init__(self):
        
        self.learning = False
        self.barriersEnabled = True
                
        pygame.init()
        
        # Class variables
        self.QTable = {}
        self.history = []
        self.gameCount = 0
        self.score = 0
        self.moveCount = 0
        self.loopArray = []
        
        # Set window size
        self.screenWidth = 400
        self.screenHeight = 240
        
        # create screen and main game bool
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.running = True
        self.gameOver = False
        
        # Default snake speed and direction
        self.speedX = 10
        self.speedY = 0
        
        # Default snake coordinates and length
        self.snakeX = self.screenWidth / 2
        self.snakeY = self.screenHeight / 2
        self.snakeLen = 1
        self.snakeBody = []
            
        # Snake speed and populate clock
        self.speed = 1000
        self.clock = pygame.time.Clock()
        
        # Loop control
        self.looping = False
        self.start = time.perf_counter()
        
        # Barrier locations
        self.barrier = []
        self.barrierTime = time.perf_counter()
        
        # RGB values
        self.green = (0, 250,0)
        self.red = (250, 0, 0)
        self.yellow = (250, 250, 0)
        self.purple = (128, 0, 128)
        
        # Default fruit condition
        self.generateNewFruit()
        
        # Default barrier condition
        if self.barriersEnabled:
            self.generateNewBarrier()

    ################################################################################
    # Gets the command line parameters
    ################################################################################
    
    def getParameters(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog='SnakeAI',
            description='Watch AI learn to play snake!\n\n Hit the \'k\' key if the snake gets stuck in a loop',
            epilog='Hisssssss.......')

        parser.add_argument('-l', '--learning', action='store_true',
                            help='A flag to indicate if the AI will learn from scratch or load a pre-populated Q-Table')

        args = parser.parse_args()
            
        # Store the argument
        self.learning = args.learning
        print("learning: ", self.learning)
        
        
        
    ################################################################################
    # Generates new barrier set and ensures they don't conflict with snake body
    ################################################################################
    def generateNewBarrier(self):
        conflict = True
        while conflict:
            self.barrier = []
            self.barrierTime = time.perf_counter()
            baseX1 = round(random.randint(0, self.screenWidth - 120) / 10) * 10 
            baseY1 = round(random.randint(0, self.screenHeight - 120) / 10) * 10 
            
            baseX2 = round(random.randint(0, self.screenWidth - 120) / 10) * 10 
            baseY2 = round(random.randint(0, self.screenHeight - 120) / 10) * 10 
            
            baseX3 = round(random.randint(0, self.screenWidth - 120) / 10) * 10 
            baseY3 = round(random.randint(0, self.screenHeight - 120) / 10) * 10 
            
            baseX4 = round(random.randint(0, self.screenWidth - 120) / 10) * 10 
            baseY4 = round(random.randint(0, self.screenHeight - 120) / 10) * 10 
            
            offset = 0
            for i in range(6):
                self.barrier.append((baseX1, baseY1 + offset))
                self.barrier.append((baseX2, baseY2 + offset))
                self.barrier.append((baseX3 + offset, baseY3))
                self.barrier.append((baseX4 + offset, baseY4))
                offset += 10
            
            conflict = (self.snakeX, self.snakeY) in self.barrier

    ################################################################################
    # Generates a new fruit and ensures it doesn't conflict with the snake body
    ################################################################################
    def generateNewFruit(self):
        conflict = True
        while conflict:
            self.fruitX = round(random.randint(0, self.screenWidth - 10) / 10) * 10
            self.fruitY = round(random.randint(0, self.screenHeight - 10) / 10) * 10 

            conflict = ((self.fruitX, self.fruitY) in self.snakeBody) or ((self.fruitX, self.fruitY) in self.barrier)
            
    ################################################################################
    # Loads an existing Q table from file
    ################################################################################
    def loadFromFile(self):
        self.speed = 30
        
        # Alternative candidate Q Tables
        #filename = "QTableWebb.json"
        filename = "QTable_v3.json"
        with open(filename, 'r') as file:
            rawData = json.load(file)
            
        # Data type conversions
        for stateParam in rawData:
            self.QTable[stateParam] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
            self.QTable[stateParam][1] = float(rawData[stateParam]['1'])
            self.QTable[stateParam][2] = float(rawData[stateParam]['2'])
            self.QTable[stateParam][3] = float(rawData[stateParam]['3'])
            self.QTable[stateParam][4] = float(rawData[stateParam]['4'])

    ################################################################################
    # Draws the game. Includes setting the caption, drawing the squares, snake,
    # fruit and score
    ################################################################################
    def drawGameBoard(self):
        # Generate screen
        self.screen.fill((50,50,50))
        pygame.display.set_caption("Game: " + str(self.gameCount) + "\t" + str(self.score))

        for x in range(int(self.screenHeight/10)):
            pygame.draw.line(self.screen, (20,20,20), (0,x*10), (self.screenWidth,x*10))

        for x in range(int(self.screenWidth/10)):
            pygame.draw.line(self.screen, (20,20,20), (x*10, 0), (x*10, self.screenHeight))
        
        # Draw snake head
        pygame.draw.rect(self.screen, self.green, [self.snakeX, self.snakeY, 10, 10])                
        
        # Draw snake tail
        for block in self.snakeBody:
            pygame.draw.rect(self.screen, self.green, [block[0], block[1], 10, 10])
            
        # Draw fruit
        pygame.draw.rect(self.screen, self.red, [self.fruitX, self.fruitY, 10, 10])
        
        # Draw barrier
        for (bX, bY) in self.barrier:
            pygame.draw.rect(self.screen, self.purple, [bX, bY, 10, 10])

        # Draw score
        font = pygame.font.SysFont(None, 35)
        value = font.render(f"Score: {self.score}", True, self.yellow)
        self.screen.blit(value, [0, 0])

        # Update display
        pygame.display.flip()

    ################################################################################
    # The main game loop. While the game is not over, the loop in this function
    # continues to take moves and update the snake and game board
    ################################################################################
    def play(self):
        # If not learning, load Q-Table from file
        if not self.learning:
            self.loadFromFile()
            
        self.start = time.perf_counter()
        self.barrierTime = time.perf_counter()
            
        while self.running:
            if not self.gameOver:
                
                # Get next action from current state and Q Table
                choice = self.getAction()
                
                if choice == 1: # Left
                    self.speedX = -10
                    self.speedY = 0
                if choice == 2: # Up
                    self.speedX = 0
                    self.speedY = -10
                if choice == 3: # Right
                    self.speedX = 10
                    self.speedY = 0
                if choice == 4: # Down
                    self.speedX = 0
                    self.speedY = 10

                # Append head to body
                self.snakeBody.append((self.snakeX, self.snakeY))

                # Update snake head location
                self.snakeX += self.speedX
                self.snakeY += self.speedY
                
                # Add to loop control array
                self.loopArray.append((self.snakeX, self.snakeY))
                
                # Check for loop behavior
                if time.perf_counter() - self.start > 1 and self.loopArray.count((self.snakeX, self.snakeY)) > 5:
                    self.looping = True
                    print("looping detected - terminate current run")
                        
                # Remove last tail location, if a fruit wasn't eaten
                if len(self.snakeBody) > self.snakeLen:
                    del self.snakeBody[:-self.snakeLen]

                # Update fruit coordinates
                if self.snakeX == self.fruitX and self.snakeY == self.fruitY:
                    if self.barriersEnabled:
                        self.generateNewBarrier()
                    self.snakeLen += 1
                    self.score += 1
                    self.generateNewFruit()
                    
                    # Reset loop control
                    self.loopArray = []
                    self.start = time.perf_counter()                                    
                    
                self.drawGameBoard()
                
                self.gameOver = self.isSnakeDead()
                
                # Iterate timer
                self.clock.tick(self.speed)

                # AI
                # 1 - LEFT
                # 2 - UP
                # 3 - RIGHT
                # 4 - DOWN
                
                self.updateQTable()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_k:
                            self.gameOver = True
                            break
                        if event.key == pygame.K_s:
                            filename = "QTable_v3.json"
                            print(self.QTable)
                            with open(filename, 'w') as file:
                                json.dump(self.QTable, file)
                                self.gameOver = True
                                self.running = False
            else:
                self.reset()

    ################################################################################
    # Resets all game and AI variables to prepare for the next iteration of the game
    ################################################################################
    def reset(self):
        self.speedX = 10
        self.speedY = 0
        self.snakeX = self.screenWidth / 2
        self.snakeY = self.screenHeight / 2
        self.snakeLen = 1
        self.fruitX = round(random.randint(0, self.screenWidth - 10) / 10) * 10
        self.fruitY = round(random.randint(0, self.screenHeight - 10) / 10) * 10 
        self.gameOver = False
        self.gameCount += 1
        self.history = []
        self.moveCount = 0
        print(self.score)
        self.score = 0
        self.looping = False
        self.start = time.perf_counter()
        if self.barriersEnabled:
            self.generateNewBarrier()

    ################################################################################
    # Determines if the snake has hit the wall or itself
    # @return result is returned and is a boolean indicating if the snake is dead
    ################################################################################
    def isSnakeDead(self):
        result = False
        # Collision with wall
        if self.snakeX < 0 or self.snakeX > self.screenWidth - 10:
            result = True
        if self.snakeY < 0 or self.snakeY > self.screenHeight - 10:
            result = True
            
        # Collision with tail
        if(self.snakeX, self.snakeY) in self.snakeBody:
            result = True
        if self.looping:
            result = True
            
        # Collision with barrier
        if (self.snakeX, self.snakeY) in self.barrier:
            result = True

        return result
            
    ################################################################################
    # Gets the current state as seen by the snake head.
    # State consists of the following:
    #   leftRight - is the fruit to the left or the right of the head
    #               -1 for left, 1 for right, 0 for equal with the head
    #   upDown    - is the fruit above or below the head
    #               -1 for above, 1 for below, 0 for equal with the head
    #   danger    - a 4 element tuple that indicates if a dangerous block is
    #               adjacent to the snake head. 1 indicates danger, 0 indicates safe
    #
    # @return All three state variables are returned as a 3 element tuple
    ################################################################################
    def getState(self):
        leftRight = 0 # X relative direction
        upDown = 0 # Y relative direction
        danger = [0, 0, 0, 0] # L, U, R, D
        
        # get relative fruit position
        
        if self.fruitX - self.snakeX > 0: # If positive
            leftRight = 1 # Fruit is right
            
        if self.fruitX - self.snakeX < 1: # If negative
            leftRight = -1 # Fruit is left
            
        if self.fruitY - self.snakeY > 0: # If positive
            upDown = 1 # Fruit is below
            
        if self.fruitY - self.snakeY < 0:
            upDown = -1 # Fruit is above

        # determine danger
        
        if self.snakeX - 10 < 0: # Off screen left
            danger[0] = 1
            
        if self.snakeX + 10 > self.screenWidth - 10: # Off screen right
            danger[2] = 1
            
        if self.snakeY - 10 < 0: # Off screen top
            danger[1] = 1
            
        if self.snakeY + 10 > self.screenHeight - 10: # Off screen bottom
            danger[3] = 1

        # Check each block in each direction against snakeBody

        if (self.snakeX - 10, self.snakeY) in self.snakeBody: # Left
            danger[0] = 1

        if (self.snakeX + 10, self.snakeY) in self.snakeBody: # Right
            danger[2] = 1

        if (self.snakeX, self.snakeY - 10) in self.snakeBody: # Up
            danger[1] = 1

        if (self.snakeX, self.snakeY + 10) in self.snakeBody: # Down
            danger[3] = 1
            
        # Check for barrier
        if (self.snakeX - 10, self.snakeY) in self.barrier: # Left
            danger[0] = 1

        if (self.snakeX + 10, self.snakeY) in self.barrier: # Right
            danger[2] = 1

        if (self.snakeX, self.snakeY - 10) in self.barrier: # Up
            danger[1] = 1

        if (self.snakeX, self.snakeY + 10) in self.barrier: # Down
            danger[3] = 1

        return (leftRight, upDown, tuple(danger))

    ################################################################################
    # Gets the next action the snake will take. This can either be a random move
    # or a move based on the Q-Table.
    #
    # @return an integer indicating which direction the snake will move next
    #           1 - Left
    #           2 - Up
    #           3 - Right
    #           4 - Down
    ################################################################################
    def getAction(self):
        
        choices = [1,2,3,4] # R,U,L,D
        epsilon = 0.1
        actionChoice = 0
        
        if self.gameCount > 200:
            epsilon = 0
        if not self.learning:
            epsilon = 0
        
        state = self.getState()
        
        newExploreValue = random.uniform(0,1)
        
        # Remove choice that allows snake to immediately double back on itself and die
        if (newExploreValue < epsilon):
            if self.speedX == -10: # Moving left
                choices.remove(3) # Remove right option
                
            if self.speedX == 10: # Moving right
                choices.remove(1) # Remove left option
                
            if self.speedY == -10: # Moving up
                choices.remove(2) # Remove down option
                
            if self.speedY == 10: # Moving down
                choices.remove(4) # Remove up option
            
            actionChoice = random.choice(choices)
            
        else:
            
            if str(state) not in self.QTable:
                self.QTable[str(state)] = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
            
            actionVals = self.QTable[str(state)]
            maxVal = max(actionVals, key=actionVals.get)
            actionChoice = maxVal
            
        manDistX = abs(self.snakeX - self.fruitX)
        manDistY = abs(self.snakeY - self.fruitY)

        self.moveCount += 1
        self.history.append((state, actionChoice, manDistX, manDistY, self.moveCount))
        
        return actionChoice

    ################################################################################
    # Updates the Q-Table after the snake has made its move. Updating the Q-Table
    # with the results of the move, given the state at the time of the move, is
    # what allows the AI to learn
    ################################################################################
    def updateQTable(self):
        snakeDead = self.isSnakeDead()
            
        # Reverse history
        history = self.history[::-1]
        
        lr = 0.8
        discount = 0.3        
        
        for i in range(len(history) - 1):           
            reward = 0
            # snake is dead, update table
            if snakeDead:
                reward = -10
                prevState = history[0][0]
                prevAction = history[0][1]
                
                # Add state if not already in dict
                if str(prevState) not in self.QTable:
                    self.QTable[str(prevState)] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                    
                # Bellman equation
                self.QTable[str(prevState)][prevAction] = (1 - lr) * self.QTable[str(prevState)][prevAction] + lr * reward
            else:
                
                # Retrieve states, actions, and value data
                curState = history[i][0]
                prevState = history[i+1][0]
                prevAction = history[i+1][1]
                
                prevManX = history[i+1][2]
                prevManY = history[i+1][3]

                curManX = history[i][2]
                curManY = history[i][3]

                # Snake is closer, reward given
                if curManX < prevManX or curManY < prevManY:
                    reward = 10
                else: # Snake is further, penalty given
                    reward = -10
                    
                upDown = curState[0]
                leftRight = curState[1]                

                # We have found the fruit, reward granted
                if upDown == 0 and leftRight == 0:
                    reward = 10

                # Build the QTable if states are not present
                if str(curState) not in self.QTable:
                    self.QTable[str(curState)] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}

                if str(prevState) not in self.QTable:
                    self.QTable[str(prevState)] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                
                # Bellman equation
                self.QTable[str(prevState)][prevAction] = (1 - lr) * self.QTable[str(prevState)][prevAction] + lr * (reward + discount * max(self.QTable[str(curState)], key=self.QTable[str(curState)].get))
        

    