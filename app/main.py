from bfs import BFS
from gui import Board


if __name__ == '__main__':
    # Open the file with a matrix
    maze = BFS('./data/matrix2.txt')

    # Define the matrix and the path
    matrix = maze.matrix
    path = maze.solve_zigzag()  # .solve() for normal BFS

    # Run the app
    app = Board(matrix, path)
    app.window.mainloop()