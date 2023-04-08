from queue import PriorityQueue

from constant import Constant
from maze import Maze



class UCS(Constant):
    """
    Class that implements the Uniform-Cost Search algorithm.
    This algorithm is complete and optimal, meaning that it finds the
    shortest path if it exists.
    """

    def __init__(self, maze:Maze):
        """
        Initializes the class instance.

        Args:
            maze (Maze): Maze instance that represents the board.
        """
        self.maze = maze.maze
        self.start = maze.start
        self.goal = maze.goal


    def solve(self) -> list|str:
        """
        Implements the Uniform-Cost Search algorithm.

        Returns:
            (List): path from the start position to the end position.
        """
        self._initialize()

        # Enqueue the starting position and mark it as visited.
        self._add_to_queue(self.start, 0)
        self._mark_visited(self.start)

        while self.queue:
            current_cost, current = self.queue.get()
            if self._is_goal(current):
                break
            self._explore_neighbors(current, current_cost)

        return self._backtrack()


    def _initialize(self):
        """
        Initializes the queue, the visited set and the parent dictionary
        to keep track of the path.
        """
        self.queue = PriorityQueue()
        self.visited = set()
        self.visited_list = []
        self.parent = {self.start: None}
        self.cost_so_far = {self.start: 0}


    def _add_to_queue(self, position:tuple[int, int], cost:int):
        """
        Adds a position to the queue.

        Args:
            position (tuple): a specific position within the maze.
            cost (int): the cost of the current path to reach this position.
        """
        self.queue.put((cost, position))


    def _explore_neighbors(self, current:tuple[int, int], current_cost:int):
        """
        Evaluates neighboring cells from a given position based on
        possible moves.

        Args:
            current (tuple): a specific position within the maze.
            current_cost (int): the cost of the current path to reach this position.
        """
        # Define the possible moves: ↑, →, ↓, ←
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for move in moves:
            # Calculates the next position according to the movement.
            next_pos = (current[0] + move[0], current[1] + move[1])

            if self._is_valid_position(next_pos):
                # Calculate the cost of the new path and add it to the queue.
                new_cost = current_cost + self.maze[next_pos]
                self._add_to_queue(next_pos, new_cost)

                # Mark the cell as visited.
                self._mark_visited(next_pos)

                # Update the parent dictionary and the cost_so_far dictionary.
                self._set_parent(next_pos, current)
                self.cost_so_far[next_pos] = new_cost


    def _is_valid_position(self, position:tuple[int, int]) -> bool:
        """
        Checks if a position is within the maze and is not an obstacle.

        Args:
        position (tuple): a specific position within the maze.

        Returns:
            (bool): True if the position is valid, False otherwise.
        """
        return (
            (0 <= position[0] < self.maze.shape[0])
            and (0 <= position[1] < self.maze.shape[1])
            and position not in self.visited
            and self.maze[position] != self.WALL
        )


    def _is_goal(self, position:tuple[int, int]) -> bool:
        """
        Checks if a position is the goal.

        Args:
            position (tuple): a specific position within the maze.

        Returns:
            (bool): True if the position is the goal, False otherwise.
        """
        return position == self.goal


    def _mark_visited(self, position:tuple[int, int]):
        """
        Marks a position as visited.

        Args:
            position (tuple): a specific position within the maze.
        """
        self.visited.add(position)
        self.visited_list.append(position)


    def _set_parent(self, child:tuple[int, int], parent:tuple[int, int]):
        """
        Sets the parent of a given position.

        Args:
            child (tuple): a specific position within the maze.
            parent (tuple): a specific position within the maze.
        """
        self.parent[child] = parent


    def _backtrack(self) -> list|str:
        """
        Backtracks from the goal position to the start position.

        Returns:
            (List): path from the start position to the end position.
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
        #path.reverse()

        return path



if __name__ == '__main__':

    # Open the file with a matrix
    maze = Maze('./data/matrix.txt')

    # Find the path from the start to the goal
    ucs = UCS(maze)
    print("Solution UCS: ", ucs.solve())