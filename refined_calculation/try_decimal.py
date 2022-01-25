#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/25 0:58
# @Author :     xujiahui
# @Project :    robust_python
# @File :       try_decimal.py
# @Version :    V0.0.1
# @Desc :       在需要精确计算的场合，使用 decimal


from decimal import Decimal


rate = Decimal("1.45")
seconds = Decimal(3 * 60 + 42)
cost = rate * seconds / Decimal(60)
print(cost)

# Decimal的初始值可以用两种办法来指定，
# 第一种，把含有数值的 str 字符串传给 Decimal 的构造函数，这样做不会让字符串里的数值由于 Python 本身的浮点数机制而出现偏差。
# 第二种，直接把 float 或 int 实例传给构造函数。两种办法在某些小数上会产生不同的效果，见下面的例子。
print(Decimal("1.45"))
print(Decimal(1.45))
