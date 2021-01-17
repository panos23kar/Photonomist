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
        self.__angle = 0
        self.__read_loading_image_bytestream()
        self.__load_image = Image.open(BytesIO(base64.b64decode(self.__filename)))

    def __read_loading_image_bytestream(self):
        try:
            with open(r'src\photonomist\gui\load_image_bytes.json') as image_bytestream:
                self.__filename = json.load(image_bytestream)["data"]
        except:
            pass

    def start_load_w_thread(self, func2run):
        self.__load_widnow_thread = Thread(target=func2run)
        self.__load_widnow_thread.start()
        # Loading Image window while photonomist is working on user's request
        self.__check_thread()
    
    def __check_thread(self):
        if not self.__load_widnow_thread.is_alive():
            self.__close_toplevel()
        else:
            self.__load_w_layout()
            self.__update_load_w = self.__draw_loading_camera().__next__
            self.__load_w_canvas.after(100, self.__update_load_w)
    
    def __close_toplevel(self):
        self.__loading_window.destroy()
        self.__loading_window.update()

    def __load_w_layout(self):
        self.__create_toplevel()
        self.__create_canvas()

    def __create_toplevel(self):
        self.__loading_window = tk.Toplevel(self.__gui)
        self.__loading_window.title("I'm working on it!!")
        self.__loading_window.grab_set()

    def __create_canvas(self):
        self.__load_w_canvas = tk.Canvas(self.__loading_window,  width=500, height=500)
        self.__load_w_canvas.pack()
    
    def __draw_loading_camera(self):
        # Redrwaing the loading image window while photonomist is working
        while self.__load_widnow_thread.is_alive():
            self.__tkimage = ImageTk.PhotoImage(self.__load_image.rotate(self.__angle))
            self.__canvas_obj = self.__load_w_canvas.create_image(250, 250, image=self.__tkimage)
            self.__loading_window.after(30,self.__update_load_w)
            yield
            self.__load_w_canvas.delete(self.__canvas_obj)
            self.__angle = (self.__angle-10)%360
        
        self.__close_toplevel()