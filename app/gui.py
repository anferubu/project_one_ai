import tkinter as tk

class Tablero:
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.ventana = tk.Tk()
        self.ventana.geometry(f"{str(len(self.matrix[0])*100)}x{str(len(self.matrix)*100)}")
        self.ventana.resizable(0,0)
        self.tablero=tk.Canvas(self.ventana)
        self.tablero.pack(fill="both", expand=1)
        self.cuadrados()
    
    def cuadrados(self):

        images = {
            0: "pinocho",
            2: "cigarro",
            3: "zorro",
            4: "gepeto"                      
        }

        color = ""

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                item = matrix[i][j]
                if(item == -1):
                    color = "black"
                else:
                    color = "white"
                
                self.tablero.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill=color)

                if(item != 1 and item != -1):
                    photo = tk.PhotoImage(file="../images/pinocho.png")
                    self.tablero.create_image(j*100, i*100, image=photo)
                    
                 
matrix =[[1, 3, 1, 3, 1],
        [0, -1,  1,  1,  1],
        [1,  1, -1, -1,  4],
        [1,  1,  1,  2,  1]]

if __name__ == "__main__":
    app = Tablero(matrix)
    app.ventana.mainloop()


# Celdas negras: -1
# Celdas blancas: 1
# Pinocho: 0
# Cigarros: 2
# Zorro: 3
# Gepetto: 4

