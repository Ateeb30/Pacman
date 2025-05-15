import random

class bot4:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def manhattandistance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def scaredghost(grid, start, goal, prev):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)

    startnode = bot4(start[0], start[1])
    pellet_pos = None
    min_dist = float('inf')

    # Find the pellet that Pacman is closer to than the ghost
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 3:
                pac_dist = manhattandistance(goal[0], goal[1], i, j)
                ghost_dist = manhattandistance(startnode.x, startnode.y, i, j)
                if pac_dist < ghost_dist and ghost_dist < min_dist:
                    pellet_pos = (i, j)
                    min_dist = ghost_dist

    # Move away from that pellet
    best_move = None
    max_dist = -1

    for dx, dy in directions:
        nx, ny = startnode.x + dx, startnode.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] in (2,3) and (nx, ny) != prev:
            if pellet_pos:
                dist = manhattandistance(nx, ny, pellet_pos[0], pellet_pos[1])
                if dist > max_dist:
                    max_dist = dist
                    best_move = (nx, ny)

    if best_move:
        return best_move

    # Fallback: move randomly
    valid_moves = []
    for dx, dy in directions:
        nx, ny = startnode.x + dx, startnode.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and (nx, ny) != prev:
            valid_moves.append((nx, ny))

    if valid_moves:
        return random.choice(valid_moves)

    return (startnode.x, startnode.y)
