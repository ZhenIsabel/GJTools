from xmlrpc.client import boolean
import numpy as np


# 读取
def load_config_from_file():
    config = np.loadtxt('config.txt', delimiter=',')
    # for i in config:
    #     print(i)
    max_move_distance_var = config[0]
    move_speed_var = config[1]
    turn_speed_var = config[2]
    count_yuanbo = config[3]
    count_no_yuanbo = config[4]
    open_box_time = config[5]
    move_distance_x = config[6]
    move_distance_y = config[7]

    config_data = Config_Data(is_yuanbo=False, config=[max_move_distance_var,
                                             move_speed_var,
                                             turn_speed_var,
                                             count_yuanbo,
                                             count_no_yuanbo,
                                             open_box_time,
                                             move_distance_x,
                                             move_distance_y
                                             ])
    return config_data


def load_config_inside(config):
    global max_move_distance_var
    global move_speed_var
    global turn_speed_var
    global count_yuanbo
    global count_no_yuanbo
    global open_box_time
    global move_distance_x
    global move_distance_y

    max_move_distance_var = config[0]
    move_speed_var = config[1]
    turn_speed_var = config[2]
    count_yuanbo = config[3]
    count_no_yuanbo = config[4]
    open_box_time = config[5]
    move_distance_x = config[6]
    move_distance_y = config[7]


# 写入
def write_config(data):
    with open('config.txt', 'w') as config:
        # config.write(str('config=['))
        length = len(data)
        for i in range(length):
            if(i == (length-1)):
                config.write(str(data[i]))
            else:
                config.write(str(data[i])+',')
        # config.write(str(']'))


# 全局变量
class Config_Data:
    # is_yuanbo
    # max_move_distance_var   # 最长经过多少距离进行转向检测
    # move_speed_var   # 步速（非扫图速度）
    # turn_speed_var   # 转向速度
    # count_yuanbo  # 渊博时最大持图数量
    # count_no_yuanbo  # 非渊博时最大持图数量
    # open_box_time   # 开盒子读条时间
    # move_distance_x   # 地图搜索时x轴步距
    # move_distance_y  # 地图搜索时y轴步距

    def __init__(self, is_yuanbo: boolean, config: list):
        self.is_yuanbo = is_yuanbo
        self.max_move_distance_var = config[0]
        self.move_speed_var = config[1]
        self.turn_speed_var = config[2]
        self.count_yuanbo = config[3]
        self.count_no_yuanbo = config[4]
        self.open_box_time = config[5]
        self.move_distance_x = config[6]
        self.move_distance_y = config[7]

    def printhhh(self):
        print(self.is_yuanbo)
        print(self.max_move_distance_var)
        print(self.move_speed_var)
        print(self.turn_speed_var)
        print(self.count_yuanbo)
        print(self.count_no_yuanbo)
        print(self.open_box_time)
        print(self.move_distance_x)
        print(self.move_distance_y)


# load_config()
