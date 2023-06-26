import sys
import os.path
import tkinter
from tkinter.ttk import Combobox
import requests
import time
import pystray
import ctypes
from PIL import Image
from pystray import MenuItem as item
from pathlib import Path
from tkinter import messagebox
from typing import Dict

flag = 0
url = "https://bing.img.run/rand.php"
proxy = {}
select = None


class WallPaper(object):
    def __init__(self):
        self.relative_path = None
        menu = (
            item(text='更换壁纸', action=self._change_wallpaper),
            item(text='退出', action=self._on_exit)
        )
        icon_path = self._resource_path(str(Path('resource/wallpaper.ico')))
        image = Image.open(icon_path)
        self.icon = pystray.Icon("name", image, "每日壁纸", menu)
        self._run()

    def _run(self):
        self.icon.run()

    @staticmethod
    def _change_wallpaper(self):
        user32 = ctypes.windll.user32
        response = requests.get(url=url, proxies=proxy)
        if response.status_code == 200:
            images = response.content

            cur_user = os.environ['USERPROFILE']
            wallpaper = f'{cur_user}\\pictures\\' + f'{time.strftime("%Y-%m-%d_%H-%M-%S")}.jpg'

            with open(wallpaper, 'wb') as file:
                file.write(images)
            if len(str(select.get()))<1:
                self._notify("随机壁纸", f"设置成功!当前源:Bing每日壁纸随机")
            else:
                self._notify("随机壁纸", f"设置成功!当前源:{select.get()}")
            print(wallpaper)
            user32.SystemParametersInfoW(20, 0, wallpaper, 0)
        else:
            self._notify("随机壁纸", "壁纸下载失败")

    def _notify(self, title: str, message: str):
        return self.icon.notify(title, message)

    def _resource_path(self, relative_path):
        self.relative_path = relative_path
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath('.')
        return Path(f'{base_path}/{relative_path}')

    def _on_exit(self):
        self.icon.stop()


class WinGUI(tkinter.Tk):
    widget_dic: Dict[str, tkinter.Widget] = {}

    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_button_ljbkcmo2"] = self.__tk_button_ljbkcmo2(self)
        self.widget_dic["tk_button_ljbkduyj"] = self.__tk_button_ljbkduyj(self)
        self.widget_dic["tk_button_666"] = self.__tk_button_666(self)
        self.widget_dic["tk_label_ljbketh6"] = self.__tk_label_ljbketh6(self)
        self.widget_dic["tk_select_box_ljbkgkq9"] = self.__tk_select_box_ljbkgkq9(self)

    def __win(self):
        self.title("壁纸预设")
        # 设置窗口大小、居中
        width = 400
        height = 200
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

        # 自动隐藏滚动条

    def scrollbar_autohide(self, bar, widget):
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)

    def __tk_button_ljbkcmo2(self, parent):
        btn = tkinter.Button(parent, text="使用clash代理", takefocus=False, )
        btn.place(x=10, y=160, width=178, height=30)
        return btn

    def __tk_button_666(self, parent):
        btn = tkinter.Button(parent, text="我网好！不用代理", takefocus=False, )
        btn.place(x=115, y=120, width=178, height=30)
        return btn
    def __tk_button_ljbkduyj(self, parent):
        btn = tkinter.Button(parent, text="使用v2ray代理", takefocus=False, )
        btn.place(x=210, y=160, width=178, height=30)
        return btn

    def __tk_label_ljbketh6(self, parent):
        label = tkinter.Label(parent, text="壁纸API选择 （不选默认为Bing）", anchor="center", )
        label.place(x=10, y=10, width=379, height=30)
        return label

    def __tk_select_box_ljbkgkq9(self, parent):
        global select
        select = tkinter.StringVar()
        cb = Combobox(parent, state="readonly", textvariable=select)
        cb['values'] = ("Bing每日壁纸随机", "Unsplash壁纸随机")
        cb.place(x=10, y=60, width=381, height=30)
        return cb


class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def use_none(self,evt):
        global url
        global proxy
        proxy = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        if select.get() == 'Unsplash壁纸随机':
            url = "https://source.unsplash.com/1920x1080/?wallpaper"
            try:
                response = requests.get(url, headers=headers, proxies=proxy, timeout=1)
            except Exception as e:
                messagebox.showerror(title="代理不可用", message="连不上啦！快去搞个代理吧")
                return
            else:
                messagebox.showinfo(title="代理可用", message="太潮啦，没代理也能连上")

        if select.get() == 'Bing每日壁纸随机':
            url = "https://bing.img.run/rand.php"
            try:
                response = requests.get(url, headers=headers, proxies=proxy, timeout=3)
            except Exception as e:
                messagebox.showerror(title="代理不可用", message="连不上啦！快去搞个代理吧")
                return
            else:
                messagebox.showinfo(title="代理可用", message="太潮啦，没代理也能连上")

        global flag
        flag = 1
        self.destroy()

    def use_clash(self, evt):
        global url
        global proxy
        proxy = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        try:
            response = requests.get(url="https://www.google.com", headers=headers, proxies=proxy, timeout=3)
        except Exception as e:
            messagebox.showerror(title="代理不可用", message="代理无效！请检查clash的http代理是否为7890端口")
            return
        else:
            messagebox.showinfo(title="代理可用", message="请求成功，代理IP有效！")

        if select.get() == 'Unsplash壁纸随机':
            url = "https://source.unsplash.com/1920x1080/?wallpaper"

        elif select.get() == 'Bing每日壁纸随机':
            url = "https://bing.img.run/rand.php"
        else:
            url = "https://bing.img.run/rand.php"

        global flag
        flag = 1
        self.destroy()

    def use_v2ray(self, evt):
        global url
        global proxy
        proxy = {
            'http': 'http://127.0.0.1:1081',
            'https': 'http://127.0.0.1:1081'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        try:
            response = requests.get(url="https://www.google.com", headers=headers, proxies=proxy, timeout=3)
        except Exception as e:
            messagebox.showerror(title="代理不可用", message="代理无效！请检查v2ray的http代理是否为1081端口")
            return
        else:
            messagebox.showinfo(title="代理可用",message="请求成功，代理IP有效！")


        if select.get() == 'Unsplash壁纸随机':
            url = "https://source.unsplash.com/1920x1080/?wallpaper"
        elif select.get() == 'Bing每日壁纸随机':
            url = "https://bing.img.run/rand.php"
        else:
            url = "https://bing.img.run/rand.php"

        global flag
        flag = 1
        self.destroy()

    def __event_bind(self):
        self.widget_dic["tk_button_ljbkcmo2"].bind('<Button-1>', self.use_clash)
        self.widget_dic["tk_button_ljbkduyj"].bind('<Button-1>', self.use_v2ray)
        self.widget_dic["tk_button_666"].bind('<Button-1>', self.use_none)


if __name__ == "__main__":
    win = Win()
    win.mainloop()

    if flag == 1:
        daily_wallpaper = WallPaper()
