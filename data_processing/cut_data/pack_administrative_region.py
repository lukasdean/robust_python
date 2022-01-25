#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/28 18:43
# @Author :     xujiahui
# @Project :    robust_python
# @File :       pack_administrative_region.py
# @Version :    V0.0.1
# @Desc :       ?


import csv
from data_processing.cut_data import csv_path_region
from std_module.handy_tools import if_odd, pairs

bad_data = []
bad_append = bad_data.append

dim_data = []
dim_extend = dim_data.extend


with open(csv_path_region) as file:
    
    # 读取csv
    reader = csv.reader(file)
    for row in reader:
        # 去除空串
        tmp_list = [s for s in row if s]
        
        # 判断列表长度是否为偶数，偶数才继续解析组装维度值和维度名，长度为奇数时放入脏数据列表中
        if if_odd(len(tmp_list)):
            bad_append(tmp_list)
        else:
            dim_extend(list(pairs(iter(tmp_list))))

# print(dim_data)
# print(bad_data)
