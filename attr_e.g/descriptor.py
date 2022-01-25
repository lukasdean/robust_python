#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/24 17:50
# @Author :     xujiahui
# @Project :    robust_python
# @File :       descriptor.py
# @Version :    V0.0.1
# @Desc :       为了保证最大限度地服用代码，python提供了描述符机制
#               下面实现一个成绩描述符，设置各科成绩时需要检查成绩是否介于0到100之间。


from weakref import WeakKeyDictionary


"""
先说明一下 Python 中的描述符机制是怎样起作用的：
以以下代码为例，
exam = Exam()
exam.writing_grade = 40
Python会把这次赋值操作转译为
Exam.__dict__['writing_grade'].__set__(exam, 40)
获取这个属性时也一样
exam.writing_grade
Python会把这次取值操作转译为
Exam.__dict__['writing_grade'].__get__(exam, Exam)
这种转译效果是由 object 的 __getattribute__ 方法促成的。
简单地说，就是当 Exam 实例里没有名为 writing_grade 的属性时，Python会转而在类的层面查找，
查询 Exam 类里面有没有这样一个属性。如果有，而且还是个实现了 __get__ 与 __set__ 方法的对象，
那么系统就认定这是想通过描述符协议定义这个属性的访问行为。
"""


class Grade:
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):

        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("Grade must be between 0 and 100")
        self._value = value


class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print("Writing ", first_exam.writing_grade)
print("Science ", first_exam.science_grade)

second_exam = Exam()
second_exam.writing_grade = 75
print(f"Second {second_exam.writing_grade} is right")
print(f"First {first_exam.writing_grade} is wrong;" f"should be 82")

"""
观察打印出的 first_exam.writing_grade 的值，显然在 second_exam.writing_grade 赋值后，
first_exam.writing_grade 的值发生了变化，这是由于这些 Exam 实例之中的 writing_grade 属性
实际上是在共享同一个 Grade 实例。在整个程序的运行过程中，这个 Grade 只会于定义 Exam 类时构造一次，
而不是每创建一个 Exam 实例都有一个新的 Grade 来与 writing_grade 属性相搭配。
为解决此问题，必须把每个 Exam 实例在这个属性上面的取值都记录下来。可以通过字典实现每个实例的状态保存。
"""


class NotReallyBetterGrade:
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self

        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("Grade must be between 0 and 100")
        self._values[instance] = value


"""
上面这种实现有什么问题呢？
它存在内存泄露的问题，在程序运行过程中，传给 __set__ 方法的那些 Exam 实例全都会被 Grade 之中的 _values 字典
所引用。于是，指向那些实例的引用数量，就永远不会降到0，这导致垃圾回收器没办法把那些实例清洗掉。
为了解决这个问题，需要使用 Python 内置的 weakref 模块。该模块里有一种特殊的字典，名为 WeakKeyDictionary。
其特殊之处在于：如果运行时系统发现，指向 Exam 实例的引用只剩一个，而这个引用又是由 WeakKeyDictionary 的键
所发起的，那么系统会将该引用从这个特殊的字典里删掉，于是指向那个 Exam 实例的引用数量就会降为0。总之，改用这种
字典来实现_values会让 Python 系统自动把内存泄露问题处理好，如果所有的 Exam 实例都不再使用了，那么_values字典
肯定是空的。
"""


class BetterGrade:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self

        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("Grade must be between 0 and 100")
        self._values[instance] = value


class Exam2:
    math_grade = BetterGrade()
    writing_grade = BetterGrade()
    science_grade = BetterGrade()


first_exam = Exam2()
first_exam.writing_grade = 82
second_exam = Exam2()
second_exam.writing_grade = 75
print(f"First {first_exam.writing_grade} is right")
print(f"Second {second_exam.writing_grade} is right")
