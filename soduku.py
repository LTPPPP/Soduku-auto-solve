import pygame
import random
import time

# Initialize pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 600, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 122, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
GREEN = (0, 255, 0)

# Fonts
TITLE_FONT = pygame.font.SysFont("arial", 48, bold=True)
NUMBER_FONT = pygame.font.SysFont("arial", 36)
BUTTON_FONT = pygame.font.SysFont("arial", 24)
TIME_FONT = pygame.font.SysFont("arial", 20)

def create_empty_board(n):
    return [[0 for _ in range(n)] for _ in range(n)]

def fill_random_cells(board, n, k):
    cells = [(i, j) for i in range(n) for j in range(n)]
    random.shuffle(cells)
    for row, col in cells[:k]:
        num = random.randint(1, n)
        if is_valid(board, num, (row, col), n):
            board[row][col] = num

def draw_board(board, n, highlighted_cell=None, solve_time=None):
    SCREEN.fill(WHITE)
    cell_size = (WIDTH - 40) // n

    # Draw title
    title = TITLE_FONT.render("Sudoku Solver", True, BLUE)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

    # Draw grid background
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (20, 70, WIDTH - 40, WIDTH - 40))

    # Draw grid lines
    for i in range(n + 1):
        line_width = 4 if i % (n // 3) == 0 else 1
        pygame.draw.line(SCREEN, BLACK, (20 + i * cell_size, 70), (20 + i * cell_size, 70 + WIDTH - 40), line_width)
        pygame.draw.line(SCREEN, BLACK, (20, 70 + i * cell_size), (WIDTH - 20, 70 + i * cell_size), line_width)

    # Draw numbers and highlight current cell
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                text = NUMBER_FONT.render(str(board[i][j]), True, BLACK)
                SCREEN.blit(text, (30 + j * cell_size + (cell_size - text.get_width()) // 2,
                                   80 + i * cell_size + (cell_size - text.get_height()) // 2))

            if (i, j) == highlighted_cell:
                pygame.draw.rect(SCREEN, LIGHT_BLUE, (20 + j * cell_size, 70 + i * cell_size, cell_size, cell_size), 3)

    # Draw buttons
    solve_button = pygame.Rect(50, HEIGHT - 60, 200, 50)
    pygame.draw.rect(SCREEN, BLUE, solve_button, border_radius=10)
    solve_text = BUTTON_FONT.render("Solve", True, WHITE)
    SCREEN.blit(solve_text, (solve_button.centerx - solve_text.get_width() // 2,
                             solve_button.centery - solve_text.get_height() // 2))

    reset_button = pygame.Rect(350, HEIGHT - 60, 200, 50)
    pygame.draw.rect(SCREEN, BLUE, reset_button, border_radius=10)
    reset_text = BUTTON_FONT.render("Reset", True, WHITE)
    SCREEN.blit(reset_text, (reset_button.centerx - reset_text.get_width() // 2,
                             reset_button.centery - reset_text.get_height() // 2))

    # Display solve time if available
    if solve_time is not None:
        time_text = TIME_FONT.render(f"Solve Time: {solve_time:.2f} seconds", True, GREEN)
        SCREEN.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT - 100))

    pygame.display.flip()

def is_valid(board, num, pos, n):
    for i in range(n):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(n):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_size = int(n ** 0.5)
    box_x, box_y = pos[1] // box_size, pos[0] // box_size
    for i in range(box_y * box_size, box_y * box_size + box_size):
        for j in range(box_x * box_size, box_x * box_size + box_size):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty(board, n):
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve(board, n):
    empty = find_empty(board, n)
    if not empty:
        return True
    row, col = empty
    for num in range(1, n + 1):
        if is_valid(board, num, (row, col), n):
            board[row][col] = num
            draw_board(board, n, (row, col))
            pygame.time.delay(25)
            if solve(board, n):
                return True
            board[row][col] = 0
            draw_board(board, n, (row, col))
            pygame.time.delay(25)
    return False

def main():
    n = 9
    if int(n ** 0.5) ** 2 != n:
        print("Board size must be a perfect square (e.g., 4x4, 9x9)")
        return

    board = create_empty_board(n)
    fill_random_cells(board, n, k=random.randint(10, 20))
    solve_time = None

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 50 <= pos[0] <= 250 and HEIGHT - 80 <= pos[1] <= HEIGHT - 30:
                    start_time = time.time()
                    solve(board, n)
                    end_time = time.time()
                    solve_time = end_time - start_time
                if 350 <= pos[0] <= 550 and HEIGHT - 80 <= pos[1] <= HEIGHT - 30:
                    board = create_empty_board(n)
                    fill_random_cells(board, n, k=random.randint(10, 20))
                    solve_time = None

        draw_board(board, n, solve_time=solve_time)

    pygame.quit()

if __name__ == "__main__":
    main()
