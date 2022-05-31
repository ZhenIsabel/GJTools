import time

import cv2
import role_move
import find_box
import numpy as np
import pyautogui
# time.sleep(3)
# role_action.reset_visual_field()


def show_imag(image, name='test'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_match_image(match_res, template, image):
    min_val, max_val, min_loc, max_loc = cv2.dminMaxLoc(match_res)
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = (top_left[0]+w, top_left[1]+h)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)
    show_imag('temp', image)


def move_test():
    begin_find_loc_2 = [-980, -530]
    begin_find_loc_1 = [-825, -540]
    find_area_2 = [55, 30]
    begin_find_direct_1 = 0.6
    find_area_1 = [65, 42]
    begin_find_direct_2 = -0.5
    role_move.move_to(begin_find_loc_1, None, 1, 5)
    role_move.turn_to(begin_find_direct_1)
    role_move.move_map(find_area_1[0],
                       find_area_1[1], find_box.find_box_under_footer,
                       origin=begin_find_loc_1,
                       region=1
                       )


# cost_20 = cv2.imread('img/cost_20.png')
# cost_800 = cv2.imread('img/cost_800.png')
time.sleep(2)
# import pyautogui
# import numpy as np
# clear_finish = cv2.imread('img/clear_finish.png')
# image_read = cv2.cvtColor(np.asarray(
# pyautogui.screenshot(region=[1930, 303, 240, 202])), cv2.COLOR_RGB2BGR)
# match_res_20 = cv2.matchTemplate(clear_finish, image_read, 5)
# min_val, max_val_count_check, min_loc, max_error_loc = cv2.minMaxLoc(
# match_res_20)
# print(max_val_count_check)
# if max_val_count_check<0.95:
#     matxh_res_800=cv2.matchTemplate(cost_800, image_read, 3)
#     min_val, max_val_count_check, min_loc, max_error_loc = cv2.minMaxLoc(
# matxh_res_800)
# print(max_val_count_check)
# if max_val_count_check < 0.95 :
#     extra_buy_count = 10
# role_move.move_to(begin_find_loc_1, None, 1, 5)
# for i in range(0,len(role_move.move_log)):
#     print(role_move.move_log[i])
read_area = [1104, 999, 368, 50]
image_origin = cv2.cvtColor(np.asarray(
    pyautogui.screenshot(region=read_area)), cv2.COLOR_RGB2BGR)
# show_imag(image_origin)
for i in range(0, 5):
    time.sleep(2)
    # 匹配开图读条区域
    image_read = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=read_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image_origin, image_read, 3)
    _, max_val, _, _ = cv2.minMaxLoc(match_res)
    print(max_val)
