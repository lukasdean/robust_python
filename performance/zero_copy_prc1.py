#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/25 22:52
# @Author :     xujiahui
# @Project :    robust_python
# @File :       zero_copy_prc1.py
# @Version :    V0.0.1
# @Desc :       ?


# 借助于 memoryview 来实现零拷贝
import timeit

data = b"shave and a haircut, two bits"
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print("Size: ", chunk.nbytes)
print("Data in view: ", chunk.tobytes())
print("Underlying data: ", chunk.obj)

# bytes有个限制，就是只能读取不能修改，我们不能单独更新其中某个位置上的字节，而 bytearray 则相当于可修改的bytes，
# 它允许我们修改任意位置上面的内容，bytearray采用整数表示其中的内容，而不像 bytes 那样，采用b开头的字面值
my_array = bytearray(b'hello')
my_array[0] = 0x79
print(my_array)

"""
bytearray 与 bytes 一样，也可以用 memoryview 封装，在这种 memoryview 上面切割出来的对象，其内容可以用另一份数据替换，
这样做，替换的实际上是 memoryview 背后那个底层缓冲区里面的相应部分。这使得我们可以通过 memoryview 来修改它所封装的 bytearray，
而不像 bytes 那样，必须先将 bytes 拆散再拼起来
"""
my_array = bytearray(b'row, row, row your boat')
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'
print(my_array)

"""
Python 里面很多库之中的方法，例如 socket.recv_into 与 RawIOBase.readinto，都使用缓冲协议来迅速接受或读取数据。
这种方法的好处是不用分配内存，也不用给原数据制作副本，它们会把收到的内容直接写入现有的缓冲区。
"""

