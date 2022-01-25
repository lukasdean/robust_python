#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@项目名称    ：tools4work
@文件名称    ：divide_line.py
@版本信息    ： 1.0
@作者       ：徐嘉辉
@创建日期    ：2021/4/10 22:00
@文件描述    ：
"""


def gen_dividing_line(
    divide_symbol: str = "-",
    basic_length: int = 30,
    unit_divide_length: int = 3,
    std_length: int = 90,
    least_length: int = 5,
    annotation: str = "",
) -> str:
    """
    分割线生成函数
    Args:
        divide_symbol: 用于分割的符号，默认'-'
        basic_length: 分割线的长度
        unit_divide_length: 为了满足standard_length的规范长度不得不进行缩进时的最小缩进距离
        std_length: 单行的标准长度
        least_length: 分割线允许的最短长度
        annotation: 注释内容
    Returns:
        拼接好的注释内容
    """

    def _cut_length(current_length: int) -> int:
        """
        用于删减分割线的长度的内部函数
        Args:
            current_length: 当前分割线的长度
        Returns:
            返回合理的分隔线长度，若无法裁剪出一个合理的长度将抛出一个ValueError
        """

        current_length = current_length - unit_divide_length

        # 进行删减后进行基本检查，当前分割线长度 >= 最小分割线长度
        if current_length < least_length:
            raise ValueError("当前输入的注释不适合在一行中显示，考虑多行注释如何")

        # 设置边界条件，将要返回字符串的长度<=单行标准长度
        if (current_length * 2) + len(annotation) + 4 <= std_length:
            return current_length

        return _cut_length(current_length)

    # 首先判断#+' ' + basic_length*2 + annotation + 两头空格的长度是否超过standard_length
    if (basic_length * 2) + len(annotation) + 4 > std_length:
        # 超过进行分割线裁剪
        basic_length = _cut_length(basic_length)

    # 未超过直接返回拼接好的字符串
    divide_line = divide_symbol * basic_length
    back_str = "# " + divide_line + " " + annotation + " " + divide_line

    return back_str


print(gen_dividing_line(annotation="业务逻辑"))
