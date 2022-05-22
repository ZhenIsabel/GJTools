import datetime
import time

import role_action
import send_message
# import config_model
import get_weather
import utils

# import config_model


def calc111():
    time.sleep(1)
    role_action.is_on_horse()


def calc():
    time.sleep(1)
    role_action.reset_visual_field()
    for i in range(0, 200):
        current_time = datetime.datetime.now()
        if 10 > current_time.hour > 5 and current_time.isoweekday() == 4:
            break
        elif current_time.hour == 5 and current_time.minute > 45:
            if current_time.isoweekday() == 4:  # 周四退出
                break
            time.sleep(16 * 60)  # 等到六点
            role_action.close_dialog()
        # 掉线检测
        utils.deal_offline()
        # 运行
        start_time = time.time()
        if not role_action.buy_map():
            role_action.try_reset()
            continue
        buy_time = time.time()
        # if not role_action.open_map():
        open_count = role_action.avoid_open_interrupt()
        if not open_count >= 0:
            role_action.try_reset()
            continue
        open_time = time.time()
        if not role_action.prepare_to_find():
            role_action.try_reset()
            continue
        on_way_time = time.time()
        # if on_way_time-open_time > 45:
        #     role_action.send_message_with_loc('出城时间太长')
        # 检测天气
        weather = get_weather.get_weather_name()
        # utils.auto_switch(weather)
        find_count, region_1_time, region_2_time = role_action.find_boxs()
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
            '天气': weather,
            # '买图耗时': buy_time-start_time,
            '开图耗时': round(open_time-buy_time, 2),
            '寻路去程耗时': round(on_way_time-open_time, 2),
            '寻路返程耗时': round(back_time-clear_time, 2),
            '找盒耗时': round((find_time-on_way_time)/60, 2),
            '区域1开盒耗时': round(region_1_time/60, 2),
            '区域2开盒耗时': round(region_2_time/60, 2),
            '清图耗时': round(clear_time-find_time, 2),
            '总耗时': round((back_time-start_time)/60, 2)
        }

        send_message.send_procedure_report(report_data, i+1)
