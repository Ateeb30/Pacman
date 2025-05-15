import time
import heapq

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.state = "NORMAL"
        self.power_timer = 0
        self.auto_mode = False

    def move(self, direction, grid):
        dx, dy = 0, 0
        if direction == "UP":
            dx = -1
        elif direction == "DOWN":
            dx = 1
        elif direction == "LEFT":
            dy = -1
        elif direction == "RIGHT":
            dy = 1

        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            if grid[new_x][new_y] != 1:  # Not a wall
                self.x, self.y = new_x, new_y

                # Normal pellet
                if grid[self.x][self.y] == 2:
                    self.score += 10
                    grid[self.x][self.y] = 0

                # Power pellet
                elif grid[self.x][self.y] == 3:
                    self.score += 50
                    grid[self.x][self.y] = 0
                    self.state = "POWERED"
                    self.power_timer = 7  # Number of turns powered

    # Power mode countdown (always active while powered)
    def update_power_state(self):
        if self.state == "POWERED":
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.state = "NORMAL"

# A* algorithm to find the best path for Pac-Man
def get_distance(start, goal):
    # Manhattan distance between two points
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def a_star_pathfinding(grid, start, goal):
    # A* requires a priority queue to store nodes based on their cost
    open_list = []
    heapq.heappush(open_list, (0, start))  # (f_cost, (x, y))
    came_from = {}  # Tracks the path taken
    g_costs = {start: 0}  # Cost to reach each node
    f_costs = {start: get_distance(start, goal)}  # Estimated cost to reach goal from node

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()  # Reverse the path to get the correct order
            return path

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4 directions (up, down, left, right)
            neighbor = (x + dx, y + dy)

            # Check if the neighbor is within bounds and not a wall
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != 1:
                tentative_g_cost = g_costs[current] + 1  # 1 step cost

                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                    came_from[neighbor] = current
                    g_costs[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + get_distance(neighbor, goal)
                    f_costs[neighbor] = f_cost
                    heapq.heappush(open_list, (f_cost, neighbor))

    return []  # Return empty if no path found

def auto_move(self, grid):
    pacman_pos = (self.x, self.y)  # Pac-Man's current position
    nearest_pellet = None
    nearest_distance = float('inf')

    # Find the nearest pellet or power pellet
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 2 or cell == 3:  # Pellet (2) or Power Pellet (3)
                distance = get_distance(pacman_pos, (i, j))
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_pellet = (i, j)

    if nearest_pellet:
        # Use A* to find the path to the nearest pellet/power pellet
        path = a_star_pathfinding(grid, pacman_pos, nearest_pellet)

        # If a path is found, move Pac-Man along the path
        if path:
            next_pos = path[0]  # The next position in the path
            dx, dy = next_pos[0] - self.x, next_pos[1] - self.y
            if dx == -1:
                self.move("UP", grid)
            elif dx == 1:
                self.move("DOWN", grid)
            elif dy == -1:
                self.move("LEFT", grid)
            elif dy == 1:
                self.move("RIGHT", grid)
