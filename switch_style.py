import pyautogui

def switch_style(style:int):
    # 左上角风格化中心坐标
    style_loc=[434,183]
    # 自定义位置
    style_custom_loc=[398,336]
    custom_confirm_loc=[1374,893]
    # 推荐位置
    style_default_loc=[404,215]

    pyautogui.moveTo(style_loc)
    pyautogui.click()
    if style==0:
        pyautogui.moveTo(style_default_loc[0],style_default_loc[1])
        pyautogui.click()
    elif style==1:
        pyautogui.moveTo(style_custom_loc[0],style_custom_loc[1])
        pyautogui.click()
        pyautogui.moveTo(custom_confirm_loc[0],custom_confirm_loc[1])
        pyautogui.click()
        pyautogui.move(400,400)
        pyautogui.click()
   
   
def auto_switch (weather_name):
    if weather_name=='雨':
        switch_style(1)
    else:
        switch_style(0)
        