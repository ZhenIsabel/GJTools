from Farm import find_box, role_move, role_loc,get_weather
import math
import config_model
import cv2
import pyautogui
import imutils
import numpy as np

find_tip = cv2.imread('img/find_tip.png')
find_tip_night = cv2.imread('img/find_tip_night.png')
too_far_tip = cv2.imread('img/too_far.png')
night_tip = cv2.imread('img/night_tip.png')
rain_tip = cv2.imread('img/rain_tip.png')



# 脚下可开盒子区域
box_under_footer_area = [1042, 740, 420, 288]

# 脚下中心点
footer_pos = [1280, 790]


# 盒子大小
box_area_up = 1400
box_area_down = 400

# 开盒子时间
open_box_time = 4

# 太远了提示位置
too_far_area = [909, 353, 150, 100]

weather_area = [1980, 160, 100, 50]


def entry(loc_list: list):
    dig_count = 0
    for i in range(0, len(loc_list)):
        role_move.move_to(loc_list[i], 0)
        seperate=4
        for j in range(0, seperate):
            role_move.turn_around(1/seperate)
            dig_count = dig_count+find_box_straight()
    pass


def find_box_straight():
    
    pass



def find_box_under_footer():
    weather_code = get_weather.get_weather_code()
    first_check = find_box_in_area_color(box_under_footer_area, weather_code)
    if not first_check:
        return False
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(
        region=too_far_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, too_far_tip, 3)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
    # print(max_val)
    if max_val > 0.9:
        pos = pyautogui.position()
        # print(pos)
        if pos[0] - footer_pos[0] > 100:
            role_move.move(2, 0)
        if pos[0] - footer_pos[0] < -100:
            role_move.move(-2, 0)
        if pos[1] - footer_pos[1] > 100:
            role_move.move(0, -0.7)
        find_box_in_area_color(box_under_footer_area, weather_code)
    find_box_in_area_color(box_under_footer_area, weather_code)
    return True


def find_box_in_area_color(region, weather_code=0,is_open_box=True):
    threshold_value = [80, 60, 40]
    if config_model.config['is_binarization']:
        threshold_value = [170, 80, 80]
    image_grey = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=region)), cv2.COLOR_RGB2GRAY)
    # cv2.imshow('img_origin', image_grey)
    # cv2.waitKey(0)
    ret, image = cv2.threshold(
        image_grey, threshold_value[weather_code], 255, cv2.THRESH_BINARY_INV)
    image = cv2.dilate(image, kernel=np.ones((3, 3), np.uint8), iterations=1)
    cnts = cv2.findContours(
        image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    # cv2.imshow('img', image)
    # cv2.waitKey(0)
    # 遍历所有轮廓
    for c in cnts:
        # 计算轮廓所包含的面积
        area = cv2.contourArea(c)
        # print(area)
        if box_area_up >= area >= box_area_down:
            # print(area)
            # 获取中心点
            M = cv2.moments(c)
            cZ = M["m00"]
            if cZ == 0:
                cZ = 1
            cX = int(M["m10"] / cZ)
            cY = int(M["m01"] / cZ)
            pyautogui.moveTo(region[0] + cX, region[1] + cY,pyautogui.easeInOutQuad)
            if is_on_box_by_tip([region[0], region[1] - 50, region[2] + 150, region[3] + 50], weather_code > 0):
                if is_open_box:
                    pyautogui.rightClick()
                    pyautogui.sleep(open_box_time)
                return True
    return False




def move_to_box_mark_on_ground():
    target_loc = get_box_mark_loc()
    if target_loc is None:
        return True
    diff_loc = [target_loc[0] - config_model.config['role_screen_pos'][0], target_loc[1] - config_model.config['role_screen_pos'][1]]
    temp_direct = math.atan2(diff_loc[1], diff_loc[0]) / math.pi + 0.5
    role_move.turn_around(temp_direct)
