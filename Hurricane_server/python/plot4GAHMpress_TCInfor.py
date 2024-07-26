#%%
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

#%%
# 설정된 경위도 범위 및 해상도
slon = 117
elon = 136
slat = 15
elat = 40
dres = 0.02
# 격자 생성
lon = np.arange(slon, elon, dres)
lat = np.arange(slat, elat, dres)
xx, yy = np.meshgrid(lon, lat)
#%%
# 현재 파이썬 파일이 위치한 디렉토리
current_dir = os.path.dirname(os.path.abspath(__file__))

# output_dir 및 input_dir 설정
output_dir = os.path.join(current_dir, 'press_figure')
input_dir = os.path.join(current_dir, 'press_processed')
print(f'save in {output_dir}')
print(f'input in {input_dir}')

# 이미지 저장 경로
os.makedirs(output_dir, exist_ok=True)
press_count = len(os.listdir('press_processed'))
print(f'pressure file : {press_count}')
#%%
file_path = current_dir+'/bwp122007.dat'
print(f'tc track info : {file_path}')
center_lats = []
center_lons = []

# 트랙 정보에서 중심 좌표 추출 
with open(file_path) as f:
    lines = f.readlines()
    for line in lines:
        parts = line.strip().split()
        lat_str = parts[6]
        lon_str = parts[7]
        lon = int(lon_str[:4]) / 10.0
        lat = int(lat_str[:3]) / 10.0
        if lat_str[-1] == 'S':
            lat = -lat
        if lon_str[-1] == 'W':
            lon = -lon
        center_lats.append(lat)
        center_lons.append(lon)
#%%
file_path = os.path.join(input_dir, f'fort.10077')

with open(file_path) as f:
    lines = f.readlines()
pressure = np.array([float(iline.strip().split()[1]) for iline in lines]).reshape(xx.shape)

# 지도 설정
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([slon, elon, slat, elat], crs=ccrs.PlateCarree())

# 해안선 및 지형 추가
ax.coastlines(color='white', linewidth=1.5)
ax.add_feature(cfeature.LAND, facecolor='white')
ax.add_feature(cfeature.OCEAN, facecolor='white')

# 바람 속도 컬러맵 표시
# p = ax.pcolormesh(xx, yy, pressure, cmap='Reds_r', shading='auto', transform=ccrs.PlateCarree(), vmin=960, vmax=1000)
p = ax.pcolormesh(xx, yy, pressure, cmap='jet_r', shading='auto', transform=ccrs.PlateCarree(), vmin=960, vmax=1000, edgecolors='k', linewidths=1)
cb = plt.colorbar(p, ax=ax, orientation='vertical', pad=0.1)
cb.set_label('Pressure (hPa)', fontsize=14)

# 태풍 진로도 표시 
ax.plot(center_lons, center_lats, color='black', linewidth=2, marker='o', markerfacecolor='gray', markeredgecolor='black', transform=ccrs.PlateCarree(), label='Nari Track intervals 6 hours')

# 쿠메지마 관측소 위치 표시
kumejima_lat = 26.33
kumejima_lon = 126.80
ax.scatter(kumejima_lon, kumejima_lat, color='red', marker='^', s=100, transform=ccrs.PlateCarree(), label='Kumejima Obs')


# 레전드 추가
ax.legend()

# 축 라벨 및 제목 추가
ax.set_xlabel('Longitude [°E]', fontsize=15)
ax.set_ylabel('Latitude [°N]', fontsize=15)
ax.set_title(f'Nari(2007)', fontsize=20)

# 그리드 라인 추가
gl = ax.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

plt.show()
# 그림 저장
output_file = os.path.join(output_dir, f'Nari_info_pres_20070915.png')
plt.savefig(output_file)
plt.close(fig)  # 메모리 해제를 위해 그림 닫기

print(f'Saved figure for fort.10077 as {output_file}')

# %%
# path = '/home/tkdals/models/GAHM/Projects/Nari/press_processed/fort.10077'
# with open(path) as f:
#     lines = f.readlines()
# pressure = np.array([float(iline.strip().split()[1]) for iline in lines]).reshape(xx.shape)
# # %%
# # 찾고자 하는 기압값 설정
# target_pressure = 934.3

# # 기압값 배열에서 해당 값과 가장 가까운 값을 찾기
# difference = np.abs(pressure - target_pressure)
# min_index = np.argmin(difference)

# # 인덱스를 사용하여 해당 위경도 좌표를 찾기
# lat_index, lon_index = np.unravel_index(min_index, pressure.shape)
# found_lat = yy[lat_index, lon_index] # 26.35
# found_lon = xx[lat_index, lon_index] # 126.81

# print(f"Pressure closest to {target_pressure} found at latitude {found_lat} and longitude {found_lon}")
# print(f"Closest pressure value: {pressure[lat_index, lon_index]}")
# # 태풍의 최소기압 좌표와 관측소 간 거리 : 3km
# # 최소기압 : 935hPa
# # 최대풍속 : 63.89m/s (1분 평균 풍속)
# # 2024년9월14일 17시00분00초 (토요일)
# # %%

# # %%

# %%
