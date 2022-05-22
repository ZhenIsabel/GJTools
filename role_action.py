import datetime
import time

import cv2
import numpy as np
import pyautogui
import win32api
import win32con
# import pyperclip

import config_model
import find_box
import log_message
import role_loc
import role_move
import send_message
import get_weather
import utils
# import fucking_flower

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
open_complete_night = cv2.imread('img/open_complete_night.png')
open_complete_day = cv2.imread('img/open_complete_day.png')
reading_tag = cv2.imread('img/reading.png')
flower_debuff = cv2.imread('img/flower_debuff.png')
cost_220 = cv2.imread('img/cost_220.png')
cost_20 = cv2.imread('img/cost_20.png')
cost_800 = cv2.imread('img/cost_800.png')

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
wait_open_time_step = 4.9

# 第一个挖宝区域大小
# begin_find_loc_1 = [-825, -530]
# begin_find_loc_1 = [-825, -526]
begin_find_loc_1 = [-825, -540]
begin_find_direct_1 = 0.6

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


def match_region(template, region, method=3):
    image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(image, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)
    # test.show_match_image(match_res,template,image)
    return max_val, max_loc

# def clear_map(count=20):


def clear_map(buy_count):
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
    # buy_count = int(
    #     config_model.config['count_yuanbo'] if config_model.config['is_yuanbo'] else config_model.config['count_no_yuanbo'])
    # log_message.log_debug("清理数量为："+str(buy_count))
    count = role_loc.get_clear_map_count()
    if buy_count < count:
        count = buy_count
    if count < 20:
        count = 45
    for i in range(0, count):
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
    return count


def buy_map():
    log_message.log_info("买图")
    max_val = 0

    for i in range(0, 10):
        time.sleep(0.2)
        # 鼠标挪到角落以防误触
        pyautogui.moveTo(first_map_pos[0], first_map_pos[1])
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
    if config_model.config['is_extra_buy']:
        buy_count = buy_count-1
    buy_count_string = str(buy_count)
    if max_val > fitness_threshold:
        # pyautogui.press('4')
        # pyautogui.press('0')
        # 增加延迟
        # improve_direction.check_ping(try_times=20)
        log_message.log_debug("买图数量为："+str(buy_count))
        for i in range(len(buy_count_string)):
            pyautogui.press(buy_count_string[i])
        # improve_direction.check_ping(try_times=20)
        pyautogui.press('enter')
        if config_model.config['is_extra_buy']:
            pyautogui.click(x=None, y=None, clicks=50-buy_count, interval=0.001,
                            button='right', duration=0.0, tween=pyautogui.linear)
        # max_val, max_loc = match_img(confirm_btn)
        # if max_val > fitness_threshold:
        #     pyautogui.moveTo(max_loc[0] + 50, max_loc[1] + 15)
        #     pyautogui.leftClick()
    log_message.log_info("买图完毕")
    return True


def remove_buff():
    buff_region = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=[858, 1005, 230, 55])), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(buff_region, flower_debuff, 3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(
        match_res)
    # print(max_loc)
    if max_val > 0.92:
        pyautogui.moveTo(858+max_loc[0] + 13, 1005+max_loc[1] + 13)
        pyautogui.rightClick()
        # # 打字嘲讽饼哥
        # pyautogui.moveTo(417, 1220)
        # pyautogui.leftClick()
        # pyperclip.copy(fucking_flower.fucking_coockie_bro())
        # time.sleep(0.5)
        # pyautogui.keyDown('ctrl')
        # pyautogui.press('v')
        # pyautogui.keyUp('ctrl')
        # pyautogui.press('enter')


def check_open_complete():
    # 判断是否开图执行完毕
    image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=[923, 369, 75, 22])), cv2.COLOR_RGB2BGR)
    match_res = cv2.matchTemplate(
        open_complete_day, image, 5)
    _, max_complete_val, _, _ = cv2.minMaxLoc(
        match_res)
    if max_complete_val < 0.7:
        match_res = cv2.matchTemplate(
            open_complete_night, image, 5)
        _, max_complete_val, _, _ = cv2.minMaxLoc(
            match_res)
    print("complete check:"+str(max_complete_val))
    log_message.log_error("complete check:"+str(max_complete_val))
    return max_complete_val > 0.7


def avoid_open_interrupt():
    # 开图读条左上角位置及长宽
    read_area = [1104, 999, 368, 50]
    image_origin = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=read_area)), cv2.COLOR_RGB2BGR)
    # 原开图操作
    role_move.move_to([-802, -703])
    role_move.move_to([-791, -702])
    role_move.move_to([-777, -701])
    role_move.move_to_nearby([-756, -703], None, 0, 5)
    max_val, max_loc = match_img(open_map_btn)
    log_message.log_debug("开图按钮匹配率："+str(max_val))
    pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
    down_horse()
    log_message.log_debug("开始开图")
    pyautogui.leftClick()
    pyautogui.sleep(1)
    max_val, _ = match_img(open_map_error)
    buy_count = int(
        config_model.config['count_yuanbo'] if config_model.config['is_yuanbo'] else config_model.config['count_no_yuanbo'])
    # wait_open_time = buy_count*config_model.config['single_map_time']
    extra_buy_count = 0
    image_read = cv2.cvtColor(np.asarray(
        pyautogui.screenshot(region=[327, 1032, 402, 203])), cv2.COLOR_RGB2BGR)
    match_res_20 = cv2.matchTemplate(cost_20, image_read, 3)
    _, max_val_count_check, _, _ = cv2.minMaxLoc(
        match_res_20)
    if max_val_count_check < 0.98:
        matxh_res_800 = cv2.matchTemplate(cost_800, image_read, 3)
        _, max_val_count_check, _, _ = cv2.minMaxLoc(
            matxh_res_800)
    if max_val_count_check < 0.98 and config_model.config['is_extra_buy']:
        extra_buy_count = 10

    # log_message.log_debug("开图时间为："+str(wait_open_time))
    if max_val < fitness_threshold:
        # 每5秒一测
        reset_times = 0
        i = 0
        pre_rest = 1
        while i < buy_count+extra_buy_count:
            time.sleep(config_model.config['single_map_time']-pre_rest)
            i = i+1
            pre_rest = 0
            # 移除不对劲的buff
            remove_buff()
            # 匹配开图读条区域
            image_read = cv2.cvtColor(np.asarray(
                pyautogui.screenshot(region=read_area)), cv2.COLOR_RGB2BGR)
            match_res = cv2.matchTemplate(image_origin, image_read, 3)
            _, max_val, _, _ = cv2.minMaxLoc(match_res)

            # print("interrupt check:"+str(max_val))
            if max_val > 0.9:
                # log_message.log_error("interrupt check:"+str(max_val))
                # 读条完成检测
                # double check
                image_read = cv2.cvtColor(np.asarray(
                    pyautogui.screenshot(region=read_area)), cv2.COLOR_RGB2BGR)
                match_res = cv2.matchTemplate(image_read, reading_tag, 3)
                _, max_val, _, _ = cv2.minMaxLoc(match_res)
                # print("reading check:"+str(max_val))
                if max_val < 0.85:
                    pyautogui.moveRel(0, -100)
                    up_horse()
                    print(("开图数量为："+str(i)))
                    return i
                # # 打断重置
                # pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
                # time.sleep(0.1)
                # pyautogui.leftClick()
                # i = 0
                # print("open map reset:"+str(max_val))
                # log_message.log_error("open map reset"+str(max_val))
                # reset_times = reset_times+1

        # pyautogui.sleep(wait_open_time)
        # time.sleep(2)
        # pyautogui.moveTo(max_loc[0] + 24, max_loc[1] + 24)
        # time.sleep(0.1)
        # pyautogui.leftClick()
        # if not check_open_complete():
        #     send_message_with_loc("Open Map Error: cannot complete")
        #     # return False
        time.sleep(1)
        pyautogui.moveRel(0, -100)
        up_horse()
        return extra_buy_count+buy_count
    else:
        close_dialog()
        up_horse()
        send_message_with_loc("Open Map Error")
        return -1


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
        # 防打断
        # 移除不对劲的debuff
        for i in range(int(0, wait_open_time, wait_open_time_step)+1):
            remove_buff()
            pyautogui.sleep(wait_open_time_step)
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

    # 第二个挖宝区域大小
    # begin_find_loc_2 = [-980, -528]
    begin_find_loc_2 = [-975, -525]
    begin_find_direct_2 = -0.5

    find_area_1 = [55, 47]
    find_area_2 = [55, 27]
    if config_model.config['is_large_region'] == 1:
        # find_area_1 = [65, 47]
        # find_area_2 = [56, 31]
        # find_area_1 = [63, 46]
        # find_area_2 = [60, 31]
        find_area_1 = [65, 42]
        find_area_2 = [61, 34]

    log_message.log_info("开始犁地")
    role_move.move_to(begin_find_loc_1, None, 1, 5)
    role_move.turn_to(begin_find_direct_1)
    start_time = time.time()
    count += role_move.move_map(find_area_1[0],
                                find_area_1[1], find_box.find_box_under_footer)
    region_1_time = time.time()-start_time
    if count <= 0:
        reset_keys()
    log_message.log_info("出发犁第二片地")
    role_move.move_to(begin_find_loc_2, None, 1, 5)
    role_move.turn_to(begin_find_direct_2)
    start_time = time.time()
    count += role_move.move_map(find_area_2[0],
                                find_area_2[1], find_box.find_box_under_footer,
                                begin_find_loc_2
                                )
    region_2_time = time.time()-start_time
    role_move.move_to([-850, -560], None, 3, 3)
    print("开盒次数" + str(count))
    # send_message.send_message("开盒次数" + str(count))
    if count <= 0:
        reset_keys()
        send_message_with_loc("Find No Box")
    return count, region_1_time, region_2_time


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
    # first_loc = [max_loc[0] + 100, max_loc[1] + 85]
    first_loc = [max_loc[0] + 100, max_loc[1] - 30]
    pyautogui.keyDown('shift')
    for j in range(0, 3):
        for i in range(0, bag_width):
            pyautogui.moveTo(
                first_loc[0] + i * bag_item_size, first_loc[1] + j * bag_item_size)
            pyautogui.rightClick()
    # for i in range(0, 10):
    #     pyautogui.moveTo(first_loc[0] + i * bag_item_size,
    #                      first_loc[1] + 3 * bag_item_size + 25)
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
    # pyautogui.press('g')
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
    pyautogui.sleep(36)

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
    pyautogui.sleep(40)

    reset_visual_field()
    time.sleep(0.5)
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
        # 检查是否掉线
        if not utils.deal_offline():
            send_message_with_loc("restart game " + str(count))
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
    # print("上马匹配率："+str(max_val))
    return max_val > 0.9


def reset_visual_field():
    x, y = 1000, 300
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 300)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -200)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def send_message_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    move_record = '\n move record:\n'
    for i in range(0, len(role_move.move_log)):
        record_i = 'loc:'+str(role_move.move_log[i][0])+','+str(
            role_move.move_log[i][1])+' direct:'+str(role_move.move_log[i][2])+' move:'+str(role_move.move_log[i][3])+','+str(role_move.move_log[i][4])
        move_record = move_record+record_i+'\n'
    send_message.send_message(
        message + " " + str(loc) + " " + str(direct)+move_record)


def print_log_with_loc(message):
    loc = role_loc.get_current_loc()
    direct = role_loc.get_current_direction()
    log_message.log_error(message + " " + str(loc) + " " + str(direct))
