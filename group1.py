import random
import math
from copy import deepcopy

GREY = (128, 128, 128) 

OFFENSIVE_FORMATION = [(0, 0), (1, 0), (2, 0), (3, 0)]  
DEFENSIVE_FORMATION = [(6, 0), (7, 0), (5, 0), (4, 0)]  

def evaluate_board1(self, board):
    my_score = 0
    opponent_score = 0

    for i in range(8):
        for j in range(8):
            square = board.getSquare(i, j)
            piece = square.squarePiece
            if piece is not None:
                if piece.color == self.color:
                    my_score += 5 
                    if piece.king:
                        my_score += 10
                    if (i, j) in OFFENSIVE_FORMATION:
                        my_score += 5
                    if (i, j) in DEFENSIVE_FORMATION:
                        my_score += 2
                else:
                    opponent_score += 5
                    if piece.king:
                        opponent_score += 10
                    if (i, j) in OFFENSIVE_FORMATION:
                        opponent_score += 5
                    if (i, j) in DEFENSIVE_FORMATION:
                        opponent_score += 2

    return my_score - opponent_score

def is_capture_move(self, move, board):
    start_pos, possible_moves = move[0], move[2]

    total_captures = 0
    king_captures = 0

    for end_pos in possible_moves:
        if isinstance(start_pos, (tuple, list)) and isinstance(end_pos, (tuple, list)):
            if abs(end_pos[0] - start_pos[0]) == 2:
                mid_x = (start_pos[0] + end_pos[0]) // 2
                mid_y = (start_pos[1] + end_pos[1]) // 2
                captured_piece = board.getSquare(mid_x, mid_y).squarePiece
                if captured_piece is not None:
                    total_captures += 1
                    if captured_piece.king:
                        king_captures += 1
        else:
            print(f"Invalid start_pos or end_pos format: start_pos={start_pos}, end_pos={end_pos}")

    return total_captures, king_captures

def getOpponentMoves(self, board):
    opponent_moves = []
    opponent_color = self.opponent_color
    
    for i in range(8):
        for j in range(8):
            square = board.getSquare(i, j)
            piece = square.squarePiece
            if piece is not None and piece.color == opponent_color:
                moves = self.getPossibleMoves(board)
                if moves:
                    for move in moves:
                        opponent_moves.append(move)
    return opponent_moves

def block_opponent_moves(self, move, board):
    block_score = 0
    opponent_color = self.opponent_color

    board_copy = deepcopy(board)
    start_pos, possible_moves = move[0], move[2]

    for choice in possible_moves:
        board_copy.move_piece(start_pos, move[1], choice[0], choice[1])

    opponent_moves = getOpponentMoves(self, board_copy)

    for opponent_move in opponent_moves:
        for end_pos in opponent_move[2]:
            if (end_pos == 7 and opponent_color == self.color) or (end_pos == 0 and opponent_color != self.color):
                block_score += 20 

            total_captures, _ = is_capture_move(self, opponent_move, board_copy)
            if total_captures > 0:
                block_score += 15 

    return block_score

def get_possible_moves(self, piece):
    possible_moves = []
    row, col = piece.row, piece.col

    directions = [(-1, -1), (-1, 1)]
    if piece.king or piece.color == (255, 255, 255):
        directions.extend([(1, -1), (1, 1)])

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target_square = self.board.getSquare(new_row, new_col)
            if target_square.squarePiece is None: 
                possible_moves.append((row, col, [(new_row, new_col, None, None)]))

        capture_row, capture_col = row + dr, col + dc
        landing_row, landing_col = capture_row + dr, capture_col + dc
        if (
            0 <= capture_row < 8 and 0 <= capture_col < 8 and
            0 <= landing_row < 8 and 0 <= landing_col < 8
        ):
            target_square = self.board.getSquare(capture_row, capture_col)
            landing_square = self.board.getSquare(landing_row, landing_col)
            if (
                target_square.squarePiece and
                target_square.squarePiece.color != piece.color and
                landing_square.squarePiece is None
            ):
                possible_moves.append((row, col, [(landing_row, landing_col, capture_row, capture_col)]))

    return possible_moves

def evaluate_board2(self, board):
    """
    Evaluates the board state from the bot's perspective.
    """
    my_score = 0
    opponent_score = 0

    for i in range(8):
        for j in range(8):
            square = board.getSquare(i, j)
            piece = square.squarePiece
            if piece:
                piece_value = 5
                if piece.king:
                    piece_value += 15
                advancement_bonus = (7 - i) if piece.color == GREY else i
                if piece.king:
                    advancement_bonus = 0

                edge_protection = 3 if j in (0, 7) else 0
                piece_score = piece_value + advancement_bonus + edge_protection

                if piece.color == self.color:
                    my_score += piece_score
                else:
                    opponent_score += piece_score

                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    neighbor_row, neighbor_col = i + dr, j + dc
                    landing_row, landing_col = neighbor_row + dr, neighbor_col + dc
                    if (
                        0 <= neighbor_row < 8 and 0 <= neighbor_col < 8 and
                        0 <= landing_row < 8 and 0 <= landing_col < 8
                    ):
                        neighbor_square = board.getSquare(neighbor_row, neighbor_col)
                        landing_square = board.getSquare(landing_row, landing_col)
                        if (
                            neighbor_square.squarePiece and
                            neighbor_square.squarePiece.color != piece.color and
                            landing_square.squarePiece is None
                        ):
                            if piece.color == self.color:
                                my_score += 10
                            else:
                                opponent_score += 10

    total_pieces = sum(1 for i in range(8) for j in range(8) if board.getSquare(i, j).squarePiece)
    if total_pieces > 12:
        my_score *= 0.9
        opponent_score *= 0.9
    elif total_pieces <= 6:
        my_score *= 1.1
        opponent_score *= 1.1

    return my_score - opponent_score

def minimax(self, board, depth, maximizing_player, alpha, beta):
    """
    Minimax with Alpha-Beta pruning.
    """
    if depth == 0:
        return evaluate_board2(self, board), None

    possible_moves = self.getPossibleMoves(board)
    if not possible_moves:
        return evaluate_board2(self, board), None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in possible_moves:
            for choice in move[2]:
                board_copy = deepcopy(board)
                board_copy.move_piece(move[0], move[1], choice[0], choice[1])
                eval_score, _ = minimax(self, board_copy, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (move, choice)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for move in possible_moves:
            for choice in move[2]:
                board_copy = deepcopy(board)
                board_copy.move_piece(move[0], move[1], choice[0], choice[1])
                eval_score, _ = minimax(self, board_copy, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (move, choice)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval, best_move

def group1(self, board):

    if self.color == GREY:
        """
        Select the best move using the Minimax algorithm.
        """
        possible_moves2 = self.getPossibleMoves(board)
        if not possible_moves2:
            self.game.end_turn()
            return

        depth = 5
        _, best_move = minimax(self, board, depth, True, -math.inf, math.inf)

        if best_move is None:
            random_move = random.choice(possible_moves2)
            rand_choice = random.choice(random_move[2])
            return random_move, rand_choice

        return best_move[0], best_move[1]

    else:
            possible_moves = self.getPossibleMoves(board)

            if not possible_moves:
                self.game.end_turn()
                return
        
            best_move = None
            best_score = -math.inf
        
            for move in possible_moves:
                for choice in move[2]:  
                    board_copy = deepcopy(board)
                    board_copy.move_piece(move[0], move[1], choice[0], choice[1])
        
                    score = evaluate_board1(self, board_copy)
        
                    total_captures, king_captures = is_capture_move(self, move, board)
        
                    score += total_captures * 10 
                    score += king_captures * 20
        
                    block_score = block_opponent_moves(self, move, board)
                    score += block_score
 
                    if (move[0] in OFFENSIVE_FORMATION) or (move[1] in OFFENSIVE_FORMATION):
                        score += 5 
        
                    if (move[0] in DEFENSIVE_FORMATION) or (move[1] in DEFENSIVE_FORMATION):
                        score += 2

                    if score > best_score:
                        best_score = score
                        best_move = (move, choice)
        
            if best_move is None:
                random_move = random.choice(possible_moves)
                rand_choice = random.choice(random_move[2])
                return random_move, rand_choice
        
            return best_move[0], best_move[1]