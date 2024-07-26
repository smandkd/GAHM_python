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

print(output_dir)
print(input_dir)

# 이미지 저장 경로
os.makedirs(output_dir, exist_ok=True)
press_count = len(os.listdir('press_processed'))
print(press_count)
#%%
first_file_num = 10001
last_file_num = first_file_num + press_count

for file_num in range(first_file_num, last_file_num):
# 파일 읽기 및 uwnd, vwnd 데이터 추출
    file_path = os.path.join(input_dir, f'fort.{file_num}')
    
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
    p = ax.pcolormesh(xx, yy, pressure, cmap='jet', shading='auto', transform=ccrs.PlateCarree(), vmin=980, vmax=1005)
    cb = plt.colorbar(p, ax=ax, orientation='vertical', pad=0.1)
    cb.set_label('Pressure (hPa)', fontsize=14)

    # 바람 벡터 필드 표시
    # ax.quiver(xx, yy, uwnd, vwnd, scale=500, transform=ccrs.PlateCarree())

    # 축 라벨 및 제목 추가
    ax.set_xlabel('Longitude [°E]', fontsize=15)
    ax.set_ylabel('Latitude [°N]', fontsize=15)
    ax.set_title(f'Pressure from fort.{file_num}', fontsize=20)

    # 그리드 라인 추가
    ax.gridlines(draw_labels=True)

    # 그림 저장
    output_file = os.path.join(output_dir, f'pressure_field_{file_num}.png')
    plt.savefig(output_file)
    plt.close(fig)  # 메모리 해제를 위해 그림 닫기

    print(f'Saved figure for fort.{file_num} as {output_file}')

# %%
