#!/usr/bin/python3
import tkinter
import tkinter.messagebox
import customtkinter
import sys
from customtkinter.customtkinter_toplevel import CTkToplevel
import random
import csv
import os
import datetime
import options

class ServoDrive(object):
    # simulate values
    def getBodyTemp(self): 
        return random.randint(0,200)
    def getBloodPresDias(self): 
        return random.randint(0,200)
    def getBloodPresSys(self): 
        return random.randint(0,200)
    def getHeartRate(self): 
        return random.randint(0,200)

class Vitals(customtkinter.CTk):

    root = tkinter.Tk()
    WIDTH = root.winfo_screenwidth()
    HEIGHT = root.winfo_screenheight()
    root.destroy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("VitalAid")
        self.minsize(Vitals.WIDTH, Vitals.HEIGHT)

        self.bodyTempVal = 0
        self.bloodPresDiasVal = 0
        self.bloodPresSysVal = 0
        self.heartRateVal = 0
        self.paused = False
        self.firstStart = True
        self.file_num = 1

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)
        
        # ============ create two CTkFrames ============
        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=("white", "gray28"))
        self.frame_right.grid(row=0, column=1, sticky="nswe")

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ============ frame_left ============

        self.button_1 = customtkinter.CTkButton(master=self.frame_left, text="OPTIONS", command=self.button_options, fg_color=None, width=Vitals.WIDTH/6, height=(Vitals.HEIGHT/2)-75, border_width=2)
        self.button_1.grid(row=1, column=0, pady=10, padx=20)

        self.create_start_button()
        # self.button_2 = customtkinter.CTkButton(master=self.frame_left, bg_color="red", text="STOP", command=self.stop_button, fg_color=None, width=App.WIDTH/6, height=(App.HEIGHT/2)-75, border_width=2)
        # self.button_2.grid(row=2, column=0, pady=10, padx=20)

        # ============ frame_right ============

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right, fg_color=("white", "gray38"))
        self.frame_info.pack(side=tkinter.LEFT)

        self.frame_info_2 = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info_2.pack(side=tkinter.LEFT)

        title_width = Vitals.WIDTH/4
        title_height = Vitals.HEIGHT/10
        label_width = Vitals.WIDTH/4
        label_height = Vitals.HEIGHT/8
        self.canvas_height = Vitals.WIDTH/6
        self.canvas_width = Vitals.HEIGHT/1.5

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

        self.create_bt_canvas()
        self.create_bp_canvas()
        self.create_hr_canvas()

    def button_options(self):
        root = customtkinter.CTk()
        main = options.MainView(root)
        main.pack(side="top", fill="both", expand=True)
        root.title("VitalAid")
        root.geometry(str(root.winfo_screenwidth()) + "x" + str(root.winfo_screenheight()))
        root.mainloop()


    def create_bt_canvas(self):
        self.canvas_bt = tkinter.Canvas(master = self.frame_info_2, width=self.canvas_width, height=self.canvas_height, background='black')
        self.canvas_bt.grid(pady=5, padx=5)
        self.bt_line = self.canvas_bt.create_line(0,0,0,0, fill="purple")
        self.bt_high_line = self.canvas_bt.create_line(0,0,0,0, fill="red")
        self.bt_low_line = self.canvas_bt.create_line(0,0,0,0, fill="red")

    def create_bp_canvas(self):
        self.canvas_bp = tkinter.Canvas(master = self.frame_info_2, width=self.canvas_width, height=self.canvas_height, background='black')
        self.canvas_bp.grid(pady=5, padx=5)
        self.bp_dias_line = self.canvas_bp.create_line(0,0,0,0, fill="green")
        self.bp_sys_line = self.canvas_bp.create_line(0,0,0,0, fill="orange")
        self.bp_high_line = self.canvas_bp.create_line(0,0,0,0, fill="red")
        self.bp_low_line = self.canvas_bp.create_line(0,0,0,0, fill="red")
    

    def create_hr_canvas(self):
        self.canvas_hr = tkinter.Canvas(master = self.frame_info_2, width=self.canvas_width, height=self.canvas_height, background='black')
        self.canvas_hr.grid(pady=5, padx=5)
        self.hr_line = self.canvas_hr.create_line(0,0,0,0, fill="blue")
        self.hr_high_line = self.canvas_hr.create_line(0,0,0,0, fill="red")
        self.hr_low_line = self.canvas_hr.create_line(0,0,0,0, fill="red")

    def check_status(self):
        if self.paused == False:
            self.update_vitals()
        
    def stop_button(self):
        self.button_2.destroy()
        self.create_start_button1()

    def start_button(self):
        self.button_2.destroy()
        self.create_stop_button()
        self.check_status()
        self.firstStart = False

    def start_button1(self):
        self.toplevel = CTkToplevel()
        center_window(self.toplevel, 300, 150)
        frame1 = customtkinter.CTkFrame(self.toplevel)
        frame1.pack()
        label5 = customtkinter.CTkLabel(frame1, text= "Would you like to continue" +
                                                        "or start again?")
        label5.grid(row=1, column=0, pady=10, padx=20)
        self.button5 = customtkinter.CTkButton(frame1, text="Start Again", command=self.startAgain_button, border_width=2)
        self.button5.grid(row=3, column=0, pady=10, padx=20)
        self.button6 = customtkinter.CTkButton(frame1, text="Continue", command=self.continue_button, border_width=2)
        self.button6.grid(row=4, column=0, pady=10, padx=20)
        self.button_2.destroy()
        self.create_stop_button()
    
    def continue_button(self):
        self.toplevel.destroy()
        self.check_status()

    def startAgain_button(self):
        self.toplevel.destroy()
        self.canvas_bt.destroy()
        self.canvas_bp.destroy()
        self.canvas_hr.destroy()
        self.create_bt_canvas()
        self.create_bp_canvas()
        self.create_hr_canvas()
        self.file_num = self.file_num + 1
        self.update_vitals()

    def create_stop_button(self):
        self.button_2 = customtkinter.CTkButton(master=self.frame_left, bg_color="red", text="STOP", command=self.stop_button, fg_color=None, width=Vitals.WIDTH/6, height=(Vitals.HEIGHT/2)-75, border_width=2)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)
        self.paused = False

    
    def create_start_button(self):
        self.button_2 = customtkinter.CTkButton(master=self.frame_left, bg_color="green", text="START", command=self.start_button, fg_color=None, width=Vitals.WIDTH/6, height=(Vitals.HEIGHT/2)-75, border_width=2)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)
        self.paused = True

    def create_start_button1(self):
        self.button_2 = customtkinter.CTkButton(master=self.frame_left, bg_color="green", text="START", command=self.start_button1, fg_color=None, width=Vitals.WIDTH/6, height=(Vitals.HEIGHT/2)-75, border_width=2)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)
        self.paused = True


    def getVitals(self):
        bodyTemp = self.bodyTempVal = self.servo.getBodyTemp()
        bloodPresDias = self.bloodPresDiasVal = self.servo.getBloodPresDias()
        bloodPresSys = self.bloodPresSysVal = self.servo.getBloodPresSys()
        heartRate = self.heartRateVal = self.servo.getBodyTemp()
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        file_name = 'Data/patient_file_'+ str(self.file_num) +'.csv'
        with open(file_name, 'a') as patient_file:
            patient_vitals = csv.writer(patient_file)
            patient_vitals.writerow([dt_string, bodyTemp, bloodPresDias, bloodPresSys, heartRate])
            patient_file.close()
        return bodyTemp, bloodPresDias, bloodPresSys, heartRate

    def update_vitals(self):
        self.update_body_temp()
        self.update_blood_pres()
        self.update_heart_rate()
        

    def update_body_temp(self):
        #self.bodyTempVal = self.servo.getBodyTemp()
        bodyTemp = self.getVitals()[0]
        self.add_body_temp(self.bt_line, bodyTemp)
        self.add_body_temp_high(self.bt_high_line)
        self.add_body_temp_low(self.bt_low_line)
        self.canvas_bt.xview_moveto(1.0)
        degree_sign = u"\N{DEGREE SIGN}" 
        self.label_info_bt_val.set_text(str(bodyTemp) + degree_sign + 'C')
        if self.paused == False:
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
        # self.bloodPresDiasVal = self.servo.getBloodPresDias()
        # self.bloodPresSysVal = self.servo.getBloodPresSys()
        bloodPresDias = self.getVitals()[1]
        bloodPresSys = self.getVitals()[2]
        self.add_blood_pres_dias(self.bp_dias_line, bloodPresDias)
        self.add_blood_pres_sys(self.bp_sys_line, bloodPresSys)
        self.add_blood_pres_high(self.bp_high_line)
        self.add_blood_pres_low(self.bp_low_line)
        self.canvas_bp.xview_moveto(1.0)
        self.label_info_bp_val.set_text(str(bloodPresDias) + '/' + str(bloodPresSys))
        if self.paused == False:
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
        #self.heartRateVal = self.servo.getBodyTemp()
        heartRate = self.getVitals()[3]
        self.add_heart_rate(self.hr_line, heartRate)
        self.add_heart_rate_low(self.hr_low_line)
        self.add_heart_rate_high(self.hr_high_line)
        self.canvas_hr.xview_moveto(1.0)
        self.label_info_hr_val.set_text(str(heartRate))
        if self.paused == False:
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

    def button_event(self):
        print("Button Pressed")

    def on_closing(self, event=0):
        self.destroy()
        
    def start(self):
        self.mainloop()

def center_window(root, width=400, height=300):
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	# calculate x and y coordinates for the Tk root window
	x = (screen_width/2) - (width/2)
	y = (screen_height/2) - (height/2)
	# set the dimensions of the screen 
	# and where it is placed
	root.geometry('%dx%d+%d+%d' % (width, height, x, y))
