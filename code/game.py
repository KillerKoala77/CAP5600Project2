import pygame
import random
import json

class SnakeGame:
    def __init__(self, learning):
        
        self.learning = learning
                
        pygame.init()
        
        self.QTable = {}
        self.history = []
        self.gameCount = 0
        self.score = 0
        self.moveCount = 0
        
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
        self.snakeX = self.screenWidth / 4 + 50
        self.snakeY = self.screenHeight / 2
        self.snakeLen = 4
        self.snakeBody = []
        for x in range(4):
            self.snakeBody.append((self.screenWidth / 4 + ((x * 10) + 10), self.snakeY))
        # Snake speed and populate clock
        #self.speed = 30
        self.speed = 1000
        self.clock = pygame.time.Clock()
        
        # RGB values
        self.green = (0, 250,0)
        self.red = (250, 0, 0)
        self.yellow = (250, 250, 0)
        
        # Default fruit condition
        self.generateNewFruit()

        if not self.learning:
            self.loadFromFile()
    
    def generateNewFruit(self):
        conflict = True
        while conflict:
            self.fruitX = round(random.randint(0, self.screenWidth - 10) / 10) * 10
            self.fruitY = round(random.randint(0, self.screenHeight - 10) / 10) * 10 

            conflict = (self.fruitX, self.fruitY) in self.snakeBody

    def loadFromFile(self):
        self.speed = 30
        filename = "QTable.json"
        with open(filename, 'r') as file:
            rawData = json.load(file)
            
        for stateParam in rawData:
            self.QTable[stateParam] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
            self.QTable[stateParam][1] = float(rawData[stateParam]['1'])
            self.QTable[stateParam][2] = float(rawData[stateParam]['2'])
            self.QTable[stateParam][3] = float(rawData[stateParam]['3'])
            self.QTable[stateParam][4] = float(rawData[stateParam]['4'])

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

        # Draw score
        font = pygame.font.SysFont(None, 35)
        value = font.render(f"Score: {self.score}", True, self.yellow)
        self.screen.blit(value, [0, 0])

        # Update display
        pygame.display.flip()
        
    def play(self):
        # Main game loop
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
                
                # Remove last tail location, if a fruit wasn't eaten
                if len(self.snakeBody) > self.snakeLen:
                    del self.snakeBody[:-self.snakeLen]

                # Update fruit coordinates
                if self.snakeX == self.fruitX and self.snakeY == self.fruitY:
                    self.snakeLen += 1
                    self.score += 1
                    self.generateNewFruit()
                
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
                            filename = "QTable.json"
                            print(self.QTable)
                            with open(filename, 'w') as file:
                                json.dump(self.QTable, file)
                                self.gameOver = True
                                self.running = False
            
                    
                        
                        
            else:
                self.reset()
                            
    def reset(self):
        self.speedX = 10
        self.speedY = 0
        self.snakeX = self.screenWidth / 4 + 50
        self.snakeY = self.screenHeight / 2
        self.snakeLen = 4
        self.fruitX = round(random.randint(0, self.screenWidth - 10) / 10) * 10
        self.fruitY = round(random.randint(0, self.screenHeight - 10) / 10) * 10 
        self.gameOver = False
        self.gameCount += 1
        self.history = []
        self.moveCount = 0
        print(self.score)
        self.score = 0

    def isSnakeDead(self):
        result = False
        # Collision with wall
        if self.snakeX < 0 or self.snakeX > self.screenWidth - 10:
            result = True
        if self.snakeY < 0 or self.snakeY > self.screenHeight - 10:
            result = True
        if(self.snakeX, self.snakeY) in self.snakeBody:
            result = True  

        return result
            
    
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

        return (leftRight, upDown, tuple(danger))


    def getAction(self):
        
        choices = [1,2,3,4] # R,U,L,D
        epsilon = 0.1
        actionChoice = 0
        
        if self.gameCount > 100:
            epsilon = 0
        if not self.learning:
            epsilon = 0
        
        state = self.getState()
        
        newExploreValue = random.uniform(0,1)
        
        # Restrict epsilon usage later on.... removing now to accelereate testing

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
            #print("Random Action: " + str(actionChoice))
            
        else:
            
            if str(state) not in self.QTable:
                self.QTable[str(state)] = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
            
            actionVals = self.QTable[str(state)]
            maxVal = max(actionVals, key=actionVals.get)
            actionChoice = maxVal
            
        # should manhatten distance take into account the move that was just decided upon?
            
        manDistX = abs(self.snakeX - self.fruitX)
        manDistY = abs(self.snakeY - self.fruitY)

        self.moveCount += 1
        self.history.append((state, actionChoice, manDistX, manDistY, self.moveCount))
        
        #print("Table Action: " + str(actionChoice))
        #return 4
        return actionChoice
        
    def updateQTable(self):
        
        # check for how curState is being defined diff between these two...
        
        prevState = self.history[-1][0]
        prevAction = self.history[-1][1]
        
        curState = self.getState()
        
        snakeDead = self.isSnakeDead()
            
        # Reverse history
        history = self.history[::-1]
        
        lr = 0.7
        discount = 0.5

        if not self.learning:
            lr = 0.001
            discount = 0.001
        elif self.gameCount > 600:
            lr = 0.001
        elif self.gameCount > 300:
            discount = 0.001
        elif self.gameCount > 200:
            lr = 0.4
            discount = 0.2
        else:
            lr = 0.7
            discount = 0.5
        
        
        for i in range(len(history) - 1):           
            reward = 0
            # snake is dead, update table
            if snakeDead:
                reward = -10
                
                if str(prevState) not in self.QTable:
                    self.QTable[str(prevState)] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                    
                self.QTable[str(prevState)][prevAction] = (1 - lr) * self.QTable[str(prevState)][prevAction] + lr * reward
            else:
                
                curState = history[i][0]
                prevState = history[i+1][0]
                prevAction = history[i+1][1]
                
                # manX, manY, leftRight, upDown, danger
                
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
                    reward += 10

                # Build the QTable if states are not present
                if str(curState) not in self.QTable:
                    self.QTable[str(curState)] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                    
                if str(prevState) not in self.QTable:
                    self.QTable[str(prevState)] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                
                    
                self.QTable[str(prevState)][prevAction] = (1 - lr) * self.QTable[str(prevState)][prevAction] + lr * (reward + discount * max(self.QTable[str(curState)], key=self.QTable[str(curState)].get))
        

    