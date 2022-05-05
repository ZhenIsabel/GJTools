import pyautogui
import config_model
import time
import cv2
import numpy as np

map_title = cv2.imread('img/map_title.png')
confirm_btn = cv2.imread('img/confirm_btn.png')
close_btn = cv2.imread('img/close_btn.png')
open_box_map_pos = [880, 191]
first_map_pos = [2069, 522]



def match_img(template, method=3):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    # test.show_match_image(match_res,template,image)
    return max_val, max_loc


def clear_map():
    pyautogui.press(config_model.config['key_map'])
    time.sleep(0.5)
    max_val, max_loc = match_img(map_title, 5)
    # print(max_val)
    if max_val < 0.6:
        # 切换到挖宝地图
        pyautogui.moveTo(open_box_map_pos[0], open_box_map_pos[1])
        pyautogui.leftClick()
    buy_count = 20
    for i in range(0, buy_count):
        pyautogui.moveTo(first_map_pos[0], first_map_pos[1])
        pyautogui.rightClick()
        pyautogui.moveTo(first_map_pos[0] + 50, first_map_pos[1] + 30)
        pyautogui.leftClick()
        pyautogui.press('enter')
        # pyautogui.moveTo(confirm_pos[0], confirm_pos[1])
        # pyautogui.leftClick()
    pyautogui.moveTo(first_map_pos[0] - 50, first_map_pos[1] - 50)
    pyautogui.leftClick()
    pyautogui.press(config_model.config['key_map'])
    return True

time.sleep(2)
clear_map()