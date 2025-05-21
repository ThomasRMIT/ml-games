# Tic-Tac-Toe Game with Minimax AI and Full Game Loop
import pygame
import sys
from agent.randomAgent import get_random_move
from agent.minimaxAgent import get_best_move

# Initialize Pygame
pygame.init()

# Constants
TOP_BAR_HEIGHT = 60
WINDOW_SIZE = 300
GRID_SIZE = 100
WINDOW_HEIGHT = WINDOW_SIZE + TOP_BAR_HEIGHT
LINE_WIDTH = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)

# Display setup
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Fonts
font = pygame.font.SysFont(None, 40)

# Game state variables
running = True
x_wins = 0
o_wins = 0
opponent_type = None
player_side = 'X'
ai_side = 'O'
current_player = 'X'
game_board = [[' ' for _ in range(3)] for _ in range(3)]
game_over = False
winner = None

# Game logic functions
def reset_game():
    global game_board, current_player, game_over, winner
    game_board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    winner = None

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    return all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3))

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Drawing functions
def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * GRID_SIZE, TOP_BAR_HEIGHT), (i * GRID_SIZE, WINDOW_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, TOP_BAR_HEIGHT + i * GRID_SIZE), (WINDOW_SIZE, TOP_BAR_HEIGHT + i * GRID_SIZE), LINE_WIDTH)

def draw_x(row, col):
    offset = GRID_SIZE // 4
    y_offset = TOP_BAR_HEIGHT
    pygame.draw.line(screen, LINE_COLOR,
                     (col * GRID_SIZE + offset, row * GRID_SIZE + offset + y_offset),
                     ((col + 1) * GRID_SIZE - offset, (row + 1) * GRID_SIZE - offset + y_offset),
                     LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR,
                     ((col + 1) * GRID_SIZE - offset, row * GRID_SIZE + offset + y_offset),
                     (col * GRID_SIZE + offset, (row + 1) * GRID_SIZE - offset + y_offset),
                     LINE_WIDTH)

def draw_o(row, col):
    offset = GRID_SIZE // 4
    y_offset = TOP_BAR_HEIGHT
    pygame.draw.circle(screen, LINE_COLOR,
                       (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2 + y_offset),
                       GRID_SIZE // 2 - offset,
                       LINE_WIDTH)

def draw_turn_indicator(current_player):
    big_font = pygame.font.SysFont(None, 50, bold=True)
    normal_font = pygame.font.SysFont(None, 50)
    small_font = pygame.font.SysFont(None, 36)

    x_center = WINDOW_SIZE // 4
    o_center = WINDOW_SIZE * 3 // 4
    y_center = TOP_BAR_HEIGHT // 2

    if current_player == 'X':
        x_surface = big_font.render("X", True, BLACK)
        o_surface = normal_font.render("O", True, (180, 180, 180))
    else:
        x_surface = normal_font.render("X", True, (180, 180, 180))
        o_surface = big_font.render("O", True, BLACK)

    x_rect = x_surface.get_rect(center=(x_center, y_center))
    o_rect = o_surface.get_rect(center=(o_center, y_center))

    screen.blit(x_surface, x_rect)
    screen.blit(o_surface, o_rect)
    if current_player == 'X':
        pygame.draw.line(screen, BLACK, (x_rect.left, x_rect.bottom + 2), (x_rect.right, x_rect.bottom + 2), 2)
    else:
        pygame.draw.line(screen, BLACK, (o_rect.left, o_rect.bottom + 2), (o_rect.right, o_rect.bottom + 2), 2)

    win_text = f"{x_wins} - {o_wins}"
    win_surface = small_font.render(win_text, True, BLACK)
    win_rect = win_surface.get_rect(center=(WINDOW_SIZE // 2, y_center))
    screen.blit(win_surface, win_rect)

def choose_opponent():
    global opponent_type
    choosing = True
    while choosing:
        screen.fill(WHITE)
        screen.blit(font.render("Choose Opponent:", True, BLACK), font.render("Choose Opponent:", True, BLACK).get_rect(center=(WINDOW_SIZE // 2, 100)))
        screen.blit(font.render("Press H for Human", True, BLACK), font.render("Press H for Human", True, BLACK).get_rect(center=(WINDOW_SIZE // 2, 140)))
        screen.blit(font.render("Press R for Random AI", True, BLACK), font.render("Press R for Random AI", True, BLACK).get_rect(center=(WINDOW_SIZE // 2, 180)))
        screen.blit(font.render("Press M for Minimax AI", True, BLACK), font.render("Press M for Minimax AI", True, BLACK).get_rect(center=(WINDOW_SIZE // 2, 220)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    opponent_type = "human"
                    choosing = False
                elif event.key == pygame.K_r:
                    opponent_type = "random"
                    choosing = False
                elif event.key == pygame.K_m:
                    opponent_type = "minimax"
                    choosing = False

def choose_player_side():
    global player_side, ai_side, current_player
    choosing = True
    while choosing:
        screen.fill(WHITE)
        screen.blit(font.render("Choose Your Side:", True, BLACK), font.render("Choose Your Side:", True, BLACK).get_rect(center=(WINDOW_SIZE // 2, 100)))
        screen.blit(font.render("Press X to be X", True, BLACK), font.render("Press X to be X", True, BLACK).get_rect(center=(WINDOW_SIZE // 2, 140)))
        screen.blit(font.render("Press O to be O", True, BLACK), font.render("Press O to be O", True, BLACK).get_rect(center=(WINDOW_SIZE // 2, 180)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    player_side = 'X'
                    ai_side = 'O'
                    current_player = 'X'
                    choosing = False
                elif event.key == pygame.K_o:
                    player_side = 'O'
                    ai_side = 'X'
                    current_player = 'X'
                    choosing = False

def draw_text_with_outline(text, pos, font, text_color, outline_color, outline_width=2):
    x, y = pos
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx != 0 or dy != 0:
                outline = font.render(text, True, outline_color)
                outline_rect = outline.get_rect(center=(x + dx, y + dy))
                screen.blit(outline, outline_rect)
    main = font.render(text, True, text_color)
    main_rect = main.get_rect(center=pos)
    screen.blit(main, main_rect)

def display_message(line1, line2):
    center_x = WINDOW_SIZE // 2
    draw_text_with_outline(line1, (center_x, WINDOW_SIZE // 2 - 20), font, BLACK, WHITE, 2)
    draw_text_with_outline(line2, (center_x, WINDOW_SIZE // 2 + 20), font, BLACK, WHITE, 2)

# Game setup
choose_opponent()
if opponent_type != 'human':
    choose_player_side()
reset_game()

# Let AI move first if applicable
if opponent_type != 'human' and current_player == ai_side:
    move, _ = get_random_move(game_board) if opponent_type == 'random' else get_best_move(game_board, ai_side, player_side)
    if move:
        game_board[move[0]][move[1]] = ai_side
        current_player = player_side

# Main game loop
while running:
    screen.fill(WHITE)
    draw_turn_indicator(current_player)
    draw_lines()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
        elif not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y > TOP_BAR_HEIGHT:
                row, col = (y - TOP_BAR_HEIGHT) // GRID_SIZE, x // GRID_SIZE
                if game_board[row][col] == ' ':
                    game_board[row][col] = current_player
                    if check_win(game_board, current_player):
                        winner = current_player
                        game_over = True
                        if winner == 'X':
                            x_wins += 1
                        else:
                            o_wins += 1
                    elif check_draw(game_board):
                        winner = "Draw"
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

    # AI move
    if not game_over and current_player == ai_side and opponent_type in ['random', 'minimax']:
        move, _ = get_random_move(game_board) if opponent_type == 'random' else get_best_move(game_board, ai_side, player_side)
        if move:
            game_board[move[0]][move[1]] = ai_side
            if check_win(game_board, ai_side):
                winner = ai_side
                game_over = True
                if winner == 'X':
                    x_wins += 1
                else:
                    o_wins += 1
            elif check_draw(game_board):
                winner = "Draw"
                game_over = True
            else:
                current_player = player_side

    # Draw board
    for r in range(3):
        for c in range(3):
            if game_board[r][c] == 'X':
                draw_x(r, c)
            elif game_board[r][c] == 'O':
                draw_o(r, c)

    if game_over:
        if winner == "Draw":
            display_message("It's a draw!", "Press R")
        else:
            display_message(f"Player {winner} wins!", "Press R")

    pygame.display.flip()

pygame.quit()
sys.exit()