from gui import Board

if __name__ == '__main__':

    # Run the app
    app = Board('./data/matrix.txt')
    app.window.mainloop()