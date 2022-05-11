import os
import tkinter as tk
from functools import singledispatch
from tkinter import ttk
from tkinter.messagebox import askokcancel

import test_weather

import window_control
import pyautogui

import calculate
import config_io
import config_model

# 是否允许鼠标挪出界自动关闭
pyautogui.FAILSAFE = False

# region 数据格式转换


@singledispatch
def tk_value_to_value(data):
    result = []
    for item in data:
        result.append(item.get())
    return result


@tk_value_to_value.register(dict)
def _(data):
    result = dict()
    for index, pair in enumerate(data.items()):
        result[pair[0]] = data[pair[0]].get()
    return result

# @singledispatch
# def value_to_tk_value(data):
#     result = []
#     for item in data:
#         result.append(item)
#     return result


# @value_to_tk_value.register(dict)
# def _(data):
#     result = dict()
#     for index,pair in enumerate(data.items()):
#         # result.update({pair[0]: data[pair[0]]})
#         # try:
#             result[pair[0]].set(data[pair[0]])
#         # except Exception as e :
#         #     print("config_model中的数据与ui中的默认形式不匹配")

#     return result
# endregion


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create control variables
        self.variables = {'is_yuanbo': tk.IntVar(),            # 是否是渊博状态
                          'is_large_region': tk.IntVar(),  # 是否扩图
                          'is_extra_buy':tk.IntVar(),  # 是否额外买到50图
                          'is_binarization': tk.IntVar(),  # 是否采用二值化风格
                          'max_move_distance': tk.DoubleVar(),  # 最长经过多少距离进行转向检测
                          'move_speed': tk.DoubleVar(),       # 步速（非扫图速度）
                          'turn_speed': tk.DoubleVar(),       # 转向速度
                          'count_yuanbo': tk.IntVar(),         # 渊博时最大持图数量
                          'count_no_yuanbo': tk.IntVar(),      # 非渊博时最大持图数量
                          'open_box_time': tk.DoubleVar(),        # 开盒子读条时间
                          'single_map_time': tk.DoubleVar(),       # 龙星阵开单张图时间
                          'move_distance_x': tk.DoubleVar(),      # 地图搜索时x轴步距
                          'move_distance_y': tk.DoubleVar(),  # 地图搜索时y轴步距
                          'is_testmode': tk.IntVar(),  # 是否是测试模式
                          'email_add': tk.StringVar(),  # 接收报错邮件的地址
                          'key_commu': tk.StringVar(),  # 交互键
                          'key_map': tk.StringVar(),  # 地图键
                          'key_horse': tk.StringVar(),  # 坐骑键

                          }

        # Create widgets :
        self.setup_widgets()

    def setup_widgets(self):
        # region main frame
        self.main_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.main_frame.grid(
            row=0, column=20, padx=0, pady=(0, 0), sticky="nsew", rowspan=20
        )
        # region 开始键

        def start(event):
            # main.main_fun()
            # config_io.write_config(tk_value_to_value(self.variables))
            # os.system('python main.py')
            print("start")
            # ui中的数据同步到config_model中
            for index, pair in enumerate(self.variables.items()):
                config_model.config[pair[0]] = self.variables[pair[0]].get()
            # 最大化古剑
            window_control.window_focus('古剑奇谭网络版')
            calculate.calc()

        self.start_button = ttk.Button(
            self.main_frame, text="运行", style="Accent.TButton"
        )
        self.start_button.grid(row=3, column=0, padx=10,
                               pady=10, sticky="nsew")
        self.start_button.bind("<Button-1>", start)
        # endregion

        # region 数值读取键
        def para_load_fun(event):
            check = askokcancel(title='确认',
                                message='确认读取数据吗？'
                                )
            if check:
                config_io.load_config_from_file()
            # 参数传递
            for index, pair in enumerate(config_model.config.items()):
                self.variables[pair[0]].set(config_model.config[pair[0]])
            print("loaded and applied")
        self.para_load = ttk.Button(self.main_frame, text="读取参数")
        self.para_load.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.para_load.bind("<Button-1>", para_load_fun)
        # endregion

        # region 数值保存键
        def para_save_fun(event):
            check = askokcancel(title='确认',
                                message='确认保存数据吗？'
                                )
            if check:
                config_io.write_config(tk_value_to_value(self.variables))
                print("saved")
        self.para_save = ttk.Button(self.main_frame, text="保存参数")
        self.para_save.grid(row=1, column=0, padx=10,
                            pady=10, sticky="nsew")
        self.para_save.bind("<Button-1>", para_save_fun)
        # endregion

        # region 天气测试键

        def weather_test(event):
            check = askokcancel(title='确认',
                                message='确认测试天气吗？'
                                )
            if check:
                 # 最大化古剑
                window_control.window_focus('古剑奇谭网络版')
                test_weather.weather_test(
                    [170, 80, 80]
                    if config_model.config['is_binarization']
                    else
                    
                    [80, 60, 40]
                )
                print("weather test completed")
        self.weather_test = ttk.Button(self.main_frame, text="天气测试")
        self.weather_test.grid(row=2, column=0, padx=10,
                               pady=10, sticky="nsew")
        self.weather_test.bind("<Button-1>", weather_test)
        # endregion

        # region Progressbar
        # self.progress = ttk.Progressbar(
        #     self.tab_parameter, value=0, variable=self.var_5, mode="determinate"
        # )
        # self.progress.grid(row=0, column=1, padx=(
        #     10, 20), pady=(20, 0), sticky="ew")
        # endregion

        # endregion

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=0, pady=(
            0, 0), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Notebook, pane #2
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_1)
        self.notebook.pack(fill="both", expand=True)

        # region Tab normal
        self.tab_normal = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_normal.columnconfigure(index=index, weight=1)
            self.tab_normal.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_normal, text="常规")

        # region 创建switch开关框架
        self.switch_frame = ttk.LabelFrame(
            self.tab_normal, text="选项开关", padding=(20, 10))
        self.switch_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        # endregion

        # region 渊博开关
        self.switch_yuanbo = ttk.Checkbutton(
            self.switch_frame, text="渊博", style="Switch.TCheckbutton",
            onvalue=1, offvalue=0,
            variable=self.variables['is_yuanbo'])

        self.switch_yuanbo.grid(row=0, column=0, padx=5,
                                pady=10, sticky="nsew")
        # endregion

        # region 扩图开关
        self.switch_large_region = ttk.Checkbutton(
            self.switch_frame, text="扩图", style="Switch.TCheckbutton",
            onvalue=1, offvalue=0, variable=self.variables['is_large_region'])

        self.switch_large_region.grid(row=1, column=0, padx=5,
                                      pady=10, sticky="nsew")
        # endregion

        # region 二值化模式开关
        self.switch_large_region = ttk.Checkbutton(
            self.switch_frame, text="二值化", style="Switch.TCheckbutton",
            onvalue=1, offvalue=0, variable=self.variables['is_binarization'])

        self.switch_large_region.grid(row=2, column=0, padx=5,
                                      pady=10, sticky="nsew")
        # endregion

        # region 额外买图开关
        self.switch_extra_buy = ttk.Checkbutton(
            self.switch_frame, text="买到50图", style="Switch.TCheckbutton",
            onvalue=1, offvalue=0, variable=self.variables['is_extra_buy'])

        self.switch_extra_buy.grid(row=3, column=0, padx=5,
                                      pady=10, sticky="nsew")
        # endregion

        # region 测试模式开关
        self.switch_testmode = ttk.Checkbutton(
            self.switch_frame, text="测试模式", style="Switch.TCheckbutton",
            onvalue=1, offvalue=0, variable=self.variables['is_testmode']
        )
        self.switch_testmode.grid(
            row=5, column=0, padx=5, pady=10, sticky="nsew")
        # endregion

        # region 创建数量调整框架
        self.para_frame = ttk.LabelFrame(
            self.tab_normal, text="数量调整", padding=(20, 10))
        self.para_frame.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        # endregion

        # region 最大拥有图数
        ttk.Label(
            self.para_frame,
            text="渊博图数",
            justify="center",
            font=('microsoft yahei ui',  10,  "normal"),
        ).grid(row=0, column=0, pady=0)
        self.entry_count_yuanbo = ttk.Entry(
            self.para_frame,
            textvariable=self.variables['count_yuanbo'],
            width=6)
        self.entry_count_yuanbo.grid(
            row=0, column=1, padx=5, pady=10, sticky="w")

        ttk.Label(
            self.para_frame,
            text="无渊博图数",
            justify="center",
            font=('microsoft yahei ui',  10,  "normal"),
        ).grid(row=1, column=0, pady=0)
        self.entry_count_no_yuanbo = ttk.Entry(
            self.para_frame,
            textvariable=self.variables['count_no_yuanbo'],
            width=6)
        self.entry_count_no_yuanbo.grid(
            row=1, column=1, padx=5, pady=10,  sticky="w")

        # endregion

        # region 地图式搜索时的步距
        # x轴
        ttk.Label(
            self.para_frame,
            text="搜索时步距\n(x,y)",
            justify="center",
            font=('microsoft yahei ui',  10,  "normal"),
        ).grid(row=2, column=0, pady=0)
        self.entry_move_distance_x = ttk.Entry(
            self.para_frame,
            textvariable=self.variables['move_distance_x'],
            width=6
        )
        self.entry_move_distance_x.grid(
            row=2, column=1, padx=5, pady=10, sticky="w")

        # y轴
        self.entry_move_distance_y = ttk.Entry(
            self.para_frame,
            textvariable=self.variables['move_distance_y'],
            width=6
        )
        self.entry_move_distance_y.grid(
            row=2, column=2, padx=5, pady=10, sticky="w")

        # endregion

        # endregion

        # region Tab parameter
        self.tab_parameter = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_parameter, text="参数")

        # region 拖条框架
        self.scale_frame = ttk.LabelFrame(
            self.tab_parameter, text="数值设置", padding=(20, 10))
        self.scale_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(0, 0), sticky="nsew", rowspan=3
        )
        # endregion

        # region 步速
        ttk.Label(
            self.scale_frame,
            text="步速",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        ).grid(row=0, column=0, pady=0)
        self.move_speed_scale = ttk.Scale(
            self.scale_frame,
            from_=0,
            to=1,
            variable=self.variables['move_speed'],
            command=lambda event: self.variables['move_speed'].set(
                self.variables['move_speed'].get()),
        )
        self.move_speed_scale.grid(row=0, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.move_speed_entry = ttk.Entry(
            self.scale_frame, textvariable=self.variables['move_speed']
        )
        self.move_speed_entry.grid(
            row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        # endregion

        # region 转向速度
        self.turn_speed_scale_label = ttk.Label(
            self.scale_frame,
            text="转向速度",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.turn_speed_scale_label.grid(row=1, column=0, pady=0)
        self.turn_speed_scale = ttk.Scale(
            self.scale_frame,
            from_=0,
            to=3,
            variable=self.variables['turn_speed'],
            command=lambda event: self.variables['turn_speed'].set(
                self.variables['turn_speed'].get()),
        )
        self.turn_speed_scale.grid(row=1, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.turn_speed_entry = ttk.Entry(
            self.scale_frame, textvariable=self.variables['turn_speed']
        )
        self.turn_speed_entry.grid(row=1, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")
        # endregion

        # region 最多移动多少距离后校准方向
        self.max_move_distance_scale_label = ttk.Label(
            self.scale_frame,
            text="最多移动多少距离后校准方向",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.max_move_distance_scale_label.grid(
            row=2, column=0, pady=0, columnspan=1, padx=(20, 10))
        self.max_move_distance_scale = ttk.Scale(
            self.scale_frame,
            from_=20,
            to=100,
            variable=self.variables['max_move_distance'],
            command=lambda event: self.variables['max_move_distance'].set(
                self.variables['max_move_distance'].get()),
        )
        self.max_move_distance_scale.grid(row=2, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.max_move_distance_entry = ttk.Entry(
            self.scale_frame, textvariable=self.variables['max_move_distance']
        )
        self.max_move_distance_entry.grid(row=2, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")
        # endregion

        # region 读条时长
        self.open_box_time_scale_label = ttk.Label(
            self.scale_frame,
            text="开盒子读条",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.open_box_time_scale_label.grid(row=3, column=0, pady=0)
        self.open_box_time_scale = ttk.Scale(
            self.scale_frame,
            from_=0,
            to=6,
            variable=self.variables['open_box_time'],
            command=lambda event: self.variables['open_box_time'].set(
                self.variables['open_box_time'].get()),
        )
        self.open_box_time_scale.grid(row=3, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.open_box_time_entry = ttk.Entry(
            self.scale_frame, textvariable=self.variables['open_box_time']
        )
        self.open_box_time_entry.grid(row=3, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")

        # endregion

        # region 开图时长
        self.single_map_time_scale_label = ttk.Label(
            self.scale_frame,
            text="龙星阵开单张图时长",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.single_map_time_scale_label.grid(row=4, column=0, pady=0)
        self.single_map_time_scale = ttk.Scale(
            self.scale_frame,
            from_=0,
            to=6,
            variable=self.variables['single_map_time'],
            command=lambda event: self.variables['single_map_time'].set(
                self.variables['single_map_time'].get()),
        )
        self.single_map_time_scale.grid(row=4, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.single_map_time_entry = ttk.Entry(
            self.scale_frame, textvariable=self.variables['single_map_time']
        )
        self.single_map_time_entry.grid(row=4, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")

        # endregion

        # region 按键设置

        # region 按键设置框架
        self.press_set_frame = ttk.LabelFrame(
            self.tab_parameter, text="按键设置", padding=(20, 10))
        self.press_set_frame.grid(
            row=0, column=1, padx=(20, 10), pady=(0, 0), sticky="nsew"
        )
        # endregion

        ttk.Label(
            self.press_set_frame,
            text="交互键",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        ).grid(row=0, column=0, pady=0)
        self.entry_count_no_yuanbo = ttk.Entry(
            self.press_set_frame,
            textvariable=self.variables['key_commu'],
            width=6)
        self.entry_count_no_yuanbo.grid(
            row=0, column=1, padx=5, pady=10,  sticky="w")

        ttk.Label(
            self.press_set_frame,
            text="地图键",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        ).grid(row=1, column=0, pady=10)
        self.entry_count_no_yuanbo = ttk.Entry(
            self.press_set_frame,
            textvariable=self.variables['key_map'],
            width=6)
        self.entry_count_no_yuanbo.grid(
            row=1, column=1, padx=5, pady=10,  sticky="w")

        ttk.Label(
            self.press_set_frame,
            text="坐骑键",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        ).grid(row=2, column=0, pady=10)
        self.entry_count_no_yuanbo = ttk.Entry(
            self.press_set_frame,
            textvariable=self.variables['key_horse'],
            width=6)
        self.entry_count_no_yuanbo.grid(
            row=2, column=1, padx=5, pady=10,  sticky="w")

        # endregion

        # endregion

        # region Tab 初始化
        self.tab_init = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_init, text="初始化")

        # # 整个游戏画面截屏键
        # self.button = ttk.Button(self.tab_init, text="截取游戏画面")
        # self.button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # # 分区截屏键
        # self.button = ttk.Button(self.tab_init, text="获取目标元素画面")
        # self.button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # # Togglebutton 选取变色键
        # self.togglebutton_loc_area = ttk.Checkbutton(
        #     self.tab_init, text="小地图坐标文字", style="Toggle.TButton"
        # )
        # self.togglebutton_loc_area.grid(
        #     row=0, column=0, padx=5, pady=10, sticky="nsew")

        # self.togglebutton_bag_item = ttk.Checkbutton(
        #     self.tab_init, text="背包格子", style="Toggle.TButton"
        # )
        # self.togglebutton_bag_item.grid(
        #     row=1, column=0, padx=5, pady=10, sticky="nsew")

        # # 背包一排格子数
        # self.entry_bag_width = ttk.Entry(self.tab_init)
        # self.entry_bag_width.insert(0, "背包一行格子数")
        # self.entry_bag_width.grid(
        #     row=2, column=0, padx=5, pady=10, sticky="nsew")

        # # 如更改分辨率，则需改动以下值
        # self.extra_capture_frame = ttk.LabelFrame(
        #     self.tab_init, text="如更改分辨率，则需改动以下值", padding=(20, 10))
        # self.extra_capture_frame.grid(
        #     row=0, column=1, padx=10, pady=(0, 0), sticky="nsew", rowspan=10
        # )
        # self.extra_capture_frame.columnconfigure(index=0, weight=1)

        # # Scrollbar
        # self.scrollbar = ttk.Scrollbar(self.extra_capture_frame)
        # self.scrollbar.pack(side="right", fill="y")

        # # Select and scroll
        # self.treeview.selection_set(10)
        # self.treeview.see(7)

        self.entry_email = ttk.Entry(
            self.tab_init,
            textvariable=self.variables['email_add']
        )
        self.entry_email.grid(
            row=10, column=1, padx=5, pady=(0, 0), sticky="w")

        self.label_entry_email = ttk.Label(
            self.tab_init,
            text="报错信息发送的邮箱",
            justify="center",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.label_entry_email.grid(row=10, column=0, padx=5, sticky="w")
        # endregion

        # region Tab about
        self.tab_about = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_about, text="帮助")

        # 帮助文档按钮
        def press_help_button(event):
            os.system('notepad readme.md')
            print("open readme")

        self.help_button = ttk.Button(self.tab_about, text="打开帮助文档")
        self.help_button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.help_button.bind("<Button-1>", press_help_button)

        # 致谢
        self.label_thanku = ttk.Label(
            self.tab_about,
            text='''
            作者：西陵鱼璃 xilingyuli
            UI：谢振衣
            版本：beta 0.1
            ''',
            justify="left",
            font=('microsoft yahei ui',  12,  "normal"),
        )
        self.label_thanku.grid(row=10, column=0, sticky="w")
        # endregion


# if __name__ == "__main__":
def ui_main():
    root = tk.Tk()
    root.title("猫猫挖宝")

    # Simply set the theme
    root.tk.call("source", "ui\sun-valley.tcl")
    root.tk.call("set_theme", "light")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) -
                      (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) -
                      (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    root.mainloop()
