import heapq

class Bot1:
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        # testing

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]

def Astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    openlist = []
    visited = set()

    h_start = manhattan_distance(*start, *goal)
    startnode = Bot1(start[0], start[1], 0, h_start)
    heapq.heappush(openlist, startnode)

    while openlist:
        curr = heapq.heappop(openlist)

        if (curr.x, curr.y) == goal:
            return reconstruct_path(curr)

        if (curr.x, curr.y) in visited:
            continue
        visited.add((curr.x, curr.y))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = curr.x + dx, curr.y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != 1:  # not a wall
                    new_g = curr.g + 1
                    new_h = manhattan_distance(nx, ny, goal[0], goal[1])
                    new_node = Bot1(nx, ny, new_g, new_h, curr)
                    heapq.heappush(openlist, new_node)

    return []  # no path found

def get_next_move(grid, ghost_pos, pacman_pos):
    path = Astar(grid, ghost_pos, pacman_pos)
    if len(path) >= 2:
        return path[1]  # path[0] is current position, path[1] is next
    return ghost_pos  # no movement
