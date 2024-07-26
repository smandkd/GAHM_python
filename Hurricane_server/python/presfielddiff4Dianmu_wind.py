#%%
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
#%%
slon = 117
elon = 153.01
slat = 10
elat = 50.01
dres = 0.045

# 격자 생성
lon = np.arange(slon, elon, dres)
lat = np.arange(slat, elat, dres)
xx, yy = np.meshgrid(lon, lat)

output_dir = '/home/tkdals/models/GAHM/Projects/Dianmu_new_presfield/Figure2'
os.makedirs(output_dir, exist_ok=True)
# %%
min_list = []
max_list = []

def read_wind_data(file_path, shape):
    with open(file_path) as f:
        lines = f.readlines()
        uwnd = np.array([float(iline.strip().split()[1]) for iline in lines]).reshape(shape)
        vwnd = np.array([float(iline.strip().split()[2]) for iline in lines]).reshape(shape)
        wind_speed = np.sqrt(uwnd**2 + vwnd**2)
        
    return wind_speed
#%%
xx_shape = xx.shape  

for file_num in range(1, 73):
    file_path = f'/home/tkdals/models/GAHM/Projects/Dianmu_new_presfield/post_process/fort.{file_num+10000}'
    file_path_2 = f'/home/tkdals/models/GAHM/Projects/Dianmu_reg_grid/post_processed/fort.{10060 + file_num}'
    
    wind_speed = read_wind_data(file_path, xx_shape)
    wind_speed_2 = read_wind_data(file_path_2, xx_shape)
        
    diff_wind_value = wind_speed_2 - wind_speed
    diff_min = diff_wind_value.min()
    diff_max = diff_wind_value.max()
    
    max_list.append(diff_max)
    min_list.append(diff_min)

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([slon, elon, slat, elat], crs=ccrs.PlateCarree())

    # 해안선 및 지형 추가
    ax.coastlines(color='white', linewidth=1.5)
    ax.add_feature(cfeature.LAND, facecolor='white')
    ax.add_feature(cfeature.OCEAN, facecolor='white')

    # 바람 속도 컬러맵 표시
    p = ax.pcolormesh(xx, yy, diff_wind_value, cmap='coolwarm', shading='auto', transform=ccrs.PlateCarree(), vmin=-3, vmax=19)
    cb = plt.colorbar(p, ax=ax, orientation='vertical', pad=0.1)
    cb.set_label('Difference Wind speed (m/s)', fontsize=14)

    # 바람 벡터 필드 표시
    # ax.quiver(xx, yy, uwnd, vwnd, scale=500, transform=ccrs.PlateCarree())

    # 축 라벨 및 제목 추가
    ax.set_xlabel('Longitude [°E]', fontsize=15)
    ax.set_ylabel('Latitude [°N]', fontsize=15)
    ax.set_title(f'Fixed_pressure wind - Ambient_pressure wind Field {file_num}', fontsize=15, pad=17)

    # 그리드 라인 추가
    ax.gridlines(draw_labels=True)

    # 그림 저장
    output_file = os.path.join(output_dir, f'diff_wind_field_{file_num}.png')
    plt.savefig(output_file)
    print(f'Saved figure for {output_file}')
    # plt.show()
    plt.close(fig)  # 메모리 해제를 위해 그림 닫기


#%%
import imageio

path = os.getcwd()
print(path)

pic_count = len(os.listdir('Figure'))
# li = [imageio.imread(f'Figure/wind_field_10{str(i).zfill(3)}.png') for i in range(1, pic_count, 1)]
li = [imageio.imread(f'Figure2/diff_wind_field_{i}.png') for i in range(1, pic_count, 1)]
imageio.mimsave(path + "/Figure2/GAHM_result.gif", li, **{'duration':2})


# %%
