#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
#%%
# 데이터 로드 및 전처리
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['날짜 및 시간'] = df['날짜 및 시간'].str.replace(' 24:00', ' 00:00')
    df['날짜 및 시간'] = pd.to_datetime(df['날짜 및 시간'], errors='coerce')
    df['날짜 및 시간'] = df['날짜 및 시간'] + pd.to_timedelta(df['날짜 및 시간'].dt.hour.eq(0).astype(int), unit='D')
    return df

# 시간 필터링
def filter_data_by_time(df, start_date_utc, end_date_utc):
    start_date_jst = pd.to_datetime(start_date_utc) + pd.Timedelta(hours=9)
    end_date_jst = pd.to_datetime(end_date_utc) + pd.Timedelta(hours=9)
    print(f'UTC date : {start_date_utc}, {end_date_utc}')
    print('Change to JST:')
    print(f'JST date : {start_date_jst}, {end_date_jst}')
    
    mask = (df['날짜 및 시간'] >= start_date_jst) & (df['날짜 및 시간'] <= end_date_jst)
    filtered_data = df.loc[mask, ['날짜 및 시간', '해수면기압(hPa)', '풍속(m/s)']]
    filtered_data.columns = ['date', 'pressure', 'wind']
    filtered_data['date'] = filtered_data['date'] - pd.Timedelta(hours=9)
    return filtered_data

# 그래프 그리기
def plot_data(df_jma, df, start_date_utc, end_date_utc, xtick_start, xtick_end, output_image_path):
    time_interval = '1H'
    time_array = pd.date_range(start=start_date_utc, end=end_date_utc, freq=time_interval)

    df_jma_filtered = df_jma[df_jma['date'].isin(time_array)]
    df_filtered = df[df['date'].isin(time_array)]

    df_jma_filtered = df_jma_filtered.set_index('date').reindex(time_array).reset_index()
    df_filtered = df_filtered.set_index('date').reindex(time_array).reset_index()

    plt.figure(figsize=(14, 8))
    plt.plot(time_array, df_jma_filtered['wind'], color='grey', label='Obs.')
    plt.plot(time_array, df_filtered['Wind'], color='blue', label='Model')

    plt.xlabel('Date', fontsize='21')
    plt.xticks(pd.date_range(xtick_start, xtick_end, freq='h'), fontsize=14)
    plt.ylabel('Wind(m/s)', fontsize='21')
    plt.yticks(np.arange(0, 80, 10), fontsize='14')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.legend(loc='upper left', fontsize=17)
    plt.title('Kumezima (26.35°N 126.80°E)', fontsize='21')
    plt.savefig(output_image_path + '_wind.png')
    plt.show()

    plt.figure(figsize=(14, 8))
    plt.plot(time_array, df_jma_filtered['pressure'], color='grey', label='Obs.')
    plt.plot(time_array, df_filtered['Pressure'], color='red', label='Model')

    plt.xlabel('Date', fontsize='21')
    plt.xticks(pd.date_range(xtick_start, xtick_end, freq='h'), fontsize=14)
    plt.ylabel('Sea Surface Pressure(hPa)', fontsize='21')
    plt.yticks(np.arange(950, 1020, 20), fontsize='14')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.legend(loc='lower left', fontsize=17)
    plt.title('Kumezima (26.35°N 126.80°E)', fontsize='21')
    plt.savefig(output_image_path + '_pressure.png')
    plt.show()

# 주어진 압력에 해당하는 시간을 찾기
def find_time_for_target_pressure(df, target_pressure, xtick_start):
    matching_rows = df[df['Pressure'] == target_pressure]

    if not matching_rows.empty:
        for index, row in matching_rows.iterrows():
            print(f"Time corresponding to pressure {target_pressure}: {row['Hour']}")
            initial_time = datetime.strptime(xtick_start, '%Y-%m-%d %H:%M')
            time_delta = timedelta(hours=int(row['Hour'] - 10000))
            new_time = initial_time + time_delta - timedelta(hours=1)
            print("Initial time:", initial_time.strftime('%Y-%m-%d %H:%M:%S'))
            print("New time:", new_time.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print(f"No matching rows found for pressure {target_pressure}")
#%%
file_path = '/home/tkdals/GAHM_Kumezima/Data/JMAdata쿠메지마.csv'
filtered_tc_csv_file_path = '/home/tkdals/GAHM_Kumezima/Data/filtered_jma_data_Trami_2.csv'
tc_press_wind_csv_from_hurri_path = '/home/tkdals/GAHM_Kumezima/Data/Trami_2_pressure_wind_data.csv'
output_image_path = '/home/tkdals/GAHM_Kumezima/Figure/Trami_2VSObs'

df = load_and_preprocess_data(file_path)
start_date_utc = '2018-09-22 00:00'
end_date_utc = '2018-10-01 00:00'

df_jma = filter_data_by_time(df, start_date_utc, end_date_utc)
df_jma.to_csv(filtered_tc_csv_file_path, index=False)

df_jma = pd.read_csv(filtered_tc_csv_file_path)
df = pd.read_csv(tc_press_wind_csv_from_hurri_path)
df_jma['date'] = pd.to_datetime(df_jma['date'], errors='coerce')
df['date'] = pd.to_datetime(df['Hour'] - 10001, unit='h', origin=pd.Timestamp(start_date_utc))

xtick_start = '2018-09-22'
xtick_end = '2018-10-01'
plot_data(df_jma, df, start_date_utc, end_date_utc, xtick_start, xtick_end, output_image_path)

target_pressure = df['Pressure'].min()
find_time_for_target_pressure(df, target_pressure, start_date_utc)

df
# %%
df_jma
# %%
df
# %%
