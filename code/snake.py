import pygame
import random

class SnakeGame:
    def __init__(self):
    
        pygame.init()
        
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
                # Generate screen
                self.screen.fill((50,50,50))

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
                # use fruit x,y and snake head x,y
                # have the head check all 4 directions and calculate manhatten distance
                # best option wins, go that direction

                self.bestDirection = ""
                self.bestValue = 100000000
                self.temp = 0
                # check up
                if (self.snakeX, self.snakeY - 10) not in self.snakeBody:
                    self.temp = abs(self.snakeX - self.fruitX) + abs(self.snakeY - 10 - self.fruitY)
                    if self.temp < self.bestValue:
                        self.bestValue = self.temp
                        self.bestDirection = "UP"

                # check down
                if (self.snakeX, self.snakeY + 10) not in self.snakeBody:
                    self.temp = abs(self.snakeX - self.fruitX) + abs(self.snakeY + 10 - self.fruitY)
                    if self.temp < self.bestValue:
                        self.bestValue = self.temp
                        self.bestDirection = "DOWN"
                # check left
                if (self.snakeX - 10, self.snakeY) not in self.snakeBody:
                    self.temp = abs(self.snakeX - 10 - self.fruitX) + abs(self.snakeY - self.fruitY)
                    if self.temp < self.bestValue:
                        self.bestValue = self.temp
                        self.bestDirection = "LEFT"

                #check right
                if (self.snakeX + 10, self.snakeY) not in self.snakeBody:
                    self.temp = abs(self.snakeX + 10 - self.fruitX) + abs(self.snakeY - self.fruitY)
                    if self.temp < self.bestValue:
                        self.bestValue = self.temp
                        self.bestDirection = "RIGHT"

                if self.bestDirection == "UP":
                    self.speedX = 0
                    self.speedY = -10
                elif self.bestDirection == "DOWN":
                    self.speedX = 0
                    self.speedY = 10
                elif self.bestDirection == "LEFT":
                    self.speedX = -10
                    self.speedY = 0
                elif self.bestDirection == "RIGHT":
                    self.speedX = 10
                    self.speedY = 0
                else:
                    #running = False
                    self.gameOver = True
                
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
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    # Game reset
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.speedX = 10
                            self.speedY = 0
                            self.snakeX = self.screenWidth / 4 + 50
                            self.snakeY = self.screenHeight / 2
                            self.snakeLen = 4
                            self.fruitX = 20
                            self.fruitY = 20
                            self.gameOver = False
                            
                        
                # Rendering on this needs to be centered, kind of out of whack
                self.screen.fill((0, 0, 0))
                pygame.display.set_caption("GAME OVER")
                font = pygame.font.Font(None, 36)
                text = font.render("Score: " + str(self.snakeLen-1), True, (255, 255, 255))
                self.screen.blit(text, (self.screenWidth / 2, self.screenHeight / 2))
                pygame.display.flip()
                    
            
        pygame.quit()
        

game = SnakeGame()
game.play()

    