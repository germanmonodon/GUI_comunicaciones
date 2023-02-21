from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkdial import Meter
from fpdf import FPDF
from PIL import ImageGrab
from pubsub import pub
from Data_sender import Sender

import threading
import os
import datetime


class MainWindow:
    def __init__(self):
        self.root = Tk()  # create a root widget
        self.root.title("Communication system")
        self.root.geometry("1000x700")
        self.root.wm_iconbitmap(os.path.dirname(os.getcwd())
                                + "\GUI_comunicaciones\Imagenes\monodon_logo.ico")

        img = ImageTk.PhotoImage(Image.open(os.path.dirname(os.getcwd())
                                            + "\GUI_comunicaciones\Imagenes\monodon_background.png"))
        label = Label(self.root, image=img)
        label.grid(row=0, column=0)

        self.button_enter = Button(text="Realizar conexión entre ROVs", command=self.connect_rovs)
        self.button_enter.place(x=250, y=600)
        self.button_data_logger = Button(text="Data Logger", command=self.logger)
        self.button_data_logger.place(x=550, y=600)
        self.logger_window = None
        self.image_pdf = None
        self.button_pdf_download = None
        self.root.mainloop()

    def connect_rovs(self):
        SecondWindow(self.root)

    def logger(self):
        self.logger_window = ThirdWindow(self.root)

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
        # Declarations
        self.angle = 0
        self.begin = True
        self.pdf_name = "NA"
        self.pdf_name_2 = "NA"
        self.text_pdf = StringVar()
        self.text_pressure_received = StringVar()
        self.text_number_samples = StringVar()
        self.text_timestamp = StringVar()
        self.text_timestamp2 = StringVar()

        self.text_pdf.set("Save Report!")

        # Principal Frame configuration
        self.frame_data = Toplevel(master)
        self.frame_data.wm_iconbitmap(os.path.dirname(os.getcwd())
                                +"\GUI_comunicaciones\Imagenes\monodon_logo.ico")
        self.frame_data.title("Data")
        self.frame_data.geometry("1300x570")

        # Labels configuration
        Label(self.frame_data, text="Pressure received").place(x=30, y=10)
        Label(self.frame_data, text="Accelerometer data").place(x=900, y=10)
        Label(self.frame_data, textvariable=self.text_number_samples).place(x=900, y=400)
        Label(self.frame_data, text="Orientation ROV2").place(x=500, y=10)
        Label(self.frame_data, textvariable=self.text_timestamp).place(x=500, y=400)
        Label(self.frame_data, text="Acc data: ").place(x=500, y=420)
        Label(self.frame_data, text="Gyro data:").place(x=500, y=440)
        Label(self.frame_data, textvariable=self.text_timestamp2).place(x=30, y=400)
        Label(self.frame_data, textvariable=self.text_pressure_received).place(x=30, y=420)
        Label(self.frame_data, text="Estimated depth: 2 meters").place(x=30, y=440)
        Label(self.frame_data, textvariable=self.text_pdf).place(x=110, y=510)
        self.frame_table = LabelFrame(self.frame_data, text="Coms statistics")
        self.frame_table.place(x=550, y=470)
        self.coms_table = Table(self.frame_table)

        self.image_pdf = ImageTk.PhotoImage(Image.open(
            r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\Imagenes\icono_pdf.png").resize((52, 52)))
        self.button_pdf = Button(self.frame_data, command=self.button_pdf_download,
                                 image=self.image_pdf)
        self.button_pdf.place(x=40, y=490)

        # Threading for interactive GUI
        pub.subscribe(topicName="BlueROV2::Heading", listener=self.plot_imu)
        self.pressure_list = []
        pub.subscribe(topicName="BlueROV2::Pressure", listener=self.plot_pressure)
        self.pitch_list = []
        self.yaw_list = []
        self.roll_list = []

        pub.subscribe(topicName="BlueROV2::Angles", listener=self.show_acc)

    def getter(self, widget, name_widget):
        x = self.frame_data.winfo_rootx() + widget.winfo_x()
        y = self.frame_data.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(name_widget)

    def button_pdf_download(self):

        pdf = FPDF()
        pdf.add_page()

        # Giving name to the pdf
        self.pdf_name = str(datetime.datetime.now())
        self.pdf_name = self.pdf_name.split(".")[0]
        self.pdf_name_2 = self.pdf_name.replace(":", "_")
        pdf.set_font("Arial", size=15)
        pdf.image(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\Imagenes\header_monodon.jpg", x=5,
                  y=5, w=10, h=10)
        # create a cell
        pdf.cell(200, 10, txt="Report Data for experiment done at " + self.pdf_name,
                 ln=1, align='C')

        pdf.text(x=20, y=40, txt="ROV acceleration")
        pdf.image(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\acc.png",
                  x=30, y=40, w=100, h=100)

        pdf.text(x=20, y=150, txt="Historic of pressure")
        pdf.image(r"C:\Users\Innovacion\Desktop\Proyectos_Coding\GUI_comunicaciones\pressure.png",
                  x=30, y=160, w=100, h=100)

        s = pdf.output(os.path.dirname(os.getcwd()) + "\GUI_comunicaciones\Informes\Monodon_" + self.pdf_name_2 + ".pdf")

        self.text_pdf.set("PDF saved correctly")
        os.remove("acc.png")
        os.remove("pressure.png")

    def show_acc(self, acc):

        fig = Figure(figsize=(5, 5),
                     dpi=70)
        self.text_timestamp.set("Timestamp last message " + str(datetime.datetime.now()).split(".")[0])

        self.roll_list.append(acc[0])
        self.yaw_list.append(acc[1])
        self.pitch_list.append(acc[2])
        # adding the subplot
        plot1 = fig.add_subplot(111)
        self.text_number_samples.set("Number of samples: " + str(len(self.roll_list)))
        # plotting the graph
        plot1.plot(self.roll_list, color="blue")
        plot1.plot(self.yaw_list, color="red")
        plot1.plot(self.pitch_list, color="yellow")
        plot1.set_xlabel('Time (s)')
        plot1.set_ylabel('Acceleration (g)')

        self.canvas_acc = FigureCanvasTkAgg(fig, master=self.frame_data)
        self.canvas_acc.draw()

        # placing the canvas on the Tkinter window
        self.canvas_acc.get_tk_widget().place(x=900, y=40)
        self.getter(self.canvas_acc.get_tk_widget(), "acc.png")

    def plot_imu(self, heading):
        if self.begin:
            self.begin = False
            self.meter3 = Meter(self.frame_data, bg="#242424", fg="#242424", radius=320, start=0, end=360,
                                major_divisions=90, border_width=0, text_color="white",
                                start_angle=0, end_angle=-360, scale_color="white", axis_color="cyan",
                                needle_color="white", scroll_steps=60, minor_divisions=10, scroll=False)
            self.meter3.set(heading * 360 / 3.14)
            self.meter3.place(x=500, y=60)
        else:
            print("Calculating angle....")
            self.meter3.set(heading * 360 / 3.14)

    def plot_pressure(self, msg):
        fig = Figure(figsize=(5, 5),
                     dpi=70)

        self.text_pressure_received.set("Presure received: " + str("{:.2f}".format(msg)) + " Pa")
        self.text_timestamp2.set("Timestamp last message " + str(datetime.datetime.now()).split(".")[0])
        self.pressure_list.append(msg)
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(self.pressure_list)
        plot1.set_xlabel('Time (s)')
        plot1.set_ylabel('Pressure (Pa)')

        self.canvas_press = FigureCanvasTkAgg(fig,
                                              master=self.frame_data)
        self.canvas_press.draw()

        self.canvas_press.get_tk_widget().place(x=40, y=40)
        self.getter(self.canvas_press.get_tk_widget(), "pressure.png")


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


def receive():
    Sender()


def window():
    MainWindow()


def main():

    x = threading.Thread(target=receive)
    x.start()
    y = threading.Thread(target=window)
    y.start()


if __name__ == "__main__":
    main()
