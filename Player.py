from ChessAI import ChessAI


class Player:

    def loc(code):
        row = 'abcdefgh'.index(code[0])
        col = int(code[1]) - 1
        return 10 * (row + 2) + (col + 1)

    def get_move(self, board):
        try:
            print(board)
            code = input("Please enter a move: ")
            if code == "helpme":
                return ChessAI().get_move(board)
            return (Player.loc(code[:2]), Player.loc(code[3:]))
        except KeyError:
            return self.get_move(board)
