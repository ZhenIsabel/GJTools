import time

import pyautogui

import cfg
from common import role_loc
from gold_symbol import role_action_gold, dig_changheshan
from message import send_message

time.sleep(3)
# dig_changheshan.try_dig_map()
send_message.send_message('test image', [pyautogui.screenshot(cfg.screenshot_region)])
