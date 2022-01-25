#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2022/1/25 9:19
# @Author :     xujiahui
# @Project :    robust_python
# @File :       try_aio_2nd.py
# @Version :    V0.0.1
# @Desc :       io密集型

import time
import asyncio
import concurrent.futures


# 声明一个阻塞型任务
def blocked_task():
    for i in range(10):
        # 为了简化代码逻辑，便于更清晰地认识混合执行阻塞与非阻塞（异步）代码，
        # 使用time.sleep函数来模拟阻塞型IO逻辑的执行效果
        time.sleep(1)
        print(f"[{time.strftime('%X')}] Blocked task {i}")


# 声明一个异步任务
async def async_task():
    for i in range(2):
        await asyncio.sleep(5)
        print(f"[{time.strftime('%X')}] Async task {i}")


async def main():
    # 创建一个线程池执行器，该执行器所允许的最大线程数是5
    executor = concurrent.futures.ThreadPoolExecutor(max_workers = 5)
    
    # 获取当前正在运行的事件循环对象
    current_running_loop = asyncio.get_running_loop()
    
    # 并发执行一个阻塞型任务和一个异步任务
    await asyncio.gather(
        # 通过函数 run_in_executor 可以让指定的函数运行在特定的执行器(Executor)中，
        # 例如线程池执行器(concurrent.futures.ThreadPoolExecutor) 或者
        # 进程执行器(concurrent.futures.ProcessPoolExecutor)
        current_running_loop.run_in_executor(executor=executor, func=blocked_task),
        async_task()
    )
    

if __name__ == "__main__":
    asyncio.run(main())
