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
from download_ei import deal_ei


def download_data(user_info, time_s, time_n, time_n_C, year):
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
            "timeRange": "[" + time_s +","+ time_n_C + "]",
            'dataFormat' : 'json',
            'pwd'        : str(passwd),
            
        }

    station_nums = CMADAAS(            
                post_data,
                url=url,
                save=os.path.join(out_path, 'output', time_n.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/")),
                keywords=None,
                year = year,
                timeout=600).text()
    f.close()
    product_name = '全球陆地小时值整合数据集(V3.0)产品'
    deal_ei(os.path.join(out_path, 'output', time_n.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/")), time_n_C, product_name, station_nums)

def write_namelist_input(time_n, year, input_rd):
    input_file = '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/namelist_input.txt'
    outpath = os.path.join('/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/output',  time_n.strftime("%Y/%Y%m/%Y%m%d/%H/"))
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    f = open(input_file, 'r')
    content = f.readlines()
    content[1] = f"input_path='{input_rd}',\n"
    content[2] = f"output_path='{outpath}',\n"
    content[3] = f"stationlist='/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/filename_{year}.TXT',\n"
    content[4] = f"iby={year}\n"
    content[5] = f"iey={year}\n"
    f.close()
    with open(input_file, 'w', encoding='utf-8') as f_n:
        f_n.write(''.join(content))

def hebing(time_n, day, num, pros):
    time_s = time_n - datetime.timedelta(days=day)
    year = time_n.strftime("%Y")
    saves = []
    for i in range(num):
        time_n_i = time_s + datetime.timedelta(hours=5*(i+1) + i)
        save=os.path.join(out_path, 'output', time_n_i.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/"))
        saves.append(save)
    if pros == 'appoint' or pros == 'offsetHour':
        time_nc = time_n - datetime.timedelta(hours=1)
    elif pros == 'offsetDay':
        time_nc = time_n + datetime.timedelta(hours=23)
    for filename in os.listdir(saves[0]):
        saves_files = []
        for save_path in saves:
            if os.path.exists(save_path + '/' + filename):
                saves_files.append(save_path + '/' + filename)
        input_folder = '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/input/'+time_nc.strftime("%Y/%Y%m/%Y%m%d/%H/")+ '/' + year + '/'
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        f=open(input_folder+filename,'w')
        #先遍历文件名
        for filepath in saves_files:
            #遍历单个文件，读取行数
            for line in open(filepath):
                f.writelines(line)
        #关闭文件
        f.close()
        folder = f'/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/filename_{year}.TXT'

        if os.path.exists(folder):
            with open(folder, 'a+') as f:
                f.write(filename + '\n')
        else:
            with open(folder, 'w') as f:
                f.write(filename + '\n')

    write_namelist_input(time_nc, year, '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/QC/input/'+ time_nc.strftime("%Y/%Y%m/%Y%m%d/%H/"))

def process(pairs):
    download_data(pairs[0], pairs[1], pairs[2], pairs[3], pairs[4])

def download_batch(time_n, day, num, user_info):
    time_s = time_n - datetime.timedelta(days=day)
    pairs = []
    for i in range(num):
        time_s_i = (time_s + datetime.timedelta(hours=5*i + i)).strftime('%Y%m%d%H') + '0000'
        time_n_i = time_s + datetime.timedelta(hours=5*(i+1) + i)
        time_n_C_i = time_n_i.strftime('%Y%m%d%H') + '0000'
        year = time_n_C_i[0:4]
        pairs.append((user_info, time_s_i, time_n_i, time_n_C_i, year))
    p = Pool(4)
    tqdm.tqdm(p.imap(process,pairs),total=len(pairs),desc='process file:')
    p.close()
    p.join()
     
   
def get_json_info(pros, parse_time):
    user_info = get_user_info("database")
    # if parse_time == "":
    #     time_n = datetime.datetime.now()
    #     download_batch(time_n, 1, 4, user_info)
    #     hebing(time_n, out_path, 1, 4)
    if pros == 'offsetHour':
        time_n = datetime.datetime.now() - datetime.timedelta(hours=abs(int(parse_time)))
        time_n = time_n + datetime.timedelta(hours=1)
        download_batch(time_n, 1, 4, user_info)
        hebing(time_n, 1, 4, 'offsetHour')
    if pros == 'offsetDay':
        start = time.time()
        time_n = datetime.datetime.now()
        time_n = time_n - datetime.timedelta(days=abs(int(parse_time)))
        time_n = datetime.datetime.strftime(time_n, "%Y%m%d")
        time_n = datetime.datetime.strptime(time_n, "%Y%m%d")
        download_batch(time_n, 4, 20, user_info)
        end = time.time()
        hebing(time_n, 4, 20, 'offsetDay')
        print(end-start)
    elif pros == "appoint":
        time_n = datetime.datetime.strptime(parse_time, "%Y%m%d%H%M%S")
        time_n = time_n + datetime.timedelta(hours=1)
        download_batch(time_n, 1, 4, user_info)
        hebing(time_n, 1, 4, 'appoint')
        
if __name__ == '__main__':
    # out_path = os.getcwd()
    if len(sys.argv) >= 3:
        input_1 = sys.argv[1]
        input_2 = sys.argv[2]
    else:
        input_1 = ""
        input_2 = ""
    get_json_info(input_1, input_2)



    

