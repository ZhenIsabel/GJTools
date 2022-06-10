import send_message
import utils
import cv2
import pyautogui
import config
import datetime

new_day_tip = cv2.imread('img/new_day_tip.png')
close_btn = cv2.imread('img/close_btn.png')
play_card_btn=cv2.imread('img/play_card_btn.png')
mode_sel_btn=cv2.imread('img/mode_sel_btn.png')
easy_mode=cv2.imread('img/easy_mode.png')
prepare_btn=cv2.imread('img/prepare_btn.png')
exit_btn=cv2.imread('img/exit_btn.png')
confirm_exit=cv2.imread('img/confirm_exit.png')
continue_btn=cv2.imread('img/continue_btn.png')
in_turn = cv2.imread('img/in_turn.png')
color_pic=[cv2.imread('img/red.jpg'),
cv2.imread('img/green.jpg'),
cv2.imread('img/blue.jpg'),
cv2.imread('img/yellow.jpg')
]


def is_my_turn():
    return utils.match_img(in_turn) > 0.95


def play_card():
    # 等待到出牌环节
    for i in range(0, 20):
        if is_my_turn():
            break
        pyautogui.sleep(1)

    # 出牌
    for i in range(0, 3):
        if utils.find_and_click(color_pic[i], [5, 5], config.config['my_card_region']):
            pyautogui.sleep(0.5)
            if utils.find_and_click(color_pic[i], [5, 5], config.config['card_pool_region']):
                break

def start_game():
    pyautogui.moveTo(config.config['longxing_pos'])
    pyautogui.click()
    pyautogui.sleep(0.5)
    if not utils.find_and_click(play_card_btn,[5,5]):
        return False
    if not utils.find_and_click(mode_sel_btn,[5,5]):
        return False
    if not utils.find_and_click(easy_mode,[5,5]):
        return False
    pyautogui.sleep(0.5)
    if not utils.find_and_click(prepare_btn,[5,5]):
        return False
    pyautogui.sleep(5)
    return True

def next_game():
    if not utils.find_and_click(continue_btn,[5,5]):
        return False
    pyautogui.sleep(0.5)
    if not utils.find_and_click(prepare_btn,[5,5]):
        return False
    pyautogui.sleep(5)
    return True

def close_game():
    if not utils.find_and_click(exit_btn,[5,5]):
        return True
    pyautogui.sleep(0.5)
    if not utils.find_and_click(confirm_exit,[5,5]):
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
    while not restart_game() and count<10:
        count += 1
        # 检查是否掉线
        if utils.deal_offline():
            send_message.send_message("restart game " + str(count))
            restart_game()
        send_message.send_message("Try reset count " + str(count))
        pyautogui.sleep(150)
        if not deal_new_day():
            return


def deal_new_day():
    current_time = datetime.datetime.now()
    if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
        # 关服了
        return False
    max_val, _ = utils.match_img(new_day_tip)
    if max_val > 0.95:
        # close_dialog
        utils.find_and_click(close_btn,[6,6])
    return True
