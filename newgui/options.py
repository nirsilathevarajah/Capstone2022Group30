#!/usr/bin/python3
import tkinter as tk
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
       self.frame_top = CTkFrame(master=self, width=1100, height=500, corner_radius=0)
       self.frame_top.grid(column=0, row=0, sticky='w',  padx=20, pady=20)
       self.frame_top.grid_propagate(0)

       self.frame_bottom= CTkFrame(master=self, width=1100, height=170, corner_radius=12)
       self.frame_bottom.grid(column=0, row=1, sticky='w', padx=20, pady=20)
       self.frame_bottom.grid_propagate(0)

       #buttons on the bottom frame
       button_instuctions = CTkButton(self.frame_bottom,text="Delete", text_font=("Roboto Medium", -85), command=self.delete_files, fg_color=None, hover = True, border_width=2)
       button_instuctions.grid(column=0, row=0, sticky='w',  padx=100, pady=40)
       button_instuctions = CTkButton(self.frame_bottom, text="Export", text_font=("Roboto Medium", -85), command=self.export_files, fg_color=None, hover = True, border_width=2)
       button_instuctions.grid(column=1, row=0, sticky='w',  padx=100, pady=40)
       self.update_files()
       
   
   def mark_checkbox(self):
       checked_files = []
       print("Length of self.arr " + str(len(self.arr)))
       for i in self.arr:
           print(i.text)
           print("Check state: " + str(i.check_state))
           if i.check_state:
               #print(i.text)
               checked_files.append(i.text)
               #os.remove(os.path.join('Data/',self.arr[i].text))
               #self.arr.remove(self.arr[i])
               print("Selected: " + i.text)
               #self.update_files()
           else:
                print("Reached else")
                continue
       print("done")
       return checked_files
        
   def delete_files(self):
        checked_files = self.mark_checkbox()
        path = os.getcwd()
        #path = '/home/pi/Desktop/Capstone2022Group30/newgui'
        for f in checked_files:
                try:
                        filename = "Data/" + f 
                        source_path = os.path.join(path, filename)
                        os.remove(source_path)
                        print("Success - " + source_path + " removed") 
                except:
                        print("No file named " + source_path)
        print("Length of self arr " + str(len(self.arr)))
        self.remove_files(checked_files)
        self.update_files()

   def remove_files(self, checked_files):
           print("Start Checked Files")
           for d in checked_files:
                   print(d)
           print("End Checked Files")     
           print("Inside self.arr" + str(len(self.arr)))
           for f in self.arr:
                   #print(f.text)
                   if f.text in checked_files:
                           print(f.text + " removed from self.arr")
                           self.arr.remove(f)
                           len(self.arr)
                   else: continue
           print("NEW SELF.ARR LENGTH: " + str(len(self.arr)))
           #self.update_files()
       
   def update_files(self):
       print("Updating Files")
       canvas = tk.Canvas(self.frame_top, bg="gray22", border_color=None)
       canvas.grid(row=0, column=0, sticky="news")
       filenames = next(os.walk("Data/"))[2]
       self.arr = []
       for i in range(len(filenames)):
           self.arr.append(i)
           self.arr[i] = CTkCheckBox(canvas, text=filenames[i], text_font=("Roboto Medium", -60), width=44, height=44)
           self.arr[i].pack(side = "top")
       
   def export_files(self):
        #Get checked marked files
        files = self.mark_checkbox() 
        
        #Check for inserted USB
        if usb_detected() == False:
            return
        else: 
        #Set up paths
            dest_usb = get_USB_name()
            path = os.getcwd()
            folder = "VitalAidExport"
            
            
            CHECK_FOLDER = os.path.isdir(folder)
            
            if not CHECK_FOLDER:
                    os.mkdir(folder)
                    print("Folder created")
            else:
                    print("folder already exists")
            
            
            dest_path = os.path.join(dest_usb, folder)
            
            
            #Loops through + copies files in source folder
            for f in files: 
                try:
                    filename = "Data/" + f 
                    source_path = os.path.join(path, filename) 
                    x = shutil.copy(source_path, dest_path) 
                    print("Success - " + x) 
                except: 
                    print("No file named " + filename)  
        
   # def refresh(self):
           # self.__init__()
                

        

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

        label_1 = CTkLabel(master=frame_left, text="OPTIONS", text_font=("Roboto Medium", -60), fg_color=None)
        label_1.grid(row=0, column=0, pady=10, padx=10)

        button_instuctions = CTkButton(master=frame_left, text="Instructions", text_font=("Roboto Medium", -70), height = 150, command=p1.show, fg_color=None, hover = True,border_width=2)
        button_instuctions.grid(row=1, column=0, pady=10, padx=20)

        button_files = CTkButton(master=frame_left, text="      Files      ", text_font=("Roboto Medium", -70), height = 150, command=p3.show, fg_color=None, border_width=2)
        button_files.grid(row=2, column=0, pady=10, padx=20)

        button_recalibrate = CTkButton(master=frame_left, text="Recalibrate", text_font=("Roboto Medium", -70), height = 150, command=p2.show, fg_color=None, border_width=2)
        button_recalibrate.grid(row=3, column=0, pady=10, padx=20)

        button_close = CTkButton(master=frame_left, text="     Close     ", text_font=("Roboto Medium", -70), height = 150, command=p2.show, fg_color=None, border_width=2)
        button_close.grid(row=4, column=0, pady=10, padx=20)

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
        
def usb_detected():
        usb_path = "/media/pi/"
        pi_detected = len(os.listdir(usb_path))
        if pi_detected < 1: return False        
        else: return True
       
def get_USB_name():
        usb_path = "/media/pi/" 
        usb_dir = os.listdir(usb_path)
        #Gets only the first 
        for usb_file in usb_dir:
            destPath = os.path.join(usb_path, usb_file)  
            return destPath

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
