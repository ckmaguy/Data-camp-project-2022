import os
import streamlit as st
from datetime import datetime, time, date
import pandas as pd
import numpy as np
import pickle

directory = 'taxi_log_2008_by_id'
dateparse = lambda dates: [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in dates]
taxis = []

lst = os.listdir(directory)
n = 0
for filename in lst:
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        if 1024 <= os.path.getsize(f) <= 10240:
            df = pd.read_csv(f, sep=',', names=["id", "time", "longitude", "latitude"], date_parser=dateparse,
                             parse_dates=[1], decimal=".", header=None)
            taxis.append(df)
            n+=1

data = pd.concat(taxis)

df = data
df["longitude"] = pd.to_numeric(df["longitude"])
df["latitude"] = pd.to_numeric(df["latitude"])
df = df[df.latitude <= 41]
df = df[df.latitude >= 39]
df = df[df.longitude >= 116]
df = df[df.longitude <= 117]

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


############## GRAPHE ##############

class Node:
    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long


class Link:
    def __init__(self, n1, n2, weight):
        self.node1 = n1
        self.node2 = n2
        weight = weight


class Graph:
    nodes = []
    links = []
    def __init__(self):
        nb_node = 0
        nb_link = 0
    def add_node(self, n1):
        for n2 in self.nodes:
            if (round(n1.latitude, 4) == round(n2.latitude, 4)) and (round(n1.longitude, 4) == round(n2.longitude, 4)):
                print("A node near enough exists !")
                return n2
        self.nodes.append(n1)
        return n1
df = data

loaded = False
with open('graph.pickle', 'r') as f:
    TaxisNetwork = pickle.load(f)
    loaded = True

if  not loaded:
    TaxisNetwork = Graph()
    n = len(df)
    print(n)
    for i in range(n):
        node = Node(df.iloc[i]["longitude"], df.iloc[i]["latitude"])
        node = TaxisNetwork.add_node(node)
        print(i)

    print(len(TaxisNetwork.nodes))
    print(len(df))
    with open('graph.pickle', "wb") as f:
        pickle.dump(TaxisNetwork, f)

