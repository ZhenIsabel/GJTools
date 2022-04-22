import string
import win32gui
import win32con
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