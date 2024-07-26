#%%
import numpy as np 
import pandas as pd
import os

#%%
current_dir = os.path.dirname(os.path.abspath(__file__))
press_output_dir = os.path.join(current_dir, 'press_processed')
wind_output_dir = os.path.join(current_dir, 'wind_processed')
press_input_dir = os.path.join(current_dir, 'press_processed')
wind_input_dir = os.path.join(current_dir, 'wind_processed')

file_count = len(os.listdir('press_processed'))
tc_name = current_dir.split('/')[6]
# %%
# 격자 생성
slon = 117
elon = 136
slat = 15
elat = 40
dres = 0.02

lon = np.arange(slon, elon, dres)
lat = np.arange(slat, elat, dres)
xx, yy = np.meshgrid(lon, lat)

# 새로 생성된 그리드에서 쿠메지마와 가장 가까운 그리드, 좌표 찾기
# 쿠메지마 좌표  
target_lat = 26.3366
target_lon = 126.8033

# %%
# 그리드에서 해당 좌표에 가장 가까운 그리드 셀을 찾기
distance = np.sqrt((xx - target_lon)**2 + (yy - target_lat)**2)
min_index = np.argmin(distance)
# %%
# 그리드 넘버 계산 (그리드는 행렬 형태로 되어 있으므로 행과 열의 인덱스가 필요)
grid_shape = xx.shape
grid_row, grid_col = np.unravel_index(min_index, grid_shape)
grid_number = grid_row * grid_shape[1] + grid_col

nearest_lat = lat[grid_row]
nearest_lon = lon[grid_col]
print(f'lat, lon nearest kumezima : {nearest_lat}, {nearest_lon}')
# %%
press_list = []
wind_list = []
hours_list = []

for file_num in range(10001, 10000+file_count):
    file_path_press = os.path.join(press_input_dir, f'fort.{file_num}')
    print(file_path_press)
    
    with open(file_path_press) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if int(parts[0]) == grid_number:
                pressure = float(parts[1])
                print(f'hour : {file_num}, matrix number : {parts[0]}, pressure : {pressure}')
                press_list.append(pressure)
                hours_list.append(file_num)
                break
    
    file_path_wind = os.path.join(wind_input_dir, f'fort.{file_num}')
    with open(file_path_wind) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if int(parts[0]) == grid_number:
                uwind = float(parts[1])
                vwind = float(parts[2])
                wind_speed = np.sqrt(uwind**2 + vwind**2)
                print(f'hour : {file_num}, matrix number : {parts[0]}, wind : {wind_speed}')
                wind_list.append(wind_speed)
                break
    
# %%
df = pd.DataFrame({'Hour': hours_list, 'Pressure': press_list, 'Wind': wind_list})
df.to_csv(f'{current_dir}/{tc_name}_pressure_wind_data.csv', index=False)
print("Data has been saved to pressure_data.csv")
print("Final pressure list:", press_list)

# %%
