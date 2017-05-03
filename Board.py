from itertools import count  # better looping over possible moves


class Board:

    ##########################################################################
    # Rules of chess
    ##########################################################################

    # Starting position of the board, with rows seperated by +'s. All +'s are
    # outside the board. Padding means even knights cannot escape table.
    starting_position = (
        '++++++++++'    # 0 - 9
        '++++++++++'   # 10 - 19
        '+rnbqkbnr+'   # 20 - 29
        '+pppppppp+'   # 30 - 39
        '+........+'   # 40 - 49
        '+........+'   # 50 - 59
        '+........+'   # 60 - 69
        '+........+'   # 70 - 79
        '+PPPPPPPP+'   # 80 - 89
        '+RNBQKBNR+'   # 90 - 99
        '++++++++++'  # 100 - 109
        '++++++++++'  # 110 - 119
    )

    N, S, E, W = -10, 10, 1, -1
    possible_moves = {
        'P': (N, N + N, N + E, N + W),
        'R': (N, S, E, W),
        'N': (N + N + E, N + N + W, S + S + E, S + S + W,
              E + E + N, E + E + S, W + W + N, W + W + S),
        'B': (N + E, N + W, S + E, S + W),
        'Q': (N, S, E, W, N + E, N + W, S + E, S + W),
        'K': (N, S, E, W, N + E, N + W, S + E, S + W)
    }

    ##########################################################################

    def __init__(self, state=starting_position):
        self.state = state
        self.undo_stack = []

    def clone(self):
        clone = Board(self.state)
        clone.undo_stack = self.undo_stack[:]  # copy list with slice
        return clone

    def rotate(self):
        self.state = self.state[::-1].swapcase()

    def move(self, move):
        start, finish = move
        if not self.state[start].isupper():
            raise KeyError
        target = self.state[finish]
        self.undo_stack.append((start, finish, target))
        self.__put(finish, self.state[start])
        self.__put(start, '.')
        self.rotate()
        return 1 if target == 'k' else 0

    def __put(self, index, value):
        self.state = self.state[:index] + value + self.state[index + 1:]

    def undo(self):
        self.rotate()
        start, finish, target = self.undo_stack.pop()
        self.__put(start, self.state[finish])
        self.__put(finish, target)

    def generate_moves(self):
        N, E, W = self.N, self.E, self.W
        for pos, piece in enumerate(self.state):
            # if p does not belong to the active player, skip it
            if not piece.isupper():
                continue
            for move in self.possible_moves[piece]:
                for dest in count(pos + move, move):
                    target = self.state[dest]
                    # break if target is friendly piece or out of board
                    if target == '+' or target.isupper():
                        break

                    # handle pawn special cases
                    if piece == 'P' and move in (N, N + N) and target != '.':
                        break
                    if piece == 'P' and move in (N + E, N + W) \
                            and target == '.':
                        break

                    yield (pos, dest)

                    # Pawn, knight, king get only one move, and break on attack
                    if piece in 'PNK' or target.islower():
                        break

    def __str__(self):
        string = ''
        for row in range(8):
            start = 10 * (row + 2) + 1
            string += self.state[start:start + 8] + '\n'
        return string
