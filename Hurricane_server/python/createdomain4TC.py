# -*- coding: utf-8 -*-

"""
==================
create_domain.py
==================

Author       : Youjung Oh
Last update  : 19-Jun-2024

1. Purpose   : Create domain for GAHM
               regular, no land

"""

#%%
import numpy as np

slon = 117
elon = 136
slat = 15
elat = 40
dres = 0.02
lon = np.arange(slon,elon,dres)
lat = np.arange(slat,elat,dres)
xx, yy = np.meshgrid(lon, lat)
xx = xx.reshape(-1,1)
yy = yy.reshape(-1,1)
#%%
xx.shape[0]
# 1187500
# %%
with open('nfort.14', 'w') as fw:

  fw.write('OceanMesh2D\n')
  fw.write(f'{xx.shape[0]*2} {xx.shape[0]}\n')
  for cou, (ii, jj) in enumerate(zip(xx, yy)):
     fw.write(f'{cou+1:10d}   {ii[0]:14.10f}   {jj[0]:14.10f}   0.0000000000e+00\n')

# %%
