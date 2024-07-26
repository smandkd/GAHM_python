#%%
import numpy as np
import pandas as pd
import os 

# %%
def openDataframe(tc_name, jma_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir,'Data')
    jma_dir = os.path.join(data_dir, jma_name)
    tc_dir = os.path.join(data_dir, tc_name)
    df_tc = pd.read_csv(tc_dir)
    df_jma = pd.read_csv(jma_dir)

    return df_tc, df_jma
#%%

tc_df_name = 'Trami_pressure_wind_data.csv'
jma_df_name = 'filtered_jma_data_Trami.csv'

df_tc, df_jma = openDataframe(tc_df_name, jma_df_name)
#%%
len_df_jma_pressure = len(df_jma['pressure'])
#%%
len(df_jma['pressure'].iloc[0:215])
df_jma['pressure'].iloc[0:215]


# %%
tc_pressure_arr = np.array(df_tc['Pressure'])
jma_pressure_arr = np.array(df_jma['pressure'].iloc[0:215])
# %%
gap_tc_jma_press = jma_pressure_arr - tc_pressure_arr

# %%
gap_tc_jma_press.max()
# %%
gap_tc_jma_press.min()
# %%
gap_tc_jma_press.mean()
# %%
