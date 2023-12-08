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
import numpy as np
import matplotlib.pyplot as plt
import cartopy
cartopy.config['pre_existing_data_dir'] = r"/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/common/cartopy_script"
import cartopy.crs as ccrs
import cartopy.feature as cfeature
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

from matplotlib import colors as cols
def draw_tave(x, y, z, title, png_name, out_path: str):
    """
    :return: 散点图->气温
    """
    plt.figure(figsize=(10,7))

    # Creates the map

    ca_map = plt.axes(projection=ccrs.PlateCarree())

    # ca_map.add_feature(cfeature.OCEAN)

    ca_map.coastlines(resolution='10m', lw=0.3, color="black")

    # To add county lines
    ca_map.xaxis.set_visible(True)

    ca_map.yaxis.set_visible(True)

    colorlevel = (-45, -40, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45)
    color_list = (
        "#0000cc", "#1a52ff", "#4dd3ff", "#33ffff", "#4dffb8", "#00FF15", "#7FFF49", "#A9FF20", "#E4FF04",
        "#FFF626", "#FFD21A", "#FFC229", "#FFA427", "#FF8426", "#FF600F", "#FF0000")
    cmap = cols.ListedColormap(color_list,)
    norm = cols.BoundaryNorm(colorlevel, cmap.N,)
    plt.scatter(x=x, y=y, c=z, s=1.5, marker = ".", cmap=cmap,norm=norm, alpha=1)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap, )
    cb = plt.colorbar(sm, orientation='horizontal', shrink=0.8, pad=0.1, ticks=colorlevel,)
    cb.ax.set_title(r'单位:℃', fontsize=11, x=1.25, y=-1.2)
    plt.ylabel("Latitude", fontsize=14)

    plt.xlabel("Longitude", fontsize=14)
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['right'].set_color('none')
    plt.title("TEM 20230312"+title)
    plt.ylim(-90,90)
    plt.xlim(-180,180)
    plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
    plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
    response_path = os.path.join(out_path, png_name)
    plt.savefig(response_path, bbox_inches='tight')
    return response_path


def draw_ps(x, y, z, title, png_name, out_path: str):
    """
    :return: 散点图->气压
    """
    plt.figure(figsize=(10,7))

    # Creates the map

    ca_map = plt.axes(projection=ccrs.PlateCarree())

    # ca_map.add_feature(cfeature.OCEAN)

    ca_map.coastlines(resolution='10m', lw=0.3, color="black")

    # To add county lines
    ca_map.xaxis.set_visible(True)

    ca_map.yaxis.set_visible(True)
    colorlevel = (500, 600, 700, 800, 850, 900, 950, 970, 990, 1000, 1100)
    color_list = (
        "#0000cc", "#4dd3ff", "#33ffff", "#7FFF49", "#A9FF20", "#E4FF04",
        "#FFA500", "#FF600F", "#FF0000", "#800000")
    cmap = cols.ListedColormap(color_list,)
    norm = cols.BoundaryNorm(colorlevel, cmap.N,)
    plt.scatter(x=x, y=y, c=z, s=1.5, marker = ".", cmap=cmap, norm=norm, alpha=1)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap, )
    cb = plt.colorbar(sm, orientation='horizontal', shrink=0.8, pad=0.1, ticks=colorlevel,)
    cb.ax.set_title(r'单位:hPa', fontsize=11, x=1.25, y=-1.2)
    plt.ylabel("Latitude", fontsize=14)

    plt.xlabel("Longitude", fontsize=14)
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['right'].set_color('none')
    plt.title("Ps 20230312"+title)
    plt.ylim(-90,90)
    plt.xlim(-180,180)
    plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
    plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
    response_path = os.path.join(out_path, png_name)
    plt.savefig(response_path, bbox_inches='tight')
    return response_path

def draw_other(x, y, z, title, png_name, out_path: str):
    """
    :return: 散点图->气压
    """
    plt.figure(figsize=(10,7))
    z = np.where(z >= 99999,np.nan,z)
    # Creates the map

    ca_map = plt.axes(projection=ccrs.PlateCarree())

    # ca_map.add_feature(cfeature.OCEAN)

    ca_map.coastlines(resolution='10m', lw=0.3, color="black")

    # To add county lines
    ca_map.xaxis.set_visible(True)

    ca_map.yaxis.set_visible(True)
    colorlevel = (0, 1, 2, 3, 4, 6, 9, 12, 15, 18, 21, 27, 33, 39, 42, 48, 54)
    color_list = (
        "#BEBEBE", "#FF0000", "#FF600F", "#FF8426", "#FFA427", "#FFC229", "#FFD21A", "#7FFF49", "#A9FF20",
        "#7FFF49", "#00FF15", "#4dffb8", "#33ffff", "#4dd3ff", "#1a52ff", "#0000cc")
    cmap = cols.ListedColormap(color_list,)
    norm = cols.BoundaryNorm(colorlevel, cmap.N,)
    plt.scatter(x=x, y=y, c=z, s=1.5, marker = ".", cmap=cmap, norm=norm, alpha=1)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap, )
    cb = plt.colorbar(sm, orientation='horizontal', shrink=0.8, pad=0.1, ticks=colorlevel,)
    cb.ax.set_title(r'单位:mm', fontsize=11, x=1.25, y=-1.2)
    plt.ylabel("Latitude", fontsize=14)

    plt.xlabel("Longitude", fontsize=14)
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['right'].set_color('none')
    plt.title(png_name.split('.')[0]+" 20230312"+title)
    plt.ylim(-90,90)
    plt.xlim(-180,180)
    plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
    plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
    response_path = os.path.join(out_path, png_name)
    plt.savefig(response_path, bbox_inches='tight')
    return response_path


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
        # try:
        CheakDir('/'.join(self.save.split('/')[:-1]))
        listType = data['Station_Id_C'].unique()
        data_i = data[data['Station_Id_C'].isin(['010640'])].sort_values(by=['Year', 'Mon', 'Day', 'Hour', 'Min'])
        x = data_i['Hour'].tolist()
        ps = []
        t = []
        td = []
        WIN_D = []
        WIN_S = []
        PRE_6h = []
        PRE_12h = []
        PRE_24h = []
        for hour in x:
            data_hour = data[data['Hour'].isin([hour])]
            ps.append(len(data_hour['PRS']) - data_hour['PRS'].value_counts()['999999'])
            t.append(len(data_hour['TEM']) - data_hour['TEM'].value_counts()['999999'])
            td.append(len(data_hour['DPT']) - data_hour['DPT'].value_counts()['999999'])
            WIN_D.append(len(data_hour['WIN_D']) - data_hour['WIN_D'].value_counts()['999999'])
            WIN_S.append(len(data_hour['WIN_S']) - data_hour['WIN_S'].value_counts()['999999'])
            PRE_6h.append(len(data_hour['PRE_6h']) - data_hour['PRE_6h'].value_counts()['999999'])
            PRE_12h.append(len(data_hour['PRE_12h']) - data_hour['PRE_12h'].value_counts()['999999'])
            PRE_24h.append(len(data_hour['PRE_24h']) - data_hour['PRE_24h'].value_counts()['999999'])
            a0 = data_hour['Station_Id_C']
            b0 = data_hour['V_TYPE_REPORT']
            a = data_hour['Lon']
            b = data_hour['Lat']
            c = data_hour['TEM']
            d = data_hour['PRS']
            e = data_hour['WIN_S']
            f = data_hour['PRE_1h']
            g = data_hour['PRE_3h']
            h = data_hour['PRE_6h']
            i = data_hour['PRE_12h']
            l = data_hour['PRE_24h']
            df = pd.concat([a0, b0, a, b, c, d, e, f, g, h, i, l], axis=1)
            df.to_csv(hour + '.csv', index=0)
            df1 = pd.read_csv(hour+'.csv')
            df1[df1['TEM']==999999] = np.nan
            a = df1['Lon']
            b = df1['Lat']
            c = df1['TEM']
            df1[df1['PRS']==999999] = np.nan
            d = df1['PRS']
            e = df1['WIN_S']
            f = df1['PRE_1h']
            g = df1['PRE_3h']
            h = df1['PRE_6h']
            i = df1['PRE_12h']
            l = df1['PRE_24h']
            draw_tave(a, b, c, hour, hour+'_TEM.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            draw_ps(a, b, d, hour, hour+'_PRS.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            draw_other(a, b, e, hour, hour+'_WIN_S.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            draw_other(a, b, f, hour, hour+'_PRE_1h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            draw_other(a, b, g, hour, hour+'_PRE_3h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            draw_other(a, b, h, hour, hour+'_PRE_6h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            draw_other(a, b, i, hour, hour+'_PRE_12h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            draw_other(a, b, l, hour, hour+'_PRE_24h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img')
            
                    
        plt.plot(x, ps, color='red', marker='o', linestyle='-', label='Ps')
        plt.plot(x, t, color='blue', marker='D', linestyle='-.', label='T')
        plt.plot(x, td, color='skyblue', marker='*', linestyle=':', label='Td')
        plt.plot(x, WIN_D, color='orange', marker='.', linestyle='-', label='wind_dir')
        plt.plot(x, WIN_S, color='yellow', marker='.', linestyle='-.', label='wind_spd')
        plt.plot(x, PRE_6h, color='purple', marker='*', linestyle=':', label='PRE_6h')
        plt.plot(x, PRE_12h, color='blueviolet', marker='.', linestyle='-.', label='PRE_12h')
        plt.plot(x, PRE_24h, color='green', marker='*', linestyle=':', label='PRE_24h')
        plt.legend()  # 显示图例
        plt.xticks(x, rotation=0)
        plt.xlabel("Hour")  # X轴标签
        plt.ylabel("Available Number of hourly data")  # Y轴标签
        plt.savefig('./img/pic-{}.png'.format('test'))

        return True
        # except Exception as err:
        #     rmdir(self.save)
        #     print(190, 'ERROR:', err)
        #     return False

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
            self._text_download(data)
            return self.save
        
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

