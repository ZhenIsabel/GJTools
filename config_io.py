from functools import singledispatch
# import numpy as np
import config_model

# 读取并写入config_model


def load_config_from_file():
    # config = np.loadtxt('config.txt', delimiter=',')
    f = open(file='config.txt', mode='r', encoding="utf-8")
    file_data = f.readlines()
    index = 0
    for each_line in file_data:
        index += 1
        each_line = each_line.strip('\n')
        item_pair = each_line.split(',')
        if item_pair[0] in config_model.config:
            if index > 12:
                config_model.config[item_pair[0]] = item_pair[1]
            else:
                config_model.config[item_pair[0]] = float(item_pair[1])
    f.close()


# '@'符号用作函数修饰符是python2.4新增加的功能
# 修饰符必须出现在函数定义前一行，不允许和函数定义在同一行。也就是说＠A def f(): 是非法的
# 只可以在模块或类定义层内对函数进行修饰，不允许修修饰一个类。
# 一个修饰符就是一个函数它将被修饰的函数做为参数，并返回修饰后的同名函数或其它可调用的东西。
# 此处用来实现函数重载
@singledispatch
def write_config(data):
    with open('config.txt', 'w') as config:
        # config.write(str('config=['))
        length = len(data)
        for i in range(length):
            if(i == (length-1)):
                config.write(str(data[i]))
            else:
                config.write(str(data[i])+'\n')
        # config.write(str(']'))


@write_config.register(dict)
def _(data):
    with open('config.txt', 'w') as config:
        # config.write(str('config=['))
        length = len(data)
        for index, key in enumerate(data):
            if(index == (length-1)):
                config.write(str(key)+','+str(data[key]))
            else:
                config.write(str(key)+','+str(data[key])+'\n')
        # config.write(str(']'))
