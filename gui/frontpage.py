#!/usr/bin/python3
import tkinter
import tkinter.messagebox
import customtkinter
import sys

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    APP_NAME = "LifeLine"
    WIDTH = 700
    HEIGHT = 400

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        self.frame_right = customtkinter.CTkFrame(master=self,
                                                  width=App.WIDTH-40,
                                                  height=App.HEIGHT-40,
                                                  corner_radius=12)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # # ============ frame_right ============

        self.frame_right.rowconfigure(0, weight=1)
        self.frame_right.rowconfigure(3, weight=1)
        self.frame_right.columnconfigure(0, weight=1)

        # self.frame_info = customtkinter.CTkFrame(master=self.frame_right,
        #                                          width=380,
        #                                          height=100)
        # self.frame_info.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky="wens")

        self.label_1 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Instructions:\n\n" +
                                                    "1. Strap device onto any side of casulaty's forearm\n" +
                                                    "2. Place Temparture Sensor on the wrist\n" +
                                                    "3. Place Heart Rate and Blood Pressure Sensor\n" + 
                                                    " an any finger.\n"+ 
                                                    "4. Press 'MEASURE' to begin.\n",
                                              text_font=("Roboto Medium", -16),  # font name and size in px
                                              fg_color=None)
        self.label_1.place(relx=0.5, rely=0.1, anchor=tkinter.N)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                width=240,
                                                height=100,
                                                text="MEASURE",
                                                text_font=("Roboto Medium", -40),
                                                command=self.button_event)
        self.button_5.place(relx=0.5, rely=0.65, anchor=tkinter.N)


    def button_event(self):
        print("Button pressed")
        self.frame_right.destroy()

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
