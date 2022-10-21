# Library imports
import streamlit as st
import os
from datetime import datetime, time, date
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static

# Sidebar
with st.sidebar:

    st.title('Data Camp October 2022')
    col1, col2, col3 = st.columns(3)
    #col2.image(Image.open('taxi.jpg'))
    st.sidebar.image('taxi.jpg')
    st.info("This project has been realized during the Data Camp, by 3 EFREI students from DAI major. Find below their LinkedIn links.")
    icon_size = 20


    st.title('Team members')
    st.write("[Kadidia Coulibaly](https://www.linkedin.com/in/kadidia-coulibaly-b2383b217/)")
    st.write("[Alysson Rodriguez](https://www.linkedin.com/in/alysson-rodriguez-6b444a1b7/)")
    st.write("[Victor Brouard](https://www.linkedin.com/in/victor-brouard-4585b5222/)")

    st.title('Where to find our web app ?')
    st.write("[Github repository](https://github.com/ckmaguy/Data-camp-project-2022)")

# Center Page
st.title('Taxi drivers project')
st.write('')
st.image('ban.jpg')

with st.expander("Beijing info"):
    st.write('Beijing is a city in China that was ranked as the most congested city in China, with the lowest commuting speed during peak hours, according to a 2021 report from Baidu Maps.')

st.write(' How can you avoid traffic jams or optimize your car journey?')
st.write('That\'s the problem we\'re trying to solve with our project.')

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
