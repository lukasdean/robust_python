#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/28 18:57
# @Author :     xujiahui
# @Project :    robust_python
# @File :       handy_tools.py
# @Version :    V0.0.1
# @Desc :       ?


from typing import Iterator, TypeVar, Tuple


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


T_ = TypeVar("T_")
Pairs_Iter = Iterator[Tuple[T_, T_]]


def pairs(iter_in: Iterator[T_]) -> Pairs_Iter:
    """
    将迭代器的元素前后元素两两组装为内含元组的迭代器返回，
    单个元素形如 (xxx, xxx)
    显然这里有一个预设要求，即传入迭代器中的元素个数是偶数
    Args:
        iter_in:

    Returns:

    """

    head = next(iter_in)

    for tail in iter_in:
        yield head, tail
        try:
            head = next(iter_in)
        except StopIteration:
            break


# a = pairs(iter(['1', '2', '3', '4', '5']))
# print(list(a))
# print(a)
