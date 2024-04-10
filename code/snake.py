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
        self.fruitX = 20
        self.fruitY = 20
        
        
    def play(self):
        
        # Main game loop
        while self.running:
            
            
            if not self.gameOver:
                
                choice = self.getAction()
                
                if choice == 1:
                    self.speedX = -10
                    self.speedY = 0
                if choice == 2:
                    self.speedX = 0
                    self.speedY = -10
                if choice == 3:
                    self.speedX = 10
                    self.speedY = 0
                if choice == 4:
                    self.speedX = 0
                    self.speedY = 10
                
                
                
                
                # Generate screen
                self.screen.fill((50,50,50))
                pygame.display.set_caption("Game: " + str(self.gameCount))

                for x in range(int(self.screenHeight/10)):
                    pygame.draw.line(self.screen, (20,20,20), (0,x*10), (self.screenWidth,x*10))

                for x in range(int(self.screenWidth/10)):
                    pygame.draw.line(self.screen, (20,20,20), (x*10, 0), (x*10, self.screenHeight))
                
                # Draw snake head
                pygame.draw.rect(self.screen, self.green, [self.snakeX, self.snakeY, 10, 10])
                
                # Record head locations
                self.snakeBody.append((self.snakeX, self.snakeY))
                
                # Draw snake tail
                if len(self.snakeBody) > self.snakeLen:
                    del self.snakeBody[:-self.snakeLen]
                
                for block in self.snakeBody:
                    pygame.draw.rect(self.screen, self.green, [block[0], block[1], 10, 10])
                    
                # Draw fruit
                pygame.draw.rect(self.screen, self.red, [self.fruitX, self.fruitY, 10, 10])
                
                # Update snake head x and y coordinates
                self.snakeX += self.speedX
                self.snakeY += self.speedY
                
                # Update fruit coordinates
                if self.snakeX == self.fruitX and self.snakeY == self.fruitY:
                    self.snakeLen += 1
                    self.fruitX = round(random.randint(0, self.screenWidth - 10) / 10) * 10
                    self.fruitY = round(random.randint(0, self.screenHeight - 10) / 10) * 10 
                    self.fruitX = 30
                    self.fruitY = 200
                
                # Collision with wall
                if self.snakeX < 0 or self.snakeX > self.screenWidth:
                    self.gameOver = True
                if self.snakeY < 0 or self.snakeY > self.screenHeight:
                    self.gameOver = True
                    
                # Collision with body
                for block in self.snakeBody:
                    if block[0] == self.snakeX and block[1] == self.snakeY:
                        self.gameOver = True
                
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
                
                # if choice == 1:
                #     self.speedX = -10
                #     self.speedY = 0
                # if choice == 2:
                #     self.speedX = 0
                #     self.speedY = -10
                # if choice == 3:
                #     self.speedX = 10
                #     self.speedY = 0
                # if choice == 4:
                #     self.speedX = 0
                #     self.speedY = 10
                    
                
                
                # Collect keyboard input
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.speedX = -10
                            self.speedY = 0
                        if event.key == pygame.K_UP:
                            self.speedX = 0
                            self.speedY = -10
                        if event.key == pygame.K_RIGHT:
                            self.speedX = 10
                            self.speedY = 0
                        if event.key == pygame.K_DOWN:
                            self.speedX = 0
                            self.speedY = 10
                    if event.type == pygame.QUIT:
                        self.gameOver = True
                        
                        
                        
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
        self.fruitX = 20
        self.fruitY = 20
        self.gameOver = False
        self.gameCount += 1
        self.history = []
        self.fruitLogger = []
            
    
    def getState(self):
        
        leftRight = 0
        upDown = 0
        danger = [0, 0, 0, 0]
        
        manDistX = abs(self.snakeX - self.fruitX)
        manDistY = abs(self.snakeY - self.fruitY)
        
        if self.fruitX - self.snakeX > 0:
            leftRight = 1
        if self.fruitX - self.snakeX < 1:
            leftRight = -1
        if self.fruitY - self.snakeY > 0:
            upDown = 1
        if self.fruitY - self.snakeY < 0:
            upDown = -1
        
        if self.snakeX - 10 == 0:
            danger[0] = 1
        if self.snakeX + 10 == self.screenWidth:
            danger[1] = 1
        if self.snakeY - 10 == 0:
            danger[2] = 1
        if self.snakeY + 10 == self.screenHeight:
            danger[3] = 1
        
            
            
        for block in self.snakeBody:
            if block[0] == self.snakeX - 10:
                danger[0] = 1
            if block[0] == self.snakeX + 10:
                danger[1] = 1
            if block[1] - 10 == self.snakeY:
                danger[2] = 1
            if block[1] + 10 == self.snakeY:
                danger[3] = 1
        if 1 in danger:
            print(danger)
            
        
        
        return (manDistX, manDistY, leftRight, upDown, tuple(danger))

        

    def getAction(self):
        choices = [1,2,3,4]
        epsilon = 0.1
        actionChoice = 0
        
        if self.gameCount > 200:
            epsilon = 0
        
        state = self.getState()
        
        newExploreValue = random.uniform(0,1)
        
        # Restrict epsilon usage later on.... removing now to accelereate testing
        if (newExploreValue < epsilon or state not in self.QTable):
            actionChoice = random.choice(choices)
        else:
            # Q table: (state, action) -> value
            
            #self.QTable[curState] = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
            
            actionVals = self.QTable[state]
            maxVal = max(actionVals, key=actionVals.get)
            actionChoice = maxVal

            
            
        self.history.append((state, actionChoice))
        self.fruitLogger.append((self.fruitX, self.fruitY))
        
        return actionChoice
        
        
        
    def updateQTable(self):
        
        # check for how curState is being defined diff between these two...
        
        prevState = self.history[-1][0]
        prevAction = self.history[-1][1]
        
        curState = self.getState()
        
        snakeDead = False

        
        
        # if dead
        if self.snakeX < 0 or self.snakeX > self.screenWidth:
            snakeDead = True
        if self.snakeY < 0 or self.snakeY > self.screenHeight:
            snakeDead = True
        
        
        for block in self.snakeBody:
            if block[0] == self.snakeX and block[1] == self.snakeY:
                snakeDead = True
                
                
        # Reverse history
        history = self.history[::-1]
        
        lr = 0.80
        reward = 0
        discount = 0.2
        
        for i in range(len(history) - 1):           
                
        # snake is dead, update table
            if snakeDead:
                reward -= 500
                
                if prevState not in self.QTable:
                    self.QTable[prevState] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                    
                self.QTable[prevState][prevAction] = (1 - lr) * self.QTable[prevState][prevAction] + lr * reward
    
            else:
                
                curState = history[i][0]
                prevState = history[i+1][0]
                prevAction = history[i+1][1]
                
                # manX, manY, leftRight, upDown, danger
                
                prevManX = prevState[0]
                prevManY = prevState[1]
                
                curManX = curState[0]
                curManY = curState[1]
                
                fruitLog = self.fruitLogger[::-1]
                
                prevFruitX = fruitLog[i+1][0]
                prevFruitY = fruitLog[i+1][1]
                
                curFruitX = fruitLog[i][0]
                curFruitY = fruitLog[i][1]      
                
                if curManX < prevManX:
                    reward += 10
                if curManX > prevManX:
                    reward -= 10
                if curManY < prevManY:
                    reward += 10
                if curManY > prevManY:
                    reward -= 10
                    
                    
                if curFruitX != prevFruitX and curFruitY != prevFruitY:
                    reward += 20
                
                  
                if curState not in self.QTable:
                    self.QTable[curState] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                    
                if prevState not in self.QTable:
                    self.QTable[prevState] = {1 : 0.0, 2 : 0.0, 3 : 0.0, 4 : 0.0}
                
                    
                self.QTable[prevState][prevAction] = (1 - lr) * self.QTable[prevState][prevAction] + lr * (reward + discount * max(self.QTable[curState], key=self.QTable[curState].get))
        
        
            
            
game = SnakeGame()
game.play()

    