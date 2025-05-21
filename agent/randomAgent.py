# randomAgent.py
import random

def get_random_move(board):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
    return random.choice(empty_cells) if empty_cells else None