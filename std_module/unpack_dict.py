# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者：徐嘉辉
@创建日期：2021/3/22
@文件名：unpack_dict.py
@模块说明：
"""


import sys


class UnpackDict(object):
    def __init__(self, unpacking_dict: dict):
        """
        初始化函数，根据传入的字典开始操作
        Args:
            unpacking_dict: 传入的外部字典对象
        """

        self.unpacking_dict = unpacking_dict

    def __getitem__(self, item):
        """
        定义对容器中某一项使用 self[key] 的方式进行赋值操作时的行为。
        它是可变容器类型必须实现的一个方法，同样应该在合适的时候产生 KeyError 和 TypeError 异常。
        此处暂不处理
        Args:
            item: 外部传入的项名称，针对当前这个类的目的来说就是字符串
        Returns:
            back_val: 指定位置的字典值
        """

        if not isinstance(item, str):
            print("必须以字符串的形式访问UnpackDict对象中的项！")
            sys.exit(0)
        else:
            # 解析字符串
            key_list = item.split("/")
            back_val = self.unpacking_dict
            # 循环获取value值
            for key in key_list:
                back_val = back_val[key]

            return back_val
