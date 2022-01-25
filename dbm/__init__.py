#!/user/bin/env python
# -*-coding:utf-8 -*-
# @CreateTime : 2021/10/29 8:36
# @Author :     xujiahui
# @Project :    robust_python
# @File :       __init__.py.py
# @Version :    V0.0.1
# @Desc :       ?


import os

import toml
from std_module.unpack_dict import UnpackDict

current_path = os.path.split(os.path.realpath(__file__))[0]
config_toml = toml.load(current_path + "/config.toml")
unpacked_config = UnpackDict(config_toml)


# ---------------------------------- 此处存放oracle数据库相关配置 ----------------------------------

# 本地2号机oracle数据库配置
ORACLE_HOST = unpacked_config['db_conf/oracle/local/oracle_host']
ORACLE_PORT = unpacked_config['db_conf/oracle/local/oracle_port']
ORACLE_USERNAME = unpacked_config['db_conf/oracle/local/oracle_username']
ORACLE_SID = unpacked_config['db_conf/oracle/local/oracle_sid']
ORACLE_SERVICE_NAME = unpacked_config['db_conf/oracle/local/oracle_service_name']
ORACLE_PASSWORD = unpacked_config['db_conf/oracle/local/oracle_password']
