#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/10 18:28
# @Author :     xujiahui
# @Project :    robust_python
# @File :       collections.py
# @Version :    V0.0.1
# @Desc :       ?


from typing import Iterator, TypeVar, Tuple


"""
通过TypeVar函数定义的类型变量T_用于准确描述legs()函数重组数据的方式。
类型标示指出输入类型决定了输出类型。
输入类型是某种类型T_组成的迭代器，与输出元组的元素类型必须一致，并且不涉及其他转换。
"""
T_ = TypeVar('T_')
Pairs_Iter = Iterator[Tuple[T_, T_]]


def legs(lat_lon_iter: Iterator[T_]) -> Pairs_Iter:
    """
    begin和end变量保存计算状态，
    使用有状态变量不符合函数式编程尽量使用不可变数据的要求，因此需要进一步优化。
    此外，它对函数的使用者是不可见的，是一种Python式混合实现风格。
    Args:
        lat_lon_iter:

    Returns:

    """
    
    begin = next(lat_lon_iter)
    for end in lat_lon_iter:
        yield begin, end
        begin = end


# 组对序列元素函数
#     处理任何类型的序列，将序列生成器给出的值组对。
#     由于循环体内部没有处理函数，需要时即可复用legs()函数。

# a = legs(iter(['1', '2', '3', '4', '5']))
# print(list(a))
