import os
import sys
import datetime
sys.path.insert(0,"/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/")
from send_info import send_data_info, load_default_di, BJT2UTC


def deal_di(FILE_NAME_O, start_time, end_time, success_flag):
    FILE_SIZE = 0
    t = datetime.datetime.now()
    ibjt = str(t)[0:16] + ':00'
    iutc = BJT2UTC(ibjt)
    DATA_TIME = str(t)[0:16]
    PROCESS_START_TIME = start_time
    PROCESS_END_TIME = end_time
    FILE_NAME_N = ''
    if success_flag:
        PROCESS_STATE = '1'
        BUSINESS_STATE = '1'
    else:
        PROCESS_STATE = '0'
        BUSINESS_STATE = '0'
    di =load_default_di(iutc, DATA_TIME, PROCESS_START_TIME, PROCESS_END_TIME, FILE_SIZE, PROCESS_STATE, BUSINESS_STATE, FILE_NAME_O, FILE_NAME_N)
    res = send_data_info(di)
    print(res)