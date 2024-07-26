#%%
import numpy as np
import pandas as pd
# %%
file_path = '/home/tkdals/GAHM_JMA/Data/JMAdata쿠메지마.csv'

df = pd.read_csv(file_path)
df.head(10)

# %%
# 시간 전처리
df['날짜 및 시간'] = df['날짜 및 시간'].str.replace(' 24:00', ' 00:00')

# 문자열 형식을 날짜 형식으로 변환
df['날짜 및 시간'] = pd.to_datetime(df['날짜 및 시간'], errors='coerce')

# '00:00' 시간을 가진 날짜를 다음 날로 이동
df['날짜 및 시간'] = df['날짜 및 시간'] + pd.to_timedelta(df['날짜 및 시간'].dt.hour.eq(0).astype(int), unit='D')

# %%
# JST 시간을 UTC 시간으로 변환
start_date_utc = '2018-09-22 00:00'
end_date_utc = '2018-10-01 00:00'

start_date_jst = pd.to_datetime(start_date_utc) + pd.Timedelta(hours=9)
end_date_jst = pd.to_datetime(end_date_utc) + pd.Timedelta(hours=9)
print(f'utc date : {start_date_utc}, {end_date_utc}')
print('change to')
print(f'jst date : {start_date_jst}, {end_date_jst}')
# 데이터 필터링
mask = (df['날짜 및 시간'] >= start_date_jst) & (df['날짜 및 시간'] <= end_date_jst)
filtered_data = df.loc[mask, ['날짜 및 시간', '해수면기압(hPa)', '풍속(m/s)']]

filtered_data.columns = ['date', 'pressure', 'wind']
df_jma = filtered_data.astype({'pressure': 'float'}, {'wind': 'float'})

df_jma['date'] = df_jma['date'] - pd.Timedelta(hours=9)
df_jma.head(10)
# %%
output_file_path = '/home/tkdals/GAHM_JMA/Data/filtered_jma_data_Trami.csv'
df_jma.to_csv(output_file_path, index=False)

print("Filtered data saved to:", output_file_path)
# %%
df = pd.read_csv('/home/tkdals/GAHM_JMA/Data/filtered_jma_data_Trami.csv')
# %%
df['pressure']
# %%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df['date'] = pd.to_datetime(df['date'], errors='coerce')

plt.plot(df['date'], df['pressure'], color='grey')

xtick_start = '2018-09-22'
xtick_end = '2018-10-01'
plt.xticks(pd.date_range(xtick_start, xtick_end, freq='h'), fontsize=14)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.show()
# %%
