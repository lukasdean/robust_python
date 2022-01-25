#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/28 19:39
# @Author :     xujiahui
# @Project :    robust_python
# @File :       pack_discipline_fields.py
# @Version :    V0.0.1
# @Desc :       ?
# 学科门类提供的的数据分为两种，维度值和维度名在一行中的以及维度值和维度名在上下两行中的


import csv
from typing import Tuple
from data_processing.cut_data import csv_path_discipline_1col
from std_module.handy_tools import if_odd, pairs


def pack_2col(path: str) -> Tuple[list, list]:
    """
    组装维度值和维度名在一行中的学科门类数据
    Args:
        path: csv文件所在路径
    Returns:
        返回数据元组，形如 ([(), (), ...], [(), (), ...])
    """

    bad_data_1_col = []
    bad_append_1_col = bad_data_1_col.append

    dim_data_2_col = []
    dim_extend_2_col = dim_data_2_col.extend

    with open(path) as file:
    
        # 读取csv
        reader = csv.reader(file)
        for row in reader:
            # 去除空串
            tmp_list = [s for s in row if s]
        
            # 判断列表长度是否为偶数，偶数才继续解析组装维度值和维度名，长度为奇数时放入脏数据列表中
            if if_odd(len(tmp_list)):
                bad_append_1_col(tmp_list)
            else:
                dim_extend_2_col(list(pairs(iter(tmp_list))))
    
    return dim_data_2_col, bad_data_1_col
    

def pack_1col(path: str) -> list:
    """
    组装维度值和维度名在两行中的学科门类数据
    Args:
        path: csv文件所在路径
    Returns:
        返回数据元组，形如 ([(), (), ...], [(), (), ...])
    """

    dim_data_1_col = []
    dim_append_1_col = dim_data_1_col.append

    with open(path) as file:
        # 读取csv
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            # 去除空串
            tmp_list = [s for s in row if s]
            
            # 若奇数行(对应的i为偶数，因为迭代器下标从0开始)则为编码，偶数行(对应的i为奇数)则为中文
            if if_odd(i):
                dim_data_1_col[int((i - 1) / 2)] += (tmp_list[0],)
            else:
                dim_append_1_col((tmp_list[0],))
    
    return dim_data_1_col


if __name__ == '__main__':
    
    test_list = pack_1col(csv_path_discipline_1col)
    print(test_list)
    
    # test_list_1, test_list_2 = pack_2col(csv_path_discipline_2col)
    # print(test_list_1)
    # print(test_list_2)
    
    # print(if_odd(0))
    