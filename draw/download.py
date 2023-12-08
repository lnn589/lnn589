import json
import os
import sys
import time
import datetime
from config import url, all_file_path, out_path
from _CMADAAS import get_user_info, CMADAAS
import pandas as pd
import tqdm
from multiprocessing import Pool


def download_data(user_info, time_s, time_n):
    f = open(out_path + '/' + 'test.json','r',encoding='utf-8')
    m = json.load(f)
    userId = user_info["user"]
    passwd = user_info["password"]
    post_data = {
            'serviceNodeId': 'NMIC_MUSIC_CMADAAS',
            'userId'     : userId,
            'interfaceId': m['interface'],
            'dataCode'   : m['dataCode'], 
            'elements'   : m['elements'],
            "timeRange": "[" + time_s +","+ time_n + "]",
            'dataFormat' : 'json',
            'pwd'        : str(passwd),
            
        }

    reslut = CMADAAS(            
                post_data,
                url=url,
                save=os.path.join(out_path, 'output'),
                keywords=None,
                timeout=600).text()
    f.close()
     
   
def get_json_info(pros, parse_time):
    user_info = get_user_info("database")
    if pros == 'replenish':
        start = time.time()
        time_n = datetime.datetime.strptime(parse_time, "%Y%m%d")
    elif pros == "appoint":
        time_n = datetime.datetime.strptime(parse_time, "%Y%m%d%H%M%S")
        time_s = time_n - datetime.timedelta(hours=12)
        time_n = datetime.datetime.strftime(time_n, "%Y%m%d%H%M%S")
        time_s = datetime.datetime.strftime(time_s, "%Y%m%d%H%M%S")
        download_data(user_info, time_s, time_n)
        
if __name__ == '__main__':
    # out_path = os.getcwd()
    if len(sys.argv) >= 3:
        input_1 = sys.argv[1]
        input_2 = sys.argv[2]
    else:
        input_1 = ""
        input_2 = ""
    get_json_info(input_1, input_2)



    

