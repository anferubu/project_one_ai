import numpy as np

from constant import Constant



class Maze(Constant):
    """
    Class that represents a maze.
    """

    def __init__(self, filename:str):
        """
        Initializes the class instance with a numeric matrix from a file.

        Args:
            filename (str): path to the file with the numeric matrix
                            representing the maze.
        """
        # Load maze from file.
        self.maze = np.loadtxt(filename, dtype=int)
        self.matrix = self.maze.tolist()

        # Define the start and goal positions.
        self.start = tuple(np.argwhere(self.maze == self.PINOCCHIO)[0])
        self.goal = tuple(np.argwhere(self.maze == self.GEPETTO)[0])