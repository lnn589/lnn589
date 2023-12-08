import os
import datetime
import glob
import sys
import pandas as pd
import tqdm
from multiprocessing import Pool
from test import main


def data_deal(tt, files, t_path):
    data = []
    for file_name in files:
        try:
            f = open(file_name)
            content = f.readlines()
            for con in content:
                content_list = con.split(' ')
                year= tt[0:4]
                mon = tt[4:6]
                day = tt[6:8]
                hour = tt[8:10]
                min = tt[10:12]
                if content_list[0] == year and content_list[7] == mon and content_list[16] == day and content_list[25] == hour and content_list[34] == min:
                    con_list = [con[55:61], con[945:951].strip(), con[76:85].strip(), con[65:74].strip(), con[131:140].strip(), con[142:151].strip(), con[153:162].strip(), con[164:173].strip(), con[186:195].strip(), con[252:261].strip(), con[274:283].strip(), con[285:294].strip(), con[307:316].strip(), con[340:349].strip()]
                    data.append(con_list)
            f.close()
        except:
            print(file_name)
    df = pd.DataFrame(data,columns=['Station_Id_C','V_TYPE_REPORT','Lon','Lat','WIN_D','WIN_S','TEM', 'DPT', 'PRS','PRE_1h','PRE_3h','PRE_6h','PRE_12h','PRE_24h'])
    outpath = '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/input/'+ t_path
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    df.to_csv(outpath + tt[0:12]+'.csv',index=0)

def process(pairs):
    data_deal(pairs[0], pairs[1], pairs[2])

def select_time(Process, ts, t):
    if Process == 'appoint':
        time_t = datetime.datetime.strptime(ts, "%Y%m%d%H%M%S")
        path = os.path.join('/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/QC/output',  time_t.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/"))
        files = glob.glob(path +'*.TXT')
        time_s = time_t - datetime.timedelta(days=1)
        pairs = []
        for i in range(1,25):
            time_i = time_s + datetime.timedelta(hours=i)
            ts = time_i.strftime('%Y%m%d%H%M%S')
            # data_deal(ts, files, time_t.strftime("%Y/%Y%m/%Y%m%d/%H/"))
            pairs.append((ts, files, time_t.strftime("%Y/%Y%m/%Y%m%d/%H/")))
        p = Pool(4)
        tqdm.tqdm(p.imap(process,pairs),total=len(pairs),desc='process file:')
        p.close()
        p.join()
        main('/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/input/'+  time_t.strftime("%Y/%Y%m/%Y%m%d/%H/"), time_t.strftime("%Y/%Y%m/%Y%m%d/%H/"), time_t.strftime("%Y%m%d%H"))
        
    elif Process == 'offsetDay':
        time_t = datetime.datetime.strptime(t, "%Y%m%d%H%M%S")
        time_n = time_t - datetime.timedelta(days=abs(int(ts)))
        ts = time_n.strftime('%Y%m%d') + '230000'
        ts_date = datetime.datetime.strptime(ts, "%Y%m%d%H%M%S")
        path = os.path.join('/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/QC/output',  ts_date.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/"))
        files = glob.glob(path +'*.TXT')
        pairs = []
        for i in range(24):
            if i < 10:
                tt = ts + '0' +  str(i) + '0000'
            else:
                tt = ts + str(i) + '0000'
            pairs.append((tt, files, ts_date.strftime("%Y/%Y%m/%Y%m%d/%H/")))
        p = Pool(4)
        tqdm.tqdm(p.imap(process,pairs),total=len(pairs),desc='process file:')
        p.close()
        p.join()
        main('/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/input/'+  ts_date.strftime("%Y/%Y%m/%Y%m%d/%H/"), ts_date.strftime("%Y/%Y%m/%Y%m%d/%H/"), ts_date.strftime("%Y%m%d%H"))
    elif Process == 'offsetHour':
        time_t = datetime.datetime.strptime(t, "%Y%m%d%H%M%S")
        time_n = time_t - datetime.timedelta(hours=abs(int(ts)))
        path = os.path.join('/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/QC/output',  time_n.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/"))
        files = glob.glob(path +'*.TXT')
        time_s = time_n - datetime.timedelta(days=1)
        pairs = []
        for i in range(1,25):
            time_i = time_s + datetime.timedelta(hours=i)
            ts = time_i.strftime('%Y%m%d%H%M%S')
            pairs.append((ts, files, time_n.strftime("%Y/%Y%m/%Y%m%d/%H/")))
        p = Pool(4)
        tqdm.tqdm(p.imap(process,pairs),total=len(pairs),desc='process file:')
        p.close()
        p.join()
        main('/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/input/'+  time_n.strftime("%Y/%Y%m/%Y%m%d/%H/"), time_n.strftime("%Y/%Y%m/%Y%m%d/%H/"), time_n.strftime("%Y%m%d%H"))


if __name__ == '__main__':
    select_time(sys.argv[1], sys.argv[2], sys.argv[3])
    # data_deal(['20230316190000'])