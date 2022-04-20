from operator import contains
import string
import pyautogui
import cv2
import win32gui
import win32con
import numpy as np
import time
import string


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


def get_GJ_window():
    target_handle = get_window_names("古剑奇谭网络版")
    # print(target_handle)
    if target_handle == 0:
        return None
    else:
        return target_handle


def fetch_game_region():
    handle = get_GJ_window()
    print(win32gui.GetWindowText(handle))
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
                         win32con.SC_RESTORE, 0)

    # 设为高亮
    win32gui.SetForegroundWindow(handle)
    time.sleep(1)
    # 截图
    grab_image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot()), cv2.COLOR_RGB2BGR)

    # cv2.imshow("grab_image", grab_image)
    time.sleep(0.5)
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
                         win32con.SC_MINIMIZE, 0)
    # 选择ROI
    roi = cv2.selectROI(windowName="original", img=grab_image,
                        showCrosshair=True, fromCenter=False)
    x, y, w, h = roi
    # 防止卡死
    cv2.waitKey()
    cv2.destroyAllWindows()
    print(x,y,w,h)
    return [x,y,w,h]


# main
fetch_game_region()
