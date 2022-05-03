import random

fucking_words = [
    '饼哥今天那么有空啊',
    '?',
    '你家柠檬还没吃完？',
    '不会酸得你半夜两点睡不着吧？',
    '夜以继日蹲在屏幕后面的你真的好帅',
    '螺丝拧完了？',
    '今天被工头骂了吧，不容易啊',
    '乌乌饼哥算了吧',
    '饼哥今天挖几张了？'
]


def fucking_coockie_bro():
    word_index = random.randint(0, len(fucking_words)-1)
    return fucking_words[word_index]

print(fucking_coockie_bro())