import time

import utils
import cv2
import numpy as np
import pyautogui
import config

time.sleep(0.5)
continue_btn=cv2.imread('img/continue_btn.png')
in_turn = cv2.imread('img/not_turn.png')

def is_my_turn():
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

    max_val, _ = utils.match_img(in_turn,method=3)
    utils.show_match_image(in_turn,image
    )
    # print(max_val)
is_my_turn()