#!/usr/bin/python3
import tkinter as tk
from turtle import screensize
from customtkinter import *
import os

class Page(CTkFrame):
    def __init__(self, *args, **kwargs):
        CTkFrame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class InstructionsPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = CTkLabel(self, text="This is page 1")
       label.pack(side="top", fill="both", expand=True)

class RecalibratePage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = CTkLabel(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class FilesPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       self.arr = []
       self.frame_left = CTkFrame(master=self,width=2000, corner_radius=0)
       self.frame_left.grid(row=0, column=0, sticky="nswe")
       self.frame_right = CTkFrame(master=self, width=400, height=2000-40, corner_radius=12)
       self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
       self.update_files()
       button_instuctions = CTkButton(self.frame_right,text="Delete", text_font=("Roboto Medium", -40), command=self.mark_checkbox, fg_color=None, hover = True, border_width=2)
       button_instuctions.pack(side = "top")
       button_instuctions = CTkButton(self.frame_right, text="Export", text_font=("Roboto Medium", -40), command=self.mark_checkbox, fg_color=None, hover = True, border_width=2)
       button_instuctions.pack(side = "top")
       self.update_files()
       
   def mark_checkbox(self):
       delete_files = []
       for i in range(0, len(self.arr)-1):
           if (self.arr[i]).check_state == True:
               print(self.arr[i].text)
               os.remove(os.path.join('Data/',self.arr[i].text))
               print("Deleted")
       #self.update_files()
       
   def update_files(self):
       self.frame_left.destroy()
       self.frame_left = CTkFrame(master=self,width=200, corner_radius=0)
       self.frame_left.grid(row=0, column=0, sticky="nswe")
       filenames = next(os.walk("Data/"))[2]
       # for i in range(len(filenames)):
           # self.arr.append('check_box' + str(i))
       for i in range(0, len(filenames)-1):
           self.arr.append(i)
           self.arr[i] = CTkCheckBox(self.frame_left, text=filenames[i], text_font=("Roboto Medium", -40))
           self.arr[i].pack(side = "top", padx = 70)
        

class MainView(CTkFrame):
    def __init__(self, *args, **kwargs):
        CTkFrame.__init__(self, *args, **kwargs)

        frame_left = CTkFrame(master=self,width=300, corner_radius=0)
        frame_left.grid(row=0, column=0, sticky="nswe")

        frame_right = CTkFrame(master=self, width=420, height=2000-40, corner_radius=12)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        frame_left.grid_rowconfigure(0, minsize=10)
        frame_left.grid_rowconfigure(5, weight=1)
        frame_left.grid_rowconfigure(8, minsize=10)

        p1 = InstructionsPage(self)
        p2 = RecalibratePage(self)
        p3 = FilesPage(self)

        label_1 = CTkLabel(master=frame_left, text="OPTIONS", text_font=("Roboto Medium", -50), fg_color=None)
        label_1.grid(row=1, column=0, pady=100, padx=10)

        button_instuctions = CTkButton(master=frame_left, text="Instructions", text_font=("Roboto Medium", -40), command=p1.show, fg_color=None, hover = True,border_width=2)
        button_instuctions.grid(row=2, column=0, pady=10, padx=20)

        button_files = CTkButton(master=frame_left, text="Files", text_font=("Roboto Medium", -40), command=p3.show, fg_color=None, border_width=2)
        button_files.grid(row=3, column=0, pady=10, padx=20)

        button_recalibrate = CTkButton(master=frame_left, text="Recalibrate", text_font=("Roboto Medium", -40), command=p2.show, fg_color=None, border_width=2)
        button_recalibrate.grid(row=4, column=0, pady=10, padx=20)

        # buttonframe = tk.Frame(self)
        # container = tk.Frame(self)
        # buttonframe.pack(side="top", fill="x", expand=False)
        # container.pack(side="top", fill="both", expand=True)

        p1.place(in_=frame_right, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=frame_right, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=frame_right, x=0, y=0, relwidth=1, relheight=1)

        # b1 = CTkButton(buttonframe, text="Page 1", command=p1.show)
        # b2 = CTkButton(buttonframe, text="Page 2", command=p2.show)
        # b3 = CTkButton(buttonframe, text="Page 3", command=p3.show)

        # b1.pack(side="left")
        # b2.pack(side="left")
        # b3.pack(side="left")

        p1.show()

def button_event():
    print("Button pressed")
    

# if __name__ == "__main__":
    # root = CTk()
    # main = MainView(root)
    # main.pack(side="top", fill="both", expand=True)
    # root.title("VitalAid")
    # root.geometry(str(root.winfo_screenwidth()) + "x" + str(root.winfo_screenheight()))
    # root.mainloop()
    # app = App()
    # app.start()

# if __name__ == "__main__":
#     root = CTkToplevel()
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     main = MainView(root)
#     main.pack(side="top", fill="both", expand=True)
#     root.title("VitalAid")
#     root.geometry(str(screen_width) + "x" + str(screen_height))
#     root.mainloop()
