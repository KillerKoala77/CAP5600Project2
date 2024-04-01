import pygame
import random

def main():
    
    pygame.init()
    
    # Set window size
    screenWidth = 800
    screenHeight = 500
    
    # create screen and main game bool
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    running = True
    gameOver = False
    
    # Default snake speed and direction
    speedX = 10
    speedY = 0
    
    # Default snake coordinates and length
    snakeX = screenWidth / 2
    snakeY = screenHeight / 2
    snakeLen = 1
    snakeBody = []
    
    # Snake speed and populate clock
    speed = 20
    clock = pygame.time.Clock()
    
    # RGB values
    green = (0, 250,0)
    red = (250, 0, 0)
    
    # Default fruit condition
    fruitX = round(random.randint(0, screenWidth) / 10) * 10
    fruitY = round(random.randint(0, screenHeight) / 10) * 10
    
    
    
    # Main game loop
    while running:
        
        if not gameOver:
            # Generate screen
            screen.fill((50,50,50))
            
            # Draw snake head
            pygame.draw.rect(screen, green, [snakeX, snakeY, 10, 10])
            
            # Record head locations
            snakeBody.append((snakeX, snakeY))
            
            # Draw snake tail
            if len(snakeBody) > snakeLen:
                del snakeBody[:-snakeLen]
            
            for block in snakeBody:
                pygame.draw.rect(screen, green, [block[0], block[1], 10, 10])
                
            # Draw fruit
            pygame.draw.rect(screen, red, [fruitX, fruitY, 10, 10])
            
            # Update snake head x and y coordinates
            snakeX += speedX
            snakeY += speedY
            
            # Update fruit coordinates
            if snakeX == fruitX and snakeY == fruitY:
                snakeLen += 1
                fruitX = round(random.randint(0, screenWidth - 10) / 10) * 10
                fruitY = round(random.randint(0, screenHeight - 10) / 10) * 10    
            
            # Collision with wall
            if snakeX < 0 or snakeX > screenWidth:
                gameOver = True
            if snakeY < 0 or snakeY > screenHeight:
                gameOver = True
                
            # Collision with body
            for block in snakeBody:
                if block[0] == snakeX and block[1] == snakeY:
                    gameOver = True
            
            # Update display
            pygame.display.flip()
            
            # Iterate timer
            clock.tick(speed)
            
            # Collect keyboard input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        speedX = -10
                        speedY = 0
                    if event.key == pygame.K_UP:
                        speedX = 0
                        speedY = -10
                    if event.key == pygame.K_RIGHT:
                        speedX = 10
                        speedY = 0
                    if event.key == pygame.K_DOWN:
                        speedX = 0
                        speedY = 10
                if event.type == pygame.QUIT:
                    gameOver = True
                    
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            # Rendering on this needs to be centered, kind of out of whack
            screen.fill((0, 0, 0))
            pygame.display.set_caption("GAME OVER")
            font = pygame.font.Font(None, 36)
            text = font.render("Score: " + str(snakeLen-1), True, (255, 255, 255))
            screen.blit(text, (screenWidth / 2, screenHeight / 2))
            pygame.display.flip()
                
        
    pygame.quit()
    

if __name__ == "__main__":
    main()