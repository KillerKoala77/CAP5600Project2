import pygame
import random

class SnakeGame:
    def __init__(self):
    
        pygame.init()
        
        # QTable needs to be initialized to all 0's
        self.QTable = {}
        self.history = []
        self.fruitLogger = []
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
        self.speed = 30
        self.clock = pygame.time.Clock()
        
        # RGB values
        self.green = (0, 250,0)
        self.red = (250, 0, 0)
        
        # Default fruit condition
        self.fruitX = round(random.randint(0, self.screenWidth - 10) / 10) * 10
        self.fruitY = round(random.randint(0, self.screenHeight - 10) / 10) * 10 
        
        
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
                
                self.snakeBody.append((self.snakeX, self.snakeY))
                
                self.snakeX += self.speedX
                self.snakeY += self.speedY
                
                #self.snakeBody.append((self.snakeX, self.snakeY))
                
                
                # Generate screen
                self.screen.fill((50,50,50))
                pygame.display.set_caption("Game: " + str(self.gameCount) + "\t" + str(self.score))

                for x in range(int(self.screenHeight/10)):
                    pygame.draw.line(self.screen, (20,20,20), (0,x*10), (self.screenWidth,x*10))

                for x in range(int(self.screenWidth/10)):
                    pygame.draw.line(self.screen, (20,20,20), (x*10, 0), (x*10, self.screenHeight))
                
                # Draw snake head
                pygame.draw.rect(self.screen, self.green, [self.snakeX, self.snakeY, 10, 10])
                
                # Record head locations
                #self.snakeBody.append((self.snakeX, self.snakeY))

                # remove last tail location, if a fruit wasn't eaten
                if len(self.snakeBody) > self.snakeLen:
                    del self.snakeBody[:-self.snakeLen]
                
                # Draw snake tail
                for block in self.snakeBody:
                    pygame.draw.rect(self.screen, self.green, [block[0], block[1], 10, 10])
                    
                # Draw fruit
                pygame.draw.rect(self.screen, self.red, [self.fruitX, self.fruitY, 10, 10])
                
                # Update snake head x and y coordinates
                #self.snakeX += self.speedX
                #self.snakeY += self.speedY
                
                # Update fruit coordinates
                if self.snakeX == self.fruitX and self.snakeY == self.fruitY:
                    self.snakeLen += 1
                    self.score += 1
                    self.fruitX = round(random.randint(0, self.screenWidth - 10) / 10) * 10
                    self.fruitY = round(random.randint(0, self.screenHeight - 10) / 10) * 10 
                    
                
                # Collision with wall
                if self.snakeX < 0 or self.snakeX > self.screenWidth - 10:
                    self.gameOver = True
                if self.snakeY < 0 or self.snakeY > self.screenHeight - 10:
                    self.gameOver = True


                if(self.snakeX, self.snakeY) in self.snakeBody:
                    self.gameOver = True
                # # Collision with body
                # for block in self.snakeBody:
                #     if block[0] == self.snakeX and block[1] == self.snakeY:
                #         self.gameOver = True
                
                # Update display
                pygame.display.flip()
                
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
            
                    
                        
                        
            else:
                self.reset()
                            
                        
                # Rendering on this needs to be centered, kind of out of whack
                # self.screen.fill((0, 0, 0))
                # pygame.display.set_caption("GAME OVER")
                # font = pygame.font.Font(None, 36)
                # text = font.render("Score: " + str(self.snakeLen-1), True, (255, 255, 255))
                # self.screen.blit(text, (self.screenWidth / 2, self.screenHeight / 2))
                # pygame.display.flip()
                
                
            
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
        self.fruitLogger = []
        #print(self.score)
        self.score = 0
            
    
    def getState(self):
        
        leftRight = 0 # X
        upDown = 0 # Y
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
            
        # for block in self.snakeBody:
        #     if block[0] == self.snakeX - 10:
        #         danger[0] = 1
        #     if block[0] == self.snakeX + 10:
        #         danger[2] = 1
        #     if block[1] == self.snakeY - 10:
        #         danger[1] = 1
        #     if block[1] == self.snakeY + 10:
        #         danger[1] = 3
                
        # direction = 0
        
        # if self.speedX == -10:
        #     direction = 1
        # if self.speedY == 10:
        #     direction = 2
        # if self.speedX == 10:
        #     direction = 3
        # if self.speedY == -10:
        #     direction = 4
            
        
            
        print(danger)
        return (leftRight, upDown, tuple(danger))

        

    def getAction(self):
        choices = [1,2,3,4] # R,U,L,D
        epsilon = 0.1
        actionChoice = 0
        
        if self.gameCount > 100:
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
            
            if state not in self.QTable:
                self.QTable[state] = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
            
            actionVals = self.QTable[state]
            maxVal = max(actionVals, key=actionVals.get)
            actionChoice = maxVal
            
        # should manhatten distance take into account the move that was just decided upon?
            
        manDistX = abs(self.snakeX - self.fruitX)
        manDistY = abs(self.snakeY - self.fruitY)

        self.moveCount += 1
        self.history.append((state, actionChoice, manDistX, manDistY, self.moveCount))
        self.fruitLogger.append((self.fruitX, self.fruitY))
        
        #print("Table Action: " + str(actionChoice))
        #return 4
        return actionChoice
        
        
        
    def updateQTable(self):
        
        # check for how curState is being defined diff between these two...
        
        prevState = self.history[-1][0]
        prevAction = self.history[-1][1]
        
        curState = self.getState()
        
        snakeDead = False
        

        
        
        # if dead
        if self.snakeX < 0 or self.snakeX > self.screenWidth - 10:
            snakeDead = True
            #print("death by wall")
        if self.snakeY < 0 or self.snakeY > self.screenHeight - 10:
            snakeDead = True
            #print("death by wall")
        

        if(self.snakeX, self.snakeY) in self.snakeBody:
            snakeDead = True
        
        # for block in self.snakeBody:
        #     if block[0] == self.snakeX and block[1] == self.snakeY:
        #         snakeDead = True
        #         #print("death by tail" + str(prevState[2]))
                
                
        # Reverse history
        history = self.history[::-1]
        
        #lr = 0.02
        lr = 0.7
        reward = 0
        discount = 0.5
        
        for i in range(len(history) - 1):           
                
        # snake is dead, update table
            if snakeDead:
                reward -= 10
                
                if prevState not in self.QTable:
                    self.QTable[prevState] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                    
            
                    
                self.QTable[prevState][prevAction] = (1 - lr) * self.QTable[prevState][prevAction] + lr * reward

                    
    
            else:
                
                curState = history[i][0]
                prevState = history[i+1][0]
                prevAction = history[i+1][1]
                
                # manX, manY, leftRight, upDown, danger
                
                #prevManX = prevState[0]
                #prevManY = prevState[1]
                prevManX = history[i+1][2]
                prevManY = history[i+1][3]

                prevMan = prevManX + prevManY
                
                #curManX = curState[0]
                #curManY = curState[1]
                curManX = history[i][2]
                curManY = history[i][3]
                
                curMan = curManX + curManY

                
                if curManX < prevManX or curManY < prevManY:
                    reward += 10
                else:
                    reward -= 10

                # manhatten distance is closer, yay
                # if curMan < prevMan:
                #     reward += 10
                    
                    
                upDown = curState[0]
                leftRight = curState[1]
                
                prevUpDown = prevState[0]
                prevLeftRight = prevState[1]
                
                # if prevUpDown != 0 and upDown == 0:
                #     reward += 20
                # if prevLeftRight != 0 and leftRight == 0:
                #     reward += 20
                
                if upDown == 0 and leftRight == 0:
                    reward += 10
                    
                # if prevUpDown == 0 and upDown != 0:
                #     reward -= 20
                # if prevLeftRight == 0 and leftRight != 0:
                #     reward -= 20
                  
                if curState not in self.QTable:
                    self.QTable[curState] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                    
                if prevState not in self.QTable:
                    self.QTable[prevState] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                
                    
                self.QTable[prevState][prevAction] = (1 - lr) * self.QTable[prevState][prevAction] + lr * (reward + discount * max(self.QTable[curState], key=self.QTable[curState].get))
        
        
            
            
game = SnakeGame()
game.play()

    