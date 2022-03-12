#!/usr/bin/python3
import tkinter
import tkinter.messagebox
import customtkinter
import sys
from page2capstone import *

class ServoDrive(object):
    # simulate values
    def getBodyTemp(self): return random.randint(0,200)
    def getBloodPresDias(self): return random.randint(0,200)
    def getBloodPresSys(self): return random.randint(0,200)
    def getHeartRate(self): return random.randint(0,200)

class App(customtkinter.CTk):

    root = tkinter.Tk()
    WIDTH = root.winfo_screenwidth()
    HEIGHT = root.winfo_screenheight()
    root.destroy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("VitalAid")
        self.minsize(App.WIDTH, App.HEIGHT)

        self.bodyTempVal = 0
        self.bloodPresDiasVal = 0
        self.bloodPresSysVal = 0
        self.heartRateVal = 0
        self.paused = False

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        self.frame_right = customtkinter.CTkFrame(master=self, width=App.WIDTH-40, height=App.HEIGHT-40, corner_radius=12)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # # ============ frame_right ============

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Instructions:\n" +
                                                    "1. Strap device onto any side of casulaty's forearm\n" +
                                                    "2. Place Temparture Sensor on the wrist\n" +
                                                    "3. Place Heart Rate and Blood Pressure Sensor\n" + 
                                                    " an any finger.\n"+ 
                                                    "4. Press 'MEASURE' to begin.\n",
                                              text_font=("Roboto Medium", -55),  # font name and size in px
                                              fg_color=None)
        self.label_1.place(relx=0.5, rely=0.1, anchor=tkinter.N)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right, width=340, height=150, text="MEASURE", text_font=("Roboto Medium", -60), command=self.button_event)
        self.button_5.place(relx=0.5, rely=0.75, anchor=tkinter.N)

    def button_event(self):
        print("Button pressed")
        self.frame_right.destroy()
        self.create_vital_page()

    def create_vital_page(self):
        
        # ============ create two CTkFrames ============
        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=("white", "gray28"))
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ============ frame_left ============

        self.button_1 = customtkinter.CTkButton(master=self.frame_left, text="OPTIONS", command=self.button_event, fg_color=None, width=App.WIDTH/6, height=(App.HEIGHT/2)-75, border_width=2)
        self.button_1.grid(row=1, column=0, pady=10, padx=20)

        self.create_stop_button()
        # self.button_2 = customtkinter.CTkButton(master=self.frame_left, bg_color="red", text="STOP", command=self.stop_button, fg_color=None, width=App.WIDTH/6, height=(App.HEIGHT/2)-75, border_width=2)
        # self.button_2.grid(row=2, column=0, pady=10, padx=20)

        # ============ frame_right ============

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right, fg_color=("white", "gray38"))
        self.frame_info.pack(side=tkinter.LEFT)

        self.frame_info_2 = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info_2.pack(side=tkinter.LEFT)

        title_width = App.WIDTH/4
        title_height = App.HEIGHT/10
        label_width = App.WIDTH/4
        label_height = App.HEIGHT/8
        canvas_height = App.WIDTH/6
        canvas_width = App.HEIGHT/1.5

        self.servo = ServoDrive()
        self.label_info_bt = customtkinter.CTkLabel(master=self.frame_info, width = title_width, height= title_height, text="Body Temperature", text_font=("Roboto Medium", -30), corner_radius=0, fg_color=("white", "gray38"))
        self.label_info_bt.grid(padx=5)

        degree_sign = u"\N{DEGREE SIGN}" 
        self.label_info_bt_val = customtkinter.CTkLabel(master=self.frame_info, width = label_width, height= label_height, text=' ', text_font=("Roboto Medium", -120), corner_radius=0, fg_color=("white", "gray48"))
        self.label_info_bt_val.grid(padx=5, pady=6)

        self.label_info_bp = customtkinter.CTkLabel(master=self.frame_info, width = title_width, height= title_height, text="Blood Pressure", text_font=("Roboto Medium", -30), corner_radius=0, fg_color=("white", "gray38"))
        self.label_info_bp.grid(padx=5)

        self.label_info_bp_val = customtkinter.CTkLabel(master=self.frame_info, width = label_width, height= label_height, text=' ', text_font=("Roboto Medium", -120), corner_radius=0, fg_color=("white", "gray48"))
        self.label_info_bp_val.grid(padx=5, pady=6)

        self.label_info_hr = customtkinter.CTkLabel(master=self.frame_info, width = title_width, height= title_height, text="Heart Rate", text_font=("Roboto Medium", -30), corner_radius=0, fg_color=("white", "gray38"))
        self.label_info_hr.grid(padx=5)

        self.label_info_hr_val = customtkinter.CTkLabel(master=self.frame_info,width = label_width, height= label_height,  text=' ', text_font=("Roboto Medium", -120), corner_radius=0, fg_color=("white", "gray48"))
        self.label_info_hr_val.grid(padx=5, pady=6)

        self.canvas_bt = tkinter.Canvas(master = self.frame_info_2, width=canvas_width, height=canvas_height, background='black')
        self.canvas_bt.grid(pady=5, padx=5)
        self.bt_line = self.canvas_bt.create_line(0,0,0,0, fill="purple")
        self.bt_high_line = self.canvas_bt.create_line(0,0,0,0, fill="red")
        self.bt_low_line = self.canvas_bt.create_line(0,0,0,0, fill="red")

        self.canvas_bp = tkinter.Canvas(master = self.frame_info_2, width=canvas_width, height=canvas_height, background='black')
        self.canvas_bp.grid(pady=5, padx=5)
        self.bp_dias_line = self.canvas_bp.create_line(0,0,0,0, fill="green")
        self.bp_sys_line = self.canvas_bp.create_line(0,0,0,0, fill="orange")
        self.bp_high_line = self.canvas_bp.create_line(0,0,0,0, fill="red")
        self.bp_low_line = self.canvas_bp.create_line(0,0,0,0, fill="red")

        self.canvas_hr = tkinter.Canvas(master = self.frame_info_2, width=canvas_width, height=canvas_height, background='black')
        self.canvas_hr.grid(pady=5, padx=5)
        self.hr_line = self.canvas_hr.create_line(0,0,0,0, fill="blue")
        self.hr_high_line = self.canvas_hr.create_line(0,0,0,0, fill="red")
        self.hr_low_line = self.canvas_hr.create_line(0,0,0,0, fill="red")

        self.check_status()

    def check_status(self):
        if self.paused == False:
            self.update_vitals()

    def stop_button(self):
        self.button_2.destroy()
        self.create_start_button()

    def start_button(self):
        self.button_2.destroy()
        self.create_stop_button()

    def create_stop_button(self):
        self.button_2 = customtkinter.CTkButton(master=self.frame_left, bg_color="red", text="STOP", command=self.stop_button, fg_color=None, width=App.WIDTH/6, height=(App.HEIGHT/2)-75, border_width=2)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)
        self.paused = False
    
    def create_start_button(self):
        self.button_2 = customtkinter.CTkButton(master=self.frame_left, bg_color="green", text="START", command=self.start_button, fg_color=None, width=App.WIDTH/6, height=(App.HEIGHT/2)-75, border_width=2)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)
        self.paused = True
              
    def update_vitals(self):
        self.update_body_temp()
        self.update_blood_pres()
        self.update_heart_rate()

    def update_body_temp(self):
        self.bodyTempVal = self.servo.getBodyTemp()
        self.add_body_temp(self.bt_line, self.bodyTempVal)
        self.add_body_temp_high(self.bt_high_line)
        self.add_body_temp_low(self.bt_low_line)
        self.canvas_bt.xview_moveto(1.0)
        degree_sign = u"\N{DEGREE SIGN}" 
        self.label_info_bt_val.set_text(str(self.bodyTempVal) + degree_sign + 'C')
        self.after(1000, self.update_body_temp)

    def add_body_temp(self, line, y):
        coords = self.canvas_bt.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(100-y)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bt.coords(line, *coords)
        self.canvas_bt.configure(scrollregion=self.canvas_bt.bbox("all"))
    
    def add_body_temp_high(self, line):
        y2 = 90
        coords = self.canvas_bt.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y2)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bt.coords(line, *coords)
        self.canvas_bt.configure(scrollregion=self.canvas_bt.bbox("all"))

    def add_body_temp_low(self, line):
        y2 = 50
        coords = self.canvas_bt.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y2)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bt.coords(line, *coords)
        self.canvas_bt.configure(scrollregion=self.canvas_bt.bbox("all"))

    def update_blood_pres(self):
        self.bloodPresDiasVal = self.servo.getBloodPresDias()
        self.bloodPresSysVal = self.servo.getBloodPresSys()
        self.add_blood_pres_dias(self.bp_dias_line, self.bloodPresDiasVal)
        self.add_blood_pres_sys(self.bp_sys_line, self.bloodPresSysVal)
        self.add_blood_pres_high(self.bp_high_line)
        self.add_blood_pres_low(self.bp_low_line)
        self.canvas_bp.xview_moveto(1.0)
        self.label_info_bp_val.set_text(str(self.bloodPresDiasVal) + '/' + str(self.bloodPresSysVal))
        self.after(1000, self.update_blood_pres)

    def add_blood_pres_dias(self, line, y):
        coords = self.canvas_bp.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bp.coords(line, *coords)
        self.canvas_bp.configure(scrollregion=self.canvas_bp.bbox("all"))
    
    def add_blood_pres_sys(self, line, y):
        coords = self.canvas_bp.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bp.coords(line, *coords)
        self.canvas_bp.configure(scrollregion=self.canvas_bp.bbox("all"))

    def add_blood_pres_low(self, line):
        y_low = 50
        coords = self.canvas_bp.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y_low)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bp.coords(line, *coords)
        self.canvas_bp.configure(scrollregion=self.canvas_bp.bbox("all"))

    def add_blood_pres_high(self, line):
        y_high = 90
        coords = self.canvas_bp.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y_high)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_bp.coords(line, *coords)
        self.canvas_bp.configure(scrollregion=self.canvas_bp.bbox("all"))

    def update_heart_rate(self):
        self.heartRateVal = self.servo.getBodyTemp()
        self.add_heart_rate(self.hr_line, self.heartRateVal)
        self.add_heart_rate_low(self.hr_low_line)
        self.add_heart_rate_high(self.hr_high_line)
        self.canvas_hr.xview_moveto(1.0)
        self.label_info_hr_val.set_text(str(self.heartRateVal))
        self.after(1000, self.update_heart_rate)

    def add_heart_rate(self, line, y):
        coords = self.canvas_hr.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_hr.coords(line, *coords)
        self.canvas_hr.configure(scrollregion=self.canvas_hr.bbox("all"))
    
    def add_heart_rate_low(self, line):
        y_low = 50
        coords = self.canvas_hr.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y_low)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_hr.coords(line, *coords)
        self.canvas_hr.configure(scrollregion=self.canvas_hr.bbox("all"))

    def add_heart_rate_high(self, line):
        y_high = 90
        coords = self.canvas_hr.coords(line)
        x = coords[-2] + 5
        coords.append(x)
        coords.append(y_high)
        coords = coords[-500:] # keep # of points to a manageable size
        self.canvas_hr.coords(line, *coords)
        self.canvas_hr.configure(scrollregion=self.canvas_hr.bbox("all"))

    def on_closing(self, event=0):
        self.destroy()
        
    def start(self):
        self.mainloop()

