#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/24 8:48
# @Author :     xujiahui
# @Project :    robust_python
# @File :       validate.py
# @Version :    V0.0.1
# @Desc :       一个简单的使用元类组合验证的例子


class BetterPolygon:

    sides = None  # Must be specified by subclass

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError("Polygons need 3+ sides")

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


# 单独使用BetterPolygon来验证多边形子类边数是否>=3
class Hexagon(BetterPolygon):
    sides = 6


assert Hexagon.interior_angles() == 720


class Filled:
    color = None  # Must be specified by subclass

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ("red", "green", "blue"):
            raise ValueError("Fills need a valid color")


class RedTriangle(Filled, BetterPolygon):
    color = "red"
    sides = 3


# 验证红色三角形是否能在边数验证和填色验证两个超类的组合验证逻辑下完整构建出来
ruddy = RedTriangle()
assert isinstance(ruddy, Filled)
assert isinstance(ruddy, BetterPolygon)

"""
总结一下， __init_subclass__ 这个特殊的类方法非常强大。
在多层的类体系中，只要通过内置的 super() 函数来调用 __init_subclass__ 方法，
就可以保证那些类在各自的 __init_subclass__ 里面所实现的验证逻辑也能够正确地执行。
不仅是上面例子中的情况，当出现菱形继承关系时， __init_subclass__ 也能处理得很好。
当然，也可以不使用 __init_subclass__ ，这是在python3.6之后提供的方法，
但手工编写和它功能类似的元类组合非常费眼睛和键盘，并且会令代码库大大膨胀，因此如果可以，尽量用它。
"""
