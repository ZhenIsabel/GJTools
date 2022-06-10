import utils
import time
import card_play

utils.window_focus('古剑奇谭网络版')
time.sleep(0.5)

card_play.start_game()

for i in range(0,1000):
    if not card_play.play_card():
        card_play.try_reset()
        continue
    if not card_play.next_game():
        card_play.try_reset()
        continue