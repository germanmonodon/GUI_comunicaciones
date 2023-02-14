from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from tkdial import Meter
from fpdf import FPDF
import numpy as np
from PIL import ImageGrab
import time
import threading
import os
import datetime



class MainWindow:
    def __init__(self):

        self.root = Tk()  # create a root widget
        self.root.title("Communication system")
        self.root.geometry("1000x700")
        # self.root.configure(background="white")
        self.root.wm_iconbitmap(os.path.dirname(os.path.abspath(__file__))+"\Imagenes\monodon_logo.ico")

        # Habría que redimensionar la imagen para que no ocupe tanto, ya sea mediante código o directamente

        img = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__))+"\Imagenes\monodon_background.png"))
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
        self.logger_window = ThirdWindow(self.root)
        self.image_pdf = ImageTk.PhotoImage(Image.open(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\Imagenes\pdf_download.jpg"))
        self.button_pdf_download = Button(height=70, width=200, command=self.button_pdf, image=self.image_pdf)

    def button_pdf(self):
        self.logger_window.button_pdf_download()

class Table:
    def __init__(self, root):
        # code for creating table
        lst = [('Packets transmitted', 4, 'Date last packet', '13/02/20223'),
               ('Mean delay', '1,3 s', 'Max delay', '2 s'),
               ('Mean of losses/s', 3, 'Max losed/s', 5)]
        total_rows = len(lst)
        total_columns = len(lst[0])
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial', 10, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])


class ThirdWindow:
    def __init__(self, master):
        self.angle = 0
        self.begin = True
        self.frame_data = Toplevel(master)
        self.frame_data.wm_iconbitmap(os.path.dirname(os.path.abspath(__file__)) + "\Imagenes\monodon_logo.ico")
        self.frame_data.title("Data")
        self.frame_data.geometry("1300x600")
        self.pdf_name = "NA"
        self.text_in_label = StringVar()
        self.entry_text = StringVar()
        self.text_in_label.set("Enter pdf name to save results and stop running")
        Label(self.frame_data, text="Pressure received").place(x=30, y=10)
        Label(self.frame_data, text="Accelerometer data").place(x=900, y=10)
        Label(self.frame_data, text="Number of samples: 80").place(x=900, y=400)
        Label(self.frame_data, text="Orientation ROV2").place(x=500, y=10)
        Label(self.frame_data, text="Timestamp last message : 13/02/2023 10:34").place(x=500, y=400)
        Label(self.frame_data, text="Acc data: ").place(x=500, y=420)
        Label(self.frame_data, text="Gyro data:").place(x=500, y=440)
        Label(self.frame_data, text="Timestamp last message : 10/02/2023 12:01").place(x=30, y=400)
        Label(self.frame_data, text="Pressure received : 1002 Pa").place(x=30, y=420)
        Label(self.frame_data, text="Estimated depth: 2 meters").place(x=30, y=440)
        self.frame_table = LabelFrame(self.frame_data, text="Coms statistics")
        self.frame_table.place(x=550, y=470)
        self.coms_table = Table(self.frame_table)
        self.image_pdf = ImageTk.PhotoImage(Image.open(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\Imagenes\pdf_download.jpg"))
        self.button_pdf_download = Button(self.frame_data, height=70, width=200, command=self.button_pdf_download, image=self.image_pdf)
        self.button_pdf_download.place(x=40, y=500)
        self.x = threading.Thread(target=self.show_acc)
        self.x.start()
        self.y = threading.Thread(target=self.plot_imu)
        self.y.start()
        self.z = threading.Thread(target=self.plot_pressure)
        self.z.start()

    def getter(self, widget, name_widget):
        x = self.frame_data.winfo_rootx() + widget.winfo_x()
        y = self.frame_data.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(name_widget)

    def button_pdf_download(self):
        pdf = FPDF()
        # Add a page
        pdf.add_page()
        # Falta buscar en el direectorio los nombres que tienes y yo lo que haría sería darle la fecha del experimento y al carajo
        # set style and size of font
        # that you want in the pdf
        self.pdf_name = str(datetime.datetime.now())
        self.pdf_name = self.pdf_name.split(".")[0]
        self.pdf_name_2 = self.pdf_name.replace(":", "_")

        # ts store timestamp of current time

        pdf.set_font("Arial", size=15)
        pdf.image(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\Imagenes\header_monodon.jpg", x=5, y=5, w=10, h=10)
        # create a cell
        pdf.cell(200, 10, txt="Report Data for experiment done at " + self.pdf_name,
                 ln=1, align='C')

        #self.getter(self.canvas_acc.get_tk_widget())
        pdf.text(x=20, y=40, txt="ROV acceleration")
        pdf.image(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\acc.png",
                  x=30, y=40, w=100, h=100)
        pdf.text(x=20, y=150, txt="Historic of pressure")
        pdf.image(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\pressure.png",
                  x=30, y=160, w=100, h=100)
        if self.pdf_name == "":
            self.text_in_label.set("Set a name for the pdf")
        else:
            self.text_in_label.set("PDF saved correctly")
            pdf.output(os.path.dirname(os.path.abspath(__file__)) + "\Informes\Monodon_" + self.pdf_name_2 + ".pdf")

    def show_acc(self):
        while True:
            fig = Figure(figsize=(5, 5),
                         dpi=70)

            # random data

            x_acc = np.random.randint(1,101,80)
            y_acc = np.random.randint(1, 101, 80)
            z_acc = np.random.randint(1, 101, 80)

            # adding the subplot
            plot1 = fig.add_subplot(111)

            # plotting the graph
            plot1.plot(x_acc, color="blue")
            plot1.plot(y_acc, color="red")
            plot1.plot(z_acc, color="yellow")
            plot1.set_xlabel('Time (s)')
            plot1.set_ylabel('Acceleration (g)')

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            self.canvas_acc = FigureCanvasTkAgg(fig,
                                       master=self.frame_data)
            self.canvas_acc.draw()

            # placing the canvas on the Tkinter window
            self.canvas_acc.get_tk_widget().place(x=900, y=40)
            self.getter(self.canvas_acc.get_tk_widget(), "acc.png")
            time.sleep(0.01)

    def plot_imu(self):
        if self.begin:
            self.begin = False
            self.meter3 = Meter(self.frame_data, bg="#242424", fg="#242424", radius=320, start=0, end=360,
                           major_divisions=90, border_width=0, text_color="white",
                           start_angle=0, end_angle=-360, scale_color="white", axis_color="cyan",
                           needle_color="white", scroll_steps=60, minor_divisions=10, scroll=False)
            self.meter3.set(15)
            self.meter3.place(x=500, y=60)
        else:
            print("Calculating angle....")
        while True:
            self.angle = self.angle + 1
            self.meter3.set(self.angle)
            time.sleep(0.4)

    def plot_pressure(self):
        while True:
            fig = Figure(figsize=(5, 5),
                         dpi=70)

            # list of squares
            y = np.random.randint(0, 300, size=100)

            # adding the subplot
            plot1 = fig.add_subplot(111)

            # plotting the graph
            plot1.plot(y)
            plot1.set_xlabel('Time (s)')
            plot1.set_ylabel('Pressure (Pa)')

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            self.canvas_press = FigureCanvasTkAgg(fig,
                                       master=self.frame_data)
            self.canvas_press.draw()

            # placing the canvas on the Tkinter window
            self.canvas_press.get_tk_widget().place(x=40, y=40)
            self.getter(self.canvas_press.get_tk_widget(), "pressure.png")
            time.sleep(0.4)


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