#!/usr/bin/python3
from email.iterators import body_line_iterator
import tkinter
import tkinter.messagebox
import customtkinter
import sys
import random
import plotting2

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class ServoDrive(object):
    # simulate values
    def getVelocity(self): return random.randint(0,100)
    def getTorque(self): return random.randint(0,100)
    def getVal(self): return random.randint(0,100)

class App(customtkinter.CTk):

    APP_NAME = "LifeLine"
    WIDTH = 700
    HEIGHT = 400

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        self.bodyTempVal = 0
        self.bloodPresVal = 0
        self.heartRateVal = 0

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two CTkFrames ============

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self,
                                                  width=420,
                                                  height=App.HEIGHT,
                                                  corner_radius=0,
                                                  fg_color=("white", "gray28"))
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="OPTIONS",
                                                command=self.button_event,
                                                fg_color=None,
                                                width=120,
                                                height=160,
                                                border_width=2)
        self.button_1.grid(row=1, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                bg_color="red",
                                                text="STOP",
                                                command=self.button_event,
                                                fg_color=None,
                                                width=120,
                                                height=160,
                                                border_width=2)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)


        # ============ frame_right ============


        self.frame_info = customtkinter.CTkFrame(master=self.frame_right,
                                                 width=100,
                                                 height=70,
                                                 fg_color=("white", "gray38"))
        self.frame_info.pack(side=tkinter.LEFT)

        self.label_info_bt = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Body Temperature",
                                                   text_font=("Roboto Medium", -15),
                                                   corner_radius=0,
                                                   fg_color=("white", "gray38"))
        self.label_info_bt.grid(padx=5)

        self.servo1 = ServoDrive()

        self.label_info_bt_val = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=self.servo1.getVelocity(),
                                                   text_font=("Roboto Medium", -70),
                                                   corner_radius=0,
                                                   fg_color=("white", "gray48"))
        self.label_info_bt_val.grid(padx=5, pady=6)

        self.label_info_2 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Label2" ,
                                                   height=120,
                                                   fg_color=("white", "gray38"))
        self.label_info_2.grid(pady=5, padx=5)

        self.label_info_3 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Label3" ,
                                                   height=120,
                                                   fg_color=("white", "gray38"))
        self.label_info_3.grid(pady=5, padx=5)

        self.frame_info_2 = customtkinter.CTkFrame(master=self.frame_right,
                                                 width=400,
                                                 height=70)
        self.frame_info_2.pack(side=tkinter.LEFT)

        self.label_info_bt = customtkinter.CTkLabel(master=self.frame_info_2,
                                                   text="BodyTempData" ,
                                                   width=400,
                                                   height=120,
                                                   fg_color=("white", "gray38"))
        #self.label_info_bt.grid(pady=5, padx=5)

        self.canvas_bt = tkinter.Canvas(master = self.frame_info_2, 
                                        width=400, 
                                        height=120, 
                                        background='black')
        self.canvas_bt.grid(pady=5, padx=5)
        self.velocity_line = self.canvas_bt.create_line(0,0,0,0, fill="red")
        self.velocity2_line = self.canvas_bt.create_line(0,0,0,0, fill="green")
        self.update_plot1()
        

        self.label_info_bp = customtkinter.CTkLabel(master=self.frame_info_2,
                                                   text="BloodPressureData" ,
                                                   width=400,
                                                   height=120,
                                                   fg_color=("white", "gray38"))
        self.label_info_bp.grid(pady=5, padx=5)

        self.label_info_hr = customtkinter.CTkLabel(master=self.frame_info_2,
                                                   text="HeartRateData" ,
                                                   width=400,
                                                   height=120,
                                                   fg_color=("white", "gray38"))
        self.label_info_hr.grid(pady=5, padx=5)


  

        # ============ frame_right -> frame_info ============



        # ============ frame_right <- ============


    def update_plot1(self):
        self.bodyTempVal = self.servo1.getVelocity()
        self.add_point1(self.velocity_line, self.bodyTempVal)
        self.add_point12(self.velocity2_line)
        self.canvas_bt.xview_moveto(1.0)
        self.label_info_bt_val.set_text(str(self.bodyTempVal))
        self.after(1000, self.update_plot1)

    def add_point1(self, line, y):
        coords = self.canvas_bt.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(100-y)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bt.coords(line, *coords)
        self.canvas_bt.configure(scrollregion=self.canvas_bt.bbox("all"))
    
    def add_point12(self, line):
        y2 = 50
        coords = self.canvas_bt.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y2)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bt.coords(line, *coords)
        self.canvas_bt.configure(scrollregion=self.canvas_bt.bbox("all"))
    
    def update_plot2(self):
        t = self.servo2.getTorque()
        self.add_point2(self.torque_line, t)
        self.canvas2.xview_moveto(1.0)
        self.after(250, self.update_plot2)

    def add_point2(self, line, y):
        coords = self.canvas2.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas2.coords(line, *coords)
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))

    def update_plot3(self):
        z = self.servo3.getVal()
        self.add_point3(self.value_line, z)
        self.canvas3.xview_moveto(1.0)
        self.after(250, self.update_plot3)

    def add_point3(self, line, y):
        coords = self.canvas3.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas3.coords(line, *coords)
        self.canvas3.configure(scrollregion=self.canvas3.bbox("all"))

    def button_event(self):
        print("Button pressed")

    def change_mode(self):
        if self.check_box_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
