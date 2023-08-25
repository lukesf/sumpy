#
# To fix timezone:
# pi@littledog:/usr/local $ sudo vi ./lib/python3.7/dist-packages/streamlit/elements/altair.py 
# change alt. utc to alt.Undefined
#
import glob
import os
import math
import time
import numpy as np
import streamlit as st
import pandas as pd
from datetime import datetime

def get_last_n_days_files(fpath,days):
    list_of_files = glob.glob(fpath) # * means all if need specific format then *.csv
    files = sorted(list_of_files, key=os.path.getctime) 
    return files[-days:]

def get_last_n_hours_readings(hours):
    sump_path = "/home/pi/raspi-sump/csv/waterlevel-*.csv"
    days = 1 + math.ceil(hours/24.)
    last_files = get_last_n_days_files(sump_path, days)
    li = []

    for filename in last_files:
        date = filename.strip('/home/pi/raspi-sump/csv/waterlevel-').strip('.csv')
        my_parser = lambda ti: datetime.strptime(date+" EST "+ti, '%Y%m%d %Z %H:%M:%S')
        df = pd.read_csv(filename, names=['ti','level'], parse_dates=['ti'], date_parser=my_parser)
        li.append(df)
    frame = pd.concat(li, ignore_index=True)
    return frame.tail(hours*60)

# Reading one large file
def get_last_n_hours_temps(hours):
    temp_path = "/home/pi/raspi-sump/csv/temp.csv"
    my_parser = lambda ti: datetime.strptime(ti, '%Y-%m-%d %H:%M:%S')
    frame = pd.read_csv(temp_path, names=['ti','c','f'], parse_dates=['ti'], date_parser=my_parser)
    return frame.tail(hours*60)

# Reading individual dated files
def get_last_n_hours_temp_files(hours):
    temp_path = "/home/pi/raspi-sump/csv/*-temp.csv"
    days = 1 + math.ceil(hours/24.)
    last_files = get_last_n_days_files(temp_path, days)
    li = []

    my_parser = lambda ti: datetime.strptime(ti, '%Y-%m-%d %H:%M:%S')
    for filename in last_files:
        df = pd.read_csv(filename, names=['ti','c','f'], parse_dates=['ti'], date_parser=my_parser)
        li.append(df)
    frame = pd.concat(li, ignore_index=True)
    return frame.tail(hours*60)



st.title("**Sump dashboard**")
option = st.selectbox('Time range (hours)', ('1', '6', '24', '72'))
st.write('You selected:', option)

df = get_last_n_hours_readings(int(option))
#print(df)
#print(df['ti'].iloc[0])
df['ti'] = df['ti'].dt.tz_localize("US/Eastern")

df = df.set_index('ti')

st.line_chart(df)
st.dataframe(df[::-1].head(30))


temp = get_last_n_hours_temp_files(int(option))
temp['ti'] = temp['ti'].dt.tz_localize("US/Eastern")
temp['c'].astype(float)
temp=temp[['ti','c']]
temp = temp.set_index('ti')
#temp = temp.sort_index()

st.line_chart(temp)
st.dataframe(temp[::-1].head(30))
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

