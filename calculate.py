import datetime
import time

import role_action
import send_message
import config_model
import get_weather

# import config_model


def calc222():
    time.sleep(1)

    for i in range(0, 100):
        start_time = time.time()
        if not role_action.buy_map():
            role_action.try_reset()
            continue
        buy_time = time.time()
        # if not role_action.open_map():
        open_count = -1
        if not open_count >= 0:
            role_action.try_reset()
            continue
        open_time = time.time()
        if not role_action.prepare_to_find():
            role_action.try_reset()
            continue
        on_way_time = time.time()
        find_count = role_action.find_boxs()
        if not find_count >= 0:
            role_action.try_reset()
            continue
        find_time = time.time()
        clear_count = role_action.clear_map()
        if not clear_count >= 0:
            role_action.try_reset()
            continue
        clear_time = time.time()
        if not role_action.back_to_store():
            role_action.try_reset()
            continue
        back_time = time.time()
        print(datetime.datetime.strftime(datetime.datetime.now(),
              '%Y-%m-%d %H:%M:%S') + " 第" + str(i + 1) + "次")
        report_data = {
            '开盒': 1,
            '总图数': 2,
            '天气': get_weather.get_weather_name(),
            '买图耗时': 3,
            '开图耗时': 4,
            '寻路耗时': 5,
            '找盒耗时': 6,
            '清图耗时': 7
        }

        send_message.send_procedure_report(report_data, i+1)


def calc():
    time.sleep(2)
    role_action.reset_visual_field()
    for i in range(0, 100):
        current_time = datetime.datetime.now()
        if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
            break
        elif current_time.hour == 5 and current_time.minute > 45:
            if current_time.isoweekday() == 4:  # 周四退出
                break
            time.sleep(16 * 60)  # 等到六点
            role_action.close_dialog()
        start_time = time.time()
        # if not role_action.buy_map():
        #     role_action.try_reset()
        #     continue
        buy_time = time.time()
        # # if not role_action.open_map():
        open_count =0
        # open_count = role_action.avoid_open_interrupt()
        # if not open_count >= 0:
        #     role_action.try_reset()
        #     continue
        open_time = time.time()
        # if not role_action.prepare_to_find():
        #     role_action.try_reset()
        #     continue
        on_way_time = time.time()
        find_count = role_action.find_boxs()
        if not find_count >= 0:
            role_action.try_reset()
            continue
        find_time = time.time()
        clear_count = role_action.clear_map(open_count)
        if not clear_count >= 0:
            role_action.try_reset()
            continue
        clear_time = time.time()
        if not role_action.back_to_store():
            role_action.try_reset()
            continue
        back_time = time.time()
        print(datetime.datetime.strftime(datetime.datetime.now(),
              '%Y-%m-%d %H:%M:%S') + " 第" + str(i + 1) + "次")
        report_data = {
            '开盒': find_count,
            '总图数': open_count,
            '清理数': clear_count,
            '天气': get_weather.get_weather_name(),
            '买图耗时': buy_time-start_time,
            '开图耗时': open_time-buy_time,
            '寻路去程耗时': on_way_time-open_time,
            '寻路返程耗时': back_time-clear_time,
            '找盒耗时': find_time-on_way_time,
            '清图耗时': clear_time-find_time,
            '总耗时': back_time-start_time
        }

        send_message.send_procedure_report(report_data, i+1)
