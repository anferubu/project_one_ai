import time

from PIL import Image, ImageTk as I
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

from constant import Constant

from maze import Maze
from bfs import BFS
from ucs import UCS



class Board(Constant):
    """
    Class that represents the GUI of the program. It consists of a board
    that shows the different characters and the path from Pinocchio to Gepetto.
    """

    TITLE = 'Métodos de búsqueda no informados'

    SQUARE_SIZE = 60

    COLORS = {
        'border': '#243B5D',
        'empty': '#FFF',
        'wall': '#2D2D2D',
        'visited': '#FAEDCB',
        'path': '#7EF5FF',
    }


    def __init__(self, filename:str):
        """
        Initializes the Board instance.

        Args:
            filename (str): path of the file with the numeric matrix
                            that represents the maze.
        """
        self._charge_file(filename)
        self._initialize()
        self._display_board()


    def _charge_file(self, filename:str):
        """
        Creates a Maze instance from a file and get the correspond matrix.

        Args:
            filename (str): path of the file with the numeric matrix
                            that represents the maze.
        """
         # Open the file with a matrix.
        self.maze = Maze(filename)

        # Define the matrix.
        self.matrix = self.maze.matrix


    def _initialize(self):
        """
        Initializes all the graphical elements of the window.
        """
        empty = self.COLORS['empty']

        # Create the window.
        self.window = tk.Tk()
        self.window.title(self.TITLE)
        self.window.resizable(True, True)

        # Create the canvas that represents the board.
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(padx=5, pady=5)

        # Create the frame that contains the radio buttons with the options.
        self.options = tk.Frame(self.window)
        self.options.pack(fill='x', expand=True, padx=10, pady=10)

        # Create the radio buttons for select the algorithm.
        self.option = tk.IntVar()
        tk.Radiobutton(self.options, text="Búsqueda por amplitud.",
            variable=self.option, value=1, font=('Arial', 12)).pack(anchor='w')
        tk.Radiobutton(self.options, text="Búsqueda por amplitud (zigzag).",
            variable=self.option, value=2, font=('Arial', 12)).pack(anchor='w')
        tk.Radiobutton(self.options, text="Búsqueda por costo uniforme.",
            variable=self.option, value=3, font=('Arial', 12)).pack(anchor='w')
        tk.Radiobutton(self.options,text="Búsqueda por profundidad iterativa.",
            variable=self.option, value=4, font=('Arial', 12)).pack(anchor='w')

        # Create the frame that contains the buttons.
        self.buttons = tk.Frame(self.window)
        self.buttons.pack(fill='x', expand=True, padx=10, pady=10)

        # Create button to find the path from start to the goal.
        self.find_path_btn = tk.Button(self.buttons, text='Find path',
            font=('Arial', 11), bg=empty, relief='groove', padx=15,
            command=self._find_path)
        self.find_path_btn.pack(side=tk.LEFT, fill='x', padx=5, pady=5)

        # Create button to clear the board.
        self.clear_btn = tk.Button(self.buttons, text='Clear',
            font=('Arial', 11), relief='groove', padx=15, bg=empty,
            command=self._display_board)
        self.clear_btn.pack(side=tk.RIGHT, anchor='e', padx=5, pady=5)

        # Create the menu.
        self.menubar = tk.Menu(self.window, border=1)
        self.window.config(menu=self.menubar)

        self.menu = tk.Menu(self.menubar, tearoff=False)
        self.menu.add_command(label='Abrir archivo', command=self._choose_file)
        self.menu.add_separator()
        self.menu.add_command(label='Acerca de', command=self.about_us)
        self.menu.add_command(label='Salir', command=self.window.quit)

        self.menubar.add_cascade(label='Archivo', menu=self.menu)


    def _choose_file(self):
        """
        Read a file and display the maze that it contains.
        """
        try:
            # Launch the file selector.
            file_path = filedialog.askopenfilename()

            # Charge the new matrix from selected path.
            self._charge_file(file_path)

        except FileNotFoundError:
            # If no file is selected it does nothing.
            return

        except Exception:
            # If the file is invalid, displays a dialog box.
            messagebox.showerror(
                title='Formato de archivo inválido',
                message='El archivo que has seleccionado no contiene una'
                       +' matriz de números o su formato es incorrecto.'
                       +'\n\nPor favor seleccione un archivo adecuado.'
            )

        # Display the new board.
        self._display_board()

        # Center the window.
        self.window.eval('tk::PlaceWindow . center')


    def about_us(self):
        """
        Show a dialog box with information about the project.
        """
        messagebox.showinfo(title='Acerca del proyecto',
                 message='Primer proyecto de Introducción a la Inteligencia'
                        +' Artificial.\n\nAutores:\n'
                        +' + Juan Sebastian González Camacho.\n'
                        +' + Andrés Felipe Ruiz Buriticá.'
        )


    def _find_path(self):
        """
        Finds the path from Pinocchio to Gepetto according a unreported
        search method.
        """
        # Determines the selected search algorithm.
        option = self.option.get()

        # If none have been selected, displays a dialog box.
        if option == 0:
            messagebox.showwarning(
                message="Debe seleccionar una de las opciones.",
                title="¡Cuidado!")
            return

        # Breadth First Search.
        if option == 1:
            bfs = BFS(self.maze)
            path = bfs.solve()
            visited = bfs.visited_list

        # Breadth First Search with zig-zag behavior.
        elif option == 2:
            bfs = BFS(self.maze)
            path = bfs.solve_zigzag()
            visited = bfs.visited_list

        # Uniform Cost Search.
        elif option == 3:
            ucs = UCS(self.maze)
            path = ucs.solve()
            visited = ucs.visited_list
            self.costs = ucs.cost_so_far

        # Iterative Deepening Search.
        elif option == 4:
            print()

        self._display_board()
        self._display_path(path, visited)


    def _config_canvas(self):
        """
        Resize canvas for show full the board.
        """
        self.height = self.SQUARE_SIZE * len(self.matrix)
        self.width = self.SQUARE_SIZE * len(self.matrix[0])
        self.canvas.config(width=self.width, height=self.height)


    def _display_board(self):
        """
        Paint the board depending on the size of the cells and the
        defined colors.
        """
        # Resize the canvas.
        self._config_canvas()

        # Shortcuts for the colors and the size.
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
        """
        Places the images on the canvas according to the numerical value of
        each cell of the matrix.
        """
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


    def _display_path(self, pathway:list=None, extends:list=None):
        """
        Display a given path.

        Args:
            path (list): set of coordinates that form a path.
            visited (list): set of coordinates that has been visited for
                            Pinocchio.
        """
        # Disable all buttons while drawing the path.
        self.find_path_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)

        # Shortcuts for used colors
        visited = self.COLORS['visited']
        path = self.COLORS['path']
        border = self.COLORS['border']

        # Shortcut for the square size of the board
        size = self.SQUARE_SIZE

        # Draw the visited cells on the canvas.
        for _, cell in enumerate(extends):
            x, y = cell
            x1, y1 = (y * size), (x * size)
            x2, y2 = (x1 + size), (y1 + size)
            self.canvas.create_rectangle(x1, y1, x2, y2, width=1,
                fill=visited, outline=border)
            self.canvas.create_rectangle(3, 3, self.width, self.height,
                fill='', outline=border, width=2)

            # If the method is Uniform Cost Search, displays the costs.
            if self.option.get() == 3:
                self.canvas.create_text(x1+size/2, y1+size/2,
                    text=self.costs[cell], font=('Arial', 11))

            self._set_images()
            self.canvas.update()
            time.sleep(0.1)

        # Draw the path on the canvas.
        for _, cell in enumerate(pathway):
            x, y = cell
            x1, y1 = (y * size), (x * size)
            x2, y2 = (x1 + size), (y1 + size)
            self.canvas.create_rectangle(x1, y1, x2, y2, width=1,
                fill=path, outline=border)
            self.canvas.create_rectangle(3, 3, self.width, self.height,
                fill='', outline=border, width=2)

            # If the method is Uniform Cost Search, displays the costs.
            if self.option.get() == 3:
                self.canvas.create_text(x1+size/2, y1+size/2,
                    text=self.costs[cell], font=('Arial', 11))

            self._set_images()
            self.canvas.update()
            time.sleep(0.1)

        # Enable all buttons.
        self.find_path_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.NORMAL)