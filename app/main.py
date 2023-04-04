import numpy as np
from queue import Queue

# Load maze from file
maze = np.loadtxt('./matrix.txt', dtype=int)

print(maze)