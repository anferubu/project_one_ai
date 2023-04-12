from collections import deque
from constant import Constant
from maze import Maze



class IDS(Constant):
    """
    Class that implements the Breadth-Preferring Search (BFS) algorithm.
    This algorithm is complete because it always finds an answer (if it
    exists), but it does not guarantee that the result is optimal.
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


    def solve(self) -> list[tuple[int, int]]:
        """
        Implements the IDDFS algorithm.

        Returns:
            (List): path from the start position to the end position.
        """
        self._initialize()
        depth = 0
        while True:
            self.visited = set()
            self.queue = [self.start]
            if self._dfs(self.start, depth):
                return self._backtrack()
            depth += 1

    def _dfs(self, current:tuple[int,int], depth:int) -> bool:
        """
        Implements the Depth-First Search (DFS) algorithm.

        Args:
            position (Tuple): a specific position within the maze.
            depth (int): the maximum depth to explore.

        Returns:
            bool: True if the goal is found.
        """
        if depth == 0:
            return False

        if self._is_goal(current):
            return True

        self._mark_visited(self.start)

        

        return self._explore_neighbors(current, depth)

    def _explore_neighbors(self, current:tuple[int, int], depth:int) -> bool:
        """
        Evaluates neighboring cells from a given position based on
        possible moves.

        Args:
            current (tuple): a specific position within the maze.
        """
        # Define the possible moves: ↑, →, ↓, ←
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for move in moves:
            next_pos = (current[0] + move[0], current[1] + move[1])
            if self._is_valid_position(next_pos):
                self._add_to_queue(next_pos)
                self._mark_visited(next_pos)
                self._set_parent(next_pos, current)
                if self._dfs(next_pos, depth - 1):
                    return True
                self.queue.pop()
        return False

    def _initialize(self):
        """
        Initializes the queue, the visited set and the parent dictionary
        to keep track of the path.
        """
        self.queue = deque()
        self.visited = set()    # disordered, unique
        self.visited_list = []  # ordered
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
        self.visited_list.append(position)


    def _add_to_queue(self, position:tuple[int, int]):
        """
        Adds a position to the queue.

        Args:
            position (tuple): a specific position within the maze.
        """
        self.queue.append(position)
       


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
        #path.reverse()

        return path



if __name__ == '__main__':

    # Open the file with a matrix
    maze = Maze('./data/matrix.txt')

    # Find the path from the start to the goal
    ids = IDS(maze)
    path = ids.solve()
    print(path)