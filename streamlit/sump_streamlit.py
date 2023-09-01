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
import matplotlib.pyplot as plt

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
        df = pd.read_csv(filename, names=['ti','level'])
        df['ti'] = pd.to_datetime(date + " EST " + df['ti'], format='%Y%m%d %Z %H:%M:%S')
        li.append(df)
    frame = pd.concat(li, ignore_index=True)
    return frame.tail(hours*60)

# Reading one large file
def get_last_n_hours_temps(hours):
    temp_path = "/home/pi/raspi-sump/csv/temp.csv"
    frame = pd.read_csv(temp_path, names=['ti','c','f'])
    frame['ti'] = pd.to_datetime(frame['ti'], format='%Y-%m-%d %H:%M:%S')
    return frame.tail(hours*60)

# Reading individual dated files
def get_last_n_hours_temp_files(hours):
    temp_path = "/home/pi/raspi-sump/csv/*-temp.csv"
    days = 1 + math.ceil(hours/24.)
    last_files = get_last_n_days_files(temp_path, days)
    li = []

    for filename in last_files:
        df = pd.read_csv(filename, names=['ti','c','f'])
        df['ti'] = pd.to_datetime(df['ti'], format='%Y-%m-%d %H:%M:%S')
        li.append(df)
    frame = pd.concat(li, ignore_index=True)
    return frame.tail(hours*60)



st.title("**Sump dashboard**")
option = st.selectbox('Time range (hours)', ('1', '6', '24', '72'))
st.write('You selected:', option)

df = get_last_n_hours_readings(int(option))
#print(df)
#print(df['ti'].iloc[0])
#df['ti'] = df['ti'].dt.tz_localize("US/Eastern")


### BOO line_chart stopped working 
#df = df.set_index('ti')
#st.line_chart(df)
###
# Using matplotlib instead

# Define X and Y variable data
x = df['ti'].to_numpy()
y = df['level'].to_numpy()
# Make plot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("Time")  # add X-axis label
ax.set_ylabel("Centermeters")  # add Y-axis label
ax.set_title("Water level")  # add title
ax.grid(True)
st.pyplot(fig)


st.dataframe(df[::-1].head(30))
#print(df[::-1].head(30))


temp = get_last_n_hours_temp_files(int(option))
temp['ti'] = temp['ti'].dt.tz_localize("US/Eastern")
temp['c'].astype(float)
temp=temp[['ti','c']]
#temp = temp.sort_index()

### BOO line_chart stopped working 
#temp = temp.set_index('ti')
#st.line_chart(temp)
###
# Using matplotlib instead

# Define X and Y variable data
x = temp['ti'].to_numpy()
y = temp['c'].to_numpy()
# Make plot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("Time")  # add X-axis label
ax.set_ylabel("Celsius")  # add Y-axis label
ax.set_title("Temperature")  # add title
ax.grid(True)
st.pyplot(fig)
st.dataframe(temp[::-1].head(30))
#print(temp[::-1].head(30))

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

