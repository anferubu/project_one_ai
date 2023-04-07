import time

from PIL import Image, ImageTk as I
import tkinter as tk
import tkinter.ttk as ttk

from constant import Constant



class Board(Constant):
    """
    Class that represents the GUI of the program. It consists of a board
    that shows the different characters and the path from Pinocchio to Gepetto.
    """

    TITLE = 'Unreported search methods'

    SQUARE_SIZE = 75;

    COLORS = {
        'border': '#243B5D',
        'empty': '#FFF',
        'wall': '#2D2D2D',
        'path': '#FAEDCB',
    }


    def __init__(self, matrix, path):
        self.matrix = matrix
        self.path = path
        self._initialize()
        self._display_board()


    def _initialize(self):
        empty = self.COLORS['empty']

        # Create the window
        self.window = tk.Tk()
        self.window.title(self.TITLE)
        self.window.resizable(False, False)

        # Create the canvas
        self.height = self.SQUARE_SIZE * len(self.matrix)
        self.width = self.SQUARE_SIZE * len(self.matrix[0])
        self.canvas = tk.Canvas(
            self.window, width=self.width, height=self.height)
        self.canvas.pack(padx=15, pady=15)

        # Create button to find the path from start to the goal
        self.find_path_btn = tk.Button(
            self.window, text='Find path', font=('Arial', 12), bg=empty,
            relief='groove', padx=15, pady=5, command=self._display_path)
        self.find_path_btn.pack(side=tk.LEFT, padx=15, pady=15)

        # Create button to clear the board
        self.clear_btn = tk.Button(
            self.window, text='Clear', font=('Arial', 12), relief='groove',
            padx=15, pady=5, bg=empty, command=self._display_board)
        self.clear_btn.pack(side=tk.LEFT, padx=15, pady=15)


    def _display_board(self):
        """
        Paint the board depending on the size of the cells and the
        defined colors.
        """
        empty = self.COLORS['empty']
        wall = self.COLORS['wall']
        border = self.COLORS['border']

        size = self.SQUARE_SIZE

        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                x1, y1 = (j * size), (i * size)
                x2, y2 = (x1 + size), (y1 + size)
                if value == self.WALL:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=wall, outline=border)
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=empty, outline=border)
                self.canvas.create_rectangle(
                    3, 3, self.width, self.height, fill='', outline=border,
                    width=2)
        self._set_images()


    def _set_images(self):
        size = self.SQUARE_SIZE
        sizes = (size, size)

        self.images = {
            self.PINOCCHIO: I.PhotoImage(
                Image.open("./images/pinocho.png").resize(sizes)),
            self.CIGAR: I.PhotoImage(
                Image.open("./images/cigarro.png").resize(sizes)),
            self.FOX: I.PhotoImage(
                Image.open("./images/zorro.png").resize(sizes)),
            self.GEPETTO: I.PhotoImage(
                Image.open("./images/gepeto.png").resize(sizes)),
        }

        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                if value not in [self.EMPTY, self.WALL]:
                    self.canvas.create_image(j*size, i*size,
                                             image=self.images[value],
                                             anchor="nw")


    def _display_path(self):
        self.find_path_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)

        path = self.COLORS['path']
        border = self.COLORS['border']

        size = self.SQUARE_SIZE

        for _, cell in enumerate(self.path):
            x, y = cell
            x1, y1 = (y * size), (x * size)
            x2, y2 = (x1 + size), (y1 + size)
            self.canvas.create_rectangle(x1, y1, x2, y2, width=1,
                                         fill=path, outline=border)
            self.canvas.create_rectangle(3, 3, self.width, self.height,
                                             fill='', outline=border, width=2)
            self._set_images()
            self.canvas.update()
            time.sleep(0.1)

        self.find_path_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.NORMAL)



if __name__ == '__main__':
    matrix = [[1,  3,  1,  3,  1],
              [0, -1,  1,  1,  1],
              [1,  1, -1, -1,  4],
              [1,  1,  1,  2,  1]]

    path = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (2, 4)]

    app = Board(matrix, path)
    app.window.mainloop()