# import cv2
import pyautogui
# import easyocr
import re


def get_clear_map_count(try_times=5):
    re_cmp = re.compile('-?[1-9]\d*')
    # 丢图藏宝图坐标
    # clear_map_area = [1698, 158, 52, 27]
    clear_map_area = [2011, 309, 52, 27]
    # 获取丢图计数二值化参数
    clear_map_count_param = 210
    image = pyautogui.screenshot(region=clear_map_area)
    # cv2.imshow("截屏", binary)
    # cv2.waitKey(0)
    reader=easyocr.Reader(lang_list=['en'],gpu=True)
    text = reader.readtext(image)
    print(text)
    # print(f'位置：{text}')
    count_str = re_cmp.findall(text)
    if count_str == []:
        clear_map_count = int(50)
    else:
        clear_map_count = int(count_str[0])
    # print(count_str)
    # print(str(clear_map_count))
    if clear_map_count>=50:
        clear_map_count=45
    return clear_map_count

get_clear_map_count()