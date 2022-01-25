#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2022/1/25 10:02
# @Author :     xujiahui
# @Project :    robust_python
# @File :       try_aio_3th.py
# @Version :    V0.0.1
# @Desc :       文件异步IO

import asyncio
import concurrent.futures


async def main():
    # 获取事件循环
    loop = asyncio.get_running_loop()
    # 将阻塞型IO的 open 函数运行在线程池执行器中
    # 以写入字符串的方式打开文件 data.txt
    f = await loop.run_in_executor(concurrent.futures.ThreadPoolExecutor(), open, "../data/data.txt", "w+")
    # 将数据写入文件中
    await loop.run_in_executor(concurrent.futures.ThreadPoolExecutor(), f.write, "aio file")
    # 关闭文件
    await loop.run_in_executor(concurrent.futures.ThreadPoolExecutor(), f.close)


if __name__ == "__main__":
    asyncio.run(main())
