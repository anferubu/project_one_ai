from collections import deque

import numpy as np

from constant import Constant



class BFS(Constant):
    """
    Class that implements the Breadth-Preferring Search (BFS) algorithm.
    This algorithm is complete because it always finds an answer (if it
    exists), but it does not guarantee that the result is optimal.
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


    def solve(self) -> list|str:
        """
        Implements the BFS algorithm.This implementation avoids returning
        to already visited nodes.

        Returns:
            (List): path from the start position to the end position.
        """
        self._initialize()

        # Enqueue the starting position and mark it as visited.
        self._add_to_queue(self.start)
        self._mark_visited(self.start)

        while self.queue:
            current = self.queue.popleft()
            if self._is_goal(current):
                break
            self._explore_neighbors(current)
        return self._backtrack()


    def solve_zigzag(self) -> list|str:
        """
        Implements the BFS algorithm in a zigzag pattern. For this, it
        uses a list and takes out the nodes from the extreme left or right
        depending on the level.

        This implementation avoids returning to already visited nodes.

        Returns:
            (List): path from the start position to the end position.
        """
        self._initialize()

        # Enqueue the starting position and mark it as visited.
        self._add_to_queue(self.start)
        self._mark_visited(self.start)

        # Initialize a variable to keep track of the direction.
        # 1 for left to right, -1 for right to left.
        direction = 1

        while self.queue:
            if direction == 1:
                current = self.queue.popleft()
            else:
                current = self.queue.pop()
            if self._is_goal(current):
                break
            self._explore_neighbors(current, direction)

            # Change direction if the queue is not empty.
            if self.queue:
                direction *= -1

        return self._backtrack()


    def _initialize(self):
        """
        Initializes the queue, the visited set and the parent dictionary
        to keep track of the path.
        """
        self.queue = deque()
        self.visited = set()
        self.parent = {self.start: None}


    def _is_goal(self, position:tuple[int, int]) -> bool:
        """
        Evaluates if a given position is the goal.

        Args:
            position (tuple): a specific position within the maze.

        Returns:
            bool: True if the position is the goal.
        """
        return position == self.goal


    def _explore_neighbors(self, current:tuple[int, int], dir:int|None=None):
        """
        Evaluates neighboring cells from a given position based on
        possible moves.

        Args:
            current (tuple): a specific position within the maze.
            dir (int): indicates the search direction.
                         1 or None: from left to right.
                        -1: from right to left.
        """
        # Define the possible moves: ↑, →, ↓, ←
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for move in moves:
            # Calculates the next position according to the movement.
            next_pos = (current[0] + move[0], current[1] + move[1])

            if self._is_valid_position(next_pos):
                self._mark_visited(next_pos)
                self._add_to_queue(next_pos, dir)
                self._set_parent(next_pos, current)


    def _is_valid_position(self, position:tuple[int, int]) -> bool:
        """
        Evaluates if the new position is within the bounds of the matrix
        and if the new position hasn't been visited and isn't a wall.

        Args:
            position (tuple): a specific position within the maze.

        Returns:
            bool: True if the position is valid, that is, it's inside the
                  matrix, it hasn't been visited and it's not a wall.
        """
        return (
            (0 <= position[0] < self.maze.shape[0])
            and (0 <= position[1] < self.maze.shape[1])
            and position not in self.visited
            and self.maze[position] != self.WALL
        )


    def _mark_visited(self, position:tuple[int, int]):
        """
        Evaluates if a given position has been visited.

        Args:
            position (tuple): a specific position within the maze.

        Returns:
            bool: True if the position has been visited.
        """
        self.visited.add(position)


    def _add_to_queue(self, position:tuple[int, int], dir:int|None=None):
        """
        Adds a position to the queue.

        Args:
            position (tuple): a specific position within the maze.
            dir (int): indicates the search direction.
                         1 or None: from left to right.
                        -1: from right to left.
        """
        if dir == None or dir == 1:
            self.queue.append(position)
        else:
            self.queue.appendleft(position)


    def _set_parent(self, child:tuple[int, int], parent:tuple[int, int]):
        """
        Sets a position as parent of another cell in the maze.

        Args:
            child (tuple): a specific position within the maze.
            parent (tuple): a specific position within the maze.
        """
        self.parent[child] = parent


    def _backtrack(self) -> list|str:
        """
        Backtrack from the goal to the start to find the path.
        """
        path = []
        current = self.goal

        while current is not self.start:
            path.append(current)

            # If goal is not a dict key, there is no path from start to goal.
            try:
                current = self.parent[current]
            except KeyError:
                return 'No existe una solución'

        path.append(self.start)
        path.reverse()

        return path



if __name__ == '__main__':

    # Open the file with a matrix
    maze = BFS('./data/matrix.txt')

    # Find the path from the start to the goal
    print("Solution BFS normal: ", maze.solve())
    print("Solution BFS intercalado: ", maze.solve_zigzag())