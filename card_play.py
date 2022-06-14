from operator import mod
import send_message
import utils
import cv2
import pyautogui
import config
import datetime
import win32api
import win32con
import time
import numpy as np
import log_message

new_day_tip = cv2.imread('img/new_day_tip.png')
close_btn = cv2.imread('img/close_btn.png')
play_card_btn = cv2.imread('img/play_card_btn.png')
mode_sel_btn = cv2.imread('img/mode_sel_btn.png')
easy_mode = cv2.imread('img/easy_mode.png')
prepare_btn = cv2.imread('img/prepare_btn.png')
exit_btn = cv2.imread('img/exit_btn.png')
confirm_exit = cv2.imread('img/confirm_exit.png')
continue_btn = cv2.imread('img/continue_btn.png')
leave_game_btn = cv2.imread('img/leave_game_btn.png')
not_turn = cv2.imread('img/not_turn.png')
opponent_count_tag=cv2.imread('img/opponent_count.png')
color_pic = [cv2.imread('img/red.png'),
             cv2.imread('img/green.png'),
             cv2.imread('img/blue.png'),
             cv2.imread('img/yellow.png')
             ]
color = ['red', 'green', 'blue', 'yellow']


def is_my_turn():
    max_val, _ = utils.match_img(not_turn)
    return max_val < 0.95


def play_card():
    start_time = time.time()
    for i in range(0, 100):
        time_spent = time.time()-start_time
        if time_spent > 80:
            # 截图保存
            print('break a game')
            utils.save_screen()
            record = 'break a game'+log_message.print_record()
            send_message.send_message(record)
            log_message.log_warning(record)
            break
        # 等待到出牌环节
        for i in range(0, 20):
            if is_my_turn():
                break
            pyautogui.sleep(1)
            if mod(i, 3) == 0 and i > 0:
                log_message.record(['wait', i+1])

        # 出牌
        success_find = pic_match_show_card(try_times=2)

        # 如果出牌失败，按颜色出牌
        # 效率比较低，不采用
        # if not success_find:
        #   success_find = col_match_show_card()

        # 如果出牌失败，顺序出牌纠错
        if not success_find:
            order_show_card()
        max_val, _ = utils.match_img(continue_btn)
        if max_val > 0.95:
            log_message.record(['info', 'finish'])
            return True
    return False

# 图像匹配出牌


def pic_match_show_card(try_times=2):
    if try_times <= 0:
        return False
    for i in range(0, 4):
        if utils.find_and_click_region(color_pic[i], offset=[5, 5], region=config.config['my_card_region']):
            pyautogui.sleep(0.2)
            origin_score = cv2.cvtColor(np.asarray(pyautogui.screenshot(
                region=config.config['score_region'])), cv2.COLOR_RGB2BGR)
            if utils.find_and_click_region(color_pic[i], offset=[5, 5], region=config.config['card_pool_region']):
                pyautogui.sleep(0.2)
                score_change_val, _ = utils.match_img_region(
                    origin_score, config.config['score_region'])
                if score_change_val < 0.95 or not is_my_turn():
                    # 记录操作
                    log_message.record(['find', color[i]])
                    return True
            else:
                pyautogui.leftClick()  # 取消选择卡片
                log_message.record(['unselect', color[i]])
    return pic_match_show_card(try_times-1)

# 颜色识别出牌


def col_match_show_card(try_times=2):
    if try_times <= 0:
        return False
    for i in range(0, 4):
        if utils.find_and_click_region(color_pic[i], offset=[5, 5], region=config.config['my_card_region']):
            log_message.record(['color', color[i]])
            find_region = cv2.cvtColor(np.asarray(pyautogui.screenshot(
                region=config.config['card_pool_region'])), cv2.COLOR_RGB2BGR)
            color_centers = utils.find_color_center(color[i], find_region)
            for index, center in enumerate(color_centers):
                not_change = utils.is_same_before_after(config.config['score_region'],
                                                        move_click,
                                                        config.config['card_pool_region'][0] +
                                                        center[0],
                                                        config.config['card_pool_region'][1] +
                                                        center[1]
                                                        )

                if not not_change or not is_my_turn():
                    # 记录操作
                    log_message.record(['find by color', color[i]])
                    return True
            utils.find_and_click_region(
                color_pic[i], offset=[5, 5], region=config.config['my_card_region'])  # 取消选择卡片
            log_message.record(['unselect', color[i]])
    return col_match_show_card(try_times-1)


# 顺序出牌
def order_show_card(try_times=1):
    if try_times <= 0:
        return False
    for i in range(0, 4):
        if utils.find_and_click_region(color_pic[i], offset=[5, 5], region=config.config['my_card_region']):
            log_message.record(['order', color[i]])
            for j in range(0, 10):
                not_change = utils.is_same_before_after(config.config['score_region'],
                                                        move_click,
                                                        config.config['first_card_loc_in_pool'][0] +
                                                        j*config.config['card_space_in_pool'],
                                                        config.config['first_card_loc_in_pool'][1],
                                                        0.2
                                                        )
                if not not_change:
                    log_message.record(['order', 'pair '+str(j)])
                    return True
    return order_show_card(try_times-1)


def move_click(x, y, sleep=0):
    pyautogui.moveTo(x, y)
    pyautogui.leftClick()
    pyautogui.sleep(sleep)


def start_game(try_times=3,refresh_times=0):
    if try_times <= 0:
        return False
    pyautogui.moveTo(config.config['longxing_pos'])
    pyautogui.sleep(0.5)
    # pyautogui.leftClick()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,
                         config.config['longxing_pos'][0], config.config['longxing_pos'][1])
    pyautogui.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    pyautogui.sleep(0.5)
    if not utils.find_and_click(play_card_btn, [5, 5]):
        return start_game(try_times-1)
    if not utils.find_and_click(mode_sel_btn, [5, 5]):
        return start_game(try_times-1)
    if not utils.find_and_click(easy_mode, [5, 5]):
        return start_game(try_times-1)
    pyautogui.sleep(0.5)
    # 刷对手珍稀卡
    pair_val,_=utils.match_img_region(opponent_count_tag,config.config['opponent_count_region'])
    if pair_val<0.95:
        if refresh_times<20:
            refresh_times=refresh_times+1
            return restart_game(try_times-1,refresh_times)
    if not utils.find_and_click(prepare_btn, [5, 5]):
        return start_game(try_times-1)
    pyautogui.sleep(5)
    return True


def next_game(try_times=3):
    if try_times <= 0:
        return False
    if not utils.find_and_click(continue_btn, [5, 5]):
        return next_game(try_times-1)
    pyautogui.sleep(0.5)
    if not utils.find_and_click(prepare_btn, [5, 5]):
        return next_game(try_times-1)
    pyautogui.sleep(5)
    return True


def close_game(try_times=3):
    if try_times <= 0:
        return False
    pyautogui.moveTo(config.config['longxing_pos'][0],config.config['longxing_pos'][1])
    if not utils.find_and_click(exit_btn, [5, 5]):
        return True
    pyautogui.sleep(0.5)
    if not utils.find_and_click(confirm_exit, [5, 5]):
        return close_game(try_times-1)
    return True


def restart_game(try_times=3):
    if try_times <= 0:
        return False
    if not close_game(try_times):
        return restart_game(try_times-1)
    if not start_game(try_times):
        return restart_game(try_times-1)
    return True


def try_reset():
    utils.save_screen()
    if not deal_new_day():
        return
    count = 0
    while not restart_game() and count < 10:
        count += 1
        # 检查是否掉线
        if utils.deal_offline():
            send_message.send_message("restart game " + str(count))
            restart_game()
        send_message.send_message("Try reset count " + str(count))
        pyautogui.sleep(150)
        if not deal_new_day():
            return

    if count >= 10:
        # 关游戏保点卡
        utils.close_window('古剑奇谭网络版')
        utils.find_and_click(leave_game_btn)
        send_message('exit game')


def deal_new_day():
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        # 关服了
        return False
    max_val, _ = utils.match_img(new_day_tip)
    if max_val > 0.95:
        close_dialog()
    return True


def close_dialog():
    utils.find_and_click(close_btn, [6, 6])
