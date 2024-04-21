# Snake AI

by Kyle Meiners and Aaron Webb

CAP5600

To run Snake AI, copy the game files to a directory

## Install pygame
Snake AI uses pygame to handle the game clock and UI rendering.

If pygame isn't installed, run the following command:

  `python3 -m pip install -U pygame --user`

## Run Snake AI

From the command line, navigate to the directory with the game files and use the following command:

  `python3 snake.py -l(optional)`
  
  -l - (Optional) - Flag to toggle learning. If learning is off (default), the Q-Table will be read from a file and the AI agent will utilize that instead of learning from scratch
