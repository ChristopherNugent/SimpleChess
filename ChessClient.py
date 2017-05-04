from itertools import count         # nicer turn counting
from Board import Board
from ChessAI import ChessAI
from Player import Player

# Ask whether each player should be human or AI.
players = []
while len(players) < 2:
    next_player = input(
        'Please input "h" for human player or "c" for an AI player: ')
    if next_player == 'h':
        players.append(Player())
    elif next_player == 'c':
        players.append(ChessAI())
    else:
        print('Invalid input!')
    print()

# Continue getting movies until the game ends.
board = Board()
for turn in count(0, 1):
    if board.move(players[turn % 2].get_move(board.clone())):
        break

print('----------Final Board---------')
print(board)
print('Total turns: ' + str(turn))
