import math
import time
import pyautogui
import numpy

import cfg
from common import role_loc
from green_map import role_action


def move(x, y):
    if x > 0:
        pyautogui.keyDown('d')
        wait_include_pause(x * cfg.move_speed)
        pyautogui.keyUp('d')
    elif x < 0:
        pyautogui.keyDown('a')
        wait_include_pause(- x * cfg.move_speed)
        pyautogui.keyUp('a')
    if y > 0:
        pyautogui.keyDown('w')
        wait_include_pause(y * cfg.move_speed)
        pyautogui.keyUp('w')
    elif y < 0:
        pyautogui.keyDown('s')
        wait_include_pause(- y * cfg.move_back_speed)
        pyautogui.keyUp('s')


def turn_around(num):
    while num > 1:
        num = num - 2
    while num < -1:
        num = num + 2
    if abs(num) <= cfg.turn_min:
        return
    if num > 0:
        pyautogui.keyDown(']')
        wait_include_pause(num * cfg.turn_speed)
        pyautogui.keyUp(']')
    elif num < 0:
        pyautogui.keyDown('[')
        wait_include_pause(- num * cfg.turn_speed)
        pyautogui.keyUp('[')


def turn_to(direct, try_times=5):
    if try_times <= 0:
        role_action.print_log_with_loc("Turn Failed to " + str(direct))
        return
    c_direct = role_loc.get_current_direction()
    if c_direct is None:
        turn_to(direct, try_times - 1)
        return
    turn_around(direct - c_direct)
    c_direct = role_loc.get_current_direction()
    if c_direct is not None and 1.9 > (abs(c_direct - direct) % 2) > 0.1:
        turn_to(direct, try_times - 1)


def move_map_correct(origin_coordinate, direct, width, height, callback_fun, try_times=2):
    current_loc = role_loc.get_current_loc(2)
    if not current_loc == None:
        offset = [origin_coordinate[0]-current_loc[0],
                  0
                  ]  # 如果当前行走完后应回到x归零位置
        if direct > 0:  # 如果当前行走完后应回到x终点位置
            offset[0] += width
        if 3 > offset[0] > -3 and 3 > offset[1] > -3:
            return None
        elif abs(offset[0]) > 200:
            return None
        else:
            move(0, offset[1])
            x = 0
            while x < abs(offset[0]):
                move(numpy.sign(offset[0]) *
                     cfg.move_distance_x, 0)
                x += cfg.move_distance_x
                callback_fun()
    if try_times > 0:
        return move_map_correct(origin_coordinate, direct, width, height, callback_fun, try_times-1)


def move_map(width, height, callback_fun=None, origin=None):
    x, y = 0, 0
    direct = 1
    count = 0
    while y < height:
        while x < width:
            move(direct * cfg.move_distance_x, 0)
            x += cfg.move_distance_x
            count += callback_fun()
        if not origin == None and y > height/2:
            move_map_correct([origin[0], origin[1]+y],
                             direct, width, height, callback_fun)
        role_action.up_horse()
        move(0, cfg.move_distance_y)
        y += cfg.move_distance_y
        count += callback_fun()
        x = 0
        direct = - direct
    return count


def move_to_nearby(target_loc, target_direct=None, diff=cfg.move_min, try_time=2):
    res = False
    for i in range(0, try_time):
        if move_directly(target_loc, diff):
            res = True
            break
        this_loc = role_loc.get_current_loc()
        if this_loc is None:
            return False
        loc_bias = numpy.power(
            target_loc[0]-this_loc[0], 2)+numpy.power(target_loc[1]-this_loc[1], 2)
        if loc_bias < 2:
            res = True
            break
    if not res:
        move_bad_case(target_loc)
        if not move_directly(target_loc, diff):
            role_action.print_log_with_loc(
                "Move Failed to " + str(target_loc) + " with try times " + str(try_time))

    current_direct = role_loc.get_current_direction()
    if target_direct is not None and current_direct is not None:
        turn_around(target_direct - current_direct)


def move_to(target_loc, target_direct=None, diff=cfg.move_min, try_time=2):
    res = False
    for i in range(0, try_time):
        if move_directly(target_loc, diff):
            res = True
            break
    if not res:
        move_bad_case(target_loc)
        if not move_directly(target_loc, diff):
            role_action.print_log_with_loc("Move Failed to " + str(target_loc) + " with try times " + str(try_time))

    current_direct = role_loc.get_current_direction()
    if target_direct is not None and current_direct is not None:
        turn_around(target_direct - current_direct)


def move_directly(target_loc, diff=cfg.move_min, try_times=5):
    if try_times <= 0:
        return False
    current_loc = role_loc.get_current_loc()
    if current_loc is None:
        return False
    if abs(current_loc[0] - target_loc[0]) <= diff and abs(current_loc[1] - target_loc[1]) <= diff:
        return True
    diff_loc = [target_loc[0] - current_loc[0], target_loc[1] - current_loc[1]]
    temp_direct = -math.atan2(diff_loc[1], diff_loc[0]) / math.pi
    turn_to(temp_direct)
    move(0, min(math.hypot(diff_loc[0], diff_loc[1]), cfg.max_move_distance))
    return move_directly(target_loc, diff, try_times - 1)


def wait_include_pause(wait_time):
    time.sleep(max(wait_time - pyautogui.PAUSE, 0.005))


def move_bad_case(target_loc):
    current_loc = role_loc.get_current_loc()
    if current_loc is not None and -682 >= current_loc[1] >= -683 and -799 >= current_loc[0] >= -806:
        move(current_loc[0] - 794, 0)
    elif current_loc is not None and -633 >= current_loc[1] >= -633 and -799 >= current_loc[0] >= -806:
        move(current_loc[0] - 794, 0)
    elif current_loc is not None and -689 >= current_loc[1] >= -690 and -789 >= current_loc[0] >= -789:
        move(0, -2)
        move(2, 0)
    else:
        if current_loc is not None and target_loc[0] - current_loc[0] < 0:
            move_x = -2
        else:
            move_x = 2
        move(0, -1)
        move(move_x, 0)
