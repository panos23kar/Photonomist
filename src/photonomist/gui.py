"""
This file hosts the graphical user interface code"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
import webbrowser
# Loading Window
from threading import Thread
from PIL import ImageTk
from PIL import Image
import base64
from io import BytesIO


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
        self.__user_paths()

        self.__start_gui() 
    
    def __main_window(self):
        """Specifies the title and dimensions of main window, and places the run button in the main window.
        |
        """
        self.__gui.title("Photonomist")
        self.__gui.geometry("440x420")

        #Run Button widget
        self.__run_button = tk.Button(self.__gui, text="Run, Forrest, Run!!", command= partial(self.__start_load_w_thread, self.__run_app), state="disabled")
        
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
        self.__main_menu.add_command(label="Info...", command=self.__info_app, underline=1)
    
    def __start_gui(self):
        """
        Starts the graphical user interface
        |
        """
        self.__gui.mainloop()

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
                self.__widgets[mode[0] + "find_photos_button"] = tk.Button(self.__gui, text="Find Photos", command= self.__excl_window)
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
            tidy_photos(self.__widgets["export_path_value"].get(), self.__excl_photos_roots, year=year, month=month, name_pattern=name_pattern)
            open_export_folder(self.__widgets["export_path_value"].get())
            
    #------------------------------ Exclude Window-------------------------------------#
    
    def __excl_window(self):
        try:
            self.__validate_input_path()
            if not self.__photos_roots:
                raise Exception
        except:
            pass
        else:
            # Triggers oading window
            self.__start_load_w_thread(self.__excl_w_layout)

    def __excl_w_layout(self):

        # Exclude window cconfiguration
        self.__found_photos_window = tk.Toplevel(self.__gui)
        self.__found_photos_window.title("Photos Folders")
        ## Exclude window gets the 'full' focus of the app
        self.__found_photos_window.grab_set()

        ##Canvas for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_canvas = tk.Canvas(self.__found_photos_window, borderwidth=0)#, background="#ffffff"
        self.__excl_w_canvas.bind_all("<MouseWheel>", self.__on_mousewheel)
        self.__excl_w_canvas.pack(side="left", fill="both", expand=True)

        ##Frame for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_frame = tk.Frame(self.__excl_w_canvas, background="grey95", padx=40)
        self.__excl_w_frame.bind("<Configure>", lambda event, canvas=self.__excl_w_canvas: self.__on_frame_configure())
        self.__excl_w_canvas.create_window((1,1), window=self.__excl_w_frame, anchor="n")

        ##Scrollbar for Exclude window
        self.__excl_w_scrollbar = tk.Scrollbar(self.__found_photos_window, orient="vertical", command=self.__excl_w_canvas.yview)
        self.__excl_w_scrollbar.pack(side="right", fill="y")
        self.__excl_w_canvas.configure(yscrollcommand=self.__excl_w_scrollbar.set)

        self.__excl_w_number_photos()
        self.__excl_w_checkboxes()
        self.__excl_w_resize_canvas()


    def __on_frame_configure(self):
        '''Reset the scroll region to encompass the inner frame'''
        self.__excl_w_canvas.configure(scrollregion=self.__excl_w_canvas.bbox("all"))
    
    def __on_mousewheel(self, event):
        """ It listens for mouse's wheel scrolling. 
        https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar"""
        self.__excl_w_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def __excl_w_number_photos(self):
        #Number of photos Label for Exclude window
        self.__number_of_photos = 0
        for photo_list in self.__photos_roots.values():
            self.__number_of_photos += len(photo_list)
        
        self.__widgets["Numb_photos_label"] = tk.Label(self.__excl_w_frame, text="I found " + str(self.__number_of_photos) + " photos in the folders below!\nUncheck the folders that you don't want me to touch!\n", justify="center")
        self.__widgets["Numb_photos_label"].pack(anchor="center")


    def __excl_w_checkboxes(self):
        self.__photos_folders = set(self.__photos_roots.keys())

        self.__excl_w_checkbox_variables = {}
        self.__excl_w_checkboxes_dict = {}
        self.__excl_w_checkboxes_arrow_label = {}

        self.__y_coord_link = 54
        for photo_folder in self.__photos_folders:
            self.__excl_w_checkbox_variables[photo_folder] = tk.IntVar(value=1)
            self.__excl_w_checkboxes_dict[photo_folder] = tk.Checkbutton(self.__excl_w_frame, text=photo_folder,  variable=self.__excl_w_checkbox_variables[photo_folder], onvalue = 1,  offvalue = 0)
            self.__excl_w_checkboxes_dict[photo_folder].pack(anchor="w")

            #link close to photo folder paths in order to open the folders in file explorer
            self.__excl_w_checkboxes_arrow_label[photo_folder] = tk.Label(self.__excl_w_frame, text="link", font="Helvetica 8 bold", fg="blue", cursor="hand2")
            self.__excl_w_checkboxes_arrow_label[photo_folder].place(x=self.__calculate_x_coord(len(photo_folder)), y=self.__y_coord_link)
            self.__excl_w_checkboxes_arrow_label[photo_folder].bind("<Button-1>", lambda e, photo_folder=photo_folder:self.__open_folder(photo_folder))
            self.__y_coord_link +=25
        
            
        self.__exclude_window_button = tk.Button(self.__excl_w_frame, text="Good2Go", command = self.__exclude_paths) #TODO --> Needs to be connected with a function
        self.__exclude_window_button.pack(side="bottom", padx=5, pady=5)
    
    def __calculate_x_coord(self, num_of_chars):#TODO-> quick and dirty. chnage it
        if num_of_chars <  20:
            return int(num_of_chars * 6.8 )
        elif num_of_chars <  30:
            return int(num_of_chars * 6.7 )
        elif num_of_chars <  40:
            return int(num_of_chars * 6.25 )
        elif num_of_chars <  50:
            return int(num_of_chars * 6.35 )
        elif num_of_chars <  60:
            return int(num_of_chars * 6.2 )
        elif num_of_chars <  70:
            return int(num_of_chars * 6.15 )
        elif num_of_chars <  80:
            return int(num_of_chars * 6.2 )
        elif num_of_chars <  90:
            return int(num_of_chars * 6.05 )
        elif num_of_chars <  100:
            return int(num_of_chars * 6.05 )
        elif num_of_chars <  110:
            return int(num_of_chars * 6)
        elif num_of_chars <  120:
            return int(num_of_chars * 5.9 )
        elif num_of_chars <  130:
            return int(num_of_chars * 5.85 )
        else:
            return int(num_of_chars * 5.85 )

    def __open_folder(self, photo_folder):
        open_export_folder(photo_folder)


    def __excl_w_resize_canvas(self):

        self.__excl_w_frame.update()


        print("Im here",self.__excl_w_frame.winfo_width())
        #self.__excl_w_frame.configure(width=self.__excl_w_frame.winfo_width() + 30)
        print("Now im here",self.__excl_w_frame.winfo_width())


        self.__excl_w_canvas.configure(width=self.__excl_w_frame.winfo_width())
        self.__excl_w_canvas.configure(height=self.__excl_w_frame.winfo_height())
        
    def __exclude_paths(self):
        """Check if I can get the excluded paths form exclude window"""
        for key,_ in self.__excl_w_checkboxes_dict.items():
            if  self.__excl_w_checkbox_variables[key.replace('\\\\','\\')].get() == 0:
                if key in self.__photos_roots:
                    del self.__photos_roots[key]
        self.__excl_photos_roots = self.__photos_roots.copy() # I had strange issues when I sent the photos_roots dict without copying
        self.__run_button["state"] = "normal"
        self.__change_widget_color(self.__widgets["inputfind_photos_button"], "grey95")
        # Close Toplevel window
        self.__found_photos_window.destroy()
        self.__found_photos_window.update()
    
    #------------------------------ Info Window-------------------------------------#

    def __info_app(self):

        # Info window cconfiguration
        self.__info_window = tk.Toplevel(self.__gui)
        self.__info_window.title("Photonomist Info")
        self.__info_window.geometry("640x400")
        ## Exclude window gets the 'full' focus of the app
        self.__info_window.grab_set()

        # Info Windows labels
        self.__info_w_labels = {}
        # Labels widget
        # Aim
        self.__info_w_labels["photonomist_title"] = tk.Label(self.__info_window, text= "Photonomist", font="Helvetica 16 bold italic")
        self.__info_w_labels["photonomist_title"].place(x=10, y=10)

        self.__info_w_labels["aim"] = tk.Label(self.__info_window, justify="left", text="Photonomist aims at helping photo-lovers (or simply photo-owners) with tidying their photos. \n\nGiven a path that contains photos, photonomist will: \n  - extract the dates of your photos, \n  - create 'date' directories \n  - group photos according to their dates", font="Helvetica 10")
        self.__info_w_labels["aim"].place(x=10, y=40)

        # Name
        self.__info_w_labels["name_title"] = tk.Label(self.__info_window, text= "It took its name from the words:", font="Helvetica 11 bold")
        self.__info_w_labels["name_title"].place(x=10, y=170)

        self.__info_w_labels["name"] = tk.Label(self.__info_window, justify="left", text="Photo..   --> Photography (art of captruring the light:: Greek root: (Φως) Φωτογραφία)\n..nomist  --> Taxonomist  (person who groups entities into categories:: Greek root: Ταξινομία ή Ταξινόμηση)", font="Helvetica 10")
        self.__info_w_labels["name"].place(x=10, y=190)

        # Email
        self.__info_w_labels["email"] = tk.Text(self.__info_window, font="Helvetica 10 bold", width=26, height=1)
        self.__info_w_labels["email"].insert(0.1,"photonomist.23@gmail.com")
        self.__info_w_labels["email"].place(x=10, y=245)
        self.__info_w_labels["email"].configure(bg=self.__info_window.cget('bg'), relief="flat")

        self.__info_w_labels["email_goals"] = tk.Label(self.__info_window, justify="left", text="  - ask for extra functionality \n  - report errors \n  - send your endless love", font="Helvetica 10")
        self.__info_w_labels["email_goals"].place(x=10, y=265)

        # Github Link
        self.__info_w_labels["github_link"] = tk.Label(self.__info_window, text="Click me.. ", font="Helvetica 10 bold", fg="blue", cursor="hand2")
        self.__info_w_labels["github_link"].place(x=10, y=339)
        self.__info_w_labels["github_link"].bind("<Button-1>", lambda e: self.__open_url("https://github.com/panos23kar/Photonomist/blob/master/README.rst"))

        self.__info_w_labels["github_link_text"] = tk.Label(self.__info_window, text=" for Motivation, Features and Development Notes. I definitely deserve your time :D !!")
        self.__info_w_labels["github_link_text"].place(x=75, y=340)
   
    def __open_url(self, url):
        webbrowser.open_new(url)
    
    #----------------------- Loading Window -----------------------------

    def __start_load_w_thread(self, func2run):
        self.__load_widnow_thread = Thread(target=func2run)
        self.__load_widnow_thread.start()

        self.__check_thread()
        #self.__loading_window.after(50, self.__check_thread)
    
    def __check_thread(self):

        if not self.__load_widnow_thread.is_alive():
            # Close Toplevel window
            self.__loading_window.destroy()
            self.__loading_window.update()

        else:
            self.__load_w_layout()
            self.__update_load_w = self.__draw_loading_camera().__next__
            self.__load_w_canvas.after(100, self.__update_load_w)            
    
    def __draw_loading_camera(self):
        image = Image.open(BytesIO(base64.b64decode(self.__filename)))
        angle = 0
        #while True:
        while self.__load_widnow_thread.is_alive():
            tkimage = ImageTk.PhotoImage(image.rotate(angle))
            canvas_obj = self.__load_w_canvas.create_image(
                250, 250, image=tkimage)
            self.__loading_window.after(30,self.__update_load_w)
            yield
            self.__load_w_canvas.delete(canvas_obj)
            angle -= 10
            angle %= 360
        
        self.__loading_window.destroy()
        self.__loading_window.update()
    
    def __load_w_layout(self):
        # Loading window image bytestream
        data = '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'
        self.__filename = data

        # Load window cconfiguration
        self.__loading_window = tk.Toplevel(self.__gui)
        self.__loading_window.title("I'm working on it!!")
        ## Load window gets the 'full' focus of the app
        self.__loading_window.grab_set()

        ##Canvas for Load window (it is need for scrolling (scrollbar) functionality)
        self.__load_w_canvas = tk.Canvas(self.__loading_window,  width=500, height=500)
        self.__load_w_canvas.pack()

if __name__ == "__main__":
    Gui()