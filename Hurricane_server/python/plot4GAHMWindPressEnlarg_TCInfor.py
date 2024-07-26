#%%
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
#%%
fort_file_num = '10040'
track_file_name = '/bwp212016.dat'
obs_date = '2016-10-03 16:00:00' # fig_1 에 들어가는 텍스트 
# 레전드 텍스트 추가
textstr = '\n'.join((
    r'Typhoon Info:',
    r'TC center Location to Observatory: 24.76 km',
    r'Min Pressure: 911 hPa',
    r'Max Wind Speed: 150 knots',
))
zoom_extent = [125, 128, 25, 28]
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

tc_name = current_dir.split('/')[6].split('_')[0]

#%%
file_path = current_dir+track_file_name
print(f'tc track info : {file_path}')
center_lats = []
center_lons = []

# 트랙 정보에서 중심 좌표 추출 
with open(file_path) as f:
    lines = f.readlines()
    tc_date = lines[0].strip().split()[2][:8]
    tc_year = tc_date[:4]
    print(tc_date)
    print(tc_year)
    for line in lines:
        parts = line.strip().split()
        lat_str = parts[6]
        lon_str = parts[7]
        lon = int(lon_str[:4]) / 10.0
         
        if len(lat_str) < 5 : 
            lat = int(lat_str[:2]) / 10.0
            print(f'{len(lat_str)} {lat}')
        else : 
            lat = int(lat_str[:3]) / 10.0
            print(f'{len(lat_str)} {lat}')
        
        if lat_str[-1] == 'S':
            lat = -lat
        if lon_str[-1] == 'W':
            lon = -lon
        center_lats.append(lat)
        center_lons.append(lon)
#%%
# ================================================
# 태풍 진로도(베스트 트랙)
# 태풍 기압 
# 관측소 위치 
# 태풍 정보 
# 그리는 코드 
# ================================================
file_path = os.path.join(input_dir, f'fort.{fort_file_num}')

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
# Reds_r jet_r 
p = ax.pcolormesh(xx, yy, pressure, cmap='jet_r', shading='auto', transform=ccrs.PlateCarree(), vmin=950, vmax=1010)
cb = plt.colorbar(p, ax=ax, orientation='vertical', pad=0.1)
cb.set_label('Sea Surface Pressure (hPa)', fontsize=14)

# 태풍 진로도 표시 
ax.plot(center_lons, center_lats, color='black', linewidth=2, marker='o', markerfacecolor='gray', markeredgecolor='black', transform=ccrs.PlateCarree(), label=f'{tc_name} Track intervals 6 hours')

# 쿠메지마 관측소 위치 표시
kumejima_lat = 26.33
kumejima_lon = 126.80
ax.scatter(kumejima_lon, kumejima_lat, color='purple', edgecolor='black', marker='^', s=300, alpha=0.7, transform=ccrs.PlateCarree(), label='Kumejima Obs')

# 날짜 텍스트 추가
ax.text(kumejima_lon - 6, kumejima_lat, obs_date, transform=ccrs.PlateCarree(), fontsize=8, verticalalignment='bottom', color='white')

# 레전드 추가
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.05, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', bbox=props)

# 레전드 추가
ax.legend()

# 축 라벨 및 제목 추가
ax.set_xlabel('Longitude [°E]', fontsize=15)
ax.set_ylabel('Latitude [°N]', fontsize=15)
ax.set_title(f'{tc_name}({tc_year})', fontsize=20)

# 그리드 라인 추가
gl = ax.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

plt.show()
# 그림 저장
output_file = os.path.join(output_dir, f'{tc_name}_info_pres_{tc_date}.png')
plt.savefig(output_file)
plt.close(fig)  # 메모리 해제를 위해 그림 닫기

print(f'Saved figure for as {output_file}')

#%%
# ================================================
# 태풍 진로도(베스트 트랙)
# 태풍 기압 
# 관측소 위치 
# 확대해서 그리는 코드 
# ================================================
file_path = os.path.join(current_dir, 'track_hourly.22')
spline_track_lon = []
spline_track_lat = []


with open(file_path) as f:
    lines = f.readlines()

    for line in lines:
        lon = line.strip().split()[1]
        lat = line.strip().split()[2]
        spline_track_lat.append(float(lat))
        spline_track_lon.append(float(lon))

# 지도 설정
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent(zoom_extent, crs=ccrs.PlateCarree())
# 해안선 및 지형 추가
ax.coastlines(color='white', linewidth=1.5)
ax.add_feature(cfeature.LAND, facecolor='white')
ax.add_feature(cfeature.OCEAN, facecolor='white')

# 바람 속도 컬러맵 표시
# Reds_r jet_r 
p = ax.pcolormesh(xx, yy, pressure, cmap='jet_r', shading='auto', transform=ccrs.PlateCarree(), vmin=950, vmax=1010)
cb = plt.colorbar(p, ax=ax, orientation='vertical', pad=0.1)
cb.set_label('Sea Surface Pressure (hPa)', fontsize=14)

contour = ax.contour(xx, yy, pressure, levels=np.arange(950, 1000, 10), colors='k', transform=ccrs.PlateCarree())
ax.clabel(contour, inline=1, fontsize=10, fmt='%1.0f')

# GAHM 태풍 진로도 표시 
ax.plot(spline_track_lon, spline_track_lat, color='black', linewidth=2, marker='o', markerfacecolor='gray', markeredgecolor='black', transform=ccrs.PlateCarree(), label=f'{tc_name} Track intervals 1 hours')


# 쿠메지마 관측소 위치 표시
kumejima_lat = 26.33
kumejima_lon = 126.80
ax.scatter(kumejima_lon, kumejima_lat, color='purple', edgecolor='black', marker='^', s=400, transform=ccrs.PlateCarree(), label='Kumejima Obs')

# 새로운 좌표 위치 표시
# new_lat = 26.33999999999976
# new_lon = 126.79999999999805
# ax.scatter(new_lon, new_lat, color='white', marker='x', s=100, transform=ccrs.PlateCarree(), label='GAHM coordinate')
ax.legend(loc='upper right')

# 축 라벨 및 제목 추가
ax.set_xlabel('Longitude [°E]', fontsize=15)
ax.set_ylabel('Latitude [°N]', fontsize=15)
ax.set_title(f'{tc_name}({tc_year})', fontsize=20)

# 그리드 라인 추가
gl = ax.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

plt.show()
plt.close(fig)  # 메모리 해제를 위해 그림 닫기

# %%
# ================================================
# 태풍 진로도(베스트 트랙)
# 태풍 바람 
# 관측소 위치 
# 확대해서 그리는 코드 
# ================================================
# 현재 파이썬 파일이 위치한 디렉토리
current_dir = os.path.dirname(os.path.abspath(__file__))

# output_dir 및 input_dir 설정
output_dir = os.path.join(current_dir, 'wind_figure')
input_dir = os.path.join(current_dir, 'wind_processed')

# 이미지 저장 경로
os.makedirs(output_dir, exist_ok=True)
wind_count = len(os.listdir('wind_processed'))
print(wind_count)

file_path = os.path.join(input_dir, f'fort.{fort_file_num}')
#%%
with open(file_path) as f:
    lines = f.readlines()
uwnd = np.array([float(iline.strip().split()[1]) for iline in lines]).reshape(xx.shape)
vwnd = np.array([float(iline.strip().split()[2]) for iline in lines]).reshape(xx.shape)
wind_speed = np.sqrt(uwnd**2 + vwnd**2)
print(f'wind max : {wind_speed.max()}') # 63.02655845675054
print(f'wind min : {wind_speed.min()}') # 0.0
#%%
# 지도 설정
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent(zoom_extent, crs=ccrs.PlateCarree())
# 해안선 및 지형 추가
ax.coastlines(color='white', linewidth=1.5)
ax.add_feature(cfeature.LAND, facecolor='white')
ax.add_feature(cfeature.OCEAN, facecolor='white')

# 바람 속도 컬러맵 표시
p = ax.pcolormesh(xx, yy, wind_speed, cmap='jet', shading='auto', transform=ccrs.PlateCarree(), vmin=0, vmax=65)
cb = plt.colorbar(p, ax=ax, orientation='vertical', pad=0.1)
cb.set_label('Wind (m/s)', fontsize=14)

contour = ax.contour(xx, yy, wind_speed, levels=np.arange(30, 70, 10), colors='k', transform=ccrs.PlateCarree())
ax.clabel(contour, inline=1, fontsize=10, fmt='%1.0f')

# 태풍 진로도 표시 
ax.plot(spline_track_lon, spline_track_lat, color='black', linewidth=2, marker='o', markerfacecolor='gray', markeredgecolor='black', transform=ccrs.PlateCarree(), label=f'{tc_name} Track intervals 1 hours')

# 쿠메지마 관측소 위치 표시
kumejima_lat = 26.33
kumejima_lon = 126.80
ax.scatter(kumejima_lon, kumejima_lat, color='purple', edgecolor='black', marker='^', s=400, transform=ccrs.PlateCarree(), label='Kumejima Obs')
# ax.scatter(kumejima_lon, kumejima_lat, color='red', marker='*', s=300, transform=ccrs.PlateCarree(), label='Kumejima Obs')

# 새로운 좌표 위치 표시
# new_lat = 26.33999999999976
# new_lon = 126.79999999999805
# ax.scatter(new_lon, new_lat, color='white', marker='x', s=100, transform=ccrs.PlateCarree(), label='GAHM coordinate')

ax.legend()

# 축 라벨 및 제목 추가
ax.set_xlabel('Longitude [°E]', fontsize=15)
ax.set_ylabel('Latitude [°N]', fontsize=15)
ax.set_title(f'{tc_name}({tc_year})', fontsize=20)

# 그리드 라인 추가
gl = ax.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

plt.show()
plt.close(fig)  # 메모리 해제를 위해 그림 닫기

# %%
