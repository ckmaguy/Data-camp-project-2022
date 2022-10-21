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



