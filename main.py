import pygame
import random
import time
import math
from grid import create_base_grid
from pacman import Pacman
from astarghost import get_next_move as astar_move
from randomghost import random_ghost_move
from minimaxghost import find_best_move as minimax_move
from escape import scaredghost
from qmanager import QManager

ACTIONS = ['ASTAR', 'RANDOM', 'MINIMAX', 'SCARED']
epsilon = 0.1
discount = 0.9
learning_rate = 0.1

# Initialize QManagers for each ghost
qmanagers = {
    "ASTAR": QManager(),
    "RANDOM": QManager(),
    "MINIMAX": QManager(),
    "SCARED": QManager()
}
qfiles = {
    "ASTAR": "qtable_astar.pkl",
    "RANDOM": "qtable_random.pkl",
    "MINIMAX": "qtable_minimax.pkl",
    "SCARED": "qtable_scared.pkl"
}
for key in qmanagers:
    qmanagers[key].load(qfiles[key])

# Initialize grid and Pacman
GRID = create_base_grid()
pacman = Pacman(1, 1)
pacman.auto_mode = False  # Disable auto-movement for Pac-Man since we're using keyboard input

ghost_positions = {
    "ASTAR": (2, 2),
    "RANDOM": (3, 3),
    "SCARED": (4, 4),
    "MINIMAX": (2, 5)
}
prev_scared_pos = ghost_positions["SCARED"]
ghost_respawn_time = 0  # Single timer for all ghosts
all_ghosts_eaten = False

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
LIGHT_BLUE = (100, 100, 255)
SCARED_COLOR = (150, 150, 255)  # Light blue for scared ghosts
POWERED_COLOR = (200, 200, 255)  # Light blue-white for powered ghosts
POWER_PELLET_COLOR = (255, 105, 180)  # Bright pink for power pellets

def get_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def calculate_reward(prev_distance, new_distance, pacman_state, pacman_caught=False, ghost_eaten=False):
    if pacman_caught:
        return 10
    elif ghost_eaten:
        return -10
    if pacman_state == "NORMAL":
        return 1 if new_distance < prev_distance else -1
    else:
        return -1 if new_distance < prev_distance else 1

def choose_action(state, q_table):
    if state not in q_table:
        q_table[state] = {a: 0 for a in ACTIONS}
    return random.choice(ACTIONS) if random.random() < epsilon else max(q_table[state], key=q_table[state].get)

def update_q_table(state, action, reward, next_state, q_table):
    if state not in q_table:
        q_table[state] = {a: 0 for a in ACTIONS}
    if next_state not in q_table:
        q_table[next_state] = {a: 0 for a in ACTIONS}
    max_next_q = max(q_table[next_state].values())
    q_table[state][action] += learning_rate * (reward + discount * max_next_q - q_table[state][action])

def get_state(pacman, ghost_pos):
    return (pacman.x, pacman.y, ghost_pos[0], ghost_pos[1], pacman.state)

def perform_action(action, ghost_pos, pacman_pos, grid, prev=None, depth=4):
    if action == 'ASTAR':
        return astar_move(grid, ghost_pos, pacman_pos)
    elif action == 'RANDOM':
        return random_ghost_move(grid, ghost_pos, pacman_pos)
    elif action == 'MINIMAX':
        return minimax_move(grid, ghost_pos, pacman_pos, depth=4)
    elif action == 'SCARED':
        return scaredghost(grid, ghost_pos, pacman_pos, prev=prev or (-1, -1))
    return ghost_pos

GRID_SIZE = 25  # Keep it small to fit more of the grid
NUM_ROWS = len(GRID)
NUM_COLS = len(GRID[0])

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

GRID_OFFSET_X = (SCREEN_WIDTH - NUM_COLS * GRID_SIZE) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - NUM_ROWS * GRID_SIZE) // 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pacman RL Game')

def draw_ghost(surface, rect, ghost_type, scared=False, powered=False):
    center = rect.center

    if powered:
        # Draw all ghosts with special powered color (not black)
        color = POWERED_COLOR
        pygame.draw.circle(surface, color, rect.center, rect.width // 2)

        # Ghost bottom wavy part
        points = []
        for x in range(rect.left, rect.right + 1, 5):
            y_offset = 3 * math.sin((x - rect.left) * math.pi * 2 / rect.width)
            points.append((x, rect.bottom - y_offset))
        points.append((rect.right, rect.bottom))
        points.append((rect.left, rect.bottom))
        pygame.draw.polygon(surface, color, points)

        # Eyes (still visible but different)
        eye_radius = rect.width // 6
        pupil_radius = rect.width // 10
        # Left eye
        pygame.draw.circle(surface, WHITE, (center[0] - 5, center[1] - 5), eye_radius)
        pygame.draw.circle(surface, BLUE, (center[0] - 5, center[1] - 5), pupil_radius)
        # Right eye
        pygame.draw.circle(surface, WHITE, (center[0] + 5, center[1] - 5), eye_radius)
        pygame.draw.circle(surface, BLUE, (center[0] + 5, center[1] - 5), pupil_radius)
    elif scared:
        # Draw scared ghost with semi-transparent body
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.circle(s, (*SCARED_COLOR, 200), (rect.width // 2, rect.height // 2), rect.width // 2)

        # Ghost bottom wavy part
        points = []
        for x in range(rect.left, rect.right + 1, 5):
            y_offset = 3 * math.sin((x - rect.left) * math.pi * 2 / rect.width)
            points.append((x, rect.bottom - y_offset))
        points.append((rect.right, rect.bottom))
        points.append((rect.left, rect.bottom))
        pygame.draw.polygon(s, (*SCARED_COLOR, 200), points)

        surface.blit(s, rect)

        # Scared eyes (wide and nervous)
        eye_radius = rect.width // 8
        # Left eye (wide open)
        pygame.draw.circle(surface, WHITE, (center[0] - 5, center[1] - 3), eye_radius)
        pygame.draw.circle(surface, BLACK, (center[0] - 5, center[1] - 3), eye_radius // 2)
        # Right eye (wide open)
        pygame.draw.circle(surface, WHITE, (center[0] + 5, center[1] - 3), eye_radius)
        pygame.draw.circle(surface, BLACK, (center[0] + 5, center[1] - 3), eye_radius // 2)

        # Scared mouth (zigzag)
        mouth_points = [
            (center[0] - 8, center[1] + 5),
            (center[0] - 4, center[1] + 8),
            (center[0], center[1] + 5),
            (center[0] + 4, center[1] + 8),
            (center[0] + 8, center[1] + 5)
        ]
        pygame.draw.lines(surface, BLACK, False, mouth_points, 2)
    else:
        # Regular ghost appearance
        if ghost_type == "ASTAR":
            color = RED
        elif ghost_type == "RANDOM":
            color = CYAN
        elif ghost_type == "MINIMAX":
            color = ORANGE

        pygame.draw.circle(surface, color, center, rect.width // 2)

        # Ghost bottom wavy part
        points = []
        for x in range(rect.left, rect.right + 1, 5):
            y_offset = 3 * math.sin((x - rect.left) * math.pi * 2 / rect.width)
            points.append((x, rect.bottom - y_offset))
        points.append((rect.right, rect.bottom))
        points.append((rect.left, rect.bottom))
        pygame.draw.polygon(surface, color, points)

        # Regular eyes
        eye_radius = rect.width // 6
        pupil_radius = rect.width // 10
        # Left eye
        pygame.draw.circle(surface, WHITE, (center[0] - 5, center[1] - 5), eye_radius)
        pygame.draw.circle(surface, BLACK, (center[0] - 5, center[1] - 5), pupil_radius)
        # Right eye
        pygame.draw.circle(surface, WHITE, (center[0] + 5, center[1] - 5), eye_radius)
        pygame.draw.circle(surface, BLACK, (center[0] + 5, center[1] - 5), pupil_radius)

def draw_grid(grid, pacman, ghost_positions):
    screen.fill(BLACK)

    # Draw grid lines
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            rect = pygame.Rect(GRID_OFFSET_X + j * GRID_SIZE, GRID_OFFSET_Y + i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            center = rect.center

            # Draw pellets
            if cell == 2:  # Normal pellet
                pygame.draw.circle(screen, WHITE, center, GRID_SIZE // 6)
            elif cell == 3:  # Power pellet (changed to pink)
                pygame.draw.circle(screen, POWER_PELLET_COLOR, center, GRID_SIZE // 4)
            elif cell == 1:  # Wall
                pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.rect(screen, (0, 0, 100), rect, 2)  # Wall border

    # Draw ghosts
    for ghost_type, pos in ghost_positions.items():
        if pos:
            ghost_rect = pygame.Rect(
                GRID_OFFSET_X + pos[1] * GRID_SIZE,
                GRID_OFFSET_Y + pos[0] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            # Draw ghost with special color when Pacman is powered
            draw_ghost(screen, ghost_rect, ghost_type,
                       scared=(ghost_type == "SCARED"),
                       powered=(pacman.state == "POWERED"))

    # Draw Pacman with open/close mouth animation
    pacman_rect = pygame.Rect(
        GRID_OFFSET_X + pacman.y * GRID_SIZE,
        GRID_OFFSET_Y + pacman.x * GRID_SIZE,
        GRID_SIZE, GRID_SIZE
    )

    # Mouth angle changes over time for animation
    mouth_angle = (math.sin(time.time() * 5) * 0.4 + 0.6) * math.pi

    # Draw Pacman as a pie shape
    pygame.draw.arc(screen, YELLOW, pacman_rect, -mouth_angle / 2, mouth_angle / 2, 0)
    pygame.draw.line(screen, YELLOW, pacman_rect.center,
                     (pacman_rect.center[0] + GRID_SIZE // 2 * math.cos(-mouth_angle / 2),
                      pacman_rect.center[1] + GRID_SIZE // 2 * math.sin(-mouth_angle / 2)), 2)
    pygame.draw.line(screen, YELLOW, pacman_rect.center,
                     (pacman_rect.center[0] + GRID_SIZE // 2 * math.cos(mouth_angle / 2),
                      pacman_rect.center[1] + GRID_SIZE // 2 * math.sin(mouth_angle / 2)), 2)

    # Pacman eye
    eye_pos = (pacman_rect.center[0], pacman_rect.center[1] - GRID_SIZE // 4)
    pygame.draw.circle(screen, BLACK, eye_pos, GRID_SIZE // 10)

    pygame.display.update()

def respawn_ghosts():
    """Respawn all ghosts only when all are eaten, after 2 seconds"""
    global ghost_positions, all_ghosts_eaten, ghost_respawn_time

    # Check if all ghosts are eaten
    if all(pos is None for pos in ghost_positions.values()) and not all_ghosts_eaten:
        all_ghosts_eaten = True
        ghost_respawn_time = time.time()

    # If all were eaten and 2 seconds have passed
    if all_ghosts_eaten and time.time() - ghost_respawn_time >= 2:
        # Choose respawn positions
        respawn_positions = [(2, 2), (3, 3), (4, 4), (2, 5)]
        random.shuffle(respawn_positions)

        for i, ghost_type in enumerate(ghost_positions.keys()):
            ghost_positions[ghost_type] = respawn_positions[i]
            if ghost_type == "SCARED":
                prev_scared_pos = respawn_positions[i]

        all_ghosts_eaten = False

def game_loop():
    global prev_scared_pos, ghost_positions, ghost_respawn_time, all_ghosts_eaten

    num_episodes = 100
    clock = pygame.time.Clock()
    FPS = 2  # Controls game speed

    for episode in range(num_episodes):
        GRID = create_base_grid()
        pacman.x, pacman.y = 1, 1
        ghost_positions = {
            "ASTAR": (2, 2),
            "RANDOM": (3, 3),
            "SCARED": (4, 4),
            "MINIMAX": (2, 5)
        }
        prev_scared_pos = ghost_positions["SCARED"]
        ghost_respawn_time = 0
        all_ghosts_eaten = False

        game_over = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for key in qmanagers:
                        qmanagers[key].save(qfiles[key])
                    pygame.quit()
                    exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                pacman.move("UP", GRID)
            elif keys[pygame.K_s]:
                pacman.move("DOWN", GRID)
            elif keys[pygame.K_a]:
                pacman.move("LEFT", GRID)
            elif keys[pygame.K_d]:
                pacman.move("RIGHT", GRID)

            # Check for ghost respawning (only when all are eaten)
            respawn_ghosts()

            draw_grid(GRID, pacman, ghost_positions)

            for ghost_type in list(ghost_positions.keys()):
                ghost_pos = ghost_positions[ghost_type]
                if ghost_pos is None:
                    continue

                qman = qmanagers[ghost_type]
                q_table = qman.q_table

                state = get_state(pacman, ghost_pos)
                prev_distance = get_distance(ghost_pos, (pacman.x, pacman.y))
                action = choose_action(state, q_table)

                new_pos = perform_action(action, ghost_pos, (pacman.x, pacman.y), GRID,
                                         prev=prev_scared_pos if ghost_type == "SCARED" else None)

                new_distance = get_distance(new_pos, (pacman.x, pacman.y))

                pacman_caught = new_pos == (pacman.x, pacman.y) and pacman.state == "NORMAL"
                ghost_eaten = new_pos == (pacman.x, pacman.y) and pacman.state == "POWERED"

                reward = calculate_reward(prev_distance, new_distance, pacman.state, pacman_caught, ghost_eaten)
                next_state = get_state(pacman, new_pos)
                update_q_table(state, action, reward, next_state, q_table)

                if pacman_caught:
                    print(f"Pacman caught by {ghost_type} ghost! Game Over.")
                    game_over = True
                    break
                elif ghost_eaten:
                    print(f"{ghost_type} ghost eaten!")
                    ghost_positions[ghost_type] = None
                    if ghost_type == "SCARED":
                        prev_scared_pos = None
                else:
                    ghost_positions[ghost_type] = new_pos
                    if ghost_type == "SCARED":
                        prev_scared_pos = ghost_pos

            pacman.update_power_state()
            clock.tick(FPS)

            if game_over:
                time.sleep(2)
                break

            if all(cell not in (2, 3) for row in GRID for cell in row):
                print(f"All pellets eaten in episode {episode + 1}")
                time.sleep(1)
                break

    # Save Q-tables when done
    for key in qmanagers:
        qmanagers[key].save(qfiles[key])
    pygame.quit()

if __name__ == "__main__":
    game_loop()