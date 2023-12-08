import os
import sys
import time
import glob
sys.path.insert(0,"/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/")
from send_info import send_error_info, load_default_ei
def deal_ei(str5, befor_month, before_qc_num, after_qc_num):
    input_filepath = str5
    filemt = ''
    ORG_TIME = ''
    
    link_name = '全球陆地小时值数据质控'
    EVENT_TITLE = link_name

    EVENT_EXT1 = str(befor_month[0:4]) + '-' + str(befor_month[4:6]) + '-' +  str(befor_month[8:10]) +' '+str(befor_month[10:12]) +':00:00'
    files = glob.glob(input_filepath + '*.TXT')
    if after_qc_num>0:
        if before_qc_num > after_qc_num:
            filemt = time.localtime(os.stat(files[0]).st_mtime)
            ORG_TIME = time.strftime("%Y%m%dT%H%M%S", filemt)
            GROUP_ID = 'OP_DPL_A-04'
            EVENT_TYPE = 'OP_DPL_A-04-01-01'
            KEvent = f'产品质控异常：产品正常质控，但质控的产品文件数量异常, 质控文件实际数量为{after_qc_num}个，应下载的数据量{before_qc_num}'
            KResult = ''
            ei = load_default_ei(GROUP_ID, EVENT_TYPE, KEvent, KResult, ORG_TIME, EVENT_TITLE, EVENT_EXT1)
            send_error_info(ei)
    else:
        GROUP_ID = 'OP_DPL_A-03'
        EVENT_TYPE = 'OP_DPL_A-03-01-01'
        KEvent = '算法运行异常：算法运行成功，但未产生产品文件'
        KResult = '产品未生成，无法提供对外服务'
        ei = load_default_ei(GROUP_ID, EVENT_TYPE, KEvent, KResult, ORG_TIME, EVENT_TITLE, EVENT_EXT1)
        send_error_info(ei)