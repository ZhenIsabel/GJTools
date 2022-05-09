import pyautogui
import cv2
import numpy as np
night_tip = cv2.imread('img/night_tip.png')
rain_tip = cv2.imread('img/rain_tip.png')
weather_area = [1980, 160, 100, 50]

def get_weather_code():
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=weather_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, night_tip, 3)
    min_val, max_val_night, min_loc, max_loc = cv2.minMaxLoc(match_res)
    is_night = max_val_night > 0.92
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=weather_area)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, rain_tip, 3)
    min_val, max_val_rain, min_loc, max_loc = cv2.minMaxLoc(match_res)
    is_rain = max_val_rain > 0.92
    if max_val_rain-max_val_night>0.04:
        is_night=False
    weather_code = 0
    if is_night:
        weather_code = 2
    elif is_rain:
        weather_code = 1
    return weather_code


def get_weather_name():
    weather_code=get_weather_code()
    if weather_code==0:
        return '晴'
    if weather_code==1:
        return '雨'
    if weather_code==2:
        return '夜'