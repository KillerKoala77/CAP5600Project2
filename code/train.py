import torch.optim as optim
from snake import SnakeGame
from QNet import QNet


def train():
    training_episodes = 100
    model = QNet()
    #optimizer = optim.Adam(model.parameters(), lr=0.001)
    game = SnakeGame()
    game.play()
    game.eventHandler(2)
    
    for episode in range(training_episodes):
        state = SnakeGame.reset()
        totalReward = 0

train()
    
            
        


