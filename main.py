from tkinter import *
from PIL import ImageTk, Image
import os

class MainWindow:
    def __init__(self):
        self.root = Tk()  # create a root widget
        self.root.title("Communication system")
        #self.root.geometry("1000x1000")
        self.root.configure(background="white")
        frame = Frame(self.root, width=1500, height=1000)
        frame.pack()
        self.root.wm_iconbitmap(os.path.dirname(os.path.abspath(__file__))+"\Imagenes\monodon_logo.ico")
        img = ImageTk.PhotoImage(Image.open("Imagenes\monodon_background.png"))

        # Create a Label Widget to display the text or Image
        label = Label(frame, image=img)
        label.pack()
        self.show_pressure()
        self.root.mainloop()

    def show_pressure(self):
        Label(self.root, text="77 Pa").place(x=5, y=0)


if __name__ == "__main__":
    MainWindow()