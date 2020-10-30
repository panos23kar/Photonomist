"""
This file hosts the graphical user interface code"""

import tkinter as tk
from tkinter import filedialog
from photonomist.__main__ import input_path_validation

class Gui:
    """This class is used to "draw" the graphical user interface through which 
    users interact with photonomist.

    |
    """
    def __init__(self):
        """Constructor method
        |
        """
        self.__gui = tk.Tk()
        self.__main_window()
        self.__input_path()

        self.__start_gui()
    
    def __main_window(self):
        """
        Specifies the title and dimensions of main window
        """
        self.__gui.title("Photonomist")
        self.__gui.geometry("460x300")
    
    def __start_gui(self):
        """
        Starts the graphical user interface
        """
        self.__gui.mainloop()
    
    def __input_path(self):
        """
        It hosts input label, input path and input button"""

        self.__input_path_label = tk.Label(self.__gui, text="Input path:")
        self.__input_path_label.place(x=20, y=20)

        self.__input_path_value = tk.StringVar()
        self.__input_path_value.trace("w", self.check_input_path)

        self.__input_path_entry = tk.Entry(self.__gui, textvariable = self.__input_path_value)
        self.__input_path_entry.place(x=90, y=22, width= 300)

        self.__input_path_file_explorer_button  = tk.Button(self.__gui, text="...", command = self.__input_path_file_explorer)
        self.__input_path_file_explorer_button.place(x=395, y=20, height=21)
    
    def __input_path_file_explorer(self):
        self.__input_path_button_value =  filedialog.askdirectory(initialdir = "/",title = "Select file")
        self.__input_path_value.set(self.__input_path_button_value)
    
    def check_input_path(self, kati1, kati2, kati3):#TODO why I need the extra values!What is sent by the .trace
        try:
            input_path_validation(self.__input_path_value.get())
        except Exception as e:
            #print(str(e))
            self.__input_path_label = tk.Label(self.__gui, text=str(e))
            self.__input_path_label.configure(foreground="red")
            self.__input_path_label.place(x=20, y=43)

if __name__ == "__main__":
    Gui()