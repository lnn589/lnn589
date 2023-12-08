# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:02:05 2023

@author: admin
"""
import matplotlib.pyplot as plt
import numpy as np
import cartopy
cartopy.config['pre_existing_data_dir'] = r"/space/cmadaas/dpl/NMIC_BASE_DATASET/LHVI/draw/common/cartopy_script"
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
from matplotlib import colors as cols
import pandas as pd
import matplotlib.ticker as mticker
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
df = pd.read_csv('11.csv')
df[df['PRS']==999999] = np.nan
x = df['Lon']
y = df['Lat']
z = df['PRS']



plt.figure(figsize=(10,7))

# Creates the map

ca_map = plt.axes(projection=ccrs.PlateCarree())

ca_map.add_feature(cfeature.OCEAN)

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
plt.scatter(x=x, y=y, c=z, s=1.5, marker = ".", cmap=cmap, alpha=0.4)
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap, )
cb = plt.colorbar(sm, orientation='horizontal', shrink=0.8, pad=0.1, ticks=colorlevel,)
cb.ax.set_title(r'单位:hPa', fontsize=11, x=1.25, y=-1.2)
plt.ylabel("Latitude", fontsize=14)

plt.xlabel("Longitude", fontsize=14)
plt.gca().spines['top'].set_color('none')
plt.gca().spines['right'].set_color('none')
plt.title("GSOD Ps 2023031011")
plt.ylim(-90,90)
plt.xlim(-180,180)
plt.xticks([i for i in range(-180, 181, 60)], ['180°', '120°W', '60°W', '0°', '60°E', '120°E', '180°'])
plt.yticks([i for i in range(-90, 91, 30)], ['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])

# major_locator = plt.MultipleLocator(30)
# print(major_locator)
# plt.gca().xaxis.set_major_locator(major_locator)
# plt.gca().yaxis.set_major_locator(major_locator)
plt.savefig('Ps.png', bbox_inches='tight')
plt.show()