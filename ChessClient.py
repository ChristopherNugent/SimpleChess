from itertools import count
from Board import Board
from ChessAI import ChessAI
from Player import Player


try:
    evaler = ChessAI()
    players = (ChessAI(), ChessAI())
    board = Board()

    for turn in count(0, 1):
        if turn % 2:
            board.rotate()
            print(board)
            print(evaler.eval(board))
            board.rotate()
        else:
            print(board)
            print(evaler.eval(board))
        print()
        if board.move(players[turn % 2].get_move(board.clone())):
            break

    print('----------Final Board---------')
    print(board)
    print('Total turns: ' + str(turn))

except KeyboardInterrupt:
    print(turn)
    print(board)
