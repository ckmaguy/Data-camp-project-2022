import os
import streamlit as st
from datetime import datetime, time, date
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static

# Density Visualization

st.header('Car Density')

directory = 'taxi_log_2008_by_id'
dateparse = lambda dates: [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in dates]

taxis2 = []

lst = os.listdir(directory)
for filename in lst:
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        if 50000 <= os.path.getsize(f) <= 55000:
            df = pd.read_csv(f, sep=',', names=["id", "time", "longitude", "latitude"], date_parser=dateparse,
                             parse_dates=[1], decimal=".", header=None)
            taxis2.append(df)

data2 = pd.concat(taxis2)
df = data2
df["longitude"] = pd.to_numeric(df["longitude"])
df["latitude"] = pd.to_numeric(df["latitude"])
df = df[df.latitude <= 41]
df = df[df.latitude >= 39]
df = df[df.longitude >= 116]
df = df[df.longitude <= 117]
data2 = df

date = st.slider(
    "Select the date :",
    min_value=date(2008, 2, 2),
    max_value=date(2008, 2, 8),
    format="YYYY-MM-DD")

hour_range = st.slider(
    "Select the time range:",
    value=(time(12, 30), time(18, 30)))
start = datetime.combine(date, hour_range[0])
end = datetime.combine(date, hour_range[1])
df = df[df['time'] >= start]
df = df[df['time'] <= end]

st.map(df[['longitude', 'latitude']])

st.subheader('How does it look like with a heatmap ?')


hmap = folium.Map(location=[39.8, 116.6], zoom_start=9)

hm_wide = HeatMap(list(zip(df.latitude.values, df.longitude.values)),
                  min_opacity=0.35,
                  radius=17, blur=10,
                  max_zoom=1,
                  )

hmap.add_child(hm_wide)

st_folium(hmap)

st.caption('The highest congested zone can be seen in red, they\'re majorly located at the center of the map' )
