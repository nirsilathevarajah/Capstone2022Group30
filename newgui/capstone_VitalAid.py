#!/usr/bin/python3
import tkinter
import tkinter.messagebox
import customtkinter
import sys
import vitalsPage
import piSerialHandlerV2

class App(customtkinter.CTk):

    root = tkinter.Tk()
    WIDTH = root.winfo_screenwidth()
    HEIGHT = root.winfo_screenheight()
    root.destroy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("VitalAid")
        self.minsize(App.WIDTH, App.HEIGHT)

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
                                                    "1. Strap device onto any side of casualty's forearm\n" +
                                                    "2. Place Temparture Sensor on the wrist\n" +
                                                    "3. Place Heart Rate and Blood Pressure Sensor\n" + 
                                                    " an any finger.\n"+ 
                                                    "4. Press 'MEASURE' to begin.\n",
                                              text_font=("Roboto Medium", -55),  # font name and size in px
                                              fg_color=None)
        self.label_1.place(relx=0.5, rely=0.02, anchor=tkinter.N)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right, width=420, height=200, text="MEASURE", text_font=("Roboto Medium", -200), command=self.button_event)
        self.button_5.place(relx=0.5, rely=0.65, anchor=tkinter.N)

    def button_event(self):
        print("Button pressed")
        #self.frame_right.destroy()
        toplevel = customtkinter.CTk()
        center_window(toplevel, 300, 150)
        frame1 = customtkinter.CTkFrame(toplevel)
        frame1.pack()
        label5 = customtkinter.CTkLabel(frame1, text= "CALIBRATING, PLEASE WAIT")
        label5.grid(row=1, column=0, pady=10, padx=20)
        toplevel.after(3000, piSerialHandlerV2.setStartMeasuring(True))
        toplevel.destroy()
        self.on_closing()
        app= vitalsPage.Vitals()
        app.start()

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

