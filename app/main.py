# BFS algorithm
# Find the shortest path. It doesn't take cost into account.
# In the matrix:
#   - Agent: 0
#   - Goal: 4
#   - Wall: -1
#   - Enemies: 2, 3


import numpy as np
from collections import deque

# Load maze from file
maze = np.loadtxt('./data/matrix.txt', dtype=int)

# Define the possible moves: ↑, →, ↓, ←
moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Define the start and goal positions
start = tuple(np.argwhere(maze == 0)[0])
goal = tuple(np.argwhere(maze == 4)[0])

# Initialize the queue and the visited set
queue = deque()
visited = set()

# Enqueue the starting position and mark it as visited
queue.append(start)
visited.add(start)

# Initialize the parent dictionary to keep track of the path
parent = {
    start: None
}

# Initialize a variable to keep track of the direction
direction = 1  # 1 for left to right, -1 for right to left

# BFS algorithm
num_nodes_at_level = 1
current_level_nodes = [start]
while queue:
    print("Current level: ", current_level_nodes)
    # Dequeue current node from left or right end of the queue
    if direction == 1:
        current = queue.popleft()
    else:
        current = queue.pop()
    # Evaluates if the node is the goal
    if current[0] == goal[0] and current[1] == goal[1]:
        break
    for move in moves:
        # Calculates the next position according to the movement
        next_pos = (current[0] + move[0], current[1] + move[1])
        # If the new position is within the bounds of the matrix
        # maze.shape[0] is the number of rows, maze.shape[1] is cols
        if (0 <= next_pos[0] < maze.shape[0]) and (0 <= next_pos[1] < maze.shape[1]):
            # If the new position has not been visited and is not a wall
            if next_pos not in visited and maze[next_pos] != -1:
                # Add the new position to the queue and to the list of visited nodes
                if direction == 1:
                    queue.append(next_pos)
                else:
                    queue.appendleft(next_pos)
                visited.add(next_pos)
                # The parent of the next position is the current node
                parent[next_pos] = current

    # Change direction if the queue is not empty
    if queue:
        direction *= -1

    # Update the current level of the tree
    current_level_nodes = [pos for pos in parent.keys() if parent[pos] == current]
    num_nodes_at_level = len(current_level_nodes)

    # If the current level is empty, it means that there are no more nodes to visit
    if num_nodes_at_level == 0:
        break

# Backtrack from the goal to the start to find the path
path = []
current = goal
while current is not start:
    path.append(current)
    current = parent[current]
path.append(start)
path.reverse()

# Print the path
print("Shortest path: ", path)