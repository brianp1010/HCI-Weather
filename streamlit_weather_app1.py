import streamlit as st
import requests
import json
import pandas as pd
import numpy as np

st.set_page_config(
    page_title = "HCI - Weather Web App",
    layout = "wide",
    menu_items = {
        'Get Help' : 'https://docs.streamlit.io/',
        'About' : '# Welcome to WWA. Developed by the team'
    }
)

st.title("US WEATHER WEB APP")
#st.header("Valuable information made accessible")

openweather_api = open("openweather_api.json")
openweather_api = json.load(openweather_api) # dictionary
api_key = openweather_api["api_key"] # string

add_selectbox = st.sidebar.selectbox(
    "Select a Page",
    ["HomePage", "Page1", "Page2", "Page3"]
)

if add_selectbox == "Page1":#Specific 1
    st.write("Soon")

elif add_selectbox == "Page2":#Specific 2
    st.write("Soon")

elif add_selectbox == "Page3":#Specific 3
    st.write("Soon")

else: # Most essential information
    st.subheader("The Weather in Miami, FL")

    country_code = "US" # United States of America
    state_code = "FL"
    city_name = "Miami"
    #zip_code = st.text_input('Zip Code')

    coordinates_url = "http://api.openweathermap.org/geo/1.0/direct?q=" + city_name +"," + state_code + "," + country_code + "&appid=" + api_key #Miami
    response0 = requests.get(coordinates_url).json()

    #st.write(response0)

    miami_lat = response0[0]["lat"]
    miami_lon = response0[0]["lon"]

    miami_d = {'lat': [miami_lat], 'lon' : [miami_lon]}
    miami_df = pd.DataFrame(data=miami_d)

    st.map(miami_df)
    st.caption("Map marking the city of Miami, FL")

    st.write("This is the longitude: " + str(miami_lon))
    st.write("This is the latitude: " + str(miami_lat))

    miami_weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(miami_lat) + "&lon=" + str(miami_lon) + "&appid=" + api_key
    response1 = requests.get(miami_weather_url).json()

    st.write(response1)