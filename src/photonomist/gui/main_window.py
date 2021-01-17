"""
This file hosts the graphical user interface code"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
import webbrowser
from info_window import InfoWindow
from loading_window import LoadingWindow
from exclude_window import ExcludeWidnow


from photonomist.__main__ import input_path_validation, export_path_validation, tidy_photos, open_export_folder

class Gui:
    """This class is used to "draw" the graphical user interface through which 
    users interact with photonomist.

    |
    """
    def __init__(self):
        """Constructor method
        |
        """
        self.__widgets = {}
        self.__photos_roots = ""
        self.__gui = tk.Tk()
        self.__main_window()
        self.__menu()
        self.__initiate_exclude_window()
        self.__user_paths()

        self.__start_gui() 
    
    def __main_window(self):
        """Specifies the title and dimensions of main window, and places the run button in the main window.
        |
        """
        self.__gui.title("Photonomist")
        self.__gui.geometry("440x420")

        #Run Button widget
        self.__run_button = tk.Button(self.__gui, text="Run, Forrest, Run!!", command= partial(LoadingWindow(self.__gui).start_load_w_thread, self.__run_app), state="disabled")
        
        self.__run_button.place(x=310, y=380, height=21)
    
    def __quit(self):
        if messagebox.askyesno("", "Are you sure you want to quit Photonomist?"):
            self.__gui.destroy()
    
    def __menu(self):
        """Menu on the top of the window
        |
        """
        #Main menu
        self.__main_menu = tk.Menu(self.__gui)
        self.__gui.config(menu=self.__main_menu)
        #SubMenu
        #SubMenu File
        self.__sub_menu_file = tk.Menu(self.__main_menu, tearoff=0)
        self.__main_menu.add_cascade(label="File", menu=self.__sub_menu_file, underline=0)
        # separator is here!
        self.__sub_menu_file.add_separator()
        self.__sub_menu_file.add_command(label="Quit", underline=0, command=self.__quit)
        #SubMenu Info
        #TODO Connect it with info_window
        self.__main_menu.add_command(label="Info...", command=InfoWindow(self.__gui).info_app, underline=1)
    
    def __start_gui(self):
        """
        Starts the graphical user interface
        |
        """
        self.__gui.mainloop()
    
    def __initiate_exclude_window(self):
        self.__exl_w = ExcludeWidnow(self)

    def __user_paths(self):
        """It hosts the label, stringvar, entry and file explorer button for the export path
        |
        """

        for mode in (("input", 20, 22),
                     ("export", 140, 142)):
            #Labels widget
            self.__widgets[mode[0] + "_path_label"] = tk.Label(self.__gui, text= mode[0].capitalize() + " path:")
            self.__widgets[mode[0] + "_path_label"].place(x=20, y=mode[1])

            #String variable widget which dynamically changes the value of the Entry widget
            self.__widgets[mode[0] + "_path_value"] = tk.StringVar()

            #Entries widget
            self.__widgets[mode[0] + "_path_entry"] = tk.Entry(self.__gui, textvariable = self.__widgets[mode[0] + "_path_value"])
            self.__widgets[mode[0] + "_path_entry"].place(x=90, y=mode[2], width= 300)
            if mode[0] == "input":
                self.__widgets[mode[0] + "_path_value"].trace("w", self.__check_input_entry)

            #Button widget
            self.__widgets[mode[0] + "_path_button"] = tk.Button(self.__gui, text="...", command = partial(self.__file_explorer, mode[0]))
            self.__widgets[mode[0] + "_path_button"].place(x=395, y=mode[1], height=21)


            #String variable widget which dynamically changes in case of invalid path
            self.__widgets[mode[0] + "_invalid_path_value"] = tk.StringVar()

            #Label widget for invalid paths
            self.__inv_input_file_label = tk.Label(self.__gui, textvariable=self.__widgets[mode[0] + "_invalid_path_value"], foreground="red")
            self.__inv_input_file_label.place(x=20, y=mode[1]+27)
            
            if mode[0] == "input":
                #Button widget
                self.__widgets[mode[0] + "find_photos_button"] = tk.Button(self.__gui, text="Find Photos", command= self.__exl_w.excl_window)
                self.__widgets[mode[0] + "find_photos_button"].place(x=340, y=mode[1]+50, height=21)
            
            #Grouping Radio Buttons trial
            self.__widgets["grouping_frame"] = tk.Frame(self.__gui, bd=2,)# background="red"
            self.__widgets["grouping_frame"].place(x=20, y=190)

            ## Grouping Label
            self.__widgets["grouping_label"] = tk.Label(self.__widgets["grouping_frame"], text= "I 'll group your photos by..")
            self.__widgets["grouping_label"].grid(row=0, column=0, columnspan=3, sticky="w", pady=5)

            self.__widgets["grouping_str_var"] = tk.StringVar()

            self.__widgets["grouping_day"] = tk.Radiobutton(self.__widgets["grouping_frame"], text='Day', variable=self.__widgets["grouping_str_var"])
            self.__widgets["grouping_day"].config(indicatoron=0, bd=2, width=8, value='day')
            self.__widgets["grouping_day"].grid(row=1, column=0)
            self.__widgets["grouping_str_var"].set("day")

            self.__widgets["grouping_month"] = tk.Radiobutton(self.__widgets["grouping_frame"], text='Month', variable=self.__widgets["grouping_str_var"])
            self.__widgets["grouping_month"].config(indicatoron=0, bd=2, width=8, value='month')
            self.__widgets["grouping_month"].grid(row=1, column=1)

            self.__widgets["grouping_year"] = tk.Radiobutton(self.__widgets["grouping_frame"], text='Year', variable=self.__widgets["grouping_str_var"])
            self.__widgets["grouping_year"].config(indicatoron=0, bd=2, width=8, value='year')
            self.__widgets["grouping_year"].grid(row=1, column=2)

            # Name Pattern
            self.__widgets["naming_label"] = tk.Label(self.__gui, text= "Click the labels that you want to add in the name of your photo folders: ")
            self.__widgets["naming_label"].place(x=20, y=270)
            ## Place 
            self.__widgets["place_var"] = tk.IntVar()
            self.__widgets["place_checkbox"] = tk.Checkbutton(self.__gui, text="_place", variable=self.__widgets["place_var"])
            self.__widgets["place_checkbox"].place(x=20, y=290)
            ## Reason
            self.__widgets["reason_var"] = tk.IntVar()
            self.__widgets["reason_checkbox"] = tk.Checkbutton(self.__gui, text="_reason", variable=self.__widgets["reason_var"])
            self.__widgets["reason_checkbox"].place(x=20, y=310)
            ## People
            self.__widgets["people_var"] = tk.IntVar()
            self.__widgets["people_checkbox"] = tk.Checkbutton(self.__gui, text="_people", variable=self.__widgets["people_var"])
            self.__widgets["people_checkbox"].place(x=20, y=330)
    
    def __check_input_entry(self, *args):
        self.__run_button["state"] = "disabled"
        self.__change_widget_color(self.__widgets["inputfind_photos_button"], "lightpink")
    
    def __change_widget_color(self, widget, color):
        widget.config(background=color)

    def __validate_input_path(self):
        try:
            self.__photos_roots = input_path_validation(self.__widgets["input_path_value"].get())
        except Exception as e:
            self.__photos_roots = ""
            self.__widgets["input_invalid_path_value"].set(str(e))
        else:
            self.__widgets["input_invalid_path_value"].set("")

    def __file_explorer(self, mode):
        self.__widgets[mode+ "_path_button_value"] = filedialog.askdirectory(initialdir = "/",title = "Select file")
        self.__widgets[mode+ "_path_value"].set(self.__widgets[mode+ "_path_button_value"])
        if mode == "input":
            self.__run_button["state"] = "disabled"
    
    def __group_option(self):
        user_option = self.__widgets["grouping_str_var"].get()
        if user_option == "month":
            return False, True
        elif user_option == "year":
            return True, False
        else:
            return False, False
    
    def __create_name_pattern(self):
        name_pattern = ""
        for name_label in ["place", "reason", "people"]:
            if self.__widgets[ name_label + "_var"].get():
                name_pattern += self.__widgets[ name_label + "_checkbox"].cget("text")
        print(name_pattern)
        return name_pattern

    def __run_app(self):
        self.__validate_input_path()
        
        try:
            export_path_validation(self.__widgets["export_path_value"].get(), self.__widgets["input_path_value"].get(), self.__photos_roots)
        except Exception as e:
            self.__widgets["export_invalid_path_value"].set(str(e))
        else:
            self.__widgets["export_invalid_path_value"].set("")
            year, month = self.__group_option()
            name_pattern = self.__create_name_pattern()
            tidy_photos(self.__widgets["export_path_value"].get(), self.__exl_w._ExcludeWidnow__excl_photos_roots, year=year, month=month, name_pattern=name_pattern)
            open_export_folder(self.__widgets["export_path_value"].get())

if __name__ == "__main__":
    Gui()