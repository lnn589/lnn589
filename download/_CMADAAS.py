# -*- coding: utf-8 -*-
import os
import time
import uuid
import copy
import json
import hashlib
import requests
import base64
import pandas as pd
import datetime
import csv
import warnings
warnings.filterwarnings("ignore") 


def get_user_info(type) -> dict:
    if "music" == type or "database" == type:
        path = r"/CMADAAS/APPDATA/DPL/NMIC_BASE_DATASET/CONFIG/DPL.env"
        un_get = dict()
        username, password = str(), str()
        with open(path, "r") as f:
            for i in f.readlines():
                res = base64.b64decode(i.encode("utf-8")).decode("utf-8")
                if type in res.strip():
                    if un_get.setdefault(type):
                        un_get[type].append(res)
                    else:
                        un_get[type] = [res]
        return {"user": [i.split(":")[-1].strip() for i in un_get[type] if "user" in i][0],
                "password": [i.split(":")[-1].strip() for i in un_get[type] if "password" in i][0]}
    else:
        raise Exception("获取方式错误")

def rmdir(path):
    if not os.listdir(path):
        os.rmdir(path)

def CheakDir(checkdir):
    if not os.path.exists(checkdir):
        os.makedirs(checkdir)


class CMADAAS(object):
    """天擎平台资料下载(URL方式)

    Args:
        post_data: 接口参数; json
        url: CIMISS接口地址
        save: 路径或文件名; 文件(非结构化): 保存的路径名; 格式化文本: 保存的文件名
        keywords: 关键字列表; 用于对文件(非结构化)的下载筛选
        timeout: 超时时间; 接口访问和数据下载的超时时间
        na_rep: 格式化文本: 保存文本时的缺省值填充
    """
    def __init__(
            self,
            post_data,
            year,
            url='http://10.48.90.120:80/music-ws/api',
            save=None,
            keywords=None,
            timeout=300,
            na_rep='999999'
            
    ):
        self.url       = url
        self.post_data = post_data
        self.save      = save
        self.keywords  = keywords
        self.timeout   = timeout
        self.na_rep    = na_rep
        self.year = year

    def _post(self, post_data: dict):
        """调取接口

        Args:
            post_data: 接口参数; json

        Returns:
            接口返回信息(json)
        """
        _post_data = self._sign(post_data)
        requ = requests.get(self.url, params=_post_data, timeout=self.timeout)
        result = json.loads(requ.text, strict=False)
        return result

    @staticmethod
    def _sign(post_data: dict):
        """计算 nonce、sign; 去掉pwd

        在 post_data 基础上计算并添加 nonce 和 sign 键, 删除 pwd 键

        Args:
            post_data: 接口参数; json

        Returns:
            _post_data: 处理后的新的 post_data
        """
        _post_data = copy.deepcopy(post_data)
        _post_data['timestamp'] = str(int(round(time.time() * 1000)))
        _post_data['nonce']     = str(uuid.uuid1())
        sign = '&'.join([key + '=' + _post_data.get(key) for key in sorted(_post_data)])
        sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest().upper()
        _post_data['sign'] = sign
        _post_data.pop('pwd')
        return _post_data
    
    def _text_download(self, data):
        """下载格式化文本

        Args:
            data: 数据

        Returns:
            bool: True,下载文件成功; False,下载文件失败
        """
        try:
            CheakDir('/'.join(self.save.split('/')[:-1]))
            listType = data['Station_Id_C'].unique()
            data['Mon'] = data['Mon'].apply(lambda x : str(x).zfill(2))
            data['Day'] = data['Day'].apply(lambda x : str(x).zfill(2))
            data['Hour'] = data['Hour'].apply(lambda x : str(x).zfill(2))
            data['Min'] = data['Min'].apply(lambda x : str(x).zfill(2))
            
            data_con = [data['Year'], data['Mon'], data['Day'], data['Hour'], data['Min'], data['Station_Id_C']]
            cols = ['Lat', 'Lon', 'Alti', 'CLO_Height_LoM', 'VIS', 'CLO_Cov', 'WIN_D', 'WIN_S', 'TEM', 'DPT', 'RHU', 'PRS', 'PRS_Sea', 'PRS_HWC', 'GPH', 'PRS_Trend', 'PRS_Change_3h', 'PRE_1h', 'PRE_2h', 'PRE_3h', 'PRE_6h', 'PRE_9h', 'PRE_12h', 'PRE_15h', 'PRE_18h', 'PRE_24h', 'WEP_Now', 'WEP_Past_1', 'WEP_Past_2', 'CLO_COV_LM', 'CLO_Fome_Low', 'CLO_FOME_MID', 'CLO_Fome_High', 'PRS_Change_24h', 'TEM_ChANGE_24h', 'TEM_Max_12h', 'TEM_Max_24h', 'TEM_Min_12h', 'TEM_Min_24h', 'GST_Min_12h', 'SCO', 'Snow_Depth', 'EVP_Day', 'SSH_1h', 'SSH_24h', 'NRA_1h', 'NRA_24h', 'QRA_24h', 'QRA_1h', 'SRA_1h', 'SRA_24h', 'LR_1h', 'LR_24h', 'SR_1h', 'SR_24h', 'DRA_1h', 'DRA_24h', 'CLO_Low_MoDir', 'CLO_Mid_Modir', 'CLO_High_Modir', 'CLO_Type', 'Bear', 'Elev', 'CLO_GENE1', 'CLO_Cov_Gene1', 'CLO_GENE1_Heigh', 'CLO_GENE2', 'CLO_Cov_Gene2', 'CLO_GENE2_Heigh', 'CLO_GENE3', 'CLO_Cov_Gene3', 'CLO_GENE3_Heigh', 'CLO_GENE_Cumlb', 'CLO_Cov_Cumlb', 'CLO_Cumlb_Heigh', 'SWEP1', 'SWEP2', 'SWEP3', 'V07005']
            for col in cols:
                data[col] = data[col].apply(lambda x : round(float(x),1))
                data[col] = data[col].apply(lambda x : str(x).rjust(8))
                data_con.append(data[col])

            data['V11003'] = data['V11003'].apply(lambda x : str(x).zfill(1))
            data_con.append(data['V11003'])
            data['V_TYPE_REPORT'] = data['V_TYPE_REPORT'].apply(lambda x : str(x).ljust(6))
            data_con.append(data['V_TYPE_REPORT'])
            col_source = ['V10051_SOURCE', 'V12001_SOURCE', 'V12003_SOURCE', 'V12014_SOURCE', 'V12015_SOURCE', 'V12016_SOURCE', 'V12017_SOURCE', 'V13019_SOURCE', 'V13020_SOURCE', 'V13021_SOURCE', 'V13022_SOURCE', 'V13023_SOURCE', 'V07005_SOURCE', 'V11001_SOURCE', 'V11002_SOURCE', 'V11003_SOURCE', 'V07004_SOURCE', 'V10063_SOURCE', 'V10061_SOURCE', 'V10062_SOURCE', 'V10009_SOURCE', 'V20013_SOURCE', 'V20010_SOURCE', 'V20011_SOURCE', 'V20350_11_SOURCE', 'V20350_12_SOURCE', 'V20350_13_SOURCE', 'V20012_01_SOURCE', 'V20011_01_SOURCE', 'V20013_01_SOURCE', 'V20012_02_SOURCE', 'V20011_02_SOURCE', 'V20013_02_SOURCE', 'V20012_03_SOURCE', 'V20011_03_SOURCE', 'V20013_03_SOURCE', 'V20001_SOURCE', 'V13003_SOURCE', 'V12405_SOURCE', 'V12013_SOURCE', 'V20003_SOURCE', 'V20004_SOURCE', 'V20005_SOURCE', 'V20063_01_SOURCE', 'V20063_02_SOURCE', 'V20063_03_SOURCE', 'V20062_SOURCE', 'V13013_SOURCE', 'V13340_SOURCE', 'V14032_24_SOURCE', 'V14032_01_SOURCE', 'V20054_01_SOURCE', 'V20054_02_SOURCE', 'V20054_03_SOURCE', 'V20012_SOURCE', 'V05021_SOURCE', 'V07021_SOURCE', 'V20012_04_SOURCE', 'V20011_04_SOURCE', 'V20013_04_SOURCE', 'V14016_01_SOURCE', 'V14015_SOURCE', 'V14021_01_SOURCE', 'V14020_SOURCE', 'V14023_01_SOURCE', 'V14022_SOURCE', 'V14002_01_SOURCE', 'V14001_SOURCE', 'V14004_01_SOURCE', 'V14003_SOURCE', 'V14025_01_SOURCE', 'V14024_SOURCE', 'V13011_02_SOURCE', 'V13011_09_SOURCE', 'V13011_15_SOURCE', 'V13011_18_SOURCE']
            for col in col_source:
                data['V10004_SOURCE'] += data[col]
            data_con.append(data['V10004_SOURCE'])
            data_con = pd.concat(data_con, axis=1)
            station_nums = 0
            for station_num in listType:
                # if station_num == '072830':
                if station_num.isdigit():
                    station_nums += 1
                    data_i = data_con[data_con['Station_Id_C'].isin([station_num])]
                    data_i = data_i.sort_values(by=['Year', 'Mon', 'Day', 'Hour', 'Min'])
                    file_name = str(station_num) + '-'+self.year+'.TXT'
                    # data_i.to_csv(self.save + file_name, sep=' ', index=False, header=0, na_rep=self.na_rep,quoting=csv.QUOTE_NONE,escapechar=' ')
                    data_i.to_csv(self.save + file_name, sep=' ', index=False, header=0)
            print(datetime.datetime.now(), 'INFO: save', self.save)
            return station_nums
        except Exception as err:
            rmdir(self.save)
            print(190, 'ERROR:', err)
            return False

    def text(self):
        """获取/下载 文件(格式化文本)

        Returns:
            若设置了save, 返回保存的文件名
            若未设置save, 返回获取的数据内容
        """
        # if self._text_diff() is True:
        #     return None
        requ = self._post(self.post_data)
        
        text_turn = int(requ['returnCode'])  # 状态码
        text_mess = requ['returnMessage']    # 状态信息
        

        if text_turn != 0:
            print(datetime.datetime.now(), 'ERROR:', text_mess)
            return None

        data = pd.DataFrame(requ['DS'])
        if self.save is None:
            return data
        else:
            station_nums = self._text_download(data)
            return station_nums
        
    def _text_diff(self):
        """比较文件(格式化文本)

        统计已存在的文件行数, 判断需不需要覆盖下载

        Returns:
            bool: True,文件相同; False,文件不同或不存在
        """
        if self.save is None:
            return False
        if os.path.exists(self.save):
            with open(self.save, 'r') as f:
                text_rows = len(f.readlines())
            post_data = copy.deepcopy(self.post_data)
            post_data['elements'] = ','.join(self.post_data['elements'].split(',')[0:2])
            requ = self._post(post_data)
            turn = int(requ['returnCode'])
            mess = requ['returnMessage']
            if turn != 0:
                print(datetime.datetime.now(), 'ERROR', mess)
                return True
            data = pd.DataFrame(requ['DS'])
            rows = len(data)
            if text_rows >= rows:
                return True
            print(datetime.datetime.now(), 'INFO: Replace')
        return False

