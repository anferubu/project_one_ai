import tkinter as tk
import os

class Tablero:
    
    def __init__(self, matrix, path):
        self.matrix = matrix
        self.path = path
        self.ventana = tk.Tk()
        #self.ventana.geometry(f"{str(len(self.matrix[0])*100)}x{str(len(self.matrix)*100)}")
        self.ventana.resizable(0,0)
        self.ventana.config(bg="black")

        self.title = tk.Label(self.ventana, text="Proyecto #1 - IA", foreground="white", background="#000")
        self.title.pack()

        self.tablero=tk.Canvas(self.ventana, width=len(self.matrix[0])*100, height=len(self.matrix)*100)
        self.tablero.pack()
        
        self.btnAlg1 = tk.Button(self.ventana, text="Amplitud")
        self.btnAlg1.pack()

        self.btnAlg2 = tk.Button(self.ventana, text="Profundidad")
        self.btnAlg2.pack()
        self.drawBoard()
        
        
    def drawBoard(self):

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                item = matrix[i][j]
                if(item == -1):
                    color = "black"
                else:
                    color = "white"
                
                self.tablero.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)

        self.printImages()

    def drawBoardSolution(self):

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                item = matrix[i][j]
                if(item == -1):
                    color = "black"
                else:
                    if((i,j) in self.path):
                        color = "#79F5FF"   #"#5AFF6C"  #"#F4FC49"
                    else:
                        color = "white"
                
                self.tablero.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)

        self.printImages()


    def printImages(self):

        self.images = {
            0: tk.PhotoImage(file=os.path.abspath("./images/pinocho.png")),
            2: tk.PhotoImage(file=os.path.abspath("./images/cigarro.png")),
            3: tk.PhotoImage(file=os.path.abspath("./images/zorro.png")),
            4: tk.PhotoImage(file=os.path.abspath("./images/gepeto.png"))                     
        }
        
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                item = matrix[i][j]

                if(item != 1 and item != -1):
                    self.tablero.create_image(j*100, i*100, image=self.images[item], anchor="nw")
                    

matrix =[[1, 3, 1, 3, 1],
        [0, -1, 1, 1, 1],
        [1, 1, -1, -1, 4],
        [1, 1, 1, 2, 1]]

path = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (2, 4)]

if __name__ == "__main__":
    app = Tablero(matrix, path)
    app.ventana.mainloop()


# Celdas negras: -1
# Celdas blancas: 1
# Pinocho: 0
# Cigarros: 2
# Zorro: 3
# Gepetto: 4

