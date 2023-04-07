import time

from PIL import Image, ImageTk as I
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

from constant import Constant

from maze import Maze
from bfs import BFS



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
        'path': '#7EF5FF',
    }


    def __init__(self, file):
        self._charge_file(file)

        self._initialize()
        self._display_board()

    def _charge_file(self, file):
         # Open the file with a matrix
        self.maze = Maze(file)

        # Define the matrix
        self.matrix = self.maze.matrix

    def _initialize(self):
        empty = self.COLORS['empty']

        # Create the window
        self.window = tk.Tk()
        self.window.title(self.TITLE)
        self.window.resizable(False, False)

        # Create the canvas
        self.canvas = tk.Canvas(
            self.window)
        self.canvas.pack(padx=15, pady=15)

        self.options = tk.Frame(self.window)
        self.options.pack(padx=15, pady=15)

        # Create the radio buttons for select the algorithm.
        self.opcion = tk.IntVar()
        tk.Radiobutton(
            self.options, text="Amplitud", variable=self.opcion, value=1, font=('Arial', 12)
            ).pack()
        tk.Radiobutton(
            self.options, text="Amplitud 2.0 (zig zag)", variable=self.opcion, value=2, font=('Arial', 12)
            ).pack()
        tk.Radiobutton(
            self.options, text="Opción 3", variable=self.opcion, value=3, font=('Arial', 12)
            ).pack()
        
        self.buttons = tk.Frame(self.window)
        self.buttons.pack(side=tk.BOTTOM)

        # Create button to select the txt matrix file.
        self.select_button = tk.Button(
            self.buttons, text='Select file', font=('Arial', 12), bg=empty,
            relief='groove', padx=15, pady=5, command=self._choose_file)
        self.select_button.pack(side=tk.LEFT, padx=15, pady=15)

        # Create button to find the path from start to the goal
        self.find_path_btn = tk.Button(
            self.buttons, text='Find path', font=('Arial', 12), bg=empty,
            relief='groove', padx=15, pady=5, command=self._find_path)
        self.find_path_btn.pack(side=tk.LEFT, padx=15, pady=15)

        
        # Create button to clear the board
        self.clear_btn = tk.Button(
            self.buttons, text='Clear', font=('Arial', 12), relief='groove',
            padx=15, pady=5, bg=empty, command=self._display_board)
        self.clear_btn.pack(side=tk.LEFT, padx=15, pady=15)

    def _find_path(self):
        option = self.opcion.get()
        
        if(option == 0):
            messagebox.showerror(message="Debe seleccionar una de las opciones.", title="Error")
            return
        # Define the path
        self.bfs = BFS(self.maze)

        METHODS = {
            1: self.bfs.solve,
            2: self.bfs.solve_zigzag
        }

        self.path = METHODS[option]()

        self._display_board()
        self._display_path()
        

    def _choose_file(self):
        # Launch the file selector.
        file_path = filedialog.askopenfilename()
        print(file_path)

        if(file_path == ''):
            messagebox.showinfo(message="No seleccionó ningún archivo de texto")
            return
        
        # Charge the new matrix from path selectionated.
        self._charge_file(file_path)

        # Display the new board.
        self._display_board()

        # Center the window.
        self.window.eval('tk::PlaceWindow . center')
        
    def _config_canvas(self):
        # Resize canvas for show full the board.
        self.height = self.SQUARE_SIZE * len(self.matrix)
        self.width = self.SQUARE_SIZE * len(self.matrix[0])
        self.canvas.config(width=self.width, height=self.height)
        
    def _display_board(self):
        """
        Paint the board depending on the size of the cells and the
        defined colors.
        """

        self._config_canvas()

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