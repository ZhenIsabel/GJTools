from distutils.command.config import config
import tkinter as tk
from tkinter import ttk

import os
import config_io
# import main
import pyautogui

# 是否允许鼠标挪出界自动关闭
pyautogui.FAILSAFE = True


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create control variables
        self.is_yuanbo = tk.BooleanVar(value=False)  # 是否开启渊博
        self.max_move_distance_var = tk.IntVar(value=50)  # 最长经过多少距离进行转向检测
        self.move_speed_var = tk.DoubleVar(value=0.18)  # 步速（非扫图速度）
        self.turn_speed_var = tk.DoubleVar(value=1.97)  # 转向速度
        self.count_yuanbo = tk.IntVar(value=36)  # 渊博时最大持图数量
        self.count_no_yuanbo = tk.IntVar(value=15)  # 非渊博时最大持图数量
        self.open_box_time = tk.DoubleVar(value=5.5)  # 开盒子读条时间
        self.move_distance_x = tk.DoubleVar(value=4.5)  # 地图搜索时x轴步距
        self.move_distance_y = tk.DoubleVar(value=3)  # 地图搜索时y轴步距

        self.config = config_io.Config_Data(self.is_yuanbo.get(),
                                            [self.max_move_distance_var.get(),
                                             self.move_speed_var.get(),
                                             self.turn_speed_var.get(),
                                             self.count_yuanbo.get(),
                                             self.count_no_yuanbo.get(),
                                             self.open_box_time.get(),
                                             self.move_distance_x.get(),
                                             self.move_distance_y.get()
                                             ])
        # Create widgets :
        self.setup_widgets()

    def setup_widgets(self):

        # region 开始键
        def start(event):
            # main.main_fun()
            config_io.write_config([self.max_move_distance_var.get(),
                                             self.move_speed_var.get(),
                                             self.turn_speed_var.get(),
                                             self.count_yuanbo.get(),
                                             self.count_no_yuanbo.get(),
                                             self.open_box_time.get(),
                                             self.move_distance_x.get(),
                                             self.move_distance_y.get()
                                             ])
            os.system('python main.py')

        self.start_button = ttk.Button(
            self, text="保存并运行", style="Accent.TButton"
        )
        self.start_button.grid(row=8, column=0, padx=10,
                               pady=10, sticky="nsew")
        self.start_button.bind("<Button-1>", start)
        # endregion

        # region Progressbar
        # self.progress = ttk.Progressbar(
        #     self.tab_parameter, value=0, variable=self.var_5, mode="determinate"
        # )
        # self.progress.grid(row=0, column=1, padx=(
        #     10, 20), pady=(20, 0), sticky="ew")
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
            onvalue=True, offvalue=False, variable=self.is_yuanbo)

        self.switch_yuanbo.grid(row=0, column=0, padx=5,
                                pady=10, sticky="nsew")
        # endregion

        # region 参数学习开关
        # self.switch_learning = ttk.Checkbutton(
        #     self.switch_frame, text="参数学习（无效）", style="Switch.TCheckbutton"
        # )
        # self.switch_learning.grid(
        #     row=1, column=0, padx=5, pady=10, sticky="nsew")
        # endregion

        # endregion

        # region Tab parameter
        self.tab_parameter = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_parameter, text="参数")

        # region 步速
        self.move_speed_scale_label = ttk.Label(
            self.tab_parameter,
            text="步速",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.move_speed_scale_label.grid(row=0, column=0, pady=0)
        self.move_speed_scale = ttk.Scale(
            self.tab_parameter,
            from_=0,
            to=3,
            variable=self.move_speed_var,
            command=lambda event: self.move_speed_var.set(
                self.move_speed_var.get()),
        )
        self.move_speed_scale.grid(row=0, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.move_speed_entry = ttk.Entry(
            self.tab_parameter, textvariable=self.move_speed_var
        )
        self.move_speed_entry.grid(row=0, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")
        # endregion

        # region 转向速度
        self.turn_speed_scale_label = ttk.Label(
            self.tab_parameter,
            text="转向速度",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.turn_speed_scale_label.grid(row=1, column=0, pady=0)
        self.turn_speed_scale = ttk.Scale(
            self.tab_parameter,
            from_=0,
            to=5,
            variable=self.turn_speed_var,
            command=lambda event: self.turn_speed_var.set(
                self.turn_speed_var.get()),
        )
        self.turn_speed_scale.grid(row=1, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.turn_speed_entry = ttk.Entry(
            self.tab_parameter, textvariable=self.turn_speed_var
        )
        self.turn_speed_entry.grid(row=1, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")
        # endregion

        # region 最多移动多少距离后校准方向
        self.max_move_distance_scale_label = ttk.Label(
            self.tab_parameter,
            text="最多移动多少距离后校准方向",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.max_move_distance_scale_label.grid(
            row=2, column=0, pady=0, columnspan=1, padx=(20, 10))
        self.max_move_distance_scale = ttk.Scale(
            self.tab_parameter,
            from_=20,
            to=100,
            variable=self.max_move_distance_var,
            command=lambda event: self.max_move_distance_var.set(
                self.max_move_distance_var.get()),
        )
        self.max_move_distance_scale.grid(row=2, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.max_move_distance_entry = ttk.Entry(
            self.tab_parameter, textvariable=self.max_move_distance_var
        )
        self.max_move_distance_entry.grid(row=2, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")
        # endregion

        # region 读条时长
        self.open_box_time_scale_label = ttk.Label(
            self.tab_parameter,
            text="开盒子读条",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.open_box_time_scale_label.grid(row=3, column=0, pady=0)
        self.open_box_time_scale = ttk.Scale(
            self.tab_parameter,
            from_=0,
            to=6,
            variable=self.open_box_time,
            command=lambda event: self.open_box_time.set(
                self.open_box_time.get()),
        )
        self.open_box_time_scale.grid(row=3, column=0, padx=(
            20, 10), pady=(50, 0), sticky="ew", columnspan=2)

        self.open_box_time_entry = ttk.Entry(
            self.tab_parameter, textvariable=self.open_box_time
        )
        self.open_box_time_entry.grid(row=3, column=1, padx=(
            0, 10), pady=(0, 0), sticky="ew")

        # endregion

        # region 地图式搜索时的步距
        # x轴
        self.label_move_distance = ttk.Label(
            self.tab_parameter,
            text="搜索时步距\n(x,y)",
            justify="center",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.label_move_distance.grid(row=2, column=5, pady=0)
        self.entry_move_distance_x = ttk.Entry(
            self.tab_parameter, textvariable=self.move_distance_x, width=6
        )
        self.entry_move_distance_x.grid(
            row=2, column=6, padx=5, pady=(0, 10), sticky="w")

        # y轴
        self.entry_move_distance_y = ttk.Entry(
            self.tab_parameter, textvariable=self.move_distance_y, width=6)
        self.entry_move_distance_y.grid(
            row=2, column=7, padx=5, pady=(0, 10), sticky="w")

        # endregion

        # region 最大拥有图数
        self.label_count_yuanbo = ttk.Label(
            self.tab_parameter,
            text="渊博图数",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.label_count_yuanbo.grid(row=0, column=5, pady=0)
        self.entry_count_yuanbo = ttk.Entry(
            self.tab_parameter, textvariable=self.count_yuanbo, width=6)
        self.entry_count_yuanbo.grid(
            row=0, column=6, padx=5, pady=(0, 10), sticky="w")

        self.label_count_no_yuanbo = ttk.Label(
            self.tab_parameter,
            text="无渊博图数",
            justify="left",
            font=('microsoft yahei ui',  10,  "normal"),
        )
        self.label_count_no_yuanbo.grid(row=1, column=5, pady=0)
        self.entry_count_no_yuanbo = ttk.Entry(
            self.tab_parameter, textvariable=self.count_no_yuanbo, width=6)
        self.entry_count_no_yuanbo.grid(
            row=1, column=6, padx=5, pady=(0, 10), sticky="w")

        # endregion

        # region 数值读取键

        def para_load_fun(event):
            self.config = config_io.load_config_from_file()

            self.max_move_distance_var.set(self.config.max_move_distance_var),
            self.move_speed_var.set(self.config.move_speed_var),
            self.turn_speed_var.set(self.config.turn_speed_var),
            self.count_yuanbo.set(self.config.count_yuanbo),
            self.count_no_yuanbo.set(self.config.count_no_yuanbo),
            self.open_box_time.set(self.config.open_box_time),
            self.move_distance_x.set(self.config.move_distance_x),
            self.move_distance_y.set(self.config.move_distance_y)
            print("applied")
        self.para_load = ttk.Button(self.tab_parameter, text="读取参数")
        self.para_load.grid(row=7, column=8, padx=10, pady=10, sticky="nsew")
        self.para_load.bind("<Button-1>", para_load_fun)
        # endregion

        # region 数值保存键
        def para_save_fun(event):
            config_data = [self.max_move_distance_var.get(),
                           self.move_speed_var.get(),
                           self.turn_speed_var.get(),
                           self.count_yuanbo.get(),
                           self.count_no_yuanbo.get(),
                           self.open_box_time.get(),
                           self.move_distance_x.get(),
                           self.move_distance_y.get()
                           ]
            config_io.write_config(config_data)
            print("saved")
        self.para_save = ttk.Button(self.tab_parameter, text="保存参数")
        self.para_save.grid(row=8, column=8, padx=10,
                            pady=10, sticky="nsew")
        self.para_save.bind("<Button-1>", para_save_fun)
        # endregion

        # endregion

        # region Tab 初始化
        self.tab_capture = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_capture, text="初始化")

        # 整个游戏画面截屏键
        self.button = ttk.Button(self.tab_capture, text="截取游戏画面")
        self.button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # 分区截屏键
        self.button = ttk.Button(self.tab_capture, text="获取目标元素画面")
        self.button.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # Togglebutton 选取变色键
        self.togglebutton_loc_area = ttk.Checkbutton(
            self.tab_capture, text="小地图坐标文字", style="Toggle.TButton"
        )
        self.togglebutton_loc_area.grid(
            row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.togglebutton_bag_item = ttk.Checkbutton(
            self.tab_capture, text="背包格子", style="Toggle.TButton"
        )
        self.togglebutton_bag_item.grid(
            row=1, column=0, padx=5, pady=10, sticky="nsew")

        # 背包一排格子数
        self.entry_bag_width = ttk.Entry(self.tab_capture)
        self.entry_bag_width.insert(0, "背包一行格子数")
        self.entry_bag_width.grid(
            row=2, column=0, padx=5, pady=10, sticky="nsew")

        # 如更改分辨率，则需改动以下值
        self.extra_capture_frame = ttk.LabelFrame(
            self.tab_capture, text="如更改分辨率，则需改动以下值", padding=(20, 10))
        self.extra_capture_frame.grid(
            row=0, column=1, padx=10, pady=(0, 0), sticky="nsew", rowspan=10
        )
        self.extra_capture_frame.columnconfigure(index=0, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.extra_capture_frame)
        self.scrollbar.pack(side="right", fill="y")

        # # Select and scroll
        # self.treeview.selection_set(10)
        # self.treeview.see(7)

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


if __name__ == "__main__":
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
