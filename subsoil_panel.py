from def_box import *

"""
新版本的tkintertools已经改名为maliang
但是本代码没有使用最新版本
而pip现在能提供的tkintertools貌似是2.6
本代码使用的却是3.0
所以想直接运行实际上有点难办
"""

move_score = 0
# 移动分,用于计算更改主栏时的移动大小

def disposition():
    """加载配置文件"""
    try:   # 尝试读取配置文件
        with open(f'{directory}\\sub_config.json', 'r') as f:
            config = json.load(f)
            language_value = config[0]['language']
            # 读取配置文件中的语言设置

            theme = config[0]['theme']
            # 读取配置文件中的主题设置

            return language_value, theme
    
    except FileNotFoundError:   # 没有配置文件时
        default_disposition = [
                {
                    "language": 0,  # 默认语言设置
                    "theme": "light"   # 默认主题设置
                }
            ]   # 创建默认配置

        with open(f'{directory}\\sub_config.json', 'w', encoding='utf-8') as f:
            json.dump(default_disposition, f, ensure_ascii=False, indent=4)
        # 写入默认配置

        return 0, "light"

class main_ui():
    """主界面"""
    def __init__(self):

        language_value, theme = disposition()   # 读取配置文件中的语言和主题设置

        style.set_color_mode(theme)   # 设置主题色
        language: list[str] = lang(language_value)   # type: ignore
        # 语言设置

        root = tkt.Tk(title='Subsoil', icon=f'{directory}\\mcb.ico')
        # 创建窗口

        cv_main = tkt.Canvas(root, zoom_item=True)
        cv_main.place(width=1280, height=720*8, x=0, y=0)
        # 主栏

        color_modes = {
            'light': {'bg': '#FFCA2C'},   # 浅色模式的颜色设置
            'dark': {'bg': '#858585'}   # 深色模式的颜色设置
        }

        cv_minor = tkt.Canvas(root, name="", bg=color_modes[theme]['bg'], zoom_item=True)
        cv_minor.place(width=300, height=720, x=0, y=0)
        # 侧栏

        tkt.Text(cv_minor, (20, 5), text="Subsoil", anchor="nw", fontsize=48)
        tkt.Text(cv_minor, (20, 55), text="Panel", anchor="nw", fontsize=48)
        # 侧栏标题

        tkt.Button(cv_minor, (45,180), (200,50), text=language[3], fontsize=24,
                command=lambda: move(cv_main, 0))        # 主页
        tkt.Button(cv_minor, (45,230), (200,50), text=language[4], fontsize=24,
                command=lambda: move(cv_main, -720))     # 环境
        tkt.Button(cv_minor, (45,280), (200,50), text=language[5], fontsize=24,
                command=lambda: move(cv_main, -720*2))   # 详细
        tkt.Button(cv_minor, (45,330), (200,50), text=language[2], fontsize=24,
                command=lambda: move(cv_main, -720*3))   # 设置
        tkt.Button(cv_minor, (45,380), (200,50), text=language[6], fontsize=24,
                command=lambda: move(cv_main, -720*4))   # 关于
        # 侧控件

        Page = page(cv_main, cv_minor, language, language_value, root)
        Page.hp_page()
        Page.env_page()
        Page.dt_page()
        Page.set_page()
        Page.abt_page()
        # 初始化界面显示

        root.mainloop()

class page():
    """页面实现"""
    def __init__(self, cv_main, cv_minor, language, lang_value, root):
        """

        实现各个页面的界面和页面之间的切换

        参数:
        - cv_main: 主界面
        - language: 语言翻译获取
        - lang_value: 语言选择
        - root: GUI主程序

        """

        self.cv_main = cv_main
        self.language = language
        self.light = light(cv_minor)
        self.lang = lang_choose
        self.lang_value = lang_value
        self.apply = apply(root)
        self.root = root

    def hp_page(self):
        """主界面"""
        tkt.Text(self.cv_main, (320, 5), text=self.language[7], fontsize=48)
        # 标题

        tkt.Label(
            self.cv_main,
            (1030, 80),
            (230, 620),
            text=self.language[8],
            fontsize=28,
            justify='left',
        )   # 公告栏

    def env_page(self):
        """环境设置界面"""
        tkt.Text(self.cv_main, (320, 725), text=self.language[4], fontsize=48)   # 大标题
        tkt.Text(self.cv_main, (320, 925), text=self.language[11], fontsize=24)
        tkt.Text(self.cv_main, (320, 1025), text=self.language[12], fontsize=24)
        tkt.Text(self.cv_main, (320, 1125), text=self.language[17], fontsize=24)
        tkt.Text(self.cv_main, (320, 1225), text=self.language[26], fontsize=24)
        # 文本显示

        pip = tkt.InputBox(self.cv_main, (600, 1220),size=(300, 45), placeholder=self.language[25])
        sce = tkt.ComboBox(self.cv_main, (600, 1120),size=(300, 45),default=1,   \
                            text=(self.language[18],self.language[19]), animation=True)
        env = tkt.ComboBox(self.cv_main, (600, 1020),size=(300, 45),default=0,   \
                            text=(self.language[13],self.language[14]), animation=True)
        pyc = tkt.ComboBox(self.cv_main, (600, 920),size=(300, 45),default=0,   \
                            text=("Python 3.11","Python 3.11(mirror)"), animation=True)
        # 选择项目

        tkt.Button(self.cv_main, (920, 920), size=(100, 45), text=self.language[20],
                   command=lambda: (download_python(self.cv_main, self.root, self.language, pyc)))
        tkt.Button(self.cv_main, (920, 1020), size=(100, 45), text=self.language[21],
                   command=lambda: (install_libraries(self.cv_main, self.root, env, sce)))
        tkt.Button(self.cv_main, (920, 1220), size=(100, 45), text=self.language[21],
                   command=lambda: (install_customization_lib(self.cv_main, self.root, pip, sce)))
        # 按钮

    def dt_page(self):
        """详细环境界面"""
        tkt.Text(self.cv_main, (320, 720*2+5), text=self.language[10], fontsize=48)
        tkt.Text(self.cv_main, (600, 720*2+185), text='Python: ', fontsize=24)
        tkt.Text(self.cv_main, (700, 720*2+185), text=check_py(self.language), fontsize=24)
        # 文本显示

        tkt.Button(self.cv_main, (320, 720*2+180), size=(100, 45), text=self.language[27],
                   )
        tkt.Button(self.cv_main, (320, 720*2+250), size=(100, 45), text='Pip list',
                   command=lambda: (get_pip_list(self.root)))
        tkt.Button(self.cv_main, (600, 720*2+250), size=(100, 45), text=self.language[30],
                   command=lambda: (open_env_file(self.root)))
        # 按钮

    def set_page(self):
        """设置界面"""
        tkt.Text(self.cv_main, (320, 720*3+5), text=self.language[9], fontsize=48)
        # 大标题

        tkt.Text(self.cv_main, (760, 720*3+695), text=self.language[0], anchor="nw", fontsize=16)
        # 版本信息

        tkt.Button(self.cv_main, (320, 720*3+265),size=(100, 50), text=self.language[16], fontsize=24
                    , animation=True, command=self.light.light)
        # 亮/暗色模式

        tkt.Text(self.cv_main, (540, 720*3+205), text=self.language[1], anchor="nw", fontsize=24)
        # 语言选择字幕

        lan_choose = "English","简体中文"
        tkt.ComboBox(self.cv_main, (320, 720*3+195),size=(180, 50), default=self.lang_value,
                    text=lan_choose, animation=True, command=lambda i:self.lang(i))
        # 语言选择控制

        tkt.Button(self.cv_main, (1170, 720*3+660),size=(100, 50), text=self.language[15], fontsize=24,
                    animation=True, command=self.apply.apply)
        # 应用按钮

    def abt_page(self):
        """About界面"""
        tkt.Text(self.cv_main, (320, 720*4+5), text=self.language[6], fontsize=48)

        html_frame = tk.Frame(self.cv_main)
        html_frame.place(x=320, y=720*4+70, width=960, height=630)
        # 初始化markdown显示框

        about = [about_en, about_cn]
        html_label = tkhtmlview.HTMLScrolledText(
            html_frame,
            html=markdown.markdown(about[self.lang_value]),
        )   # markdown显示框

        html_label.pack(fill=tk.BOTH, expand=True)
        # 布局HTML组件

class light():
    """主题色控制"""
    def __init__(self, cv_minor):
        self.cv = cv_minor

    def light(self):
        """亮/暗色模式"""
        if style.get_color_mode() == 'dark':   # 深色模式时
            style.set_color_mode('light')
            theme = "light"

        else:   # 浅色模式时
            style.set_color_mode('dark')
            theme = "dark"

        current_mode = style.get_color_mode()
        # 获得现在的主题色

        color_modes = {
            'light': {'bg': '#FFCA2C'},   # 浅色模式的颜色设置
            'dark': {'bg': '#858585'}   # 深色模式的颜色设置
        }

        self.cv.configure(bg=color_modes[current_mode]['bg'])
        # 更新颜色模式和画布背景颜色

        with open(f'{directory}\\sub_config.json', 'r') as f:   # 修改配置文件
            disposition = json.load(f)
            disposition[0]['theme'] = theme

        with open(f'{directory}\\sub_config.json', 'w') as f:
            json.dump(disposition, f, indent=4)
            # 将修改后的数据写回文件

class lang_choose():
    """语言选择"""
    def __init__(self, choose):
        self.choose = choose   # 选择的语言

        with open(f'{directory}\\sub_config.json', 'r') as f:   # 修改配置文件
            disposition = json.load(f)
            disposition[0]['language'] = self.choose

        with open(f'{directory}\\sub_config.json', 'w') as f:
            json.dump(disposition, f, indent=4)
            # 将修改后的数据写回文件

class apply():
    """应用设置"""
    def __init__(self, root):
        self.root = root

    def apply(self):
        self.root.destroy()       # 销毁当前窗口

        global move_score
        move_score = 0
        # 重置移动分

        main_ui()

def move(cv, aim):
    """
    移动界面
    - cv: 移动的画布
    - aim: 目标值
    """
    global move_score   # 声明变量
    amt.MoveTkWidget(cv, 500, (0, aim-move_score), controller=amt.smooth, fps=60).start()
    # 移动画布

    move_score = aim   # 更变移动分

if __name__ == '__main__':
    main_ui()
