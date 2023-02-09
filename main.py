from tkinter import *

class MainWindow:
    def __init__(self):
        root = Tk()  # create a root widget
        root.title("Communication system")
        root.configure(background="white")
        root.wm_iconbitmap('myicon.ico')
        root.mainloop()




if __name__ == "__main__":
    MainWindow()