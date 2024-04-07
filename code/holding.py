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