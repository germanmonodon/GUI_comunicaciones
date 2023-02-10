from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os


class MainWindow:
    def __init__(self):

        self.root = Tk()  # create a root widget
        self.root.title("Communication system")
        self.root.geometry("1000x700")
        # self.root.configure(background="white")
        self.root.wm_iconbitmap(os.path.dirname(os.path.abspath(__file__))+"\Imagenes\monodon_logo.ico")

        # Habría que redimensionar la imagen para que no ocupe tanto, ya sea mediante código o directamente

        img = ImageTk.PhotoImage(Image.open("Imagenes\monodon_background.png"))
        label = Label(self.root, image=img)
        label.grid(row=0, column=0)

        self.button_enter = Button(text="Realizar conexión entre ROVs", command=self.connect_ROVs)
        self.button_enter.place(x=400, y=600)
        self.root.mainloop()

    def connect_ROVs(self):
        nueva_ventana = SecondWindow(self.root)


class SecondWindow:
    def __init__(self, master):
        self.frameROVs = Toplevel(master)
        self.frameROVs.wm_iconbitmap(os.path.dirname(os.path.abspath(__file__)) + "\Imagenes\monodon_logo.ico")
        self.frameROVs.title("Interfaz de comunicación")
        self.frameROVs.geometry("1000x700")
        self.frameROVs.grid_columnconfigure(0, weight=1)
        self.frameROVs.grid_columnconfigure(1, weight=1)
        self.frameROVs.grid_rowconfigure(0, weight=1)

        master_rov = Frame(self.frameROVs, bg="#38E7E5")
        master_rov.grid(row=0, column=0, sticky="nesw")
        slave_rov = Frame(self.frameROVs, bg="#3FF6A1")
        slave_rov.grid(row=0, column=1, sticky="nesw")
        Label(master_rov,
              text="Master ROV").place(x=250, y=50)
        Label(slave_rov,
              text="Slave ROV").place(x=250, y=50)
        Label(master_rov, text="Enviando mensaje..").place(x=250, y=100)
        progressbar = ttk.Progressbar(self.frameROVs)
        progressbar.place(x=400, y=100, width=200)
        Label(master_rov, text="Recibiendo mensaje..").place(x=250, y=200)
        progressbar = ttk.Progressbar(self.frameROVs)
        progressbar.place(x=400, y=200, width=200)


def main():
    MainWindow()


if __name__ == "__main__":
    main()