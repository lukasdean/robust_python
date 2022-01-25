#!/user/bin/env python
# -*-coding:utf-8 -*-
# ******************************************************************************
# **  创建者:   chenchen
# **  创建日期: 2019/12/11
# **  修改日志:
# **  修改日期:
# ** ---------------------------------------------------------------
# **
# ** ---------------------------------------------------------------
# **
# **  日期、时间工具模块
# *******************************************************************************
import calendar
import datetime
import math
import sys
import time
from datetime import timedelta
from functools import wraps

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule


FORMAT_BASE = "%Y-%m-%d %H:%M:%S"
FORMAT_BASE_12 = "%Y-%m-%d %I:%M:%S"
FORMAT_YYYYMMDD = "%Y%m%d"
FORMAT_YYYY_MM_DD = "%Y-%m-%d"
FORMAT_YYYYMM = "%Y%m"
FORMAT_YYYY_MM = "%Y-%m"


# -------------------------------------------- 历史遗留函数 --------------------------------------------


def get_ndays_away_from_date(allotted_day: str, num: int):
    """
    get_days_away_from_date函数的原始版本，根据传入日期和天数返回指定计算后的日期
    Args:
        allotted_day: 传入日期
        num: 将要进行计算的日期数
    Returns:
        yyyymmdd格式的日期字符串
    """

    return get_days_away_from_date(allotted_day, num)


def get_last_month(base_day):
    """
    根据传入日期获取上个月月份
    Args:
        base_day: 传入日期
    Returns:
        yyyymm格式月字符串
    """

    return get_months_away_from_date(base_day, -1)


def get_n_pre_day(base_day, n_days):
    """
    根据传入日期和天数获取n天前日期
    Args:
        base_day: 传入日期
        n_days: 将要进行计算的日期数
    Returns:
        yyyymm格式月字符串
    """

    return get_days_away_from_date(base_day, -abs(n_days))


# -------------------------------------------- 后续新增函数 --------------------------------------------

# ***************************************************************************************************
# 函数作用:
#   根据提供的时间元组获取下n日或上n日时间元组,可传参days设定想要获取多少天的日期，正数向后取,负数向前取时间，不传默认取下一日
# 输入参数:
#   start datetime类型
# 返回数据:
#   n_pre_month timedelta类型
# 作者:
#   徐嘉辉
# 日期:
#   2020/04/30
# ***************************************************************************************************
def gen_date_tuple(start, days=1):
    day = timedelta(1)

    for i in range(days):
        yield start + day * i


# ***************************************************************************************************
# 函数作用:
#   根据提供的起始日期生成中间的日期列表, end_date参数为.时取当前系统时间
# 输入参数:
#   start_date string类型, YYYYMMDD格式
#   end_date string类型, YYYYMMDD格式
# 返回数据:
#   date_list list类型, 形如['20200305','20200306']
# 作者:
#   徐嘉辉
# 日期:
#   2020/04/30
# ***************************************************************************************************
def gen_date_list(start_date, end_date):
    start = datetime.datetime.strptime(start_date, "%Y%m%d")

    if end_date == ".":
        end = datetime.datetime.now()
    else:
        end = datetime.datetime.strptime(end_date, "%Y%m%d")

    date_list = []

    for d in gen_date_tuple(start, ((end - start).days + 1)):
        date_list.append(d.strftime("%Y%m%d"))

    return date_list


# ***************************************************************************************************
# 函数作用:
#   根据提供的日期获取该日期上个月的月末日期
# 输入参数:
#   allotted_day string类型,形如20200518
# 返回数据:
#   last_date string类型,形如20200518
# 作者:
#   徐嘉辉
# 日期:
#   2020/05/18
# ***************************************************************************************************
def get_last_day_of_pre_month(allotted_day: str):
    """
    get_last_day_of_pre_month:
        :param allotted_day:指定日期(str),形如20200518
        :return: 返回last_date(str),形如20200518
    """

    allotted_date = datetime.datetime.strptime(allotted_day, "%Y%m%d")
    # 首先获取指定日期所在月份的第一天，然后往回减一天就得到上月最后一天
    last_date_of_month = datetime.datetime(
        allotted_date.year, allotted_date.month, 1
    ) + relativedelta(months=0, days=-1)
    # 将datetime解析为YYYYMMDD格式的日期字符串
    last_date = last_date_of_month.strftime("%Y%m%d")[:10]

    return last_date


# ***************************************************************************************************
# 函数作用:
#   根据提供的日期获取该日期前或者后n日日期
# 输入参数:
#   allotted_day string类型,形如20200518
#   num int类型,形如1或者-1
# 返回数据:
#   the_day_i_want string类型,形如20200517或者20200519
# 作者:
#   徐嘉辉
# 日期:
#   2020/05/24
# ***************************************************************************************************
def get_days_away_from_date(allotted_day: str, num: int):
    """
        get_days_away_from_date:
            :param allotted_day:指定日期(str),形如20200518
            :param num:指定时间间隔(int),形如1或者-1
            :return: the_day_i_want:输入日期的前或者后n日日期(str),形如20200517或者20200519
    """

    allotted_date = datetime.datetime.strptime(allotted_day, "%Y%m%d")
    the_day_i_want = allotted_date + datetime.timedelta(days=num)
    return the_day_i_want.strftime(FORMAT_YYYYMMDD)


def get_months_away_from_date(given_date: str, mon_cnt: int):
    """
    根据提供的日期获取该日期所在月份前或者后n = |mon_cnt| 个月的月份
    @日期: 2021/02/03
    @作者: 徐嘉辉
    :param given_date: 给定日期(str),形如20200518
    :param mon_cnt: 指定时间间隔(int),形如1 或者 -1(当然如果你愿意,0也是可以传入的)
    :return: 格式化后的月份字符串
    """

    # 解析指定日期为datetime对象
    given_month = datetime.datetime.strptime(given_date[0:6], "%Y%m")
    back_month = (given_month + relativedelta(months=mon_cnt)).strftime("%Y%m")

    return back_month


def get_years_away_from_date(given_date: str, year_cnt: int):
    """
    根据提供的日期获取该日期所在年份前或者后n = |year_cnt| 年的年份
    @日期: 2021/02/03
    @作者: 徐嘉辉
    :param given_date: 给定日期(str),形如20200518
    :param year_cnt: 指定时间间隔(int),形如1 或者 -1(当然如果你愿意,0也是可以传入的)
    :return: 格式化后的年份字符串
    """

    # 解析指定日期为datetime对象
    given_year = datetime.datetime.strptime(given_date[0:4], "%Y")
    back_year = (given_year + relativedelta(years=year_cnt)).strftime("%Y")

    return back_year


def get_week_with_first_thursday(date_param: str):
    """
    基于国标自然周的判断标准
    根据传入日期获取当前为自然年第几周
    注意！！！任何处理都应当基于下述假设前提
    根据中华人民共和国国家标准GB/T 7408-2005《数据元和交换格式信息交换日期和时间表示法》中4.3.3.2部分
    即一年中的第一个 日历星期包括该年的第一个星期四，
    并且日历年的最后一个日历星期就是在下一个日历年的第一个日历星期之前的那个星期，
    日历星期数是其在该年中的顺序。
    例如20210101是周五，因此属于2020年的最后一周,而20210104才是2021年的第一周
    @日期: 2021/02/03
    @作者: 徐嘉辉
    @更新日志:
            2021/03/04 修改注释和函数名
    :param date_param: 给定日期
    :return: 当前日期按上述标准属于哪一年(str),如2020或者2021等
             当前日期为该年份第几周(str),如53或者01等
    """

    given_date = datetime.datetime.strptime(date_param, "%Y%m%d")
    year_of_this_week = str(given_date.isocalendar()[0])
    pre_this_week_in_year = given_date.isocalendar()[1]
    this_week_in_year = str(pre_this_week_in_year).zfill(2)

    return year_of_this_week, this_week_in_year


def nature_week_decorator(func):
    """
    定义一个返回自然周周次以及该周次所属自然年的装饰器
    :param func: 将要使用的某个标准的自然周计算函数
    :return:
    @日期: 2021/03/04
    @作者: 徐嘉辉
    """

    # 定义一个包含自然周计算方式的字典
    week_func_dict = {
        # 包含第一个周四为当年首个自然周
        "first_thursday": get_week_with_first_thursday,
    }

    @wraps(func)
    def get_week_with_specific_standard(*args):
        # 调用具体某个标准的自然周计算函数
        return week_func_dict["first_thursday"](*args)

    return get_week_with_specific_standard


@nature_week_decorator
def get_nature_week(date_param: str):
    """
    统一对外提供的根据指定格式日期返回自然周以及该自然周所属年份的函数
    :param date_param: yyyymmdd格式的日期字符串
    :return: 自然周所属年份(str), 自然周周次(str)
    @日期: 2021/03/04
    @作者: 徐嘉辉
    """

    pass


# ***************************************************************************************************
# 函数作用:
#          根据日期返回第几季度
# 输入参数:
#   day_param string类型,形如20200518或202005
# 返回数据:
#   get_quarter_in_year string类型,形如第一季度
# 作者:
#   张运锋
# 日期:
#   2020/05/24
# ***************************************************************************************************
def get_quarter_in_year(date_param: str):
    """
    :param date_param: 给定日期
    :return: 当前日期为本年第几季度
    """

    data_quarter = ""
    if len(date_param) >= 6:
        mon = date_param[4:5]
    else:
        return ""
    if mon in ("01", "02", "03"):
        data_quarter = "第一季度"
    elif mon in ("04", "05", "06"):
        data_quarter = "第二季度"
    elif mon in ("07", "08", "09"):
        data_quarter = "第三季度"
    elif mon in ("10", "11", "12"):
        data_quarter = "第四季度"

    return data_quarter


def format_mill_time_stamp(time_stamp: int):
    """
    将毫秒级时间戳转换为常用可读的时间格式字符串 形如：2020-12-29 14:15:56.514000
    @日期: 2020/12/29
    @作者: 徐嘉辉
    :param time_stamp: 毫秒级时间戳
    :return:
    """

    datetime_obj = datetime.datetime.fromtimestamp(time_stamp / 1000)

    # 转换成新的时间格式(精确到毫秒)
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")


def get_years_from_date(given_day: str, count_num: int):
    """
    根据指定的日期和数值计算并返回包含该日期所在年份的前或者后n年的年份元组
    @日期: 2021/01/11
    @作者: 徐嘉辉
    :param given_day: 标准yyyymmdd格式日期字符串，如20210111
    :param count_num: 需要计算的年份数量，如-2或者3等
    :return: 一个包含前或者后n年年份的元组，如('2021', '2020', '2019')
    """

    given_year = datetime.datetime.strptime(given_day[0:4], "%Y")
    time_tuple = ()
    for i in range(min(0, count_num), max(0, count_num) + 1):
        return_year = (given_year + relativedelta(years=i)).strftime("%Y")
        time_tuple = time_tuple + (return_year,)

    return time_tuple


def format_str2time_stamp(time_str: str):
    """
    将字符串转换为unix时间戳
    @日期: 2021/02/01
    @作者: 徐嘉辉
    :param time_str: 时间字符串，如 2021-02-01 10:30:10.269000
    :return:
    """

    time_stamp = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

    return time_stamp


def get_head_nature_date(nature_year: str):
    """
    根据传入自然年的年份获取该自然年第一自然周第一天的日期
    @日期: 2021/05/07
    @作者: 徐嘉辉
    Args:
        nature_year: 自然年字符串，形如2020

    Returns:
        yyyymmdd格式的自然年第一自然周第一天的日期
    """

    """
        判断本年度1月1日属于哪个自然年，若属于上一年则判断1.1是星期几，
        得到本年度第一自然周第一天为(周一为1 周日为7) 1.1 加上 7-(1.1所属星期几)+1 天
        若属于本自然年，得到本年度第一自然周第一天为(周一为1 周日为7) 1.1 减去 (1.1所属星期几)-1 天
    """
    first_date = nature_year + '0101'

    belong_year, belong_week = get_nature_week(first_date)

    # 本年度1月1日属于本自然年，返回本年度第一自然周第一天为(周一为1 周日为7) 1.1 减去 (1.1所属星期几)-1 天
    if belong_year == nature_year:
        datetime_obj = datetime.datetime.strptime(first_date, '%Y%m%d')
        day_of_first_date = datetime_obj.isoweekday()
        back_date = datetime_obj - datetime.timedelta(days = day_of_first_date-1)

        return back_date.strftime('%Y%m%d')
    else:
        # 本年度1月1日属于上一自然年，返回本年度第一自然周第一天为(周一为1 周日为7) 1.1 加上 7-(1.1所属星期几)+1 天
        datetime_obj = datetime.datetime.strptime(first_date, '%Y%m%d')
        day_of_first_date = datetime_obj.isoweekday()
        back_date = datetime_obj + datetime.timedelta(days = 7-day_of_first_date+1)

        return back_date.strftime('%Y%m%d')


def get_tail_nature_date(nature_year: str):
    """
    根据传入自然年的年份获取该自然年最后自然周最后一天的日期
    @日期: 2021/05/07
    @作者: 徐嘉辉
    Args:
        nature_year: 自然年字符串，形如2020

    Returns:
        yyyymmdd格式的自然年最后自然周最后一天的日期
    """

    """
        判断本年度12月31日属于哪个自然年，若属于本年度则判断12.31的自然周，得到本年度最后一个自然周的周次，
        而本年度最后自然周最后一天为(周一为1 周日为7) 12.31 加上 7-(12.31所属星期几) 天
        若属于下一年，则本年度最后自然周最后一天为(周一为1 周日为7) 12.31 减去 12.31所属星期几 天
        对应最后一周周次则通过该最后一天所属周次获得
    """
    last_date = nature_year + '1231'

    belong_year, belong_week = get_nature_week(last_date)

    # 本年度12月31日属于本自然年，返回本年度最后一个自然周的周次以及
    # 最后自然周最后一天 为(周一为1 周日为7) 12.31 加上 7-(12.31所属星期几) 天
    if belong_year == nature_year:
        datetime_obj = datetime.datetime.strptime(last_date, '%Y%m%d')
        day_of_last_date = datetime_obj.isoweekday()
        back_date = datetime_obj + datetime.timedelta(days = 7-day_of_last_date)

        return belong_week, back_date.strftime('%Y%m%d')
    else:
        # 本年度12月31日属于下一自然年，返回本年度最后一个自然周的周次以及
        # 最后自然周最后一天 为(周一为1 周日为7) 12.31 减去 12.31所属星期几 天
        datetime_obj = datetime.datetime.strptime(last_date, '%Y%m%d')
        day_of_last_date = datetime_obj.isoweekday()
        back_date = datetime_obj - datetime.timedelta(days = day_of_last_date)

        return get_nature_week(back_date.strftime('%Y%m%d'))[1], back_date.strftime('%Y%m%d')


def gen_dates_from_nature_week(nature_week: str):
    """
    根据传入的自然周周次生成该周次每一天的日期字符串(yyyymmmdd格式)
    @日期: 2021/05/07
    @作者: 徐嘉辉
    Args:
        nature_week: 自然周字符串，形如202001

    Returns:
        一个包含自然周七天日期的迭代器
    """

    # 输入自然周字符串长度检查
    assert len(nature_week) == 6, '输入周次字符串长度不合法！'

    # 截取自然年
    nature_year = nature_week[:4]
    # 截取自然周
    pure_nature_year = int(nature_week[4:])

    # 获取该自然周所属自然年的最后一个自然周以及该周次最后一天，判断传入周次是否合法
    last_week, tail_date = get_tail_nature_date(nature_year)

    # 自然周在自然年中存在性检查
    assert 1 <= pure_nature_year <= int(last_week), '输入周次不在对应自然年中！'

    # 获取所属自然年首个自然周的第一天
    head_date = get_head_nature_date(nature_year)

    # 传入周次为所属自然年第一自然周
    if pure_nature_year == 1:
        for i in range(0, 7):

            yield get_days_away_from_date(head_date, i)
    # 传入周次为所属自然年最后一个自然周
    if pure_nature_year == int(last_week):
        for i in range(6, -1, -1):

            yield get_days_away_from_date(tail_date, -i)
    # 传入周次为所属自然年第一自然周和最后一个自然周之间
    if 1 < pure_nature_year < int(last_week):
        # 基于第一周第一天 + (周次*7 - 1) 天，得到该周次最后一天，遍历输出总共七天的格式化日期字符串
        last_date_of_nature_week = get_days_away_from_date(head_date, pure_nature_year*7 - 1)
        for i in range(6, -1, -1):

            yield get_days_away_from_date(last_date_of_nature_week, -i)


def get_head_n_tail(time_param: str, week_flag: bool = False):
    """
    根据传入的时间字符串解析获得该时间范围的开始和结束日期
    当前支持年、月、周
    @日期: 2021/03/24
    @作者: 徐嘉辉
    Args:
        time_param: 格式为 yyyyww/yyyymm/yyyy 之一的字符串
        week_flag: 传入字符串是否是周次字符串，默认关闭，开启将会返回传入周次的首日和最后一日
    Returns:
        head, tail: 开始和结束日期
    """

    # 定义内部函数，根据指定年月解析日期为标准格式字符串
    def gen_head_n_tail(input_year: int, mon_tuple: tuple):

        # 获取月份的首日和最后一日
        _, tail_of_month = calendar.monthrange(input_year, mon_tuple[1])

        # 获取指定年月的首日和最后一日
        head_of_year = datetime.date(
            year=input_year, month=mon_tuple[0], day=1
        ).strftime("%Y%m%d")
        tail_of_year = datetime.date(
            year=input_year, month=mon_tuple[1], day=tail_of_month
        ).strftime("%Y%m%d")

        return head_of_year, tail_of_year

    if week_flag:
        # 传入时间类型为周次
        date_list = []
        for date in gen_dates_from_nature_week(time_param):
            date_list.append(date)

        return date_list[0], date_list[-1]

    if len(time_param) == 6:
        # 判断为月字符串
        head_mon = int(time_param[4:6])
        tail_mon = int(time_param[4:6])

        return gen_head_n_tail(int(time_param[0:4]), (head_mon, tail_mon))

    if len(time_param) == 4:
        # 判断为年字符串
        head_mon = 1
        tail_mon = 12

        return gen_head_n_tail(int(time_param), (head_mon, tail_mon))


def get_tech_week_at_sch(start_date_param: str, stop_date_param: str, date_param: str):
    """
    由于各高校校历时间不统一，现根据大部分高校校历安排，计算高校教学周次
    学校开学那天所在周次不安排教学任务，不算在第一周
    高校总周数组成：第一周为学术周或者准备周；第二周开始作为教学周第一周，其中包含两周为考试周
    例如大连海事大学校历：20210228为返校日，20210301开始上课，20210301为周一作为教学周第一周
    @日期: 2021/03/05
    @作者: 张运锋
    @更新日志:
    :param start_date_param: 给定学期开学日期,
           stop_date_param: 给定学期结束日期
           date_param: 需要计算周次的日期
    :return: 0: 学术周或者准备周
             -1：日期不在本学期内
    """

    start_date = ''
    given_date = ''
    stop_date = ''
    if type(start_date_param) is str:
        start_date = datetime.datetime.strptime(start_date_param, '%Y%m%d')
    elif type(start_date_param) is datetime.datetime:
        start_date = start_date_param
    if type(stop_date_param) is str:
        stop_date = datetime.datetime.strptime(stop_date_param, '%Y%m%d')
    elif type(stop_date_param) is datetime.datetime:
        start_date = stop_date_param
    if type(date_param) is str:
        given_date = datetime.datetime.strptime(date_param, '%Y%m%d')
    elif type(date_param) is datetime.datetime:
        given_date = date_param
    if (start_date <= given_date) & (given_date <= stop_date):
        tech_week = math.floor(((given_date - start_date).days + 1) / 7)
        return tech_week
    else:
        print('所给日期不在本学期！！')
        return -1


def get_week_day_from_date(given_day: str):
    """
    根据提供yyyymmdd格式日期字符串返回星期几
    @日期: 2021/05/25
    @作者: 徐嘉辉
    Args:
        given_day: 例如，20210525

    Returns:
        星期几，例如2指星期二(周一至周日对应于1-7)
    """

    return datetime.datetime.strptime(given_day, '%Y%m%d').isoweekday()


def get_mon_tail_with_date(date_in: str) -> str:
    """
    根据传入日期返回该日期所属月份的最后一天
    @日期: 2021/06/30
    @作者: 徐嘉辉
    Args:
        date_in: 输入日期字符串，应为yyyymmdd格式

    Returns:
        格式化的最后一日字符串
    """

    d = datetime.datetime.strptime(date_in, FORMAT_YYYYMMDD)
    mon_tail = datetime.datetime(d.year, d.month, calendar.monthrange(d.year, d.month)[1])

    return mon_tail.strftime(FORMAT_YYYYMMDD)

