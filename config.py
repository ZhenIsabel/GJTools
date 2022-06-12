config = {
    'my_card_region': [714, 840, 900, 180], # 自己的出牌区域，第三个是长，第四个是宽，其他不改
    'card_pool_region': [606, 549, 1075, 224], # 卡池区域，第四个是宽，其他不改
    'my_card_to_edge':[396,670], # 出牌左上角到游戏边框的距离，第一个是到左边，第二个是到上边
    'card_pool_to_edge':[265,392],# 卡池左上角到游戏边框的距离，第一个是到左边，第二个是到上边
    'receive_email_add': 'code_test_message@163.com',  # 接收报错邮件的地址
    'send_email_add':'code_test_message@163.com',  # 发送报错邮件的地址
    'send_email_pw':'RYXVVTELHMNPHJUY',# 发送邮件的密码
    'send_email_host':"smtp.163.com",# 发送邮件的服务商的host
    'key_commu': 'g',  # 交互键
    'longxing_pos':[1280,600],# 龙星阵位置，人在中间不需要改
    'first_card_loc_in_pool':[677,645],# 卡池中第一张卡的位置
    'card_space_in_pool':85,# 卡池中卡牌间隔像素
    'score_region':[0,0,60,26],# 自己的分数区，第三个是长，第四个是宽，其他不改
    'target_run_hour':60,# 运行多久后自动停止
}

# 1080p或者其他分辨率窗口模式开1080p的，只需要改邮件相关信息及运行时长