def create_base_grid():

    return [
        [2, 2, 3, 2, 1, 2, 2],
        [2, 1, 2, 2, 3, 2, 2],
        [2, 3, 2, 2, 2, 1, 2],
        [1, 2, 2, 1, 2, 1, 2],
        [2, 2, 3, 2, 3, 1, 2],
        [2, 1, 1, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2]
    ]


def initialize_entities():

    return {
       'P': (3, 3),    # Pac-M        'G1': (5, 1),   # Ghost 1
        'G2': (5, 6),   # Ghost 2
        'G3': (2, 5)    # Ghost 3
   }


def display_grid(static_grid, entities):

    grid = [row.copy() for row in static_grid]

    for entity, (x, y) in entities.items():
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            grid[x][y] = entity

    for row in grid:
        print(" ".join(row))
    print()
