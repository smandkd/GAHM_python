#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
# %%
file_path_jma = '/home/tkdals/GAHM_JMA/Data/filtered_jma_data_Manyi.csv'
file_path = '/home/tkdals/GAHM_JMA/Data/Manyi_pressure_wind_data.csv'
df_jma = pd.read_csv(file_path_jma)
df = pd.read_csv(file_path)

df_jma['date'] = pd.to_datetime(df_jma['date'], errors='coerce')
df['date'] = pd.to_datetime(df['Hour']-10001, unit='h', origin=pd.Timestamp('2007-07-10 00:00')) 
df['date']
#%%
file_path_jma = '/home/tkdals/GAHM_JMA/Data/filtered_jma_data_Nari.csv'
df_jma = pd.read_csv(file_path_jma)
df_jma['date'] = pd.to_datetime(df_jma['date'], errors='coerce')
#%%
# 시간 범위 설정
start_date_utc = '2007-09-13 12:00'
end_date_utc = '2007-09-16 12:00'
time_interval = '1H'
time_array = pd.date_range(start=start_date_utc, end=end_date_utc, freq=time_interval)

# 시간 범위에 해당하는 데이터 필터링
df_jma_filtered = df_jma[df_jma['date'].isin(time_array)]
df_filtered = df[df['date'].isin(time_array)]

# 시간 배열과 데이터 매칭
df_jma_filtered = df_jma_filtered.set_index('date').reindex(time_array).reset_index()
df_filtered = df_filtered.set_index('date').reindex(time_array).reset_index()

#%%
plt.figure(figsize=(14, 8))
plt.plot(time_array, df_jma_filtered['pressure'], color='grey', label='Obs.')
plt.plot(time_array, df_filtered['Pressure'], color='red', label='Model')

# plt.figure(figsize=(14, 8))
# plt.plot(df_jma['date'], df_jma['pressure'], color='grey', label='Obs.')
# plt.plot(df_jma['date'], df['Pressure'], color='red', label='Model')

plt.xlabel('Date', fontsize='21')
plt.xticks(pd.date_range(start='2007-09-13', end='2007-09-16', freq='h'), fontsize=14)
plt.ylabel('Sea Surface Pressure(hPa)', fontsize='21')
plt.yticks(np.arange(950, 1020, 20), fontsize='14')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.legend(loc='lower left', fontsize=17)
plt.title('Kumezima (26.35°N 126.80°E)', fontsize='21')
# 그래프를 이미지 파일로 저장 (옵션)
output_image_path = '/home/tkdals/GAHM_JMA/Figure/Nari_splineVSobs_pressure.png'
plt.savefig(output_image_path)

# 그래프를 화면에 표시
plt.show()

# %%
df['Pressure'].min() 
# Ewiniar : 988.9494018554688
# %%
file_path = '/home/tkdals/GAHM_JMA/Data/Nari_interp_pressure_wind_data.csv'
df = pd.read_csv(file_path)
df.head(10)
# %%
target_pressure = df['Pressure'].min()
matching_rows = df[df['Pressure'] == target_pressure]

if not matching_rows.empty:
    for index, row in matching_rows.iterrows():
        print(f"Time corresponding to pressure {target_pressure}: {row['Hour']}")
        print(int(row['Hour']-10000))
        initial_time_str = '2007091312'
        initial_time = datetime.strptime(initial_time_str, '%Y%m%d%H')
        
        time_delta = timedelta(hours=int(row['Hour']-10000))
        new_time = initial_time + time_delta
        print("Initial time:", initial_time.strftime('%Y-%m-%d %H:%M:%S'))
        print("new time:", new_time.strftime('%Y-%m-%d %H:%M:%S'))
else:
    print(f"No matching rows found for pressure {target_pressure}")

# fungwong : 10007
# chaba : 10040
# jelewat : 10228 Initial time: 2012-09-19 12:00:00 new time: 2012-09-29 00:00:00
# Nari spline : 10029 Initial time: 2007-09-13 12:00:00 new time: 2007-09-14 17:00:00
# %%
df.loc[df['date'].isin(df_jma['date']), 'Pressure']
# %%
df['date'].isin(df_jma['date'])
# %%
