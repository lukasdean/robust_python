#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/24 21:05
# @Author :     xujiahui
# @Project :    robust_python
# @File :       try_aio_1st.py
# @Version :    V0.0.1
# @Desc :       计算密集型

import time
import asyncio
import concurrent.futures

from numba import jit


@jit
def compute_pi():
    count = 100000
    part = 1.0 / count
    inside = 0.0
    for i in range(1, count):
        for j in range(1, count):
            x = part * i
            y = part * j
            if x * x + y * y <= 1:
                inside += 1
    pi = inside / (count * count) * 4
    
    return pi


async def print_pi(pool):
    print(f"[{time.strftime('%X')}] Started to compute PI")
    # 将圆周率计算（cpu密集型）的代码交给进程池执行器执行
    pi = await asyncio.get_running_loop().run_in_executor(
        pool,
        compute_pi
    )
    print(f"[{time.strftime('%X')}] {pi}")


async def task():
    for i in range(5):
        print(f"[{time.strftime('%X')}] Step {i}")
        await asyncio.sleep(1)


async def main():
    # 声明一个进程池执行对象
    pool = concurrent.futures.ProcessPoolExecutor()
    
    await asyncio.gather(
        # 将进程池对象 pool 传入 print_pi 函数，由 print_pi 函数执行 CPU 密集型代码逻辑，
        # 并且将 CPU 密集型代码与异步代码并行执行
        print_pi(pool),
        task()
    )


if __name__ == "__main__":
    # 这里定义的 if 代码块是必须的，只有在文件名为 __main__ 时才执行主程序，
    # 避免在创建子进程时重复运行主程序而产生错误
    asyncio.run(main())
