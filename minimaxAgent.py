# minimaxAgent.py
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']

def print_board_state(board, depth, move=None, score=None):
    print(f"\n{'-'*20}\nDepth: {depth}")
    if move is not None:
        print(f"Evaluating move: {move} -> Score: {score}")
    for row in board:
        print(' '.join(row))
    print(f"{'-'*20}")

def minimax(board, depth, is_maximizing, ai_side, player_side):
    if check_win(board, ai_side):
        return 1
    elif check_win(board, player_side):
        return -1
    elif check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row, col in get_empty_cells(board):
            board[row][col] = ai_side
            score = minimax(board, depth + 1, False, ai_side, player_side)
            board[row][col] = ' '
            #print_board_state(board, depth, move=(row, col), score=score)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row, col in get_empty_cells(board):
            board[row][col] = player_side
            score = minimax(board, depth + 1, True, ai_side, player_side)
            board[row][col] = ' '
            #print_board_state(board, depth, move=(row, col), score=score)
            best_score = min(score, best_score)
        return best_score

def get_best_move(board, ai_side, player_side):
    best_score = -float('inf')
    move = None
    scores = {}
    for row, col in get_empty_cells(board):
        board[row][col] = ai_side
        score = minimax(board, 0, False, ai_side, player_side)
        board[row][col] = ' '
        scores[(row, col)] = score
        if score > best_score:
            best_score = score
            move = (row, col)
    return move, scores