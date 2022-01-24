#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as tkFont

value = 0 

def heartRateValue():
        value = 25
        return value

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

class MainPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label_main_page = tk.Label(self, text="Click 'Start Tracking' for Touchless Mouse")
        label_main_page.pack(fill="both", expand=True, ipady = 40)
        # canvas1 = tk.Canvas(self, width = 400, height = 300,  relief = 'raised')
        # canvas1.pack()
        
        # label1 = tk.Label(self, text='Welcome to Touchless Mouse')
        # label1.config(font=('helvetica', 14))
        # canvas1.create_window(200, 25, window=label1)

class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label_settings = tk.Label(self, text="Please change Settings")
        label_settings.pack(ipady = 10)

        canvas = tk.Canvas(self)
        canvas.pack(ipady= 10)
        submit_button = tk.Button(self, text='Submit').pack()


class InstructionsPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

class MeasurePage(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label_settings = tk.Label(self, text="Heart Rate")
        label_settings.pack(ipady = 10)
        ft = tkFont.Font(family='Times',size=50)
        label_settings["font"] = ft
        label_settings["fg"] = "#333333"
        label_settings["justify"] = "center"
        label_settings["text"] = "Heart Rate:"

        heart_rate = tk.Label(self, text="Heart Rate")
        heart_rate.pack(ipady = 10)
        ft = tkFont.Font(family='Times',size=50)
        heart_rate["font"] = ft
        heart_rate["fg"] = "#333333"
        heart_rate["justify"] = "center"
        heart_rate["text"] = heartRateValue()


        # canvas = tk.Canvas(self)
        # canvas.pack(ipady= 10)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        main_page = MainPage(self)
        settings_page = SettingsPage(self)
        instructions_page = InstructionsPage(self)
        measure_page =  MeasurePage(self)

        button_frame = tk.Frame(self)
        container = tk.Frame(self)
        button_frame.pack(anchor = 's')
        container.pack(side="top", fill="both", expand=True)

        #Frames that are shows on each of the Pages
        main_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        settings_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        instructions_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        measure_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        #All the buttons on the Main Page
        settings_button = tk.Button(button_frame, text="Settings Page", command=settings_page.lift)
        settings_button.pack()

        inst_button= tk.Button(button_frame,text="Instructions Page", command=instructions_page.lift)
        inst_button.pack()

        touchless_window_button = tk.Button(button_frame, bg = 'green', text="Measure", height = 5, width = 30, command=measure_page.lift)
        touchless_window_button.pack(ipady = 20)

        main_page.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    #setting title
    root.title("Capstone Group 30")
    #setting window size
    width=600
    height=500
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)
    root.mainloop()