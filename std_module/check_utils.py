# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者：徐嘉辉
@创建日期：2021/3/24
@文件名：check_tool.py
@模块说明：通用的脚本执行时参数检查工具
"""


import sys

from config import ETL_INPUT_PARAMS_NUM
from msgOutput import msgOutput


def input_check(inputs):
    """
    这是一个入参检查函数
    Args:
        inputs: 脚本执行时输入参数列表
    Returns:
        一个bool值，当入参个数符合预设值时返回True，否则返回False
    """
    # 检查输入参数个数
    if len(inputs) != ETL_INPUT_PARAMS_NUM:
        print(msgOutput("参数错误!", 0))
        print(msgOutput("dateNo:操作数据业务时间格式(yyyyMMdd)", 0))
        print(msgOutput("例如:%s %s" % (inputs[0], 20210324), 0))

        return False

    return True
