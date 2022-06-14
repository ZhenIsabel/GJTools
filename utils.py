import pyautogui
import cv2
import numpy as np
import pyautogui
import win32gui
import win32con
import win32api
import time
import string


def find_and_click(img, offset, threshold=0.95):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, img, 3)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
    if max_val > threshold:
        pyautogui.moveTo(max_loc[0] + offset[0], max_loc[1] + offset[1])
        pyautogui.leftClick()
        return True
    return False


def find_and_click_region(img, offset, region, method=3, threshold=0.95):
    image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, img, method)
    # show_imag(image)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
    if max_val > threshold:
        pyautogui.moveTo(max_loc[0] + offset[0]+region[0],
                         max_loc[1] + offset[1]+region[1])
        pyautogui.leftClick()
        return True
    return False


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


def show_imag(image, name='test'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_match_image(template, image, method=3):
    match_res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    print(max_val)
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = (top_left[0]+w, top_left[1]+h)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)
    show_imag(image)


def is_same_before_after(region: tuple, fun, *fun_paras, threshold=0.95):
    origin = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
    fun(*fun_paras)
    max_val, _ = match_img_region(origin, region)
    return max_val > threshold


def find_color_center(color_name, image):
    color = {
        "blue": {"color_lower": np.array([100, 43, 106]), "color_upper": np.array([125, 180, 200])},
        "red": {"color_lower": np.array([156, 43, 46]), "color_upper": np.array([180, 255, 255])},
        "yellow": {"color_lower": np.array([21, 43, 46]), "color_upper": np.array([34, 100, 255])},
        "green": {"color_lower": np.array([35, 43, 46]), "color_upper": np.array([77, 255, 255])},
    }
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 转成HSV
    img = cv2.GaussianBlur(img, (5, 5), 0)  # 高斯滤波降噪，模糊图片
    # img = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)[1]
    color_img = cv2.inRange(
        img, color[color_name]["color_lower"], color[color_name]["color_upper"])  # 筛选出符合的颜色
    kernel = np.ones((3, 3), np.uint8)  # 核定义
    color_img = cv2.erode(color_img, kernel, iterations=2)  # 腐蚀除去相关性小的颜色
    color_img = cv2.GaussianBlur(color_img, (5, 5), 0)  # 模糊图像
    cnts = cv2.findContours(
        color_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]  # 找出轮廓
    centers = []
    for cnt in cnts:  # 遍历所有符合的轮廓
        x, y, w, h = cv2.boundingRect(cnt)
        if w*h < 15*20:
            continue
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        centers.append([int((x+w)/2), int((y+h)/2)])
    return centers


def save_screen():
    image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    time_str = time.strftime('%m-%d-%H-%M-%S')
    return cv2.imwrite('./error_screenshot/'+time_str+'.png', image)


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


def deal_offline():
    # print('check offline')
    offline_tag = cv2.imread('img/offline.png')
    open_game_in_login = cv2.imread('img/open_game_in_login.png')
    open_game_in_role = cv2.imread('img/open_game_in_role.png')
    # 确认是否掉线
    if find_and_click(offline_tag, [30, 30]):
        pyautogui.sleep(15)
    # 重新登录
    window_focus('古剑奇谭网络版')
    if find_and_click(open_game_in_login, [30, 30]):
        pyautogui.sleep(50)
        window_focus('古剑奇谭网络版')
        pyautogui.sleep(2)
        pyautogui.leftClick()
        pyautogui.sleep(10)

    if find_and_click(open_game_in_role, [30, 30]):
        # 等待进入游戏
        pyautogui.sleep(40)
        reset_visual_field()
        pyautogui.sleep(0.5)
        reset_visual_field()
        return True
    return False


# 查找含有关键字的窗口，返回该窗口的handle
def get_window_from_name(keyword: string):
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for hwnd in hWndList:
        if win32gui.IsWindowVisible(hwnd):
            # class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            if not title:
                continue
            if str.find(title, keyword) != -1:
                # print(title)
                return hwnd

            # print(class_name)
            # print('------------------------------------')
    return None

def window_focus(name: string):
    handle = get_window_from_name(name)
    if handle is None:
        return
    print(win32gui.GetWindowText(handle))
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
                         win32con.SC_RESTORE, 0)

    # 设为高亮
    win32gui.SetForegroundWindow(handle)


def window_minimize(name: string):
    handle = get_window_from_name(name)
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
                         win32con.SC_MINIMIZE, 0)


def get_window_size(name: string):
    handle = get_window_from_name(name)
    if handle is None:
        return False
    size = win32gui.GetWindowRect(handle)
    return size  # x,y, width+x, height+y


def close_window(name: string):
    window_size = get_window_size(name)
    pyautogui.moveTo(window_size[2] - 15, window_size[1]+15)
    pyautogui.leftClick()
