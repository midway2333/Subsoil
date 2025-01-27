from tkintertools import animation as amt
import tkintertools as tkt
import tkintertools.style as style
import tkinter as tk
from tkinter import ttk
from lang import *
from about import *
from pathlib import Path
import threading, ctypes, zipfile, json, os, subprocess, sys
import urllib.request
from tkinter import messagebox

script_path = os.path.abspath(__file__)  # 获取当前脚本的绝对路径
directory = os.path.dirname(script_path)  # 获取该脚本所在目录

def download_python(cv, root, language, pyc):
    """下载Python"""
    def _check_environment(path):
        """验证Python环境完整性"""
        required_files = {
            'python.exe',        # Python主程序
            'python311.dll',     # 3.11版本核心库
            'python3.dll',       # 通用兼容库
        }
        return any(os.path.exists(os.path.join(path, f)) for f in required_files)

    def _show_env_exists():
        """显示环境已存在提示"""
        messagebox.showerror(
            "error",
            language[22]
        )
        spinner.destroy()
        # 删除进度圈

    def install_pip():
        """自动为嵌入式Python安装pip"""
        sub_env_dir = os.path.join(directory, "sub_env")
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"

        try:
            urllib.request.urlretrieve(get_pip_url, os.path.join(sub_env_dir, "get-pip.py"))
            # 下载get-pip.py

            pth_path = os.path.join(sub_env_dir, "python311._pth")
            with open(pth_path, "r+") as f:
                content = f.read()
                content = content.replace("#import site", "import site")
                if "Lib\\site-packages" not in content:
                    content += "\nLib\\site-packages\n"
                f.seek(0)
                f.write(content)
            # 修改python311._pth

            cmd = f'{os.path.join(sub_env_dir, "python.exe")} {os.path.join(sub_env_dir, "get-pip.py")}'
            # 构造需要以管理员身份运行的命令

            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas",    # 请求管理员权限
                "cmd.exe", 
                f'/c {cmd}',   # 使用cmd /c来运行命令并关闭
                None, 
                0   # 不显示窗口
            )

        except Exception as e:
            messagebox.showerror("error", f"get-pip.py download: {str(e)}")
            return
            
    def _download_task():
        """下载流程"""
        url = ["https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip",
            "https://mirrors.aliyun.com/python-release/windows/python-3.11.9-embed-amd64.zip"]
        sub_env_dir = os.path.join(directory, "sub_env")
        zip_save_path = os.path.join(sub_env_dir, "python-embed.zip")
        # 路径处理

        try:
            if os.path.exists(sub_env_dir):
                if _check_environment(sub_env_dir):
                    root.after(0, _show_env_exists)
                    return   # 环境检查

            root.after(0, lambda: spinner.set(0.0))
            # 初始化进度圈

            root.after(0, lambda: os.makedirs(sub_env_dir, exist_ok=True))
            root.after(0, lambda: spinner.set(0.05))
            # 创建目录

            def _update_progress(count, block_size, total_size):
                progress = 0.05 + (count * block_size / total_size) * 0.85
                root.after(0, lambda: spinner.set(min(progress, 0.7)))
            # 更新进度圈

            urllib.request.urlretrieve(url[pyc.get()], zip_save_path, reporthook=_update_progress)
            root.after(0, lambda: spinner.set(0.8))
            # 下载完成

            with zipfile.ZipFile(zip_save_path, 'r') as zip_ref:
                zip_ref.extractall(sub_env_dir)
            root.after(0, lambda: spinner.set(0.85))
            # 解压文件

            os.remove(zip_save_path)
            root.after(0, lambda: spinner.set(0.9))
            # 清理压缩包

            install_pip()
            root.after(0, lambda: spinner.set(1.0))
            root.after(0, lambda: messagebox.showinfo("subsoil", language[24]))
            root.after(2000, lambda: spinner.destroy())
            # 安装pip

        except Exception as e:  # 捕获异常
            error_msg = str(e)   # 将错误信息转换为字符串并显式传递
            root.after(0, lambda msg=error_msg: messagebox.showerror("error", msg))
            root.after(0, lambda: spinner.destroy())
            return

    spinner = tkt.Spinner(cv, (1040, 927))
    # 创建进度组件

    threading.Thread(target=_download_task, daemon=True).start()
    # 启动后台线程,为了防止程序卡死


def install_libraries(cv, root, env_choose: tkt.ComboBox, source_choose: tkt.ComboBox):
    """安装指定库"""
    
    def _get_python_path():
        """获取嵌入式Python路径"""
        sub_env_dir = os.path.join(directory, "sub_env")
        python_exe = os.path.join(sub_env_dir, "python.exe")

        if not os.path.exists(python_exe):
            return root.after(0, lambda: messagebox.showerror("error", 'Not Find Python'))
        # 验证路径有效性

        return f'"{python_exe}"' if ' ' in python_exe else python_exe   # 处理空格路径

    def _get_library_list(env_index):
        """根据选择的环境获取库列表"""
        library_sets = {
            0: 'numpy torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 sentencepiece rich markdown',
            # 基础
            1: 'numpy torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 sentencepiece rich markdown galore-torch rich maliang opencc pyarrow sympy markdown pandas tkintertools typing_extensions tkhtmlview'
            # 开发
        }
        return library_sets.get(env_index,)

    def _get_pip_source(source_index):
        """获取对应的pip源"""
        sources = [
            "https://pypi.org/simple/",                   # 官方源
            "https://pypi.tuna.tsinghua.edu.cn/simple/"   # 清华镜像
        ]
        return sources[source_index]

    def _install_task():
        try:
            env_index = env_choose.get()
            source_index = source_choose.get()
            # 获取用户选择    

            python = _get_python_path()
            libraries = _get_library_list(env_index)
            source = _get_pip_source(source_index)
            # 获取安装参数

            root.after(0, lambda: spinner.set(0.0))
            # 初始化进度条

            cmd = python+ " -m " + "pip" + " install "+ libraries +" -i " + source   # type: ignore

            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas",    # 请求管理员权限
                "cmd.exe", 
                f'/c {cmd}',   # 使用cmd /c来运行命令并关闭
                None, 
                1   # 显示窗口
            )

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("error", str(e)))
        finally:
            root.after(3000, lambda: spinner.destroy())
        # 错误处理

    spinner = tkt.Spinner(cv, (1040, 1027))
    # 创建进度条

    threading.Thread(target=_install_task, daemon=True).start()
    # 启动线程

def install_customization_lib(cv, root, pip_choose: tkt.InputBox, source_choose: tkt.ComboBox):
    """安装自定义库"""

    def _get_python_path():
        """获取嵌入式Python路径"""
        sub_env_dir = os.path.join(directory, "sub_env")
        python_exe = os.path.join(sub_env_dir, "python.exe")

        if not os.path.exists(python_exe):
            return root.after(0, lambda: messagebox.showerror("error", 'Not Find Python'))
        # 验证路径有效性

        return f'"{python_exe}"' if ' ' in python_exe else python_exe   # 处理空格路径

    def _get_pip_source(source_index):
        """获取对应的pip源"""
        sources = [
            "https://pypi.org/simple/",                   # 官方源
            "https://pypi.tuna.tsinghua.edu.cn/simple/"   # 清华镜像
        ]
        return sources[source_index]
    
    def _install_task():
        try:
            pip_index = pip_choose.get()
            source_index = source_choose.get()
            # 获取用户选择    
        
            python = _get_python_path()
            source = _get_pip_source(source_index)
            # 获取安装参数

            root.after(0, lambda: spinner.set(0.0))
            # 初始化进度条

            cmd = python + " -m " + "pip" + " install " + pip_index + " -i "+ source   # type: ignore

            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas",    # 请求管理员权限
                "cmd.exe", 
                f'/c {cmd}',   # 使用cmd /c来运行命令并关闭
                None, 
                1   # 显示窗口
            )

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("error", str(e)))
        finally:
            root.after(3000, lambda: spinner.destroy())
        # 错误处理

    spinner = tkt.Spinner(cv, (1040, 1227))
    # 创建进度条

    threading.Thread(target=_install_task, daemon=True).start()
    # 启动线程

def get_pip_list(root, ):
    """获得pip list"""
    def _get_python_path():
        """获取嵌入式Python路径"""
        sub_env_dir = os.path.join(directory, "sub_env")
        python_exe = os.path.join(sub_env_dir, "python.exe")

        if not os.path.exists(python_exe):
            return root.after(0, lambda: messagebox.showerror("error", 'Not Find Python'))
        # 验证路径有效性

        return f'"{python_exe}"' if ' ' in python_exe else python_exe   # 处理空格路径
    
    def pip_list():
            python = _get_python_path()
            cmd = python + " -m " + "pip list"    # type: ignore
            # 获得路径

            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas",    # 请求管理员权限
                "cmd.exe", 
                f'/k {cmd}',   # 使用cmd /k来运行命令并关闭
                None, 
                1   # 显示窗口
            )

    threading.Thread(target=pip_list, daemon=True).start()
    # 启动线程

def check_py(language):
    """检查python版本"""
    sub_env_dir = os.path.join(directory, "sub_env")
    python_exe = os.path.join(sub_env_dir, "python.exe")

    if not os.path.exists(python_exe):   # 不存在python时
        return language[28]

    for i in range(7, 14):   # 遍历可能的版本
        py_vision = os.path.join(sub_env_dir, f'python3{i}.dll')

        if os.path.exists(py_vision):
            return f"3.{i}"

    else:
        return language[29]

def open_env_file(root):
    """打开环境文件夹"""
    sub_env_dir = os.path.join(directory, "sub_env")

    try:
        os.startfile(sub_env_dir)
        # 在Windows资源管理器中打开文件夹

    except:   # 未安装时
        return root.after(0, lambda: messagebox.showerror("error", 'Not Find Python'))

