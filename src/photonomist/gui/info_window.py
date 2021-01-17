import tkinter as tk
import webbrowser


class InfoWindow():
    def __init__(self, main_window):
        self.__gui = main_window

    def info_app(self):
        """Info window configuration"""

        self.__init_window()

        ## Exclude window gets the 'full' focus of the app
        self.__info_window.grab_set()

        # Info Window's labels
        self.__info_w_labels = {}

        self.__title()
        self.__aim()
        self.__name()
        self.__email()
        self.__github()
    
    def __init_window(self):
        self.__info_window = tk.Toplevel(self.__gui)
        self.__info_window.title("Photonomist Info")
        self.__info_window.geometry("640x400")
    
    def __title(self):
        self.__info_w_labels["photonomist_title"] = tk.Label(self.__info_window, text= "Photonomist", font="Helvetica 16 bold italic")
        self.__info_w_labels["photonomist_title"].place(x=10, y=10)
    
    def __aim(self):
        self.__info_w_labels["aim"] = tk.Label(self.__info_window, justify="left", text="Photonomist aims at helping photo-lovers (or simply photo-owners) with tidying their photos. \n\nGiven a path that contains photos, photonomist will: \n  - extract the dates of your photos, \n  - create 'date' directories \n  - group photos according to their dates", font="Helvetica 10")
        self.__info_w_labels["aim"].place(x=10, y=40)
    
    def __name(self):
        self.__info_w_labels["name_title"] = tk.Label(self.__info_window, text= "It took its name from the words:", font="Helvetica 11 bold")
        self.__info_w_labels["name_title"].place(x=10, y=170)

        self.__info_w_labels["name"] = tk.Label(self.__info_window, justify="left", text="Photo..   --> Photography (art of captruring the light:: Greek root: (Φως) Φωτογραφία)\n..nomist  --> Taxonomist  (person who groups entities into categories:: Greek root: Ταξινομία ή Ταξινόμηση)", font="Helvetica 10")
        self.__info_w_labels["name"].place(x=10, y=190)
    
    def __email(self):
        self.__info_w_labels["email"] = tk.Text(self.__info_window, font="Helvetica 10 bold", width=26, height=1)
        self.__info_w_labels["email"].insert(0.1,"photonomist.23@gmail.com")
        self.__info_w_labels["email"].place(x=10, y=245)
        self.__info_w_labels["email"].configure(bg=self.__info_window.cget('bg'), relief="flat")

        self.__info_w_labels["email_goals"] = tk.Label(self.__info_window, justify="left", text="  - ask for extra functionality \n  - report errors \n  - send your endless love", font="Helvetica 10")
        self.__info_w_labels["email_goals"].place(x=10, y=265)

    def __github(self):
        self.__info_w_labels["github_link"] = tk.Label(self.__info_window, text="Click me.. ", font="Helvetica 10 bold", fg="blue", cursor="hand2")
        self.__info_w_labels["github_link"].place(x=10, y=339)
        self.__info_w_labels["github_link"].bind("<Button-1>", lambda e: self.__open_url("https://github.com/panos23kar/Photonomist/blob/master/README.rst"))

        self.__info_w_labels["github_link_text"] = tk.Label(self.__info_window, text=" for Motivation, Features and Development Notes. I definitely deserve your time :D !!")
        self.__info_w_labels["github_link_text"].place(x=75, y=340)
   
    def __open_url(self, url):
        webbrowser.open_new(url)