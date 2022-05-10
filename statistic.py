import numpy as np

data_set = {
    '开盒': [1,2,3],
    '总图数': [4,5,6],
    '清理数': [7,8,9],
    '天气': [9,9,9],
    '买图耗时': [10,11,9],
    '开图耗时': [12,13,9],
    '寻路耗时': [14,15,9],
    '找盒耗时': [16,17,18],
    '清图耗时': [0,9,9],
    '总耗时': [20,9,9]
}


def write_data_set_1():
    with open('dataset.txt', 'a') as write_data:
        total_length = len(data_set)
        for index, key in enumerate(data_set):
            for i in data_set[key]:
                length = len(data_set[key])
                if(i == (length-1)):
                    write_data.write(str(data_set[key][i]))
                else:
                    write_data.write(str(data_set[key][i])+',')
            if not index == total_length-1:
                write_data.write('\n')

def write_data_set():
    data_array=[]
    for index, key in enumerate(data_set):
        data_array.append(data_set[key])
    np_data=np.array(data_array,dtype=np.float16)
    np.savetxt('dataset.txt',np_data)

def draw():
    pass

def calc():
    pass