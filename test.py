import time

import cv2
import role_move
import role_action
import find_box
import config_model
import pyautogui
import pyperclip
import numpy as np

# time.sleep(3)
# role_action.reset_visual_field()

def show_imag(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_match_image(match_res,template,image):
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = (top_left[0]+w, top_left[1]+h)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)
    show_imag('temp', image)


def move_test():
    begin_find_loc_2 = [-980, -530]
    find_area_2 = [55, 30]
    begin_find_direct_2 = -0.5
    role_move.move_to(begin_find_loc_2, None, 1, 5)
    role_move.turn_to(begin_find_direct_2)
    role_move.move_map(find_area_2[0],
                                find_area_2[1], find_box.find_box_under_footer,
                                begin_find_loc_2
                                )
# move_test()
time.sleep(3)
# role_action.remove_debuff()
# role_action.find_boxs()
# role_action.avoid_open_interrupt()

# image=cv2.imread('D:/test.png')
# temp=cv2.imread('D:/open_complete_day.png')

# pyautogui.moveTo(417,1220)
# pyautogui.leftClick()
# pyperclip.copy('饼哥好')
# time.sleep(0.5)
# pyautogui.keyDown('ctrl')
# pyautogui.press('v')
# pyautogui.keyUp('ctrl')
# pyautogui.press('enter')

# para=input('test')
# print(para)\
cost_220=cv2.imread('img/cost_20.png')
extra_buy_count=0
image_read = cv2.cvtColor(np.asarray(
                pyautogui.screenshot(region=[327,1022,402,203])), 
                cv2.COLOR_RGB2BGR
                )
match_res = cv2.matchTemplate(cost_220, image_read, 3)
min_val, max_val_count_check, min_loc, max_error_loc = cv2.minMaxLoc(match_res)
if max_val_count_check < 0.95:
        extra_buy_count = 10
print('匹配：'+str(max_val_count_check)+', 额外购买：'+str(extra_buy_count))
show_match_image(match_res,cost_220,image_read)