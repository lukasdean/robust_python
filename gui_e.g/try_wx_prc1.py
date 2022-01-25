#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/25 0:25
# @Author :     xujiahui
# @Project :    robust_python
# @File :       try_wx_prc1.py
# @Version :    V0.0.1
# @Desc :       ?


import wx


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        super().__init__(parent, id, title, size)


class MyApp(wx.App):
    def __init__(self):
        super().__init__()

    def OnInit(self):
        frame = MainFrame(None, -1, "试试", (300, 500))
        frame.Show()
        frame.Center(True)

        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
