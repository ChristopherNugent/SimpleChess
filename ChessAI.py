class ChessAI:

    piece_values = {
        'p': -1, 'P': 1,
        'n': -3, 'N': 3,
        'b': -3.5, 'B': 3.5,
        'r': -5, 'R': 5,
        'q': -10, 'Q': 10,
        'k': -20000, 'K': 20000,
        '+': 0, '.': 0
    }

    def eval(self, board):
        return sum(ChessAI.piece_values[p] for p in board.state)

    def trim_search(self, board, height=2, guarantee=-9999999):
        """Returns the best possible guaranteed evaluation of the board
        height turns in the future."""
        # Base case upon hitting ground. Just score the board.
        if height == 0:
            self.think_count += 1
            return self.eval(board)
        min_score = 9999999
        for move in board.generate_moves():
            board.move(move)
            # We pass the negative of our minimum score, since that is
            # what the children must try to do better than. The first
            # child always passes.
            # We take the negative of the return, as it
            # represents the opponent's score.
            if board.state[move[1]] == 'k':
                board.undo()
                return 999999
            score = -self.trim_search(board, height - 1, -min_score)
            if score < guarantee:
                # We can't beat siblings, so just return this anyway.
                board.undo()
                return score
            elif score < min_score:
                min_score = score
            board.undo()
        # This point reached when there are no early termination due to better
        # siblings in the tree. Thus, we pass our guarantee upward.
        return min_score

    def get_move(self, board):
        self.think_count = 0
        best_score, best_move = -9999999, None
        for move in board.generate_moves():
            board.move(move)
            guarantee = -self.trim_search(board)
            if guarantee > best_score:
                best_score = guarantee
                best_move = move
            board.undo()
        return best_move
