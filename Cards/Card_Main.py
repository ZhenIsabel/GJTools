import datetime
import time
from operator import mod

from Cards import card_play, config, send_message, utils

utils.window_focus('古剑奇谭网络版')
time.sleep(0.5)




def card_main(runtime=60):
    config.init_config()
    card_play.close_game()
    card_play.start_game()
    start_time=time.time()
    for i in range(0, 5000):
        try:
            this_time=time.time()
            if this_time-start_time>runtime*60*60:
                break
            current_time = datetime.datetime.now()
            if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
                break
            elif current_time.hour == 5 and current_time.minute > 57:
                if current_time.isoweekday() == 4:  # 周四退出
                    break
                time.sleep(4 * 60)  # 等到六点
                card_play.close_dialog()
            if not card_play.play_card():
                card_play.try_reset()
                continue
            if not card_play.next_game():
                card_play.try_reset()
                continue
            if mod(i, 10) == 0:
                send_message.send_message('card success: '+str(i)+' times')
                print('card success: '+str(i)+' times')
        except Exception as e:
            send_message.send_message(str(e))
            return False
