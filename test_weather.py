import time
import cv2
import numpy as np
import pyautogui
import get_weather

# 脚下可开盒子区域
box_under_footer_area = [1042, 740, 474, 288]
# 脚下可开盒子区域
# box_under_footer_area = [1035, 735, 500, 250]

# 脚下中心点
# footer_pos = [1285,790]
# 测试值
test_value = 60


def weather_test(threshold_value: list):
    time.sleep(1)

    weather_code = get_weather.get_weather_code()
    if weather_code == 0:
        print('晴')
    if weather_code == 1:
        print('雨')
    if weather_code == 2:
        print('夜')
    image_grey = cv2.cvtColor(np.asarray(pyautogui.screenshot(
        region=box_under_footer_area)), cv2.COLOR_RGB2GRAY)

    ret, image = cv2.threshold(
        image_grey, threshold_value[weather_code], 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Default Find Box", image)
    print("当前设置参数为" + str(threshold_value[weather_code]))

    ret, image = cv2.threshold(
        image_grey, test_value, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Test Find Box", image)
    print("当前测试参数为" + str(test_value))

    # ret, image = cv2.threshold(
    #     image_grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # cv2.imshow("Auto Find Box", image)
    # print("当前推荐参数为" + str(ret))
    cv2.waitKey()
