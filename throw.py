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


def clear_map(buy_count):
    pyautogui.press(config_model.config['key_map'])
    time.sleep(0.5)
    max_val, max_loc = match_img(map_title, 5)
    # print(max_val)
    if max_val < 0.6:
        # 切换到挖宝地图
        pyautogui.moveTo(open_box_map_pos[0], open_box_map_pos[1])
        pyautogui.leftClick()
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


def buy_map():
    
    map_in_store = cv2.imread('img/map_in_store.png')
    open_map_btn = cv2.imread('img/open_map.png')
    map_title = cv2.imread('img/map_title.png')
    buy_map_tip = cv2.imread('img/buy_map_tip.png')
    confirm_btn = cv2.imread('img/confirm_btn.png')
    bag_left = cv2.imread('img/bag_left.png')
    store_npc = cv2.imread('img/store_npc.png')
    max_val = 0
    fitness_threshold=0.95
    pyautogui.press('g')
    #  pyautogui.press('f')
    time.sleep(1)
    max_val, max_loc = match_img(map_in_store)
    if max_val <= fitness_threshold:
        return False
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.keyDown('shift')
    pyautogui.rightClick()
    pyautogui.keyUp('shift')
    max_val, max_loc = match_img(buy_map_tip)
    # 确定买图数量
    buy_count = int(
        config_model.config['count_yuanbo'] if config_model.config['is_yuanbo'] else config_model.config['count_no_yuanbo'])
    buy_count_string = str(buy_count)
    if max_val > 0.95:
        pyautogui.press('3')
        pyautogui.press('9')
        # 增加延迟
        # # improve_direction.check_ping(try_times=20)
        # for i in range(len(buy_count_string)):
        #     pyautogui.press(buy_count_string[i])
        # improve_direction.check_ping(try_times=20)
        pyautogui.press('enter')
        pyautogui.click(x=None, y=None, clicks=11, interval=0.001,
                        button='right', duration=0.0, tween=pyautogui.linear)
        # max_val, max_loc = match_img(confirm_btn)
        # if max_val > fitness_threshold:
        #     pyautogui.moveTo(max_loc[0] + 50, max_loc[1] + 15)
        #     pyautogui.leftClick()
    return True



buy_count=input('count of throw\n')
time.sleep(2)
clear_map(int(buy_count))

# time.sleep(1)
# buy_map()