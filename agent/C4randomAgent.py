# C4randomAgent.py
import random
from connect4 import get_valid_locations

def get_random_move(board):
    valid_locations = get_valid_locations(board)
    return random.choice(valid_locations) if valid_locations else None