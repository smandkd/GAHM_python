#%%
import os
import matplotlib.pyplot as plt
import numpy as np
import imageio
#%%
path = os.getcwd()
print(path)
#%%
wind_count = len(os.listdir('wind_figure'))
press_count = len(os.listdir('press_figure'))
li = [imageio.imread(f'wind_figure/pressure_field_10{str(i).zfill(3)}.png') for i in range(1, pic_count-2, 1)]

# li = [imageio.imread(f'Figure/wind_field_10{str(i).zfill(3)}.png') for i in range(1, pic_count, 1)]
imageio.mimsave(path + "/wind_figure/pressure_result.gif", li, **{'duration':2})
# %%
wind_count = len(os.listdir('wind_figure'))
# %%
