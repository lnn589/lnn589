import os
import datetime
import glob
import sys
from encry_db_music import con_xgdb
from update_ei import deal_ei
from update_di import deal_di

def update_into_info(data, ts_date, file_names, start_time):
    try:
        conn, cur, ip = con_xgdb()
        sql = "UPDATE USR_SOD.SURF_WEA_GLB_MUL_COMBINE_TAB SET QR05001=?,Q05001=?,QR06001=?,Q06001=?,QR20013=?,Q20013=?,QR20001=?,Q20001=?,QR20010=?,Q20010=?,QR11001=?,Q11001=?,QR11002=?,Q11002=?,QR12001=?,Q12001=?,QR12003=?,Q12003=?,QR13003=?,Q13003=?,QR10004=?,Q10004=?,QR10051=?,Q10051=?,QR07004=?,Q07004=?,QR10009=?,Q10009=?,QR10063=?,Q10063=?,QR10061=?,Q10061=?,QR13019=?,Q13019=?,QR13011_02=?,Q13011_02=?,QR13020=?,Q13020=?,QR13021=?,Q13021=?,QR13011_09=?,Q13011_09=?,QR13022=?,Q13022=?,QR13011_15=?,Q13011_15=?,QR13011_18=?,Q13011_18=?,QR13023=?,Q13023=?,QR20003=?,Q20003=?,QR20004=?,Q20004=?,QR20005=?,Q20005=?,QR20011=?,Q20011=?,QR20350_11=?,Q20350_11=?,QR20350_12=?,Q20350_12=?,QR20350_13=?,Q20350_13=?,QR10062=?,Q10062=?,QR12405=?,Q12405=?,QR12014=?,Q12014=?,QR12016=?,Q12016=?,QR12015=?,Q12015=?,QR12017=?,Q12017=?,QR12013=?,Q12013=?,QR20062=?,Q20062=?,QR13013=?,Q13013=?,QR13340=?,Q13340=?,QR14032_01=?,Q14032_01=?,QR14032_24=?,Q14032_24=?,QR14016_01=?,Q14016_01=?,QR14015=?,Q14015=?,QR14021_01=?,Q14021_01=?,QR14020=?,Q14020=?,QR14023_01=?,Q14023_01=?,QR14022=?,Q14022=?,QR14002_01=?,Q14002_01=?,QR14001=?, Q14001=?, QR14004_01=?,Q14004_01=?,QR14003=?,Q14003=?,QR14025_01=?,Q14025_01=?,QR14024=?,Q14024=?,QR20054_01=?,Q20054_01=?,QR20054_02=?,Q20054_02=?,QR20054_03=?,Q20054_03=?,QR20012=?,Q20012=?,QR05021=?,Q05021=?,QR07021=?,Q07021=?,QR20012_01=?,Q20012_01=?,QR20011_01=?,Q20011_01=?,QR20013_01=?,Q20013_01=?,QR20012_02=?,Q20012_02=?, QR20011_02=?,Q20011_02=?,QR20013_02=?,Q20013_02=?,QR20012_03=?,Q20012_03=?,QR20011_03=?,Q20011_03=?,QR20013_03=?,Q20013_03=?,QR20012_04=?,Q20012_04=?,QR20011_04=?,Q20011_04=?,QR20013_04=?,Q20013_04=?,QR20063_01=?,Q20063_01=?,QR20063_02=?,Q20063_02=?,QR20063_03=?,Q20063_03=?,QR07005=?,Q07005=? WHERE D_DATETIME=? and V01301=? and V_TYPE_REPORT=?"
        # print(sql%data[0])
        cur.executemany(sql,data)
        # print(len(data))
        # for i in range(len(data)):
        #     cur.execute(sql%data[i])
        conn.commit()
        print('save success')
        end_time = str(datetime.datetime.now()).split('.')[0]
        deal_di(file_names, start_time, end_time, True)
    except Exception as e:
        # print(sql%data[i])
        deal_ei(ts_date, ip, e)
        deal_di(file_names, start_time, end_time, False)
        conn.rollback()
    cur.close()
    conn.close()

def data_deal(tt):
    data = []
    start_time = str(datetime.datetime.now()).split('.')[0]
    for t in tt:
        ts_date = datetime.datetime.strptime(t, '%Y%m%d%H%M%S')
        path = os.path.join('/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/OCEAN/LHVI_TEST/QC/output',  ts_date.strftime("%Y/%Y%m/%Y%m%d/%H/%Y/"))
        files = glob.glob(path +'*.TXT')
        file_names = ''
        for file_name in files:
            try:
                f = open(file_name)
                f_n = os.path.split(file_name)[1]
                file_names += f_n + ','
                content = f.readlines()
                for con in content:
                    content_list = con.split(' ')
                    for ts in tt:
                        year= ts[0:4]
                        mon = ts[4:6]
                        day = ts[6:8]
                        hour = ts[8:10]
                        min = ts[10:12]
                        if content_list[0] == year and content_list[7] == mon and content_list[16] == day and content_list[25] == hour and content_list[34] == min:
                            con_list = [content_list[0]+'-'+content_list[7]+'-'+content_list[16]+' '+content_list[25]+':'+ content_list[34]+':00', content_list[43], content_list[-166], content_list[-156:]]
                            con_list[3].append(datetime.datetime.strptime(con_list[0], '%Y-%m-%d %H:%M:%S'))
                            con_list[3].append(con_list[1])
                            con_list[3].append(con_list[2])
                            con_list[3][-4] = con_list[3][-4][:-1]
                            con_tuple = tuple(con_list[3])
                            data.append(con_tuple)
                f.close()
            except:
                print(file_name)
    update_into_info(data, ts_date.strftime("%Y%m%d%H"), file_names, start_time)

def select_time(Process, ts, t):
    if Process == 'appoint':
        data_deal([ts])
    elif Process == 'offsetDay':
        time_t = datetime.datetime.strptime(t, "%Y%m%d%H%M%S")
        time_n = time_t - datetime.timedelta(days=abs(int(ts)))
        ts = time_n.strftime('%Y%m%d')
        tt = []
        for i in range(24):
            if i < 10:
               tt.append(ts + '0' +  str(i) + '0000')
            else:
                tt.append(ts + str(i) + '0000') 
        data_deal(tt)
    elif Process == 'offsetHour':
        time_t = datetime.datetime.strptime(t, "%Y%m%d%H%M%S")
        time_n = time_t - datetime.timedelta(hours=abs(int(ts)))
        ts = time_n.strftime('%Y%m%d%H%M%S')
        data_deal([ts])


if __name__ == '__main__':
    select_time(sys.argv[1], sys.argv[2], sys.argv[3])

                
