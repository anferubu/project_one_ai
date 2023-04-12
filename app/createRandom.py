import numpy as np

import tkinter as tk
from tkinter import messagebox

from constant import Constant

from maze import Maze

class Random(Constant):
    
    def __init__(self, parent):
        self.parent=parent
        self.master = tk.Tk()
        self.master.resizable(False, False)

        tk.Label(self.master, text="Ingrese los datos").grid(row=0, column=0, columnspan=2)
        tk.Label(self.master, text="Filas:").grid(pady=5, row=1, column=0, sticky='nw')
        tk.Label(self.master, text="Columnas:").grid(pady=5, row=2, column=0, sticky='nw')

        self.rows = tk.Entry(self.master, width=20)
        self.rows.grid(padx=5, row=1, column=1)
        self.columns = tk.Entry(self.master, width=20)
        self.columns.grid(padx=5, row=2, column=1)

        tk.Button(self.master, text='Cancelar', command=self._destroy).grid(pady=10, row=3, column=0, sticky='nsew')
        tk.Button(self.master, text="Aceptar", command=self._generate_matrix).grid(pady=10, row=3, column=1, sticky='nsew')

        self.master.mainloop()

    def _destroy(self):
        self.master.destroy()

    def _print_data(self):
        print(self.rows.get(), self.columns.get())

    def _generate_matrix(self):
        values = [self.CIGAR, self.WALL, self.EMPTY, self.FOX]
        n = self.rows.get()
        m = self.columns.get()

        if not str.isdigit(n) or not str.isdigit(m):
            messagebox.showerror(message="Debe ingresar números", title="Ocurrió un error")
            return
        
        n = int(n)
        m = int(m)
        new_matrix = np.random.choice(values, size=(n,m))
        new_matrix[np.random.randint(0,n)][np.random.randint(0, m)] = self.PINOCCHIO

        while True:
            row_g = np.random.randint(0,n)
            col_g = np.random.randint(0, m)

            if(new_matrix[row_g][col_g] != self.PINOCCHIO):
                new_matrix[row_g][col_g] = self.GEPETTO
                break

        self.parent.maze = Maze('', matrix=new_matrix)
        self.parent.matrix = self.parent.maze.matrix
        self.parent._show_new_board()

        self._destroy()
