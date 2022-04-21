import tkinter as tk
from tkinter import Entry, ttk

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.parameter_option_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.parameter_option_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):
       
        # Accentbutton
        self.accentbutton = ttk.Button(
            self, text="开始运行", style="Accent.TButton"
        )
        self.accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=0, pady=(
            25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)


        # Notebook, pane #2
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_1)
        self.notebook.pack(fill="both", expand=True)

        # Tab normal
        self.tab_normal = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_normal.columnconfigure(index=index, weight=1)
            self.tab_normal.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_normal, text="常规")

         # 创建switch开关框架
        self.switch_frame = ttk.LabelFrame(self, text="选项开关", padding=(20, 10))
        self.switch_frame.grid(
            row=0, column=2, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        # Switch
        self.switch_yuanbo = ttk.Checkbutton(
            self.tab_normal, text="渊博", style="Switch.TCheckbutton"
        )
        self.switch_yuanbo.grid(row=0, column=0, padx=5,
                                pady=10, sticky="nsew")

        self.switch_learning = ttk.Checkbutton(
            self.tab_normal, text="参数学习（无效）", style="Switch.TCheckbutton"
        )
        self.switch_learning.grid(
            row=1, column=0, padx=5, pady=10, sticky="nsew")

        
        # Tab parameter
        self.tab_parameter = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_parameter, text="参数")
        
        # Scale
        self.scale = ttk.Scale(
            self.tab_parameter,
            from_=100,
            to=0,
            variable=self.var_5,
            command=lambda event: self.var_5.set(self.scale.get()),
        )
        self.scale.grid(row=0, column=0, padx=(
            20, 10), pady=(20, 0), sticky="ew")

        # Progressbar
        self.progress = ttk.Progressbar(
            self.tab_parameter, value=0, variable=self.var_5, mode="determinate"
        )
        self.progress.grid(row=0, column=1, padx=(
            10, 20), pady=(20, 0), sticky="ew")

        # Tab 初始化
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
        self.entry_bag_width.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

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

        # Treeview
        self.treeview = ttk.Treeview(
            self.extra_capture_frame,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=120)
        self.treeview.column(1, anchor="w", width=120)
        self.treeview.column(2, anchor="w", width=120)

        # Define treeview data
        treeview_data = [
            ("", 1, "Parent", ("Item 1", "Value 1")),
            (1, 2, "Child", ("Subitem 1.1", "Value 1.1")),
            (1, 3, "Child", ("Subitem 1.2", "Value 1.2")),
            (1, 4, "Child", ("Subitem 1.3", "Value 1.3")),
            (1, 5, "Child", ("Subitem 1.4", "Value 1.4")),
            ("", 6, "Parent", ("Item 2", "Value 2")),
            (6, 7, "Child", ("Subitem 2.1", "Value 2.1")),
            (6, 8, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (8, 9, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
            (8, 10, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
            (8, 11, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
            (6, 12, "Child", ("Subitem 2.3", "Value 2.3")),
            (6, 13, "Child", ("Subitem 2.4", "Value 2.4")),
            ("", 14, "Parent", ("Item 3", "Value 3")),
            (14, 15, "Child", ("Subitem 3.1", "Value 3.1")),
            (14, 16, "Child", ("Subitem 3.2", "Value 3.2")),
            (14, 17, "Child", ("Subitem 3.3", "Value 3.3")),
            (14, 18, "Child", ("Subitem 3.4", "Value 3.4")),
            ("", 19, "Parent", ("Item 4", "Value 4")),
            (19, 20, "Child", ("Subitem 4.1", "Value 4.1")),
            (19, 21, "Sub-parent", ("Subitem 4.2", "Value 4.2")),
            (21, 22, "Child", ("Subitem 4.2.1", "Value 4.2.1")),
            (21, 23, "Child", ("Subitem 4.2.2", "Value 4.2.2")),
            (21, 24, "Child", ("Subitem 4.2.3", "Value 4.2.3")),
            (19, 25, "Child", ("Subitem 4.3", "Value 4.3")),
        ]

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
            )
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview.item(item[1], open=True)  # Open parents

        # Select and scroll
        self.treeview.selection_set(10)
        self.treeview.see(7)

        # Tab about
        self.tab_about = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_about, text="帮助")
        

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
