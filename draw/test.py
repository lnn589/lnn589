# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:02:05 2023

@author: admin
"""
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import cartopy
cartopy.config['pre_existing_data_dir'] = r"/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/common/cartopy_script"
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import colors as cols
import pandas as pd
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

def draw_wind_spd(x, y, z, title, png_name, out_path: str):
    """
    :return: 散点图->风速
    """
    plt.figure(figsize=(10,7))


    ca_map = plt.axes(projection=ccrs.PlateCarree())

    ca_map.coastlines(resolution='10m', lw=0.3, color="black")

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
    cb.ax.set_title(r'单位:m/s', fontsize=11, x=1.25, y=-1.2)
    plt.ylabel("Latitude", fontsize=14)

    plt.xlabel("Longitude", fontsize=14)
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['right'].set_color('none')
    plt.title("TEM 202303"+title)
    plt.ylim(-90,90)
    plt.xlim(-180,180)
    plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
    plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    response_path = os.path.join(out_path, png_name)
    plt.savefig(response_path, bbox_inches='tight')
    return response_path

def draw_tave(x, y, z, title, png_name, out_path: str):
    """
    :return: 散点图->气温
    """
    plt.figure(figsize=(10,7))


    ca_map = plt.axes(projection=ccrs.PlateCarree())

    ca_map.coastlines(resolution='10m', lw=0.3, color="black")

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
    plt.title("TEM 202303"+title)
    plt.ylim(-90,90)
    plt.xlim(-180,180)
    plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
    plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    response_path = os.path.join(out_path, png_name)
    plt.savefig(response_path, bbox_inches='tight')
    return response_path


def draw_ps(x, y, z, title, png_name, out_path: str):
    """
    :return: 散点图->气压
    """
    plt.figure(figsize=(10,7))
    ca_map = plt.axes(projection=ccrs.PlateCarree())
    ca_map.coastlines(resolution='10m', lw=0.3, color="black")
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
    plt.title("Ps 202303"+title)
    plt.ylim(-90,90)
    plt.xlim(-180,180)
    plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
    plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    response_path = os.path.join(out_path, png_name)
    plt.savefig(response_path, bbox_inches='tight')
    return response_path


def draw_other(x, y, z, title, png_name, out_path: str):
    """
    :return: 散点图->降水量
    """
    plt.figure(figsize=(10,7))
    z = np.where(z >= 999999,np.nan,z)
    ca_map = plt.axes(projection=ccrs.PlateCarree())


    ca_map.coastlines(resolution='10m', lw=0.3, color="black")

    ca_map.xaxis.set_visible(True)

    ca_map.yaxis.set_visible(True)
    colorlevel = (0, 0.1, 1, 2, 3, 6, 9, 12, 18, 21, 27, 33, 39, 42, 48, 54, 999,999998)
    color_list = (
        "#BEBEBE", "#FF600F", "#FF8426", "#FFA427", "#FFC229", "#FFD21A", "#7FFF49", "#E4FF04", "#A9FF20",
        "#7FFF49", "#00FF15", "#4dffb8", "#33ffff", "#4dd3ff", "#1a52ff", "#0000cc", "#FF0000")
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
    plt.title(png_name.split('.')[0]+" 202303"+title)
    plt.ylim(-90,90)
    plt.xlim(-180,180)
    plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
    plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    response_path = os.path.join(out_path, png_name)
    plt.savefig(response_path, bbox_inches='tight')
    return response_path

def main(path, t_path, png_t):
    files = glob.glob(path+'*.csv')
    files=sorted(files, key=lambda name: int(os.path.split(name)[1].split('.')[0]))
    x = []
    ps = []
    t = []
    td = []
    WIN_D = []
    WIN_S = []
    PRE_6h = []
    PRE_12h = []
    PRE_24h = []
    for f in files:
        df1 = pd.read_csv(f)
        f_n = os.path.split(f)[1].split('.')[0][6:10]
        x.append(f_n)
        a = df1['Lon']
        b = df1['Lat']
        c = df1['TEM']
        d = df1['PRS']
        e = df1['WIN_S']
        f = df1['PRE_1h']
        g = df1['PRE_3h']
        h = df1['PRE_6h']
        i = df1['PRE_12h']
        l = df1['PRE_24h']
        draw_tave(a, b, c, f_n, f_n+'_TEM.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path)
        draw_ps(a, b, d, f_n, f_n+'_PRS.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path)
        draw_other(a, b, e, f_n, f_n+'_WIN_S.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path)
        draw_other(a, b, f, f_n, f_n+'_PRE_1h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path)
        draw_other(a, b, g, f_n, f_n+'_PRE_3h.png','/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path)
        draw_other(a, b, h, f_n, f_n+'_PRE_6h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path)
        draw_other(a, b, i, f_n, f_n+'_PRE_12h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path)
        draw_other(a, b, l, f_n, f_n+'_PRE_24h.png', '/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/img/'+t_path) 
        ps.append(len(df1['PRS']) - df1['PRS'].value_counts()[999999.0])
        t.append(len(df1['TEM']) - df1['TEM'].value_counts()[999999.0])
        td.append(len(df1['DPT']) - df1['DPT'].value_counts()[999999.0])
        WIN_D.append(len(df1['WIN_D']) - df1['WIN_D'].value_counts()[999999.0])
        WIN_S.append(len(df1['WIN_S']) - df1['WIN_S'].value_counts()[999999.0])
        PRE_6h.append(len(df1['PRE_6h']) - df1['PRE_6h'].value_counts()[999999.0])
        PRE_12h.append(len(df1['PRE_12h']) - df1['PRE_12h'].value_counts()[999999.0])
        PRE_24h.append(len(df1['PRE_24h']) - df1['PRE_24h'].value_counts()[999999.0])
            
    plt.figure(figsize=(10,7))             
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
    plt.savefig('./img/pic-{}.png'.format(png_t))

# if __name__ == '__main__':
#     main()


