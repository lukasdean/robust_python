#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/24 21:39
# @Author :     xujiahui
# @Project :    robust_python
# @File :       better_pickle.py
# @Version :    V0.0.1
# @Desc :       更好地使用pickle


import copyreg
import pickle

"""
Python 内置的 pickle 模块非常简单易用，但是要注意这个模块设计之初就仅仅是为了做一件简单的事，
快速、轻松地把 Python 对象序列化成二进制数据，它使用的这种序列化格式本身就没有考虑过安全问题，
如果尝试直接使用这个模块来实现比这更复杂的需求，那么可能会看到奇怪的结果。
另外，由于 pickle 格式会把原有的 Python 对象记录下来，让系统可以在稍后予以重建，假如记录的
这个对象本身含有恶意行为，那么通过反序列化还原出来之后，就有可能破坏整个程序。
跟 pickle 不同，json 模块考虑到了安全问题。序列化之后的 JSON 数据表示的只不过是一套对象体系
而已，把这样的数据反序列化不会给程序带来风险。如果要在彼此不信任的两个人或两个程序之间传递数据，
那么应该使用 JSON 这样的格式。
更好的使用方式，是使用内置的 copyreg 模块解决。这个模块允许我们向系统注册相关的函数，把 Python
对象的序列化与反序列化操作交给那些函数去处理，这样的话，pickle 模块就运作得更加稳定了。
"""


class GameState:
    def __init__(self, level=1, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


def pickle_game_state(game_state):
    kwargs = game_state.__dict__

    return unpickle_game_state, (kwargs,)


def unpickle_game_state(kwargs):
    return GameState(**kwargs)


# 注册 pickle_game_state、unpickle_game_state 这两个函数，在使用 copyreg 注册时，
# 写到数据里的引入路径是 unpickle_game_state 函数，而不是 GameState 这样的类名，
# 因此 unpickle_game_state 所在模块的路径不能变，因为这个函数名已经写到了序列化之后的数据里，
# 将来反序列化的时候，系统要先找到这个函数，然后才能通过它正确地还原对象。
copyreg.pickle(GameState, pickle_game_state)

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)
