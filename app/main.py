from bfs import BFS
from gui import Board
from maze import Maze


if __name__ == '__main__':
    # Open the file with a matrix
    maze = Maze('./data/matrix2.txt')

    # Define the matrix
    matrix = maze.matrix

    # Define the path
    bfs = BFS(maze)
    path = bfs.solve_zigzag()  # .solve() for normal BFS

    # Run the app
    app = Board(matrix, path)
    app.window.mainloop()