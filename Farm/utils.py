import pyautogui
import cv2
import numpy as np
import pyautogui
import window_control
import config_model
import win32api
import win32con
import time

def switch_style(style: int):
    # 左上角风格化中心坐标
    style_loc = [434, 183]
    # 自定义位置
    style_custom_loc = [398, 336]
    custom_confirm_loc = [1374, 893]
    # 推荐位置
    style_default_loc = [404, 215]

    pyautogui.moveTo(style_loc)
    pyautogui.click()
    if style == 0:
        pyautogui.moveTo(style_default_loc[0], style_default_loc[1])
        pyautogui.click()
    elif style == 1:
        pyautogui.moveTo(style_custom_loc[0], style_custom_loc[1])
        pyautogui.click()
        pyautogui.moveTo(custom_confirm_loc[0], custom_confirm_loc[1])
        pyautogui.click()
        pyautogui.move(400, 400)
        pyautogui.click()


def auto_switch(weather_name):
    if weather_name == '雨':
        switch_style(1)
    else:
        switch_style(0)


def find_and_click(img, offset, threshold=0.95):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, img, 3)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
    if max_val > threshold:
        pyautogui.moveTo(max_loc[0] + offset[0], max_loc[1] + offset[1])
        pyautogui.leftClick()
        return True
    return False


def reset_visual_field():
    x, y = 1000, 300
    win32api.SetCursorPos((x, y))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 300)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -200)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def match_img(template, method=3):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, method)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
    # test.show_match_image(match_res,template,image)
    return max_val, max_loc


def match_img_region(template, region, method=3):
    image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    # test.show_match_image(match_res,template,image)
    return max_val, max_loc

def deal_offline():
    # print('check offline')
    offline_tag = cv2.imread('img/offline.png')
    open_game_in_login = cv2.imread('img/open_game_in_login.png')
    open_game_in_role = cv2.imread('img/open_game_in_role.png')
    # 确认是否掉线
    if find_and_click(offline_tag, [30, 30]):
        pyautogui.sleep(15)
    # 重新登录
    if find_and_click(open_game_in_login, [30, 30]):
        pyautogui.sleep(50)
        window_control.window_focus('古剑奇谭网络版')
        pyautogui.sleep(2)
        pyautogui.leftClick()
        pyautogui.sleep(10)
    
    if find_and_click(open_game_in_role, [30, 30]):
        # 等待进入游戏
        pyautogui.sleep(80)

        # 取消勾选小地图标记
        pyautogui.press('m')
        pyautogui.sleep(2)
        pyautogui.moveTo(496, 851)  # 勾选框位置
        pyautogui.leftClick()
        pyautogui.press('m')
        pyautogui.sleep(2)
        # 视角和上马
        pyautogui.scroll(-20000)
        reset_visual_field()
        time.sleep(0.5)
        reset_visual_field()
        return True
    return False
