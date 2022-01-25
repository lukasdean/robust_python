#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/25 0:37
# @Author :     xujiahui
# @Project :    robust_python
# @File :       try_wx_prc2.py
# @Version :    V0.0.1
# @Desc :       ?


# -*- coding: utf-8 -*-

import wx

APP_TITLE = u"基本框架"


class main_Frame(wx.Frame):
    """程序主窗口类，继承自wx.Frame"""

    def __init__(self):
        """构造函数"""

        wx.Frame.__init__(
            self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.Center()

        self.st_0 = wx.StaticText(
            self, -1, u"", pos=(40, 50), size=(100, -1), style=wx.ALIGN_RIGHT
        )
        self.st_1 = wx.StaticText(
            self, -1, u"", pos=(40, 80), size=(100, -1), style=wx.ALIGN_RIGHT
        )
        self.st_2 = wx.StaticText(
            self, -1, u"", pos=(40, 100), size=(100, -1), style=wx.ALIGN_RIGHT
        )
        self.btn_one = wx.Button(self, -1, u"按钮1", pos=(350, 50), size=(100, 25))
        self.btn_two = wx.Button(self, -1, u"按钮2", pos=(350, 80), size=(100, 25))
        self.btn_thr = wx.Button(self, -1, u"按钮3", pos=(350, 110), size=(100, 25))

        self.Bind(wx.EVT_BUTTON, self.On_Click, self.btn_one)
        self.Bind(wx.EVT_BUTTON, self.On_Click, self.btn_two)
        self.Bind(wx.EVT_BUTTON, self.On_Click, self.btn_thr)

    def On_Click(self, evt):

        if evt.GetEventObject() == self.btn_one:
            print("按钮1")
            self.st_0.SetLabel(u"静态文本1")
            self.st_1.SetLabel(u"")
            self.st_2.SetLabel(u"")

        if evt.GetEventObject() == self.btn_two:
            print("按钮2")
            self.st_0.SetLabel(u"")
            self.st_1.SetLabel(u"静态文本2")
            self.st_2.SetLabel(u"")

        if evt.GetEventObject() == self.btn_thr:
            print("按钮3")
            self.st_0.SetLabel(u"")
            self.st_1.SetLabel(u"")
            self.st_2.SetLabel(u"静态文本3")


class main_App(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.frame = main_Frame()
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = main_App()
    app.MainLoop()
