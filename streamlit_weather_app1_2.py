import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt

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

if add_selectbox == "3 Hour Forecast":#Specific 1
    st.write("Soon")

elif add_selectbox == "Search the weather by Zip Code":#Specific 2
    st.write("Soon")

elif add_selectbox == "Return coordinates based off zipcode":#Specific 3
    st.write("Soon")

else: # Most essential information
    def k_to_C_F(kelvin):
        celsius = kelvin - 273.15
        fahrenheit = celsius * (9/5) + 32
        return celsius, fahrenheit

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

    #st.map(miami_df)
    #st.caption("Map marking the city of Miami, FL")
    st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/satellite-streets-v12',
    initial_view_state= pdk.ViewState(
        latitude=miami_lat,
        longitude=miami_lon,
        zoom=11.5,
        pitch=50,
    )
    ))
    st.caption("Map marking the city of Miami, FL")

    #st.write("This is the longitude: " + str(miami_lon))
    #st.write("This is the latitude: " + str(miami_lat))

    miami_weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(miami_lat) + "&lon=" + str(miami_lon) + "&appid=" + api_key
    response1 = requests.get(miami_weather_url).json()

    #st.write(response1)

    temp_kelvin = response1["main"]["temp"]
    temp_celsius, temp_fahrenheit = k_to_C_F(temp_kelvin)
    feels_like_kelvin = response1["main"]["feels_like"]
    feels_like_celsius, feels_like_fahrenheit = k_to_C_F(feels_like_kelvin)
    humidity = response1["main"]["humidity"]
    wind_speed = response1["wind"]["speed"]
    sun_rise = dt.datetime.utcfromtimestamp(response1["sys"]["sunrise"] + response1["timezone"])
    sun_set = dt.datetime.utcfromtimestamp(response1["sys"]["sunset"] + response1["timezone"])
    icon = response1["weather"][0]["icon"]
    icon_url = "https://openweathermap.org/img/wn/" + icon + "@2x.png"

    st.subheader("Current Weather Info")

    temp_units = st.radio('Select Temperature Measurement',["Celsius (C°)", "Fahrenheit (°F)"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write('Temperature')
        st.image(icon_url)
        if temp_units == "Celsius (C°)":
            st.write("{:.2f} C°".format(temp_celsius))
        elif temp_units == "Fahrenheit (°F)":
            st.write("{:.2f} °F".format(temp_fahrenheit))


    with col2:
        #st.write('Feels like')
        if temp_units == "Celsius (C°)":
            #st.write("{:.2f} C°".format(feels_like_celsius))
            st.metric(label="Feels Like", value="{:.2f} °F".format((feels_like_celsius)))
        elif temp_units == "Fahrenheit (°F)":
            #st.write("{:.2f} °F".format(feels_like_fahrenheit))
            st.metric(label="Feels Like", value="{:.2f} °F".format((feels_like_fahrenheit)))

    with col3:
        #st.write('Humidity')
        #st.write(str(humidity) + "%")
        st.metric(label="Humidity", value="{} %".format((humidity)))

    with col4:
        #st.write('Wind')
        #st.write(str(wind_speed) + " m/s")
        st.metric(label="Wind", value="{} m/s".format((wind_speed)))

    sun_times = st.checkbox("Sunset & Sunrise Times")

    if sun_times:
        st.subheader("Sunset & Sunrise Times")
        st.write("Sunrise: {}".format(sun_rise))
        st.write("Sunset: {}".format(sun_set))

    st.subheader("Weather Maps")
    col1, col2 = st.columns(2)
    layer = ""
    zoom = 0
    x = 0
    y = 0

    with col1:
        zoom = 0
        x = 0
        y = 0
        layer = "temp_new"
        weather_maps_url = "https://tile.openweathermap.org/map/" + layer + "/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".png?appid=" + api_key
        st.image(weather_maps_url)
        st.caption("Worldwide Temperature Map")

        zoom = 0
        x = 0
        y = 0
        layer = "wind_new"
        weather_maps_url = "https://tile.openweathermap.org/map/" + layer + "/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".png?appid=" + api_key
        st.image(weather_maps_url)
        st.caption("Worldwide Wind Map")

    with col2:
        zoom = 0
        x = 0
        y = 0
        layer = "precipitation_new"
        weather_maps_url = "https://tile.openweathermap.org/map/" + layer + "/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".png?appid=" + api_key
        st.image(weather_maps_url)
        st.caption("Worldwide Precipitation Map")

        zoom = 0
        x = 0
        y = 0
        layer = "pressure_new"
        weather_maps_url = "https://tile.openweathermap.org/map/" + layer + "/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".png?appid=" + api_key
        st.image(weather_maps_url)
        st.caption("Worldwide Pressure Map")