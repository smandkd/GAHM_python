#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy import geodesic
from shapely.geometry import Polygon
from datetime import datetime, timedelta
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# 데이터 로드
ds = xr.open_dataset('/home/tkdals/homework_3/IBTrACS.WP.v04r00.nc')

# 쿠메지마 관측소의 좌표
kumejima_lat = 26.3366
kumejima_lon = 126.8033

# 2000년부터 2023년까지의 데이터 필터링
ds_filtered = ds.where((ds.season >= 2000) & (ds.season <= 2023), drop=True)
tc_chaba = ds_filtered.where(ds_filtered.sid == b'2016269N15165', drop=True)

lon = tc_chaba.lon.data[0]
lat = tc_chaba.lat.data[0]
time_data = tc_chaba.time.data[0]

# 유효한 경도, 위도, 시간 데이터 필터링
valid_idx = ~np.isnan(lat) & ~np.isnan(lon) & ~np.isnan(time_data)
valid_lon = lon[valid_idx]
valid_lat = lat[valid_idx]
valid_time = time_data[valid_idx]

# 날짜 데이터 변환
time_format = '%Y-%m-%dT%H:%M:%S.%f'
time_data_str = valid_time.astype(str)
formatted_date_array = []

# 각 날짜 값을 원하는 형식으로 변환
for date_str in time_data_str:
    date_str_trimmed = date_str.split('.')[0]
    date_obj = datetime.strptime(date_str_trimmed, '%Y-%m-%dT%H:%M:%S')
    formatted_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    formatted_date_array.append(formatted_date_str)

# 2일 간격으로 날짜 필터링
date_format = '%Y-%m-%d %H:%M:%S'
dates = [datetime.strptime(date, date_format) for date in formatted_date_array]
filtered_indices = [0]  # 첫 번째 날짜는 항상 포함
for i in range(1, len(dates)):
    if (dates[i] - dates[filtered_indices[-1]]).days >= 1:
        filtered_indices.append(i)

filtered_lon = valid_lon[filtered_indices]
filtered_lat = valid_lat[filtered_indices]
filtered_dates = [formatted_date_array[i] for i in filtered_indices]

# 지도 설정
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})
ax.set_extent([115, 170, 10, 50], crs=ccrs.PlateCarree())

# 해안선 및 지형 추가
ax.coastlines(color='black', linewidth=1.5)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)

# 태풍 진로 표시 (얇은 검은색 선)
ax.plot(valid_lon, valid_lat, color='black', linewidth=1, transform=ccrs.PlateCarree())

# 쿠메지마로부터 반경 100km의 원 그리기
g = geodesic.Geodesic()
circle = g.circle(lon=kumejima_lon, lat=kumejima_lat, radius=100*1000)  # radius in meters
ax.add_geometries([Polygon(circle)], ccrs.PlateCarree(), facecolor='none', edgecolor='red', linewidth=1)

# 날짜 레이블 추가 및 좌표에 점 표시
ax.scatter(filtered_lon, filtered_lat, color='red', zorder=5, transform=ccrs.PlateCarree())
for lon, lat, date in zip(filtered_lon, filtered_lat, filtered_dates):
    ax.text(lon - 0.3, lat + 0.5, date.split(' ')[0], fontsize=10, ha='right', transform=ccrs.PlateCarree())

# 축 라벨 및 제목 추가
ax.set_xlabel('Longitude [°E]', fontsize=15)
ax.set_ylabel('Latitude [°N]', fontsize=15)
ax.set_title('Chaba(2016) Track with Dates', fontsize=20)

# 그리드 라인 추가
gl = ax.gridlines(draw_labels=True)
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()

# 지도 보여주기
plt.show()
# %%
combined_ecco2_lat = np.concatenate(ecco2_lat)
combined_ecco2_lon = np.concatenate(ecco2_lon)
haitang_center_points_lon = df_tc.usa_lon
haitang_center_points_lat = df_tc.usa_lat
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Set map extent to cover the area of interest  
ax.set_extent([100, 180, 1, 40], crs=ccrs.PlateCarree())

# Add map features for clarity and context
ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='gray')
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor='black')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.LAND, facecolor='lightgreen', edgecolor='black', zorder=1)

# Define the coordinates to be plotted (these are sample coordinates)
# Plot the points on the map with a different color and size for distinction
ax.scatter(combined_ecco2_lon, combined_ecco2_lat, color='red', s=50, transform=ccrs.PlateCarree(), label='input area')
ax.scatter(haitang_center_points_lon, haitang_center_points_lat, color='black', s=5, transform=ccrs.PlateCarree(), label='Typhoon Track Centers')

# Add titles, labels, and a legend
ax.set_title("Typhoon Haitang Affected Coordinates")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.legend(loc='upper left')

# Save and show the plot
plt.savefig("haitang_track_intensity_modified.pdf")
plt.show()