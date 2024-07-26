# -*- coding: utf-8 -*-

"""
==================
Interp_track_hourly_final.py
==================

Author       : Youjung Oh
Origination  : 19-July-2024
Last update  : 19-July-2024

1. Purpose   : Interpolation of best-track data* using spline method
               best-track data*: JTWC (6 hourly) only for NWP TC
2. Input     : NWS_20_fort.22   - result of aswip
3. Output    : track_hourly.22  - will use for new Subr_GAHM.for

50번째 if 조건식에 typ==0 추가
-> 태풍 트랙 정보에서 EX 상태의 반경 정보가 0일 때가 있어 
   조건식 추가해줌 

"""
#%%
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta as dt
from scipy.interpolate import PchipInterpolator
from scipy.interpolate import interp1d
#%%
def myrange(start, end, step):
    r = start
    while (r < end):
        yield r
        r += step

def Load_NWS_20(fnm='NWS_20_fort.22'):

    with open(fnm) as f:
      data = f.readlines()

    lons, lats, times = [], [], []
    lonp, latp = 0, 0

    for line in data:
        ndate = str(line.split(',')[2].strip())
        yyl, mml, ddl, hhl = int(ndate[0:4]), int(ndate[4:6]), int(ndate[6:8]), int(ndate[8:10])
        ddate = datetime(yyl, mml, ddl, hhl)
        typ = int(line.split(',')[11].strip())
        latn = float(line.split(',')[6].replace('N', '').replace('S', '-')) * 0.1
        lonn = float(line.split(',')[7].replace('E', '').replace('W', '-')) * 0.1

        if (typ == 34 or typ == 0) and (lonn != lonp) and (latn != latp):
            lonp, latp = lonn, latn
            times.append(ddate)
            lons.append(lonn)
            lats.append(latn)

    return np.array(times), np.array(lons), np.array(lats)

def Save_track(times, lons, lats, ofnm='track_hourly.22'):
    with open(ofnm, 'w') as fw:
      for timed, lon, lat in zip(times, lons, lats):
        fw.write(f'{timed} {lon:8.2f}  {lat:8.2f}\n')

def Time_Count(sdate, edate, ddt=dt(hours=1)):
    return np.array(list(myrange(sdate, edate+dt(hours=1), ddt)))

def Compare_track(olons, olats, clons, clats):
    plt.figure(figsize=(8,6))
    plt.plot(olons, olats, '-o', color='.3', label='Original track')
    plt.plot(clons, clats, '-o', color='r', alpha=0.5, label='Converted track')
    plt.plot(olons, olats, 'o', color='k')
    plt.legend()
    plt.grid(True)
    plt.show()

def Compare_track_all(olons, olats, clons_spline, clats_spline, clons_linear, clats_linear):
    plt.figure(figsize=(8,6))
    plt.plot(olons, olats, '-o', color='.3', markersize=10, label='Original track')
    plt.plot(clons_spline, clats_spline, '-', color='r', markersize=8, alpha=0.5, label='Spline')
    plt.plot(clons_linear, clats_linear, '--', color='b', markersize=5, alpha=0.5, label='Linear')
    plt.legend()
    plt.grid(True)
    plt.show()


def Interp_NWS2hourly(org_times, new_times, lons, lats, Display=False):
    '''
    scipy.interpolate.PchipInterpolator
    : PCHIP 1-D monotonic cubic interpolation

    **** class PchipInterpolator(x, y, axis=0, extrapolate=None)
    x and y are arrays of values used to approximate some function f,
    with y = f(x). The interpolant uses monotonic cubic splines 
    to find the value of new points. 

    PCHIP stands for Piecewise Cubic Hermite Interpolating Polynpomial
    '''
    pchip_lat = PchipInterpolator(org_times, lats)
    pchip_lon = PchipInterpolator(org_times, lons)

    c_lats = pchip_lat(new_times)
    c_lons = pchip_lon(new_times)

    if Display == True:
      Compare_track(lons, lats, c_lons, c_lats)
    return c_lons, c_lats

def Interp_NWS2hourly_linear(org_times, new_times, lons, lats, Display=False):

    f_lon = interp1d(org_times, lons)
    f_lat = interp1d(org_times, lats)
    c_lons = f_lon(new_times)
    c_lats = f_lat(new_times)

    if Display == True:
      Compare_track(lons, lats, c_lons, c_lats)
    return c_lons, c_lats

def Main():

    times, lons, lats = Load_NWS_20()
    all_times = Time_Count(sdate=times[0], edate=times[len(times)-1])

    org_times = np.array([(t - times[0]).total_seconds() / 3600.0 for t in times])
    new_times = np.array([(t - times[0]).total_seconds() / 3600.0 for t in all_times])

    c_spline_lons, c_spline_lats = Interp_NWS2hourly(org_times, new_times, lons, lats, Display=False)
    c_linear_lons, c_linear_lats = Interp_NWS2hourly_linear(org_times, new_times, lons, lats, Display=False)

    Compare_track_all(lons, lats, c_spline_lons, c_spline_lats, c_linear_lons, c_linear_lats)

    new_timesd = np.array([t.strftime('%Y%m%d%H') for t in all_times])
    Save_track(new_timesd, c_spline_lons, c_spline_lats)
#%%
if __name__ == '__main__':

  Main()


# %%
