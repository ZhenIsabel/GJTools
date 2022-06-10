import send_message
import utils
import cv2
import pyautogui
import config
import datetime
import win32api
import win32con

new_day_tip = cv2.imread('img/new_day_tip.png')
close_btn = cv2.imread('img/close_btn.png')
play_card_btn = cv2.imread('img/play_card_btn.png')
mode_sel_btn = cv2.imread('img/mode_sel_btn.png')
easy_mode = cv2.imread('img/easy_mode.png')
prepare_btn = cv2.imread('img/prepare_btn.png')
exit_btn = cv2.imread('img/exit_btn.png')
confirm_exit = cv2.imread('img/confirm_exit.png')
continue_btn = cv2.imread('img/continue_btn.png')
leave_game_btn=cv2.imread('img/leave_game_btn.png')
not_turn = cv2.imread('img/not_turn.png')
color_pic = [cv2.imread('img/red.png'),
             cv2.imread('img/green.png'),
             cv2.imread('img/blue.png'),
             cv2.imread('img/yellow.png')
             ]


def is_my_turn():
    max_val, _ = utils.match_img(not_turn,method=5)
    # print (max_val)
    return max_val < 0.95


def play_card():
    for i in range(0,100):
        # 等待到出牌环节
        for i in range(0, 20):
            if is_my_turn():
                break
            pyautogui.sleep(1)

        # 出牌
        for i in range(0, 4):
            if utils.find_and_click_region(color_pic[i], offset=[5, 5], region=config.config['my_card_region']):
                pyautogui.sleep(0.5)
                if utils.find_and_click_region(color_pic[i], offset=[5, 5], region=config.config['card_pool_region']):
                    pyautogui.sleep(0.5)
                    break
        max_val,_=utils.match_img(continue_btn)
        if max_val>0.95:
            return True
    return False


def start_game():
    pyautogui.moveTo(config.config['longxing_pos'])
    pyautogui.sleep(0.5)
    # pyautogui.leftClick()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 
    config.config['longxing_pos'][0], config.config['longxing_pos'][1])
    pyautogui.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    pyautogui.sleep(0.5)
    if not utils.find_and_click(play_card_btn, [5, 5]):
        return False
    if not utils.find_and_click(mode_sel_btn, [5, 5]):
        return False
    if not utils.find_and_click(easy_mode, [5, 5]):
        return False
    pyautogui.sleep(0.5)
    if not utils.find_and_click(prepare_btn, [5, 5]):
        return False
    pyautogui.sleep(5)
    return True


def next_game():
    if not utils.find_and_click(continue_btn, [5, 5]):
        return False
    pyautogui.sleep(0.5)
    if not utils.find_and_click(prepare_btn, [5, 5]):
        return False
    pyautogui.sleep(5)
    return True


def close_game():
    if not utils.find_and_click(exit_btn, [5, 5]):
        return True
    pyautogui.sleep(0.5)
    if not utils.find_and_click(confirm_exit, [5, 5]):
        return False
    return True


def restart_game():
    if not close_game():
        return False
    if not start_game():
        return False
    return True


def try_reset():
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
    
    if count>=10:
        # 关游戏保点卡
        utils.close_window('古剑奇谭网络版')


def deal_new_day():
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        # 关服了
        return False
    max_val, _ = utils.match_img(new_day_tip)
    if max_val > 0.95:
        # close_dialog
        utils.find_and_click(close_btn, [6, 6])
        utils.find_and_click(leave_game_btn,[15,15])
    return True
