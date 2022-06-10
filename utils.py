import pyautogui
import cv2
import numpy as np
import pyautogui
import win32gui
import win32con
import time
import string


def find_and_click(img, offset,region=[0,0,2560,1440], threshold=0.95):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, img, 3)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_res)
    if max_val > threshold:
        pyautogui.moveTo(max_loc[0] + offset[0]+region[0], max_loc[1] + offset[1]+region[1])
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


def show_match_image(template, image):
    match_res = cv2.matchTemplate(image, template, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    print(max_val)
    top_left = max_loc
    h, w = template.shape[:2]
    bottom_right = (top_left[0]+w, top_left[1]+h)
    cv2.rectangle(image, top_left, bottom_right, 255, 2)
    show_imag(image)


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
        window_focus('古剑奇谭网络版')
        pyautogui.sleep(2)
        pyautogui.leftClick()
        pyautogui.sleep(10)
    
    if find_and_click(open_game_in_role, [30, 30]):
        # 等待进入游戏
        pyautogui.sleep(40)
        return True
    return False


# 查找含有关键字的窗口，返回该窗口的handle
def get_window_names(keyword: string):
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


def get_window_from_name(name:string):
    target_handle = get_window_names(name)
    # print(target_handle)
    if target_handle == 0:
        return None
    else:
        return target_handle

def window_focus(name:string):
    handle = get_window_from_name(name)
    print(win32gui.GetWindowText(handle))
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
                         win32con.SC_RESTORE, 0)

    # 设为高亮
    win32gui.SetForegroundWindow(handle)

def window_minimize(name:string):
    handle = get_window_from_name(name)
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
                         win32con.SC_MINIMIZE, 0)