#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/24 9:09
# @Author :     xujiahui
# @Project :    robust_python
# @File :       auto_reg.py
# @Version :    V0.0.1
# @Desc :       这里介绍的例子是另一个元类的常用用途：自动记录(或者说注册)程序之中的类型。
#               利用这个功能，我们就能根据某个标识符反向查出它所对应的类。


import json


"""
现在，假设想做这件事：我们想按照自己的办法给Python对象做序列化处理，并将其表示成JSON格式的数据。
"""


class Serializable:
    """
    定义一个基类，让想支持上述这种序列化功能的类都继承这个基类，
    并把构造时所使用的参数上报，以便让此基类将参数转换成为一份JSON字典。
    """

    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({"args": self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super(Point2D, self).__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point2d({self.x}, {self.y})"


# 当使用的是Point2D这样简单而不可变的数据，可以很容易把它转化成JSON字符串
point = Point2D(5, 3)
print("Object: ", point)
print("Serialized: ", point.serialize())

"""
假如现在还想实现反序列化的功能，将反序列化的操作留给继承了 Serializable 的子类即可，
但是，这个方案的缺点也很明显，必须提前知道JSON字符串所表示的类型，然后才能将它还原成对象。
如果只用一个函数就能把各种JSON字符串分别还原成对应类型的Python对象那就更好了，
可以为此定义字典和注册函数，只要所有类继承了序列化的功能基类，就将其注册到字典中，
这样在之后可以通过字典中的类名来反序列化，
手工调用这个注册函数比较麻烦，并且容易遗忘，为此，使用元类在子类定义时拦截，然后自动调用注册函数。
"""
registry = {}


def register_class(target_class):
    registry[target_class.__name__] = target_class


def deserialize(data):
    params = json.loads(data)
    name = params["class"]
    target_class = registry[name]

    return target_class(*params["args"])


class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):

        return json.dumps(
            {
                "class": self.__class__.__name__,
                "args": self.args,
            }
        )

    def __repr__(self):
        name = self.__class__.__name__
        args_str = ", ".join(str(x) for x in self.args)

        return f"{name}({args_str})"


class BetterRegisteredSerializable(BetterSerializable):
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)


class Vector1D(BetterRegisteredSerializable):
    def __init__(self, magnitude):
        super(Vector1D, self).__init__(magnitude)
        self.magnitude = magnitude


before = Vector1D(6)
print("Before: ", before)
data = before.serialize()
print("Serialized: ", data)
print("After: ", deserialize(data))

"""
总结一下， 在类体系正确无误的前提下，通过 __init_subclass__ (或元类)自动注册子类可以避免程序由于用户忘记注册儿引发问题。
这不仅适用于上述序列化与反序列化功能的实现，而且还可以用在数据库的对象关系映射(object-relational mapping, ORM)、
可扩展的插件系统以及回调挂钩上面。
"""
