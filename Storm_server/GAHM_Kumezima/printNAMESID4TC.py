#%%
import xarray as xr
import pandas as pd
# %%
tc_list = [
b'2004156N16117',
b'2004227N15141',
b'2004263N13153',
b'2006180N06140',
b'2007188N04148',
b'2007254N18140',
b'2011140N08142',
b'2011208N09145',
b'2012263N15141',
b'2015122N07144',
b'2015226N12151',
b'2016269N15165',
b'2018179N19134',
b'2018263N12146',
b'2018271N06154',
b'2019322N11144',
b'2020239N13134']
# %%
ds = xr.open_dataset('/home/tkdals/homework_3/IBTrACS.WP.v04r00.nc')
ds_fitered = ds.where((ds.season >= 2000) & (ds.season <= 2023), drop=True)
# %%
# Filter the dataset based on the tc_list
passing_kumezima_tc = ds_fitered.where(ds_fitered.sid.isin(tc_list), drop=True)# %%

# %%
passing_kumezima_tc.sid
# %%
tc_names_and_sids = pd.DataFrame({
    'Name': passing_kumezima_tc.name.values,
    'SID': passing_kumezima_tc.sid.values,
    'Date': passing_kumezima_tc.season.values,
})

# Print the DataFrame
print(tc_names_and_sids)
# %%
