import numpy as np
from copy import deepcopy

# Helper functions
def manhattan_distance(state, goal):
    """Calculate the Manhattan Distance heuristic."""
    distance = 0
    for i in range(1, 9):  # Skip the empty tile (0)
        x1, y1 = np.where(state == i)
        x2, y2 = np.where(goal == i)
        distance += abs(x1[0] - x2[0]) + abs(y1[0] - y2[0])
    return distance

def misplaced_tiles(state, goal):
    """Calculate the number of misplaced tiles heuristic."""
    return np.sum((state != goal) & (state != 0))  # Exclude the empty tile (0)

def get_neighbors(state):
    """Generate all possible neighbor states."""
    neighbors = []
    x, y = np.where(state == 0)  # Find the position of the empty tile
    x, y = x[0], y[0]
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = deepcopy(state)
            new_state[x, y], new_state[nx, ny] = new_state[nx, ny], new_state[x, y]
            neighbors.append(new_state)
    return neighbors

def hill_climbing(initial, goal, heuristic):
    """Solve the 8 Puzzle problem using Hill Climbing."""
    current_state = initial
    steps = [current_state]  # Track the steps taken
    current_score = heuristic(current_state, goal)

    while True:
        neighbors = get_neighbors(current_state)
        neighbor_scores = [(neighbor, heuristic(neighbor, goal)) for neighbor in neighbors]
        neighbor_scores.sort(key=lambda x: x[1])  # Sort by heuristic value (ascending)
        best_neighbor, best_score = neighbor_scores[0]

        if best_score >= current_score:  # No improvement (local maxima or plateau)
            return steps, current_state, False  # Failed to find the goal
        if np.array_equal(best_neighbor, goal):  # Goal state reached
            steps.append(best_neighbor)
            return steps, best_neighbor, True

        # Move to the best neighbor
        current_state = best_neighbor
        current_score = best_score
        steps.append(current_state)

# Example usage
initial_state = np.array([[7, 2, 4],
                           [5, 0, 6],
                           [8, 3, 1]])
goal_state = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 0]])

