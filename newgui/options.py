#!/usr/bin/python3
import tkinter as tk
from customtkinter import *
import os
from capstone_VitalAid import *
from vitalsPage import *

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
       self.frame_top = CTkFrame(master=self, width=1377, height=730, corner_radius=0, bg_color=None)
       self.frame_top.grid(column=0, row=0, sticky='w',  padx=20, pady=20)
       self.frame_top.grid_propagate(0)

       self.frame_bottom= CTkFrame(master=self, width=1377, height=150, corner_radius=12)
       self.frame_bottom.grid(column=0, row=1, sticky='w', padx=20, pady=20)
       self.frame_bottom.grid_propagate(0)

       #buttons on the bottom frame
       button_instuctions = CTkButton(self.frame_bottom,text="Delete", text_font=("Roboto Medium", -100), command=self.delete_files, fg_color=None, hover = True, border_width=2)
       button_instuctions.grid(column=0, row=0, sticky='w',  padx=150, pady=10)
       button_instuctions = CTkButton(self.frame_bottom, text="Export", text_font=("Roboto Medium", -100), command=self.export_files, fg_color=None, hover = True, border_width=2)
       button_instuctions.grid(column=1, row=0, sticky='w',  padx=150, pady=10)
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
                        self.pop_up_window("Delete Successful") 
                except:
                        print("No file named " + source_path)
                        self.pop_up_window("Delete Unsuccessful")
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
       canvas = tk.Canvas(self.frame_top, border_color=None, width = 1375, height=730, bg_color=None)
       canvas.grid(row=0, column=0, sticky="news")
       filenames = next(os.walk("Data/"))[2]
       self.arr = []
       for i in range(len(filenames)):
           self.arr.append(i)
           self.arr[i] = CTkCheckBox(canvas, text=filenames[i], text_font=("Roboto Medium", -85), width=80, height=80)
           self.arr[i].pack(side = "top")
       
   def export_files(self):
        #Get checked marked files
        files = self.mark_checkbox() 
        
        #Check for inserted USB
        if usb_detected() == False:
            self.pop_up_window("Export Unsuccessful\n" +
                                " USB not found")
        else: 
        #Set up paths
            dest_usb = get_USB_name()
            path = os.getcwd()
            folder = "VitalAidExport"
            
            test_path = dest_usb + "/" + folder + "/"
            
            
            CHECK_FOLDER = os.path.isdir(test_path)
            
            if not CHECK_FOLDER:
                    os.mkdir(dest_usb + "/" + folder)
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
                    self.pop_up_window("Export Successful")
                except: 
                    print("No file named " + filename) 
                    self.pop_up_window("Export Unsuccessful")
                    
   def pop_up_window(self, s):
        self.toplevel = CTkToplevel()
        center_window(self.toplevel, 750, 400)
        frame1 = customtkinter.CTkFrame(self.toplevel, height = 650, width= 350, bg_color = "white")
        frame1.pack()
        label5 = customtkinter.CTkLabel(frame1, text= s, text_font=("Roboto Medium", -70))
        label5.grid(row=1, column=0, pady=20, padx=20)
        self.button5 = customtkinter.CTkButton(frame1, text="OK", text_font=("Roboto Medium", -90), command=self.close, border_width=2)
        self.button5.grid(row=3, column=0, pady=30, padx=20)
        
   def close(self):
        print("Closeing")
        self.toplevel.destroy()

        
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

        button_instuctions = CTkButton(master=frame_left, text="Instruction", text_font=("Roboto Medium", -70), height = 250, command=p1.show, fg_color=None, hover = True,border_width=2)
        button_instuctions.grid(row=2, column=0, pady=10, padx=20)

        button_files = CTkButton(master=frame_left, text="      Files      ", text_font=("Roboto Medium", -70), height = 250, command=p3.show, fg_color=None, border_width=2)
        button_files.grid(row=1, column=0, pady=10, padx=20)

        button_recalibrate = CTkButton(master=frame_left, text="Recalibrate", text_font=("Roboto Medium", -70), height = 250, command=p2.show, fg_color=None, border_width=2)
        button_recalibrate.grid(row=3, column=0, pady=10, padx=20)

        button_close = CTkButton(master=frame_left, text="    <- BACK    ", text_font=("Roboto Medium", -70), height = 80, command=self.destroy, fg_color=None, bg_color ='red', border_width=2)
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

        p3.show()
        
        def close_button(self):
            self.destroy()
            
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
    
    
def center_window(root, width=400, height=300):
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	# calculate x and y coordinates for the Tk root window
	x = (screen_width/2) - (width/2)
	y = (screen_height/2) - (height/2)
	# set the dimensions of the screen 
	# and where it is placed
	root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    

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
    # root = CTk()
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # main = MainView(root)
    # main.pack(side="top", fill="both", expand=True)
    # root.title("VitalAid")
    # root.geometry(str(screen_width) + "x" + str(screen_height))
    # root.mainloop()
