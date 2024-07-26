# ==========================================================
# 쿠메지마로부터 반경 100km 영역을 지나는 태풍 필터링
# 또한 usa_r34,50,64 자료 없으면 드랍(총 17개 태풍만 남음).
# 그 후 트랙 플로팅하고 
# 이 태풍 중 가장 강한 태풍은 CHABA
# ==========================================================


#%%
import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from cartopy import geodesic

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
#%%
# Haversine 공식을 사용하여 두 지점 간의 거리를 계산하는 함수
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # 지구의 반지름 (km)
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c
    return distance
# %%
# 쿠메지마 관측소의 좌표
kumejima_lat = 26.3366
kumejima_lon = 126.8033
# %%
# 데이터 로드
ds = xr.open_dataset('/home/tkdals/homework_3/IBTrACS.WP.v04r00.nc')

# %%
# 2000년부터 2023년까지의 데이터 필터링
ds_filtered = ds.where((ds.season >= 2000) & (ds.season <= 2023), drop=True)

# %%
# 쿠메지마로부터 반경 100km 내의 영역을 지나는 태풍 리스트
kumejima_passed_tc_list = []
# 태풍 경로의 경도 및 위도 데이터
ibtracks_lon = ds_filtered.lon.data
ibtracks_lat = ds_filtered.lat.data
# %%
for i in range(len(ibtracks_lon)):
    for j in range(len(ibtracks_lon[i])):
        tc_lon = ibtracks_lon[i][j]
        tc_lat = ibtracks_lat[i][j]
        if np.isnan(tc_lon) or np.isnan(tc_lat):
            continue
        distance = haversine(tc_lon, tc_lat, kumejima_lon, kumejima_lat)
        if distance <= 100:
            tc_sid = ds_filtered.sid.data[i]
            tc_ds = ds_filtered.where(ds_filtered.sid == tc_sid, drop=True)
            if not np.all(np.isnan(tc_ds.usa_r34.data)):
                if not np.all(np.isnan(tc_ds.usa_r50.data)):
                    if not np.all(np.isnan(tc_ds.usa_r64.data)):
                        print(f'sid : {tc_sid} distance : {distance}')
                        print(distance)
                        kumejima_passed_tc_list.append(tc_sid)
                        print('=====================================================')
                    break
                break
            break

print("Total number of typhoons passing within 100km of Kumejima with non-nan usa_r34 values: ", len(kumejima_passed_tc_list))
#%%
kumejima_passed_tc_list
# %%
condi = ds_filtered.sid.isin(kumejima_passed_tc_list)

kumaegiwa_IBTrACKs_tc = ds_filtered.where(condi, drop=True)
kumaegiwa_IBTrACKs_tc.lon.data[0]
kumaegiwa_IBTrACKs_tc.lat.data[0]
lon_data = kumaegiwa_IBTrACKs_tc.lon.data
lat_data = kumaegiwa_IBTrACKs_tc.lat.data

fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
# 그리드 추가 및 격자선 설정
ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle='--')
ax.coastlines()
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
ax.add_feature(cfeature.OCEAN, zorder=0)
ax.set_extent([115, 140, 10, 40], crs=ccrs.PlateCarree())

# 각 태풍의 경로를 지도에 플로팅
for i in range(len(lon_data)):
    ax.plot(lon_data[i], lat_data[i], color='black', linewidth=0.5, transform=ccrs.PlateCarree())

g = geodesic.Geodesic()
circle = g.circle(lon=kumejima_lon, lat=kumejima_lat, radius=100*1000)  # radius in meters
ax.add_geometries([Polygon(circle)], ccrs.PlateCarree(), facecolor='none', edgecolor='red', linewidth=1)

plt.suptitle('Typhoons Passing Through Kumezima 2(total number of Tc 17)')
plt.savefig('/home/tkdals/web_crowlling/Typhoons Passing Through Kumezima 2(total 17).png')
plt.title('Typhoons Passing Through Kumezima(total number of Tc 17)')
plt.show()
# %%
# usa_wind 최대값 찾기
max_wind_speed = -np.inf
max_wind_tc_sid = None

for sid in kumejima_passed_tc_list:
    tc_ds = ds_filtered.where(ds_filtered.sid == sid, drop=True)
    max_wind = np.nanmax(tc_ds.usa_wind.data[0])
    if max_wind > max_wind_speed:
        max_wind_speed = max_wind
        max_wind_tc_sid = sid

print(f"The typhoon with the maximum usa_wind value is: {max_wind_tc_sid}")
print(f"The maximum usa_wind value is: {max_wind_speed}")
# The typhoon with the maximum usa_wind value is: b'2016269N15165', CHABA
# The maximum usa_wind value is: 150.0
# distance from Kumezima : 59
#%%
