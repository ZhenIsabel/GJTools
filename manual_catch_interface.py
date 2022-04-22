from curses import window
from operator import contains
import string
import pyautogui
import cv2
import win32gui
import win32con
import numpy as np
import time
import string

import window_control


def fetch_game_region():
    window_control.window_focus()
    time.sleep(1)
    # 截图
    grab_image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

    # cv2.imshow("grab_image", grab_image)
    time.sleep(0.5)
    window_control.window_minimize()
    # 选择ROI
    roi = cv2.selectROI(windowName="original", img=grab_image,
                        showCrosshair=True, fromCenter=False)
    x, y, w, h = roi
    # 防止卡死
    cv2.waitKey()
    cv2.destroyAllWindows()
    print(x,y,w,h)
    return [x,y,w,h]


# main
fetch_game_region()
