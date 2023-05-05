from collections import deque

from constant import Constant
from maze import Maze



class BFS(Constant):
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

        level = 0

        while self.queue:
            current = self.queue.popleft()
            if self.levels[current] > level:
                level = self.levels[current]
            if self._is_goal(current):
                break
            self._explore_neighbors(current, level)
            print(current)
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
        self._add_to_queue(self.start)
        self._mark_visited(self.start)

        direction = 1  # 1 for left to right, -1 for right to left.
        level = 0

        while self.queue:
            # Determine the level of the current to know its direction.
            current = self.queue[0] if direction == 1 else self.queue[-1]
            if self.levels[current] > level:
                level = self.levels[current]
                direction *= -1
            current = self.queue.popleft() if direction == 1 else self.queue.pop()
            print(f'{current} ({direction})')
            if self._is_goal(current):
                break
            self._explore_neighbors(current, level, direction)

        return self._backtrack()


    def _initialize(self):
        """
        Initializes the queue, the visited set and the parent dictionary
        to keep track of the path.
        """
        self.queue = deque()
        self.visited = set()    # disordered, unique
        self.visited_list = []  # ordered
        self.parent = {self.start: None}
        self.levels = {self.start: 0}  # the level of a node


    def _is_goal(self, position:tuple[int, int]) -> bool:
        """
        Evaluates if a given position is the goal.

        Args:
            position (tuple): a specific position within the maze.

        Returns:
            bool: True if the position is the goal.
        """
        return position == self.goal


    def _explore_neighbors(self, current:tuple[int, int], level:int|None=None, dir:int|None=None):
        """
        Evaluates neighboring cells from a given position based on
        possible moves.

        Args:
            current (tuple): a specific position within the maze.
            level (int): indicates the level of the current node.
            dir (int): indicates the search direction.
                         1 or None: from left to right.
                        -1: from right to left.
        """
        # Define the possible moves: ↑, →, ↓, ←
        if dir == None or dir == 1:
            moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        else:
            moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for move in moves:
            # Calculates the next position according to the movement.
            next_pos = (current[0] + move[0], current[1] + move[1])

            if self._is_valid_position(next_pos):
                self._mark_visited(next_pos)
                self._add_to_queue(next_pos, dir)
                self._set_parent(next_pos, current)

                # Set the level of the next position.
                self.levels[next_pos] = level + 1


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
        #path.reverse()

        return path



if __name__ == '__main__':

    # Open the file with a matrix
    maze = Maze('./data/matrix.txt')

    # Find the path from the start to the goal
    bfs = BFS(maze)
    print("Solution BFS normal: ", bfs.solve())
    print("Solution BFS intercalado: ", bfs.solve_zigzag())