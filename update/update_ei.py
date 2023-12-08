import os
import sys
import time
import glob
sys.path.insert(0,"/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/")
from send_info import send_error_info, load_default_ei
def deal_ei(befor_month, ip, e):
    ORG_TIME = ''
    
    link_name = '全球陆地小时值数据质控'
    EVENT_TITLE = link_name

    EVENT_EXT1 = str(befor_month[0:4]) + '-' + str(befor_month[4:6]) + '-' +  str(befor_month[8:10]) +' '+str(befor_month[10:12]) +':00:00'

    GROUP_ID = 'OP_DPL_A-03'
    EVENT_TYPE = 'OP_DPL_A-03-01-01'
    KEvent = f'数据库异常： IP地址:{ip}，错误信息:{e}'
    KResult = '产品未生成，无法提供对外服务'
    ei = load_default_ei(GROUP_ID, EVENT_TYPE, KEvent, KResult, ORG_TIME, EVENT_TITLE, EVENT_EXT1)
    send_error_info(ei)