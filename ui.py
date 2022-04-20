import tkinter
from tkinter import ttk
import win32api
import win32con

def create_window(name: str):  # 创建窗口
    win = tkinter.Tk()
    win.title(name)
    # Main Window min width
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) 
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    window_width = screen_width * .01
    window_height = screen_height * .04

    # Window startst in center of screen
    window_start_x = (screen_width/2)
    window_start_y = (screen_height/2)
    win.geometry("%dx%d+%d+%d" % (window_width,
                              window_height, window_start_x, window_start_y))
    # buttonsFrame.pack(side=TOP)
    # win.mainloop()


create_window("猫猫挖宝")
