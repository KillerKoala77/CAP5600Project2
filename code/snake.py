import pygame
import random
import time

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
        

class Node:

    def __init__(self, parent, position: Coordinate):
        self.parent = parent
        self.position = position

        self.g = 0
        self.f = 0

    # Override equality operator
    def __eq__(self, other: object) -> bool:
        return self.position == other.position

def gbfs(fruitX, fruitY, headX, headY, body):
    # use fruit x,y and snake head x,y
    # have the head check all 4 directions and calculate manhatten distance
    # best option wins, go that direction
    
    bestDirection = ""
    bestValue = 100000000
    temp = 0
    # check up
    if (headX, headY - 10) not in body:
        temp = abs(headX - fruitX) + abs(headY - 10 - fruitY)
        if temp < bestValue:
            bestValue = temp
            bestDirection = "UP"

    # check down
    if (headX, headY + 10) not in body:
        temp = abs(headX - fruitX) + abs(headY + 10 - fruitY)
        if temp < bestValue:
            bestValue = temp
            bestDirection = "DOWN"
            
    # check left
    if (headX - 10, headY) not in body:
        temp = abs(headX - 10 - fruitX) + abs(headY - fruitY)
        if temp < bestValue:
            bestValue = temp
            bestDirection = "LEFT"

    #check right
    if (headX + 10, headY) not in body:
        temp = abs(headX + 10 - fruitX) + abs(headY - fruitY)
        if temp < bestValue:
            bestValue = temp
            bestDirection = "RIGHT"

    return bestDirection

def aStarSearch(fruit: Coordinate, head: Coordinate, body, boardSize: tuple):

    # Head is the start of the search
    startNode = Node(None, head)

    # Fruit is the end of the search
    fruitNode = Node(None, fruit)

    # Start with the start node in the frontier
    frontier = [startNode]
    searchedNodes = []

    # We will search UP, DOWN, LEFT and RIGHT
    searchDirections = [(0, -10), (0, 10), (-10, 0), (10, 0)]

    # Search while we have new places to search
    while len(frontier) > 0:
        # Take the first node of the frontier
        currentNode = frontier.pop(0)

        # Add it to the list of searched nodes
        searchedNodes.append(currentNode)

        if(currentNode == fruitNode):
            return currentNode
            # We found the fruit
            # TODO: Return path

        nextNodes = []

        for nextMove in searchDirections:

            position = Coordinate(currentNode.position.x + nextMove[0], currentNode.position.y + nextMove[1])

            # Check if new position is valid
            if position.x >= boardSize[0] or position.x < 0 or position.y >= boardSize[1] or position.y < 0:
                continue

            # Check if new position is part of snake body
            if position in body:
                continue

            # This location is valid, create new node
            newNode = Node(currentNode, position)

            # Check if node has already been searched
            if newNode in searchedNodes:
                continue

            # Node is valid and never been searched, set g and f
            newNode.g = currentNode.g + 1

            # F is the manhatten distance to the fruit node
            newNode.f = abs(newNode.position.x - fruitNode.position.x) + abs(newNode.position.y - fruitNode.position.y)

            found = False
            for frontierNode in frontier:
                if frontierNode == newNode:
                    found = True
                    if newNode.g <= frontierNode.g:
                        frontier.remove(frontierNode)
                    break
                
            if not found:
                frontier.append(newNode)

        frontier.sort(key=lambda x: x.f)

    time.sleep(1)
                

            
                        

            



    

def main():
    
    pygame.init()
    
    # Set window size
    screenWidth = 400
    screenHeight = 240
    
    # create screen and main game bool
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    running = True
    gameOver = False
    
    # Default snake speed and direction
    speedX = 10
    speedY = 0
    
    # Default snake coordinates and length
    snakePosition = Coordinate(screenWidth / 4 + 50, screenHeight / 2)
    snakeX = screenWidth / 4 + 50
    snakeY = screenHeight / 2
    snakeLen = 4
    snakeBody = []
    for x in range(4):
        t = screenWidth / 4
        s = ((x * 10) + 10)
        snakeBody.append(Coordinate(t + s, snakeY))
    # Snake speed and populate clock
    speed = 30
    clock = pygame.time.Clock()
    
    # RGB values
    green = (0, 250,0)
    red = (250, 0, 0)
    
    # Default fruit condition
    fruitPosition = Coordinate(round(random.randint(0, screenWidth) / 10) * 10, round(random.randint(0, screenHeight) / 10) * 10)
    fruitX = round(random.randint(0, screenWidth) / 10) * 10
    fruitY = round(random.randint(0, screenHeight) / 10) * 10

    path = []
    
    
    
    # Main game loop
    while running:
        
        if not gameOver:
            # Generate screen
            screen.fill((50,50,50))

            for x in range(int(screenHeight/10)):
                pygame.draw.line(screen, (20,20,20), (0,x*10), (screenWidth,x*10))

            for x in range(int(screenWidth/10)):
                pygame.draw.line(screen, (20,20,20), (x*10, 0), (x*10, screenHeight))
            
            # Draw snake head
            pygame.draw.rect(screen, green, [snakePosition.x, snakePosition.y, 10, 10])
            
            # Record head locations
            snakeBody.append(Coordinate(snakePosition.x, snakePosition.y))
            
            # Draw snake tail
            if len(snakeBody) > snakeLen:
                del snakeBody[:-snakeLen]
            
            for block in snakeBody:
                pygame.draw.rect(screen, green, [block.x, block.y, 10, 10])
                
            # Draw fruit
            pygame.draw.rect(screen, red, [fruitPosition.x, fruitPosition.y, 10, 10])
            
            # Update snake head x and y coordinates
            snakePosition.x += speedX
            snakePosition.y += speedY
            
            # Update fruit coordinates
            if snakePosition == fruitPosition:
                snakeLen += 1
                fruitPosition.x = round(random.randint(0, screenWidth - 10) / 10) * 10
                fruitPosition.y = round(random.randint(0, screenHeight - 10) / 10) * 10    
            
            # Collision with wall
            if snakePosition.x < 0 or snakePosition.x > screenWidth:
                gameOver = True
            if snakePosition.y < 0 or snakePosition.y > screenHeight:
                gameOver = True
                
            # Collision with body
            if snakePosition in snakeBody:
                gameOver = True
            # for block in snakeBody:
            #     if block[0] == snakeX and block[1] == snakeY:
            #         gameOver = True
            
            # Update display
            pygame.display.flip()
            
            # Iterate timer
            clock.tick(speed)

            # If there is no defined path, calculate one
            if len(path) == 0:
                # AI
                #bestDirection = gbfs(fruitX, fruitY, snakeX, snakeY, snakeBody)

                result = aStarSearch(fruitPosition, snakePosition, snakeBody, (screenWidth, screenHeight))

                
                current = Node(result.parent, result.position)
                
                # Walk backwards through all parents to build a path
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                if len(path) == 0:
                    time.sleep(1)
                    
                # Remove last position as that is equal to the current head
                path.pop()


            nextMove = path.pop()

            speedX = nextMove.x - snakePosition.x
            speedY = nextMove.y - snakePosition.y

            # AI A*
            # from current head, check valid moves.
            # add valid moves plus f value to sorted list
            # pop best move from top of list and make it current head
            # repeat

            # if bestDirection == "UP":
            #     speedX = 0
            #     speedY = -10
            # elif bestDirection == "DOWN":
            #     speedX = 0
            #     speedY = 10
            # elif bestDirection == "LEFT":
            #     speedX = -10
            #     speedY = 0
            # elif bestDirection == "RIGHT":
            #     speedX = 10
            #     speedY = 0
            # else:
            #     gameOver = True
            
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