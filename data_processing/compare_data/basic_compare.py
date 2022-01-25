#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/29 11:04
# @Author :     xujiahui
# @Project :    robust_python
# @File :       basic_compare.py
# @Version :    V0.0.1
# @Desc :       ?


import csv
from typing import Tuple
from std_module.handy_tools import pairs


def _trans_parentheses(str_in: str) -> str:
    str_in = str_in.replace(")", "）")
    str_in = str_in.replace("(", "（")

    return str_in


def fill_dim_list(path_1: str, path_2: str) -> Tuple[list, list]:
    """
    根据输入csv文件的路径，返回两个填满[(dim_code, dim_name), (dim_code, dim_name), ...]的列表
    Args:
        path_1:
        path_2:
    Returns:

    """

    list_1 = []
    list_2 = []

    list_extend_1 = list_1.extend
    list_extend_2 = list_2.extend

    with open(path_1, encoding="utf8") as file:
        # 读取csv
        reader = csv.reader(file)
        for row in reader:
            # 去除空串
            tmp_list = [s for s in row if s]

            if 1 < len(tmp_list) < 3:
                list_extend_1(
                    list(pairs(iter((tmp_list[-2], _trans_parentheses(tmp_list[-1])))))
                )
            if len(tmp_list) > 2:
                list_extend_1(
                    list(pairs(iter((tmp_list[-3], _trans_parentheses(tmp_list[-1])))))
                )

    with open(path_2, encoding="utf8") as file:
        # 读取csv
        reader = csv.reader(file)
        for row in reader:
            # 去除空串
            tmp_list = [s for s in row if s]

            if 1 < len(tmp_list) < 3:
                list_extend_2(
                    list(pairs(iter((tmp_list[-2], _trans_parentheses(tmp_list[-1])))))
                )
            if len(tmp_list) > 2:
                list_extend_2(
                    list(pairs(iter((tmp_list[-3], _trans_parentheses(tmp_list[-1])))))
                )

    return list_1, list_2


def compare_data(list_in_dlmu: list, dict_std: dict) -> Tuple[list, list]:

    list_mapped = []
    list_unmapped = []

    list_mapped_append = list_mapped.append
    list_unmapped_append = list_unmapped.append

    get_std = dict_std.get

    for dlmu_code, dlmu_name in list_in_dlmu:
        if get_std(dlmu_name):
            list_mapped_append((dlmu_code, dlmu_name, get_std(dlmu_name), dlmu_name))
        else:
            list_unmapped_append((dlmu_code, dlmu_name))

    return list_mapped, list_unmapped


def write_csv(list_in: list, path: str):

    # print(list_in)

    # 升序排序
    def sort_asc(unsorted_list: list):
        for i in range(0, len(unsorted_list)):
            low = i
            for j, tmp_tuple in enumerate(unsorted_list):
                code, name = tmp_tuple[0], tmp_tuple[1]
                if int(code) < int(unsorted_list[low][0]):
                    unsorted_list[low], unsorted_list[j] = (
                        unsorted_list[j],
                        unsorted_list[low],
                    )

    sort_asc(list_in)

    with open(path, encoding="utf8", mode="w+") as file:
        list_in.reverse()
        for dtuple in list_in:
            file.write(",".join(dtuple) + "\n")
