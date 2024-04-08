import pygame
import random
import torch
import torch.nn as nn
import torch.optim as optim



    
class SnakeGame:
    def __init__(self):
    
        pygame.init()
        
        # QTable needs to be initialized to all 0's
        self.QTable = {}
        self.history = []
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
        self.fruitX = 20 #round(random.randint(0, screenWidth) / 10) * 10
        self.fruitY = 20 #round(random.randint(0, screenHeight) / 10) * 10
        
        
    def play(self):
        
        # Main game loop
        while self.running:
            
            
            if not self.gameOver:
                
                choice = self.getAction()
                print("Choice: ", choice)
                
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
                
                
                self.updateQTable(choice)
                
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
            
    
    def getState(self):
        xDistance = self.snakeX - self.fruitX
        yDistance = self.snakeY - self.fruitY
        relativeX = 0
        relativeY = 0
        
        # 1 - Fruit is left of snake
        # 2 - Fruit is right snake
        # 3 - Fruit is below of snake
        # 4 - Fruit is above snake
        # 0 - Fruit is level with snake
        
        if self.fruitX < self.snakeX:
            relativeX = 1
        if self.fruitX > self.snakeX:
            relativeX = 2
        if self.fruitX == self.snakeX:
            relativeX = 0
            
        if self.fruitY < self.snakeY:
            relativeY = 3
        if self.fruitY > self.snakeY:
            relativeY = 4
        if self.fruitY == self.snakeY:
            relativeY = 0
            
        direction = 0
            
        if self.speedX == -10:
            direction = 1
        if self.speedY == 10:
            direction = 2
        if self.speedX == 10:
            direction = 3
        if self.speedY == -10:
            direction = 4
        
        # Add more in here to describe walls and immediate moves
        return (xDistance, yDistance, relativeX, relativeY, direction)
        
        
        

    def getAction(self):
        choices = [1,2,3,4]
        epsilon = .1
        actionChoice = 0
        
        state = self.getState()
        
        newExploreValue = random.uniform(0,1)
        
        # Restrict epsilon usage later on.... removing now to accelereate testing
        if (newExploreValue < epsilon or state not in self.QTable):
            actionChoice = random.choice(choices)
        else:
            # Q table: (state, action) -> value
            actVals = self.QTable[state]
            print(actVals)
            
            #self.QTable[curState] = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
            
            actionVals = self.QTable[state]
            actionChoice = max(actionVals, key=actionVals.get)

            
            
        self.history.append((state, actionChoice))
        
        return actionChoice
        
        
        
    def updateQTable(self, choice):
        curState = self.getState()
        prevState = self.history[-1][0]
        prevAction = self.history[-1][1]
        reward = 0        
        
        # State
        # Xdist, Ydist, relX, relY
        
        # Aligns horizontally
        # if prevState[2] != 0 and curState[2] == 0:
        #     reward += 1
            
        # # Aligns vertically
        # if prevState[3] != 0 and curState[3] == 0:
        #     reward += 1
        
        # Fruit gets closer
        if curState[0] < prevState[0]:
            reward += 1
        if curState[1] < prevState[1]:
            reward += 1
            
        # Fruit gets farther away
        if curState[0] > prevState[0]:
            reward -= 1
        if curState[1] > prevState[1]:
            reward -= 1
            
        # Fruit attained
        if self.snakeX == self.fruitX and self.snakeY == self.fruitY:
            reward += 50
            
        # Death by wall
        if self.snakeX < 0 or self.snakeX > self.screenWidth:
            reward -= 50
        if self.snakeY < 0 or self.snakeY > self.screenHeight:
            reward -= 50
            
        # # Death by body
        for block in self.snakeBody:
            if block[0] == self.snakeX and block[1] == self.snakeY:
                reward -= 50
        
        # Bellman Equation
        if curState not in self.QTable:
            self.QTable[curState] = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
        #self.QTable[curState].append((choice, reward))
        
        alpha = 0.4
        gamma = 0.2
        
        # Not working
        self.QTable[curState][prevAction] = (1 - alpha) * self.QTable[curState][prevAction] + alpha * (float(reward))
        
        
        #QTable needs to look like this: fix in lookup in choose action function too
        
        #    STATE   |   (action LEFT, value)    |   (action UP, value)   |   (action RIGHT, value)   |   (action DOWN, value)
        
            
        
            
            
game = SnakeGame()
game.play()

    