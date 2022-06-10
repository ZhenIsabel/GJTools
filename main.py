from operator import mod
import utils
import time
import card_play
import send_message

import datetime

utils.window_focus('古剑奇谭网络版')
time.sleep(0.5)

card_play.close_game()
card_play.start_game()

for i in range(0,2000):
    try:
        current_time = datetime.datetime.now()
        if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
            break
        elif current_time.hour == 5 and current_time.minute > 45:
            if current_time.isoweekday() == 4:  # 周四退出
                break
            time.sleep(16 * 60)  # 等到六点
            card_play.close_dialog()
        if not card_play.play_card():
            card_play.try_reset()
            continue
        if not card_play.next_game():
            card_play.try_reset()
            continue
        if mod(i,10)==0:
            send_message.send_message('card success: '+str(i)+' times')
            print('card success: '+str(i)+' times')
    except Exception as e:
        send_message.send_procedure_report(str(e), i+1)