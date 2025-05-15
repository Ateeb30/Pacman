import random

class bot3:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

def random_ghost_move(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    first = bot3(start[0], start[1])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    valid_moves = []
    for dx, dy in directions:
        nx = first.x + dx
        ny = first.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] in (2,3):
            valid_moves.append((nx, ny))

    # 60% chance to prioritize chasing when in same row or column
    if random.random() <= 0.6:
        if first.x == goal[0]:
            if goal[1] > first.y and (first.x, first.y + 1) in valid_moves:
                return (first.x, first.y + 1)
            elif goal[1] < first.y and (first.x, first.y - 1) in valid_moves:
                return (first.x, first.y - 1)
        elif first.y == goal[1]:
            if goal[0] > first.x and (first.x + 1, first.y) in valid_moves:
                return (first.x + 1, first.y)
            elif goal[0] < first.x and (first.x - 1, first.y) in valid_moves:
                return (first.x - 1, first.y)

    # Otherwise move randomly from valid directions
    if valid_moves:
        return random.choice(valid_moves)

    return (first.x, first.y)  # No move possible

