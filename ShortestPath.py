import math
import os
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import pickle
import folium
from streamlit_folium import st_folium

directory = 'taxi_log_2008_by_id'
dateparse = lambda dates: [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in dates]
taxis1 = []

lst = os.listdir(directory)
for filename in lst:
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        if 75780 <= os.path.getsize(f) <= 75804:
            df = pd.read_csv(f, sep=',', names=["id", "time", "longitude", "latitude"], date_parser=dateparse,
                             parse_dates=[1], decimal=".", header=None)
            taxis1.append(df)

data1 = pd.concat(taxis1)

df = data1
df["longitude"] = pd.to_numeric(df["longitude"])
df["latitude"] = pd.to_numeric(df["latitude"])
df = df[df.latitude <= 41]
df = df[df.latitude >= 39]
df = df[df.longitude >= 116]
df = df[df.longitude <= 117]
data1 = df


############## GRAPHE ##############

class Node:
    nb_node = 0

    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long
        self.id = Node.nb_node
        Node.nb_node += 1

    def get_pos(self):
        return [self.longitude, self.latitude]

    def __str__(self):
        return str(self.id)


class Link:
    def __init__(self, n1, n2, timestamp1, timestamp2):
        self.node1 = n1
        self.node2 = n2
        self.weight = (timestamp2 - timestamp1).total_seconds()

    def replace_node(self, node):
        self.node2 = node

    def __str__(self):
        return str(self.node1) + " " + str(self.node2)


class Graph:
    def __init__(self):
        self.nodes = []
        self.links = []

    def add_node(self, n1):
        for n2 in self.nodes:
            if (round(n1.latitude, 4) == round(n2.latitude, 4)) and (round(n1.longitude, 4) == round(n2.longitude, 4)):
                print("A node near enough exists !")
                return n2
        self.nodes.append(n1)
        return n1

    def add_link(self, link):
        for l in self.links:
            if l.node1 == link.node1 and l.node2 == link.node2:
                if l.weight > link.weight:
                    self.links.remove(l)
                else:
                    print("A shortest link exists !")
                    return l
        self.links.append(link)
        return link


df = data1

if os.path.exists("graph.pickle"):
    with open('graph.pickle', 'rb') as f:
        TaxisNetwork = pickle.load(f)
        print("Graph Successfully loaded")
        print(len(TaxisNetwork.nodes))
        print(len(TaxisNetwork.links))
else:
    TaxisNetwork = Graph()
    n = len(df)

    previous_node = Node(df.iloc[0]["longitude"], df.iloc[0]["latitude"])
    previous_time = df.iloc[0]["time"]
    previous_taxiID = df.iloc[0]["id"]
    TaxisNetwork.add_node(previous_node)
    for i in range(1, n):
        node = Node(df.iloc[i]["longitude"], df.iloc[i]["latitude"])
        node_time = df.iloc[i]["time"]
        node_taxiID = df.iloc[i]["id"]
        if round(node.latitude, 4) != round(previous_node.latitude, 4) or round(node.longitude, 4) != round(
                previous_node.longitude, 4):
            node_to_replace = TaxisNetwork.add_node(node)
            if previous_taxiID == node_taxiID:
                link = Link(previous_node, node_to_replace, previous_time, node_time)
                TaxisNetwork.add_link(link)
            previous_node = node_to_replace
        else:
            print("Same node !")
        previous_time = node_time
        previous_taxiID = node_taxiID
        print(i)
    print("Graph created")
    with open('graph.pickle', "wb") as f:
        pickle.dump(TaxisNetwork, f)
        print("Graph pickled")


def closest_pos(longitude, latitude):
    closest_node = [0, 0]
    previous_dist = math.sqrt((closest_node[0] - longitude) ** 2 + (closest_node[1] - latitude) ** 2)
    for node in TaxisNetwork.nodes:
        dist = math.sqrt((node.longitude - longitude) ** 2 + (node.latitude - latitude) ** 2)
        if previous_dist > dist:
            previous_dist = dist
            closest_node = node
    return closest_node


def adjacency_matrix(graph):
    mat = []
    for i in range(len(TaxisNetwork.nodes)):
        tmp = [math.inf for i in range(len(TaxisNetwork.nodes))]
        mat.append(tmp)
    for link in graph.links:
        mat[graph.nodes.index(link.node1)][graph.nodes.index(link.node2)] = link.weight
        if link.weight < mat[graph.nodes.index(link.node2)][graph.nodes.index(link.node1)]:
            mat[graph.nodes.index(link.node2)][graph.nodes.index(link.node1)] = link.weight
    return mat


def shortest_path(graph, source, destination):
    shortest_distance = {}
    track_predecessor = {}
    infinity = math.inf
    path = []
    unvisited_nodes = [i for i in range(len(graph))]

    for node in unvisited_nodes:
        shortest_distance[node] = infinity
    shortest_distance[source] = 0

    while unvisited_nodes:
        min_distance_node = None
        for node in unvisited_nodes:
            if min_distance_node is None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node

        path_options = []
        for i in range(len(graph)):
            if graph[min_distance_node][i] < infinity:
                path_options.append((i, graph[min_distance_node][i]))

        for child_node, weight in path_options:
            if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
                track_predecessor[child_node] = min_distance_node
        unvisited_nodes.remove(min_distance_node)

    current_node = destination
    while current_node != source:
        try:
            path.insert(0, current_node)
            current_node = track_predecessor[current_node]
        except KeyError:
            print("Path not found !")
            break
    path.insert(0, source)
    if shortest_distance[destination] < infinity:
        return shortest_distance[destination], path
    else:
        return None


if os.path.exists("matrix.pickle"):
    with open('matrix.pickle', 'rb') as f:
        matrix = pickle.load(f)
        print("Matrix Successfully loaded")
else:
    matrix = adjacency_matrix(TaxisNetwork)
    with open('matrix.pickle', "wb") as f:
        pickle.dump(matrix, f)
        print("Matrix pickled")


map = folium.Map(location=[39.8, 116.6], zoom_start=9)
map.add_child(folium.LatLngPopup())
mapdata = st_folium(map)


if "departure" not in st.session_state:
    st.session_state.departure = None
if "destination" not in st.session_state:
    st.session_state.destination = None

departure = st.session_state.departure
destination = st.session_state.destination

if st.button("Clear"):
    departure = None
    destination = None
    st.write("Click on departure then on destination !")
else:
    if departure is None and mapdata["last_clicked"]:
        departure = [mapdata["last_clicked"]["lng"], mapdata["last_clicked"]["lat"]]
    elif destination is None and mapdata["last_clicked"]:
        destination = [mapdata["last_clicked"]["lng"], mapdata["last_clicked"]["lat"]]

    if mapdata["last_clicked"]:
        if departure:
            st.write("Departure : Longitude = " + str(departure[0]) + " Latitude = " + str(departure[1]))
        if destination:
            st.write("Destination : Longitude = " + str(destination[0]) + " Latitude = " + str(destination[1]))
    else:
        st.write("Click on departure then on destination !")

st.session_state.departure = departure
st.session_state.destination = destination

if st.session_state.departure is not None and st.session_state.destination is not None:
    source = closest_pos(st.session_state.departure[0], st.session_state.departure[1])
    goal = closest_pos(st.session_state.destination[0], st.session_state.destination[1])

    results = shortest_path(matrix, TaxisNetwork.nodes.index(source), TaxisNetwork.nodes.index(goal))
    if results[0] == 0:
        st.write("No path found within the recorded taxis travel !")
    else:
        st.write("Duration : " + str(timedelta(seconds=results[0])))

    loc = []
    for nodeID in results[1]:
        node = TaxisNetwork.nodes[nodeID]
        lng = node.longitude
        lat = node.latitude
        loc.append((lng, lat))
    folium.PolyLine(loc,
                    color='red',
                    weight=15,
                    opacity=0.8).add_to(map)