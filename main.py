from tkinter import *
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
        Label(self.frameROVs,
              text="Master ROV").place(x=250, y=50)
        Label(self.frameROVs,
              text="Slave ROV").place(x=750, y=50)
        #self.boton_cerrar = Button(
        #    self,
         #   text="Cerrar ventana",
          #  command=self.destroy
        #)
        #self.boton_cerrar.place(x=75, y=75)
        #self.focus()
        # self.grab_set()





def main():
    MainWindow()


if __name__ == "__main__":
    main()