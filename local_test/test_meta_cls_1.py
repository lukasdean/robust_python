#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/11/10 22:50
# @Author :     xujiahui
# @Project :    robust_python
# @File :       test1.py
# @Version :    V0.0.1
# @Desc :       ?


class TestA:
    # def __init_subclass__(cls):
    #     super().__init_subclass__()
    
    def __init__(self, a):
        self.a = a


class TestA2(TestA):
    def __init__(self, a):
        super(TestA2, self).__init__(a)


class TestA3(TestA):
    def __init__(self, a):
        super(TestA3, self).__init__(a)
        

a1 = TestA2(1)
print("a1.a: ", a1.a)
a2 = TestA3(2)
print("a2.a: ", a2.a)
