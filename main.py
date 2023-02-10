from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
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
        self.button_enter.place(x=250, y=600)
        self.button_data_logger = Button(text="Data Logger", command=self.logger)
        self.button_data_logger.place(x=550, y=600)
        self.root.mainloop()

    def connect_ROVs(self):
        nueva_ventana = SecondWindow(self.root)

    def logger(self):
        logger_window = ThirdWindow(self.root)


class ThirdWindow:
    def __init__(self, master):
        self.frame_data = Toplevel(master)
        self.frame_data.wm_iconbitmap(os.path.dirname(os.path.abspath(__file__)) + "\Imagenes\monodon_logo.ico")
        self.frame_data.title("Data")
        self.frame_data.geometry("1000x700")
        Label(self.frame_data, text="Pressure received").place(x=30, y=10)
        Label(self.frame_data, text="Timestamp last message : 10/02/2023 12:01").place(x=30, y=400)
        Label(self.frame_data, text="Pressure received : 1002 Pa").place(x=30, y=420)
        Label(self.frame_data, text="Estimated depth: 2 meters").place(x=30, y=440)
        self.plot_pressure()

    def plot_pressure(self):
        fig = Figure(figsize=(5, 5),
                     dpi=70)

        # list of squares
        y = [i ** 2 for i in range(101)]

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(y)
        plot1.set_xlabel('Time (s)')
        plot1.set_ylabel('Pressure (Pa)')

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=self.frame_data)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().place(x=40, y=40)


class SecondWindow:
    def __init__(self, master):
        self.frameROVs = Toplevel(master)
        self.frameROVs.wm_iconbitmap(os.path.dirname(os.path.abspath(__file__)) + "\Imagenes\monodon_logo.ico")
        self.frameROVs.title("Interfaz de comunicación")
        self.frameROVs.geometry("1000x300")
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