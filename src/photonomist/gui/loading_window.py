from threading import Thread
from PIL import ImageTk
from PIL import Image
import base64
from io import BytesIO
import tkinter as tk
import json

class LoadingWindow():
    def __init__(self, main_window):
        self.__gui = main_window

    def start_load_w_thread(self, func2run):
        self.__load_widnow_thread = Thread(target=func2run)
        self.__load_widnow_thread.start()

        self.__check_thread()
        #self.__loading_window.after(50, self.__check_thread)
    
    def __close_toplevel(self):
        self.__loading_window.destroy()
        self.__loading_window.update()
    
    def __check_thread(self):

        if not self.__load_widnow_thread.is_alive():
            self.__close_toplevel()
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
        with open(r'src\photonomist\gui\load_image_bytes.json') as image_bytestream:
            data = json.load(image_bytestream)
            self.__filename = data["data"]

        # Load window cconfiguration
        self.__loading_window = tk.Toplevel(self.__gui)
        self.__loading_window.title("I'm working on it!!")
        ## Load window gets the 'full' focus of the app
        self.__loading_window.grab_set()

        ##Canvas for Load window (it is need for scrolling (scrollbar) functionality)
        self.__load_w_canvas = tk.Canvas(self.__loading_window,  width=500, height=500)
        self.__load_w_canvas.pack()