# -*- coding: utf-8 -*-

import streamlit as st
import folium
import pandas as pd
import numpy as np
import codecs
import os
from unidecode import unidecode

from streamlit_folium import st_folium
from streamlit_folium import folium_static

import streamlit.components.v1 as components

# streamlit run st_visualization.py


# read the data, store it in memory to save time
@st.cache
def get_data():
    filename = './data/amenities-vancouver_n.json.gz'
    d1 = pd.read_json(filename, lines=True, orient='records', compression='gzip')
    d2 = pd.read_json('./data/data_food.json', lines=True, orient='records', compression='gzip')
    d3 = pd.read_json('./data/data_transport.json', lines=True, orient='records', compression='gzip')
    d4 = pd.read_json('./data/data_education.json', lines=True, orient='records', compression='gzip')
    d5 = pd.read_json('./data/data_entertainment.json', lines=True, orient='records', compression='gzip')
    d6 = pd.read_json('./data/data_health.json', lines=True, orient='records', compression='gzip')
    d7 = pd.read_json('./data/data_payment.json', lines=True, orient='records', compression='gzip')
    d8 = pd.read_json('./data/data_others.json', lines=True, orient='records', compression='gzip')
    d9 = pd.read_json('./data/data_store.json', lines=True, orient='records', compression='gzip')
    
    return [d1, d2, d3, d4, d5, d6, d7, d8, d9]

# Adds the markers for the different amenities
def add_row_as_marker(row, group, color_marker = 'green'):
    
    if row['name'] != None: # avoid strings with errors
        name = unidecode(row['name'])
    else:
        name = '' # amenitie has no name

    # add the marker
    folium.CircleMarker(location=[row.lat, row.lon],
                        radius=1, color = color_marker,
                        popup= name,  tooltip= name,
                        weight=5).add_to(group)
    
# biuld the map, save it to restore it later
def build_map(data_show):
    
    m = folium.Map(location=[49.2792366, -122.9239230], zoom_start=14)
    
    # adaptd from
    # https://stackoverflow.com/questions/37466683/create-a-legend-on-a-folium-map
    lgd_txt = '<span style="color: {col};">{txt}</span>' 

    # for loop used for visualization
    for key, value in data_show.items():
        # get the data for that category
        data_temp = value[0]
        # get the color for that category
        color_temp = value[1]
        # create group for the map
        fg = folium.FeatureGroup(name= lgd_txt.format(txt= key, col= color_temp))
        # add the markers
        data_temp[['lat', 'lon', 'name']].apply(add_row_as_marker, color_marker = color_temp, 
                                            group = fg, axis = 1)
        # add the group to the map
        m.add_child(fg)

    # Save map, so we can open it later instead of biulding it again
    # check if the directory exists
    if not(os.path.isdir('maps')):
        os.mkdir('maps') # create the directory
    
    
    folium.map.LayerControl('topleft', collapsed= False).add_to(m)
    m.save("./maps/map.html")
    


# If map file exists, get the code of the html
def get_code():
    HtmlFile = open("./maps/map.html", 'r', encoding='utf-8')
    return HtmlFile.read() 


def main():
    
    st.title('Visualization for the project')
    st.subheader('Explore vancouver')
    
    # get the data, cache
    [data, food, transport, education, entertainment, health, payment, others, store] = get_data()
    
    # Define only the amenities to show, this can be easily changed
    data_show = {
                 'food': [food, 'green'],
                 'entertainment': [entertainment, 'red'],
                 'transport': [transport, 'black'],
                 'payment': [payment, 'orange'],
                 'education' : [education, 'purple'],
                 'store': [store, 'blue']
                 }
    
    if not(os.path.exists('./maps/map.html')):  # map does not exists
        build_map(data_show)               # biuld it and save it
    
    source_code = get_code() # cached fucntion with html code 
    components.html(source_code, height = 600) # show the map
    
    # Show the data frames
    st.subheader('Show Raw data')
    selection = options = st.multiselect(
        'Categories',
        list(data_show.keys()))
    
    # show only the df's selected in the multiselect
    for category in selection:
        st.write('Data for ' +  str(category))
        # show only the rows of: lat, lon, name and amenity
        st.write(data_show[category][0][['lat', 'lon', 'name', 'amenity']])


if __name__ == '__main__':
    main()
