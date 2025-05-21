# C4minimaxAgent.py
import math
import random
from connect4 import (
    get_valid_locations, get_next_open_row, drop_piece,
    is_terminal_node, winning_move, score_position, PLAYER_PIECE, AI_PIECE
)

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if is_terminal:
        if winning_move(board, AI_PIECE):
            return (None, float('inf'))
        elif winning_move(board, PLAYER_PIECE):
            return (None, -float('inf'))
        else:
            return (None, 0)

    if depth == 0:
        return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            _, score = minimax(b_copy, depth - 1, alpha, beta, False)
            if score > value:
                value = score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            _, score = minimax(b_copy, depth - 1, alpha, beta, True)
            if score < value:
                value = score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def get_minimax_move(board):
    col, _ = minimax(board, 5, -math.inf, math.inf, True)
    return col