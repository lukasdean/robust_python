# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@项目名称    ：etl_pyscripts
@文件名称    ：code_fragment.py
@版本信息    ： 1.0
@作者       ：徐嘉辉
@创建日期    ：2021/4/13 17:28
@文件描述    ：一些可能有用的代码段
"""


import os
import copy
import math
from collections.abc import Iterable

import pandas as pd


def fill_none_iterable(none_iterable):
    """
    专门用于填充包含None值的可迭代对象，逻辑为将None值填充为上一个不为None的对象
    @日期: 过去的某个时刻
    @作者: 徐嘉辉
    Args:
        none_iterable: 包含None值的可迭代对象

    Returns:
        返回填充完毕的元组
    """

    tmp = None
    back_tuple = ()
    for element in none_iterable:

        if element is not None:
            tmp = element

        back_tuple = back_tuple + (tmp,)

    return back_tuple


def eliminate_duplicates(duplicated_iterable):
    """
    对于包含重复元素且基于数组(可以通过下标访问)的可迭代对象，清除其重复元素并保持原顺序不变
    @日期: 过去的某个时刻
    @作者: 徐嘉辉
    Args:
        duplicated_iterable: 包含重复元素且基于数组(可以通过下标访问)的可迭代对象

    Returns:
        返回一个保持了原来元素顺序且去重完毕的列表
    """

    return sorted(set(duplicated_iterable), key=duplicated_iterable.index)


def replace_with_element(pending_iterable, pattern_tuple):
    """
    对于可迭代对象根据提供的模式进行元素值替换
    @日期: 过去的某个时刻
    @作者: 徐嘉辉
    Args:
        pending_iterable: 可迭代对象
        pattern_tuple: 模式元组(待替换元素,用于替换元素,待替换元素,用于替换元素...)

    Returns:
        返回替换完毕的原可迭代对象的列表副本
    """

    # 判断pattern_tuple长度是否为偶数
    if len(pattern_tuple) & 1:
        # 长度为奇数，抛出ValueError
        raise ValueError("输入的模式元组长度为奇数，请检查其正确性！")

    pending_copy = list(copy.deepcopy(pending_iterable))

    for i, element in enumerate(pending_iterable):

        for j, pattern in enumerate(pattern_tuple):

            if (j & 1) and (element == pattern_tuple[j - 1]):
                # 奇数下标时判断当前元素是否和模式元组中上一个元素值相等，相等则进行替换并跳出当前循环
                pending_copy[i] = pattern_tuple[j]

                break

    return pending_copy


def flatten(iterable_sth):
    """
    拉平函数，用于将嵌套结构拉平成一个迭代器
    @日期: 过去的某个时刻
    @作者: 徐嘉辉
    Args:
        iterable_sth:

    Returns:
        返回一个包含传入可迭代对象中所有元素的迭代器
    """

    if isinstance(iterable_sth, Iterable) and not isinstance(iterable_sth, str):
        for sth in iterable_sth:
            for x in flatten(sth):
                yield x
    else:
        yield iterable_sth


def chinese2digits(uchars_chinese: str):
    """
    将传入小写汉字数字转换成阿拉伯数字
    @日期: 2021/01/12
    @作者: 徐嘉辉
    :param uchars_chinese: 小写汉字数字
    :return: total str类型，阿拉伯数字
    """
    
    common_used_numerals = {
        "零": 0,
        "一": 1,
        "二": 2,
        "两": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "百": 100,
        "千": 1000,
        "万": 10000,
        "亿": 100000000,
    }

    total = 0
    # 表示单位：个十百千...
    r = 1
    if uchars_chinese is not None:
        for i in range(len(uchars_chinese) - 1, -1, -1):
            val = common_used_numerals.get(uchars_chinese[i])
            # 应对 十三 十四 十*之类
            if val is not None and val >= 10 and i == 0:
                if val > r:
                    r = val
                    total = total + val
                else:
                    r = r * val
            elif val is not None and val >= 10:
                if val > r:
                    r = val
                else:
                    r = r * val
            elif val is not None:
                total = total + r * val
    return total


def substr_by_num(given_str: str, max_num: int):
    """
    一个按给定长度切割字符串的函数
    @日期: 2021/01/12
    @作者: 徐嘉辉
    :param given_str: 待切割的函数
    :param max_num: 每隔max_num个字符切割出一个字符串
    :return: 返回一个字符串列表，其中存放所有切割完毕的字符串
    """
    
    loop_num = len(given_str) / max_num
    if loop_num > 1:
        back_list = []
        for i in range(1, math.ceil(loop_num) + 1):
            start_num = (i - 1) * max_num
            end_num = i * max_num
            back_list.append(given_str[start_num:end_num])
        return back_list
    else:
        return [given_str]


def gen_interval_tuple(series, interval_num: int, close_flag: str = "1", decimal_digit=0):
    """
    根据传入的series和要切分的区间个数返回一个包含区间开始结束值的嵌套数据结构
    @日期: 2021/01/12
    @作者: 徐嘉辉
    Args:
        series: pandas的Series数据结构或者一个一维的ndarray
        interval_num: 将要切分的区间个数
        close_flag: 开闭区间的选取方式,不传默认1-左闭右开,传入2-左开右闭
        decimal_digit: 区间端点的小数位数, 默认 0位 取整

    Returns:
        返回一个嵌套的元组 形如((左端点, 右端点), (左端点, 右端点), ...)
    """

    dict_close = {
        # 区间左闭右开
        "1": (True, False),
        # 区间左开右闭
        "2": (False, True),
    }

    interval_tuple = ()

    if len(series) > 0:

        interval_info = pd.cut(
            x=series,
            bins=interval_num,
            retbins=False,
            # 表示区间的左边是开还是闭的
            include_lowest=dict_close[close_flag][0],
            # 表示是否包含区间右部
            right=dict_close[close_flag][1],
            # 区间端点保留小数点位数
            precision=decimal_digit
        )

        for interval in interval_info.cat.categories:
            interval_tuple += ((interval.left, interval.right),)

    return interval_tuple


def if_odd(number: int):
    """
    判断传入数字是奇数还是偶数
    @日期: 2021/05/27
    @作者: 徐嘉辉
    Args:
        number: int类型数字

    Returns:
        偶数时返回False，奇数时返回True
    """

    return (number & 1) > 0


def set_interval(start_hour: int, end_hour: int):
    """
    根据传入起始时间点获取时间段元组(包含start_hour不包含end_hour)
    例如 1 -> ('00', '01')
    @日期: 2021/06/22
    @作者: 徐嘉辉
    Args:
        start_hour: 开始时间点
        end_hour: 结束时间点

    Returns:

    """

    for i in range(start_hour, end_hour):
        head = str(i - 1).zfill(2)
        tail = str(i).zfill(2)

        yield head, tail


def del_files(
    model_path: str, keep_num: int, model_date: str, untrained_names: Iterable
):
    """
    用于清理指定目录下的 keep_num-1 天前的模型文件和untrained文件
    @日期: 2021/06/24
    @作者: 徐嘉辉
    Args:
        model_path: 脚本生成模型的存放路径(末尾带有/)
        keep_num: 将要保存的文件个数
        model_date: 指定日期
        untrained_names: 未建模文件的名称，可以是任意可迭代对象，
                         存储着形如"ele_tmr_mid_sum_untrained"的文件名字符串

    Returns:

    """

    # 获取指定路径下所有文件的文件名
    file_names = os.listdir(model_path)

    for model_name in file_names:

        # 去除学校简写和日期的模型前半部分名称
        base_tmp_name = "_".join(model_name.split("_")[:-2])
        # 模型日期
        base_tmp_date = model_name.split("_")[-1].rstrip(".pkl")
        # 未建模文件名称集合
        untrained_set = set(untrained_names)

        if base_tmp_name in untrained_set:
            # 删除未训练文件(不论出于什么原因生成了这个文件)

            os.remove(model_path + model_name)
        elif int(base_tmp_date) <= (int(model_date) - keep_num):

            # 删除已经不需要了的模型
            os.remove(model_path + model_name)


def dump_untraind_file(
    model_path: str,
    model_without_suffix: str,
    index_type: str,
    comment: str,
    model_date: str,
    week_day_mark: str = None,
):
    """
    用于生成指定目录下的 untrained 文件
    @日期: 2021/06/24
    @作者: 徐嘉辉
    Args:
        model_path: 脚本生成模型的存放路径(末尾带有/)
        model_without_suffix: 模型名前缀，例如 busi_tmr或者ele_tmr
        index_type: 指标类型，例如 cnt/fee/sum 等
        comment: 将要写入文件的一句说明，通常是警告和友善的提示，但也有可能在抱怨
        model_date: 建模脚本执行日期
        week_day_mark: 用于标识当前是周中还是周末的字符串，'end'-周末 'mid'-周中 None(默认情况)-不需要区分周中周末

    Returns:

    """

    untraind_model_name = ""

    if week_day_mark:
        # 模型需要区分周中和周末

        untraind_model_name = (
            f"{model_without_suffix}_{week_day_mark}_{index_type}_untrained_{model_date}"
        )
    else:
        # 模型不需要区分周中和周末

        untraind_model_name = (
            f"{model_without_suffix}_{index_type}_untrained_{model_date}"
        )

    untraind_model_path = model_path + untraind_model_name

    with open(untraind_model_path, mode="w+", encoding="utf-8") as save_file:
        save_file.write(comment)


def simple_relu(input_x: float) -> float:
    """
    正如其名称暗示的，这是一个用于数据清洗(通常)用的relu函数
    @日期: 2021/06/25
    @作者: 徐嘉辉
    Args:
        input_x: 输入数据

    Returns:
        0和输入数据之间的最大值
    """

    return max(0.00, input_x)


def is_chinese(str_in: str):
    """
    检查整个字符串是否包含中文
    @日期: 2021/07/10
    @作者: 徐嘉辉
    Args:
        str_in: 待检查的字符串

    Returns:
        bool值
    """
    for s in str_in:
        if u'\u4e00' <= s <= u'\u9fff':
            return True

    return False
