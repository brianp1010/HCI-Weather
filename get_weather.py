import streamlit as st
import requests
import json
import pandas as pd
import numpy

def get_weather_by_zip():
        st.title("Weather Tracker")
        st.write("Enter your zip code to get weather updates")
        zip_code = st.text_input("Zip Code")

        if st.button("Get Weather"):
            coordinates_url = "http://api.openweathermap.org/geo/1.0/zip?zip=" + zip_code + "&appid=" + api_key
            response0 = requests.get(coordinates_url).json()
            zip_lat = response0["lat"]
            zip_lon = response0["lon"]

            #Returning weather data by coordinates
            weather_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(zip_lat) +"&lon="+ str(zip_lon) + "&exclude=hourly,minutely,alerts,daily"+"&appid=" + api_key
            response1 = requests.get(weather_url).json()
            st.write(response0)
            st.write(response1)
            current_state= response1["current"]["weather"][0]["description"]
            temperature = response1["current"]["temp"]
            humid= response1["current"]["humidity"]
            cloud= response1["current"]["clouds"]
            wind = response1["current"]["wind_speed"]

            if zip_code:
                    st.metric(label="Current Weather State", value=f"{current_state}")
                    st.metric(label= "Temperature", value=f"{temperature}°F", )
                    st.metric(label= "Humidity", value=f"{humid}")
                    st.metric(label="Clouds", value=f"{cloud}")
                    st.metric(label="Wind Speed", value=f"{wind}")
    if __name__ == "__main__":
        get_weather_by_zip()


