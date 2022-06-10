import time

import utils
import cv2
import numpy as np
import pyautogui

time.sleep(1)
continue_btn=cv2.imread('img/continue_btn.png')

utils.show_match_image(continue_btn,cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
)