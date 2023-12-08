import configparser
import json
import os
from datetime import datetime
from functools import lru_cache
import socket
import requests
import yaml
from const import config_dirname, monitorConfigPath

ConfigName = "info.json"

config_file_name = 'config.yaml'

# 北京时转换成时间时
def BJT2UTC(ibjt):
    ibjt = str(ibjt)
    iutc = datetime.strptime(ibjt, "%Y-%m-%d %H:%M:%S")
    iutc = datetime.strftime(iutc, "%Y-%m-%d %H:%M") + ':00'
    return iutc

@lru_cache()
def read_info_file(filename):
    with open(filename, 'rb') as f:
        return json.load(f)


def read_default_di():
    filename = os.path.join(config_dirname, ConfigName)
    cfg = read_info_file(filename)
    return cfg.get("data_info")


def read_default_ei():
    filename = os.path.join(config_dirname, ConfigName)
    cfg = read_info_file(filename)
    return cfg.get("errors_info")


def get_millisecond_timestamp(t: datetime = None):
    if t:
        return int(t.timestamp() * 1000)
    return int(datetime.now().timestamp() * 1000)


def load_default_di(product_time: datetime, DATA_TIME, PROCESS_START_TIME, PROCESS_END_TIME, FILE_SIZE, PROCESS_STATE, BUSINESS_STATE, FILE_NAME_O, FILE_NAME_N):
    """
    PROCESS_START_TIME: "${质控程序开始运行时间}"
    PROCESS_END_TIME: "${质控程序结束运行时间}"
    FILE_SIZE: "${读取生成文件大小，放这儿}" 生成结果为文件的，文件大小（单位为B），多个之间以','间隔
    PROCESS_STATE: "根据实际生成文件数量决定"
    """
    data = read_default_di()
    product_time = datetime.strptime(product_time, "%Y-%m-%d %H:%M:%S")
    data["occur_time"] = get_millisecond_timestamp(product_time)
    data["fields"]["DATA_TIME"] = DATA_TIME
    data["fields"]["FILE_NAME"] = FILE_NAME_N
    data["fields"]["PROCESS_START_TIME"] = PROCESS_START_TIME
    data["fields"]["PROCESS_END_TIME"] = PROCESS_END_TIME
    data["fields"]["FILE_SIZE"] = FILE_SIZE
    data["fields"]["PROCESS_STATE"] = PROCESS_STATE
    data["fields"]["BUSINESS_STATE"] = BUSINESS_STATE
    data["fields"]["FILE_NAME_O"] = FILE_NAME_O
    data["fields"]["FILE_NAME_N"] = FILE_NAME_N
    data["fields"]["RECORD_TIME"] = str(data["occur_time"])
    # data1=json.dumps(data, ensure_ascii=False)
    # with open('di_data.json', 'w') as json_file:
    #     json_file.write(data1)
    return data


def load_default_ei(GROUP_ID, EVENT_TYPE, KEvent, KResult, ORG_TIME, EVENT_TITLE, EVENT_EXT1):
    data = read_default_ei()
    now = datetime.now()
    data["occur_time"] = get_millisecond_timestamp(now)
    data["fields"]["ORG_TIME"] = ORG_TIME
    data["fields"]["EVENT_TIME"] = now.strftime("%Y-%m-%d %H:%M:%S")
    data["fields"]["GROUP_ID"] = GROUP_ID
    data["fields"]["EVENT_TYPE"] = EVENT_TYPE
    data["fields"]["KEvent"] = KEvent
    data["fields"]["KResult"] = KResult
    filename = os.path.join(config_dirname, config_file_name)
    with open(filename, "rb") as fp:
        cfg = yaml.load(fp, yaml.FullLoader)
    data["fields"]["EVENT_TITLE"] = '加工流水线产品质量异常：任务名称：' + cfg.get('TASK_NAME') + ' 环节名称：'+ EVENT_TITLE + ',产品名称：' + cfg.get('PRODUCT_NAME')
    data["fields"]["EVENT_EXT1"] = EVENT_EXT1
    data["fields"]["EVENT_EXT2"] = ''
    # print(data)
    # data1=json.dumps(data, ensure_ascii=False)
    # with open('ei_data.json', 'w') as json_file:
    #     json_file.write(data1)
    return data


@lru_cache()
def read_env_properties():
    section_header = "[env]"
    data = [section_header, "\n"]
    file_congfig = os.path.join(config_dirname, config_file_name)
    with open(file_congfig, "rb") as fp:
        cfg = yaml.load(fp, yaml.FullLoader)
    if cfg.get('SEND_DI_EI_ADDRESS_FLAG') == 1:
        filename = monitorConfigPath
    else:
        filename = cfg.get('MONITOR_CONFIG_PATH')
    print(filename)
    with open(filename, "r") as f:
        for line in f:
            data.append(line)
    data = "".join(data)

    config_parser = configparser.ConfigParser()
    config_parser.read_string(data)
    return config_parser


def get_value_from_env_properties(key):
    config_parser = read_env_properties()
    return config_parser.get("env", key)


def get_ei_url():
    return get_value_from_env_properties("monitor.ei.single.url")


def get_di_url():
    return get_value_from_env_properties("monitor.di.single.url")


def send_info(url, data: dict):
   
    # 1、增加重试连接次数
    requests.DEFAULT_RETRIES = 5
    s = requests.session()
    # 2、关闭多余的连接
    s.keep_alive = False
    header = {'content-type': "application/json"}
    return s.post(url, data=json.dumps(data), headers=header)


def send_error_info(data):
    return send_info(get_ei_url(), data)


def send_data_info(data):
    return send_info(get_di_url(), data)
