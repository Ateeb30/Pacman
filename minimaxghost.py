class Bot2:
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g  # depth
        self.h = h  # evaluation score
        self.parent = parent

    def __lt__(self, other):
        return self.h < other.h

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def evaluate(ghost_pos, pacman_pos):
    return -manhattan_distance(ghost_pos[0], ghost_pos[1], pacman_pos[0], pacman_pos[1])

def minimax(bot, pacman_pos, depth, grid, alpha, beta, maximizing, visited=None):
    if visited is None:
        visited = set()

    if depth == 0 or (bot.x, bot.y) == pacman_pos:
        bot.h = evaluate((bot.x, bot.y), pacman_pos)
        return bot.h

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rows = len(grid)
    cols = len(grid[0])

    if maximizing:
        max_score = float("-inf")
        for dx, dy in directions:
            x = bot.x + dx
            y = bot.y + dy
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] in (2,3) and (x, y) not in visited:
                visited.add((x, y))
                child = Bot2(x, y, bot.g + 1, 0, bot)
                score = minimax(child, pacman_pos, depth - 1, grid, alpha, beta, False, visited.copy())
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return max_score

    else:
        min_score = float("inf")
        for dx, dy in directions:
            x = pacman_pos[0] + dx
            y = pacman_pos[1] + dy
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 0 and (x, y) not in visited:
                visited.add((x, y))
                score = minimax(bot, (x, y), depth - 1, grid, alpha, beta, True, visited.copy())
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return min_score

def find_best_move(grid, ghost_pos, pacman_pos, depth):
    best_val = float('-inf')
    best_move = ghost_pos

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rows = len(grid)
    cols = len(grid[0])

    for dx, dy in directions:
        x = ghost_pos[0] + dx
        y = ghost_pos[1] + dy
        if 0 <= x < rows and 0 <= y < cols and grid[x][y] in (2,3):
            bot = Bot2(x, y, 1, 0, None)
            move_val = minimax(bot, pacman_pos, depth - 1, grid, float('-inf'), float('inf'), False)
            if move_val > best_val:
                best_val = move_val
                best_move = (x, y)
    return best_move