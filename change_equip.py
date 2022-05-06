import pyautogui
import cv2


def match_img(template):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    return max_val, max_loc



def change_equip():
    equip_box = cv2.imread('img/equip_box.png')
    equip_empty = cv2.imread('img/equip_empty.png')

    pyautogui.press('c')
    pyautogui.sleep(0.5)
    max_val, max_loc = match_img(equip_empty)
    if max_val > 0.9:
        pyautogui.moveTo(max_loc[0] + 14, max_loc[1] + 14)
        pyautogui.click()
    pyautogui.sleep(1)
    max_val, max_loc = match_img(equip_box)
    if max_val > 0.9:
        pyautogui.moveTo(max_loc[0] + 14, max_loc[1] + 14)
        pyautogui.click()
    pyautogui.sleep(0.5)
    pyautogui.press('c')

