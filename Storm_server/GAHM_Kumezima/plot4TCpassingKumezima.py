# ===================================================================
# Kumezima 
# 26.3366°N 126.8033°E
# 20000101 ~ 20231231
# 경도 125 ~ 130 
# 위도 25 ~ 30 
# 위 격자를 지나는 태풍 조사 후 플러팅
# [b'BOLAVEN', b'JELAWAT', b'SAOMAI', b'BOPHA', b'YAGI', b'XANGSANE',
#        b'NOT_NAMED', b'CIMARON', b'NARI', b'HAIYAN', b'NOGURI',
#        b'RAMMASUN', b'HALONG', b'NAKRI', b'RUSA', b'SINLAKU', b'KUJIRA',
#        b'SOUDELOR', b'ETAU', b'MAEMI', b'CHOI-WAN', b'NOT_NAMED',
#        b'MELOR', b'CONSON', b'DIANMU', b'MEGI', b'CHABA', b'SONGDA',
#        b'MEARI', b'TOKAGE', b'NOCK-TEN', b'EWINIAR', b'SAOMAI',
#        b'SHANSHAN', b'MAN-YI', b'NARI', b'NOT_NAMED', b'SINLAKU',
#        b'JANGMI', b'CHAN-HOM', b'LUPIT', b'NOT_NAMED', b'DIANMU',
#        b'KOMPASU', b'MALOU', b'CHABA', b'AERE', b'SONGDA', b'MUIFA',
#        b'KULAP', b'ROKE', b'MAWAR', b'GUCHOL', b'KHANUN', b'HAIKUI',
#        b'BOLAVEN', b'SANBA', b'JELAWAT', b'PRAPIROON', b'LEEPI',
#        b'NOT_NAMED', b'TORAJI', b'FITOW', b'DANAS', b'FRANCISCO',
#        b'HAGIBIS', b'NEOGURI', b'NAKRI', b'FENGSHEN', b'VONGFONG',
#        b'NOUL', b'CHAN-HOM', b'HALOLA', b'GONI', b'NOT_NAMED', b'MALOU',
#        b'MALAKAS', b'CHABA', b'HAIMA', b'NANMADOL', b'TALIM', b'SAOLA',
#        b'NOT_NAMED', b'GAEMI', b'PRAPIROON', b'AMPIL', b'JONGDARI',
#        b'YAGI', b'RUMBIA', b'SOULIK', b'TRAMI', b'KONG-REY', b'SEPAT',
#        b'LINGLING', b'NOT_NAMED', b'TAPAH', b'FUNG-WONG', b'JANGMI',
#        b'BAVI', b'MAYSAK', b'CHOI-WAN', b'IN-FA', b'LUPIT', b'MIRINAE',
#        b'OMAIS', b'AERE', b'SONGDA', b'HINNAMNOR', b'MAWAR', b'KHANUN']
# ===================================================================
#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# %%
ds = xr.open_dataset('/home/tkdals/homework_3/IBTrACS.WP.v04r00.nc')
ds
# %%
ds_fitered = ds.where((ds.season >= 2000) & (ds.season <= 2023), drop=True)
ds_fitered.time.data
# %%
ibtracks_lon = ds_fitered.lon.data
ibtracks_lat = ds_fitered.lat.data
# %%
kumaegiwa_passed_tc_list = []

for i in range(0, len(ibtracks_lon)):
    for j in range(0, len(ibtracks_lon[i])):
        tc_lon = ibtracks_lon[i][j]
        tc_lat = ibtracks_lat[i][j]
        if (tc_lon >= 125) & (tc_lon <= 130) & (tc_lat >=25) & (tc_lat <= 30):
            tc_sid = ds_fitered.sid.data[i]
            print(tc_sid)
            kumaegiwa_passed_tc_list.append(tc_sid)
            print('=====================================================')
            break

# %%
condi = ds_fitered.sid.isin(kumaegiwa_passed_tc_list)
# %%
kumaegiwa_IBTrACKs_tc = ds_fitered.where(condi, drop=True)
# %%
kumaegiwa_IBTrACKs_tc.lon.data[0]
kumaegiwa_IBTrACKs_tc.lat.data[0]
# %%
lon_data = kumaegiwa_IBTrACKs_tc.lon.data
lat_data = kumaegiwa_IBTrACKs_tc.lat.data

fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
# 그리드 추가 및 격자선 설정
ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle='--')
# 특정 경위도 범위의 격자를 빨간색으로 표시
red_gridlines = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                             linewidth=1, color='red', alpha=0.6, linestyle='--')
red_gridlines.xlocator = plt.FixedLocator([125, 130])
red_gridlines.ylocator = plt.FixedLocator([25, 30])

ax.coastlines()
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
ax.add_feature(cfeature.OCEAN, zorder=0)
ax.set_extent([100, 150, 5, 50], crs=ccrs.PlateCarree())

# 각 태풍의 경로를 지도에 플로팅
for i in range(len(lon_data)):
    
    ax.plot(lon_data[i], lat_data[i], color='black', linewidth=0.5, transform=ccrs.PlateCarree())

plt.suptitle('Typhoons Passing Through Kumezima(total number of Tc 110)')
plt.savefig('/home/tkdals/web_crowlling/Typhoons Passing Through Kumezima(total 110).pdf')
plt.title('Typhoons Passing Through Kumezima(total number of Tc 110)')
plt.show()
# %%
len(lat_data)
# %%
kumaegiwa_IBTrACKs_tc.name.data
kumaegiwa_IBTrACKs_tc.sid.data
# %%
kumaegiwa_IBTrACKs_tc.usa_wind.data
# %%
