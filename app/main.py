from gui import Board


if __name__ == '__main__':
    print('Running app...')
    # Run the app
    app = Board('./data/matrix.txt')
    app.window.mainloop()