from asyncio.log import logger
import datetime
import time

import cv2
import numpy as np
import pyautogui
import win32api
import win32con

import config_model
import find_box
import log_message
import role_loc
import role_move
import send_message


map_in_store = cv2.imread('img/map_in_store.png')
open_map_btn = cv2.imread('img/open_map.png')
map_title = cv2.imread('img/map_title.png')
buy_map_tip = cv2.imread('img/buy_map_tip.png')
confirm_btn = cv2.imread('img/confirm_btn.png')
bag_left = cv2.imread('img/bag_left.png')
store_npc = cv2.imread('img/store_npc.png')
open_map_error = cv2.imread('img/open_map_error.png')
home_door_btn = cv2.imread('img/home_door_btn.png')
home_main_btn = cv2.imread('img/home_main_btn.png')
back_origin_btn = cv2.imread('img/back_origin_btn.png')
new_day_tip = cv2.imread('img/new_day_tip.png')
close_btn = cv2.imread('img/close_btn.png')
horse = cv2.imread('img/horse.png')


# 点开藏宝地图模式位置
# open_box_map_pos = [500, 50]
open_box_map_pos = [880, 191]

# 要丢掉的首张图位值
# first_map_pos = [1750, 350]
first_map_pos = [2069, 522]

# 确定按钮位置
confirm_pos = [880, 450]

# 傻逼的opencv模式匹配的匹配度阈值
# 再给我在游戏截图里匹配出95%的缺头怪我就把你大爷杀了
# by 无能狂怒的谢振衣
fitness_threshold = 0.95


# 打开藏宝图等待时间
# wait_open_time = 148 # 无渊博75
# wait_open_time = 75

# 第一个挖宝区域大小
begin_find_loc_1 = [-825, -525]
begin_find_direct_1 = 0.6
# find_area_1 = [55, 47]
# # find_area_1 = [60, 47]

# 第二个挖宝区域大小
begin_find_loc_2 = [-980, -530]
begin_find_direct_2 = -0.5
# find_area_2 = [55, 27]
# # find_area_2 = [60, 30]

# 背包格子大小
bag_item_size = 36
bag_width = 12

# 家园走到门口的位移距离
home_to_door = [-10, 0]


def match_img(template, method=3):
    image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    # test.show_match_image(match_res,template,image)
    return max_val, max_loc


# def clear_map(count=20):
def clear_map():
    log_message.log_info("清理残图")
    pyautogui.press(config_model.config['key_map'])
    time.sleep(0.5)
    max_val, max_loc = match_img(map_title, 5)
    # print(max_val)
    if max_val < 0.6:
        # 切换到挖宝地图
        log_message.log_info("切换到挖宝地图")
        log_message.log_debug("匹配率："+str(max_val))
        pyautogui.moveTo(open_box_map_pos[0], open_box_map_pos[1])
        pyautogui.leftClick()
    buy_count = int(
        config_model.config['count_yuanbo'] if config_model.config['is_yuanbo'] else config_model.config['count_no_yuanbo'])
    log_message.log_debug("清理数量为："+str(buy_count))
    for i in range(0, buy_count):
        pyautogui.moveTo(first_map_pos[0], first_map_pos[1])
        pyautogui.rightClick()
        pyautogui.moveTo(first_map_pos[0] + 50, first_map_pos[1] + 30)
        pyautogui.leftClick()
        pyautogui.press('enter')
        # pyautogui.moveTo(confirm_pos[0], confirm_pos[1])
        # pyautogui.leftClick()
    pyautogui.moveTo(first_map_pos[0] - 50, first_map_pos[1] - 50)
    pyautogui.leftClick()
    pyautogui.press(config_model.config['key_map'])
    log_message.log_info("清理残图完毕")
    return True


def buy_map():
    log_message.log_info("买图")
    max_val = 0
    for i in range(0, 10):
        time.sleep(0.2)
        max_val, max_loc = match_img(store_npc)
        # print(max_val)
        if max_val > fitness_threshold:
            log_message.log_debug("藏宝商人匹配率："+str(max_val))
            break
        role_move.move_to([-803, -721])
        role_move.move_to([-803, -716], None, 1)
    if max_val <= fitness_threshold:
        send_message_with_loc("Find Map NPC Error")
        return False
    pyautogui.press(config_model.config['key_commu'])
    #  pyautogui.press('f')
    time.sleep(1)
    max_val, max_loc = match_img(map_in_store)
    log_message.log_debug("藏宝图物品匹配率："+str(max_val))
    if max_val <= fitness_threshold:
        send_message_with_loc("Open Map Store Error")
        return False
    clear_bag()
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.keyDown('shift')
    pyautogui.rightClick()
    pyautogui.keyUp('shift')
    max_val, max_loc = match_img(buy_map_tip)
    # 确定买图数量
    buy_count = int(
        config_model.config['count_yuanbo'] if config_model.config['is_yuanbo'] else config_model.config['count_no_yuanbo'])
    buy_count_string = str(buy_count)
    if max_val > fitness_threshold:
        # pyautogui.press('4')
        # pyautogui.press('0')
        log_message.log_debug("买图数量为："+str(buy_count))
        for i in range(len(buy_count_string)):
            pyautogui.press(buy_count_string[i])
        pyautogui.press('enter')
        # max_val, max_loc = match_img(confirm_btn)
        # if max_val > fitness_threshold:
        #     pyautogui.moveTo(max_loc[0] + 50, max_loc[1] + 15)
        #     pyautogui.leftClick()
    log_message.log_info("买图完毕")
    return True


def open_map():
    role_move.move_to([-802, -703])
    role_move.move_to([-791, -702])
    role_move.move_to([-777, -701])
    role_move.move_to([-756, -703], None, 0, 5)
    max_val, max_loc = match_img(open_map_btn)
    log_message.log_debug("开图按钮匹配率："+str(max_val))
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    down_horse()
    log_message.log_debug("开始开图")
    pyautogui.leftClick()
    pyautogui.sleep(1)
    max_val, max_loc = match_img(open_map_error)
    buy_count = int(
        config_model.config['count_yuanbo'] if config_model.config['is_yuanbo'] else config_model.config['count_no_yuanbo'])
    wait_open_time = buy_count*config_model.config['single_map_time']
    log_message.log_debug("开图数量为："+str(buy_count))
    log_message.log_debug("开图时间为："+str(wait_open_time))
    if max_val < fitness_threshold:
        pyautogui.sleep(wait_open_time)
        pyautogui.moveRel(0, -100)
        up_horse()
        return True
    else:
        close_dialog()
        up_horse()
        send_message_with_loc("Open Map Error")
        return False


def down_horse():
    if not is_on_horse():
        return
    # pyautogui.keyDown('ctrl')
    # pyautogui.press('r')
    # pyautogui.keyUp('ctrl')
    log_message.log_debug("按下马键")
    pyautogui.press(config_model.config['key_horse'])
    pyautogui.press('shift')
    pyautogui.sleep(3)
    if config_model.config['is_testmode']:
        if not is_on_horse():
            log_message.log_debug("成功下马")


def up_horse():
    if is_on_horse():
        return
    # pyautogui.keyDown('ctrl')
    # pyautogui.press('r')
    # pyautogui.keyUp('ctrl')
    log_message.log_debug("按上马键")
    pyautogui.press(config_model.config['key_horse'])
    pyautogui.sleep(3)
    if config_model.config['is_testmode']:
        if is_on_horse():
            log_message.log_debug("成功上马")


def close_dialog():
    max_val, max_loc = match_img(close_btn)
    if max_val > fitness_threshold:
        pyautogui.moveTo(max_loc[0] + 6, max_loc[1] + 6)
        pyautogui.leftClick()


def prepare_to_find():
    log_message.log_info("出发去寻找")
    role_move.move_to([-779, -701])
    role_move.move_to([-793, -703])
    role_move.move_to([-793, -677])
    role_move.move_to([-795, -666])
    role_move.move_to([-795, -640])
    role_move.move_to(begin_find_loc_1, None, 1, 5)
    role_move.turn_to(begin_find_direct_1)
    loc = role_loc.get_current_loc()
    if loc is not None and abs(loc[0] - begin_find_loc_1[0]) < 5 and abs(loc[1] - begin_find_loc_1[1]) < 5:
        return True
    else:
        send_message_with_loc("Go to Find Box Error")
        return False


def find_boxs():
    count = 0
    find_area_1=[55, 47]
    find_area_2 = [55, 27]
    if config_model.config['is_large_region']==1:
        find_area_1 = [65, 47]
        find_area_2 = [55, 28]
    log_message.log_info("开始犁地")
    role_move.move_to(begin_find_loc_1, None, 1, 5)
    role_move.turn_to(begin_find_direct_1)
    count += role_move.move_map(find_area_1[0],
                                find_area_1[1], find_box.find_box_under_footer)
    log_message.log_info("出发犁第二片地")
    role_move.move_to(begin_find_loc_2, None, 1, 5)
    role_move.turn_to(begin_find_direct_2)
    count += role_move.move_map(find_area_2[0],
                                find_area_2[1], find_box.find_box_under_footer,
                                begin_find_loc_2
                                )
    role_move.move_to([-850, -560], None, 3, 3)
    print("开盒次数" + str(count))
    send_message.send_message("开盒次数" + str(count))
    if count <= 0:
        reset_keys()
        send_message_with_loc("Find No Box")
    return True


def back_to_store():
    log_message.log_info("回商店")
    role_move.move_to([-795, -644])
    role_move.move_to([-795, -667])
    role_move.move_to([-795, -702])
    role_move.move_to([-802, -702])
    role_move.move_to([-803, -721])
    role_move.move_to([-803, -716], None, 0, 5)
    loc = role_loc.get_current_loc()
    if loc is not None and abs(-803 - loc[0]) < 5 and abs(-716 - loc[1]) < 5:
        return True
    else:
        send_message_with_loc("Back To Store Error")
        return False


def clear_bag():
    log_message.log_info("出售背包物品")
    max_val, max_loc = match_img(bag_left)
    log_message.log_debug("背包左侧匹配率："+str(max_val))
    if max_val < fitness_threshold:
        log_message.log_debug('无法匹配背包位置')
        return
    first_loc = [max_loc[0] + 100, max_loc[1] + 85]
    pyautogui.keyDown('shift')
    for j in range(0, 3):
        for i in range(0, bag_width):
            pyautogui.moveTo(
                first_loc[0] + i * bag_item_size, first_loc[1] + j * bag_item_size)
            pyautogui.rightClick()
    for i in range(0, 10):
        pyautogui.moveTo(first_loc[0] + i * bag_item_size,
                         first_loc[1] + 3 * bag_item_size + 25)
        pyautogui.rightClick()
    pyautogui.keyUp('shift')
    log_message.log_info("出售完毕")


def reset_to_store():
    log_message.log_info("重置到商店位置")
    log_message.log_debug("获取当前位置")
    current_loc = role_loc.get_current_loc()
    if current_loc is None:
        return False
    # 处理在商店附近情况
    if abs(-803 - current_loc[0]) < 5 and abs(-716 - current_loc[1]) < 5:
        log_message.log_debug("角色在商店附近，移动到商店")
        role_move.move_to([-803, -721])
    down_horse()
    log_message.log_debug("角色不在商店附近，尝试通过仙府重置")
    max_val, max_loc = match_img(home_door_btn)
    if max_val < fitness_threshold:
        log_message.log_debug("找不到仙府图标，上马")
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    pyautogui.leftClick()
    pyautogui.sleep(5)
    log_message.log_debug("对话")
    pyautogui.press(config_model.config['key_commu'])
    #  pyautogui.press('f')
    pyautogui.moveRel(-100, -100)
    time.sleep(1)

    log_message.log_debug("找到仙府图标，回家")
    max_val, max_loc = match_img(home_main_btn)
    if max_val < fitness_threshold:
        log_message.log_debug("找不到'枕剑仙乡·卧云'选项")
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 30, max_loc[1] + 15)
    pyautogui.leftClick()
    pyautogui.sleep(30)

    log_message.log_debug("从仙府返回回川入世符定点位置")
    role_move.move(home_to_door[0], home_to_door[1])
    pyautogui.press(config_model.config['key_commu'])
    #  pyautogui.press('f')
    time.sleep(1)
    max_val, max_loc = match_img(back_origin_btn)
    if max_val < fitness_threshold:
        log_message.log_debug("找不到'回川入世符-返回荒狼原'选项")
        up_horse()
        return False
    pyautogui.moveTo(max_loc[0] + 30, max_loc[1] + 15)
    pyautogui.leftClick()
    pyautogui.sleep(30)

    reset_visual_field()

    loc = role_loc.get_current_loc()
    up_horse()
    if loc is not None and abs(-803 - loc[0]) < 5 and abs(-715 - loc[1]) < 5:
        return True
    return False


def reset_keys():
    log_message.log_info("重置视角")
    pyautogui.keyDown('shift')
    pyautogui.keyUp('shift')
    pyautogui.sleep(2)
    pyautogui.moveTo(find_box.footer_pos[0], find_box.footer_pos[1])
    pyautogui.sleep(2)
    pyautogui.mouseDown(button='left')
    pyautogui.sleep(2)
    pyautogui.mouseUp(button='left')
    pyautogui.sleep(2)
    pyautogui.mouseDown(button='right')
    pyautogui.sleep(2)
    pyautogui.mouseUp(button='right')
    pyautogui.sleep(2)


def try_reset():
    if not deal_new_day():
        return
    count = 0
    while not reset_to_store():
        count += 1
        send_message_with_loc("Try reset count " + str(count))
        role_move.move(-10, -10)
        time.sleep(600)
        if not deal_new_day():
            return


def deal_new_day():
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        # 关服了
        return False
    max_val, max_loc = match_img(new_day_tip)
    if max_val > fitness_threshold:
        close_dialog()
    return True


def is_on_horse():
    max_val, max_loc = match_img(horse, 5)
    log_message.log_debug("上马匹配率："+str(max_val))
    return max_val > fitness_threshold


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


def send_message_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    send_message.send_message(message + " " + str(loc) + " " + str(direct))


def print_log_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    log_message.log_error(message + " " + str(loc) + " " + str(direct))
