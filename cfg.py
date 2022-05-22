
# 开盒子时间
open_box_time = 5

# 单张开图时间
single_open_time=5
# 买图量
buy_map_count=36
# 是否额外买图到50
is_extra_buy=True

# 下马判断
judge_horse = False
# 鲜花饼判断
judge_flower = False


# 获取绝对坐标的屏幕位置
current_loc_area = [2130, 174, 104, 29]
# 获取绝对坐标二值化参数
loc_threshold_param = 220

# 小地图的屏幕位置
small_map_area = [1941, 206, 298, 235]
# 小地图箭头颜色范围
arrow_color_high = [120, 255, 255]
arrow_color_low = [20, 140, 190]
# 小地图箭头区域大小
arrow_area_max = 500
arrow_area_min = 200

# 天气区域
weather_area = [1980, 160, 100, 50]

# 脚下中心点
footer_pos = [1280,790]
# 脚下可开盒子区域
box_under_footer_area = [1042, 740, 420, 288]

# 太远了提示位置
too_far_area = [909, 353, 150, 100]

# 点开藏宝地图模式位置
open_box_map_pos = [880, 191]

# 要丢掉的首张图位值
first_map_pos = [2069, 522]

# 确定按钮位置
confirm_pos = [880, 450]


# 背包格子大小
bag_item_size = 36
bag_width = 12
bag_empty_lines = 3
# 买图次数
buy_map_times = 1


# 家园走到门口的位移距离
home_to_door = [-10, 0]

# 按键配置
key_map='m' # 地图键
key_commu='g' # 交互键
key_horse='t' # 坐骑键

# 盒子二值化参数
threshold_value = [80, 60, 40]
# 盒子大小
box_area_up = 1400
box_area_down = 400


# 开始挖宝的坐标方向和大小
begin_find_loc_1 = [-825, -540]
begin_find_direct_1 = 0.6
find_area_1 = [65, 42]
# 挖宝区域大小
begin_find_loc_2 = [-975, -525]
begin_find_direct_2 = -0.5
find_area_2 = [61, 34]

# 地图式搜索时的步距
move_distance_x = 4.5
move_distance_y = 3


# 速度值
move_speed = 0.1
move_back_speed = 2.5
turn_speed = 1.5
# 转动可识别的最小角度
turn_min = 0.025
# 移动可识别的最小坐标差
move_min = 1

# 最多移动多少距离后校准方向
max_move_distance = 50

# 邮件设置
receive_addr = "code_test_message@163.com"
send_addr="code_test_message@163.com"
send_password='RYXVVTELHMNPHJUY'


# 金像间隔
gold_interval_time = 4 * 60 * 60 + 10 * 60

# 绿图换角色间隔
green_interval_time = 1.5 * 60 * 60

# 游戏界面变化检查时间
check_game_state_step = 5

# 角色选择界面参数
first_role_loc = [2144, 257]
# 角色选择页滚轮到底部后，第一个头像的位置
next_page_role_loc = [2144, 289]
role_distance = 97
role_page_count = 7

# 区服选择界面参数
# 区服选择按钮和开始游戏按钮距离
choose_regional_distance = [-100, 45]
first_regional_loc = [110, 95]
# 翻页后第一个区的位置
next_page_regional_loc = [110, 130]
# 区服区域大小
regional_size = [170, 50]
regional_page_line_count = 4

open_game_time = 30

goto_huanglangyuan_time = 50
goto_changheshan_time = 30
goto_huaixiucun_time = 30
goto_huahai_time = 30
goto_zhongnanshan_time = 30
goto_baicaogu_time = 30

# 角色在屏幕里中心点
# role_screen_pos = [965, 520]
role_screen_pos = [1280, 720]
# 发邮件截图区
screenshot_region = [660, 240, 600, 600]

# 空中移动参数
sky_speed_default = -22.7
sky_speed_min = -30
sky_speed_max = -10
sky_move_times = 5

map_debug = False

# 入战处理
auto_kill_monster = True

# 自动挖金像
auto_dig_gold_symbols = True

# 要开的区
region_list = [[1, 0, 8], [1, 3, 8]]
