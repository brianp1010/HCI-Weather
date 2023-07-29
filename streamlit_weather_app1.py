import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import pydeck as pdk
import datetime as dt

st.set_page_config(
    page_title = "Weather-Fy",
    layout = "wide",
    menu_items = {
        'Get Help' : 'https://docs.streamlit.io/',
        'About' : '# Welcome to WWA. Developed by the team'
    }
)

#ALL TEMPERATURES ARE IN KELVIN, CONVERT TO F
def kelvin_to_farenheit(kelvin):
    return (kelvin - 273.15) * 1.8 + 32
#LOAD API KEY
openweather_api = open("openweather_api.json")
openweather_api = json.load(openweather_api) # dictionary
api_key = openweather_api["api_key"] # string

st.title("Weather-Fy")
st.subheader("The US Weather WebApp")
#st.header("Valuable information made accessible")

#City Details
country_code = "US" # United States of America
state_code = "FL"
city_name = "Miami"

#get coords
coordinates_url = "http://api.openweathermap.org/geo/1.0/direct?q=" + city_name +"," + state_code + "," + country_code + "&appid=" + api_key #Miami
response0 = requests.get(coordinates_url).json()

miami_lat = response0[0]["lat"]
miami_lon = response0[0]["lon"]

city_coords = [miami_lat, miami_lon]

add_selectbox = st.sidebar.selectbox(
    "Select a Page",
    ["HomePage", "3-Hour Weather Report", "Search by ZIP", "Return Coordinates and Weather Data"]
)

if add_selectbox == "3-Hour Weather Report": #Specific 1
    st.subheader("Weather forecast, updated in intervals of 3 hours.")

    city = st.text_input("Input a city: ")
    geocoding_url = "http://api.openweathermap.org/geo/1.0/direct?q=" + city + "&limit=5&appid=" + api_key
    geocoding_response = requests.get(geocoding_url).json()

    color = st.color_picker("Pick a line color for additional weather metrics", "#00f900")
    st.write("The chosen color is", color)   
    
    if st.button("Search"):
        try:
            with st.container():
        
                currentW_url =  "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + api_key
                currentW_response = requests.get(currentW_url).json()
                df = pd.json_normalize(currentW_response, 'list')

                #st.json(currentW_response)
        
                st.write("Current Weather: ")
        
                for i in range(len(currentW_response)):
                    col1, col2 = st.columns(2)
                
                    time = currentW_response["list"][i]["dt_txt"]
                    temp_min = round(kelvin_to_farenheit(currentW_response["list"][i]['main']['temp_min']))
                    temp_max = round(kelvin_to_farenheit(currentW_response["list"][i]['main']['temp_max']))
                    sea_lvl = currentW_response["list"][i]['main']['sea_level']
                    grnd_lvl = currentW_response["list"][i]['main']['grnd_level']
                    general = currentW_response["list"][i]['weather'][0]['main']
                    icon_id = currentW_response["list"][i]['weather'][0]['icon']
                    humidity = currentW_response["list"][i]['main']['humidity']
                    temp = round(kelvin_to_farenheit(currentW_response["list"][i]['main']['temp']))
                    feels_like = round(kelvin_to_farenheit(currentW_response["list"][i]['main']['feels_like']))
                    icon = "https://openweathermap.org/img/wn/" + icon_id + "@2x.png"
                
                    st.divider()
                
                    with col1:
                        st.metric(label= "Date and Time", value= f"{time}")
                        st.metric(label= "Temperature", value=f"{temp}°F")
                        st.metric(label= "Humidity", value=f"{humidity}%")
                    with col2:
                        st.success(general)
                        st.metric(label= "Feels Like", value=f"{feels_like}°F")
                        st.image(icon)
                        
            with st.expander("Additional Weather Metrics"):
                
     
                fig = px.line(
                    df,
                    x = 'dt_txt',
                    y = 'wind.speed',
                    title = "Wind Speed (m/s)"
                )
                fig.update_traces(line_color=color)
                st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Humidity, Percent of Precipitation(POP), Clouds Stats:")
                    st.bar_chart(df[['main.humidity', 'pop', 'clouds.all']])
                
                with col2:
                    st.subheader("Min and Max Temp Stats: ")
                    
                    st.dataframe(
                    round(kelvin_to_farenheit(df[['main.temp_max', 'main.temp_min']])),
                        column_config={
                            "main.temp_max" : "Max Temp",
                            "main.temp_min" : "Min Temp",
                        },
                    )
        
                               
        except KeyError:
            st.error("Please enter a valid response!")
            
        #url = "http://api.openweathermap.org/data/2.5/forecast?lat=" + str(miami_lat) + "&lon=" + str(miami_lon) + "&appid=" + api_key
        #response = requests.get(url).json()
        #st.write(response)
        
        #st.write("5 - day forecast in Miami")  
        
elif add_selectbox == "Search by ZIP": #Specific 2
    
    def get_weather_by_zip():
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
            #st.write(response0)
            #st.write(response1)
            
            current_state= response1["current"]["weather"][0]["description"]
            temperature = round(kelvin_to_farenheit(response1["current"]["temp"]))
            humid= response1["current"]["humidity"]
            cloud= response1["current"]["clouds"]
            wind = response1["current"]["wind_speed"]
            icon = response1["current"]["weather"][0]["icon"]
            icon_url = "https://openweathermap.org/img/wn/" + icon + "@2x.png"

            if zip_code:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(label="Current Weather State", value=f"{current_state.capitalize()}")
                    st.metric(label= "Temperature", value=f"{temperature}°F", )
                    st.image(icon_url)
                with col2:
                    st.metric(label= "Humidity", value=f"{humid}%")
                    st.metric(label="Clouds", value=f"{cloud}%")
                    st.metric(label="Wind Speed", value=f"{wind} m/s")
    if __name__ == "__main__":
        get_weather_by_zip()

elif add_selectbox == "Return Coordinates and Weather Data":#Specific 3
    def get_weather_by_zip(zip_code, api_key):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "zip": f"{zip_code},us",  # Assuming US ZIP code, change country code if needed
            "appid": api_key,
            "units": "imperial"  # You can change the units to "metric" for Celsius
        }
        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                return data
            else:
                st.error(f"Error: {data['message']}")
                return None

        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
            return None
        
    # Replace 'YOUR_API_KEY' with your actual API key from OpenWeatherMap
    zip_code = st.text_input("Please input the ZIP Code to get coordinates")   # Replace with the ZIP code you want to get weather data for
    
    geocoord_url = "http://api.openweathermap.org/geo/1.0/zip?zip=" + zip_code + "&appid=" + api_key
    geocoord_response = requests.get(geocoord_url).json()
    
    if st.button("Search"):   
        try:            
            map_lat = geocoord_response['lat']
            map_lon = geocoord_response['lon']
            weather_data = get_weather_by_zip(zip_code, api_key)
            map_data = {'lat': [map_lat], 'lon': [map_lon]}
            mapdata_df = pd.DataFrame(data=map_data)
            st.map(mapdata_df)
            st.caption("Coordinates Returned by ZIP Code")

            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Weather Data and Coordinates in: " + str(geocoord_response['name'] + ", " + zip_code ))
                st.success("Coordinates is at: " + str(map_lat) + ", " + str(map_lon))
            with col2:
                st.info(f"Weather: {weather_data['weather'][0]['main']}; " + f" {weather_data['weather'][0]['description'].capitalize()}")
                st.metric(label= "Temperature", value=f"{weather_data['main']['temp']}°F", )
            with col3:
                st.metric(label ="Humidity", value =f"{weather_data['main']['humidity']}%")
                st.metric(label = "Wind Speed", value =f" {weather_data['wind']['speed']} m/s")
        except TypeError:
            st.error("Failed to retrieve weather data.")
        except KeyError:
            st.error("Invalid key!")

else: # Most essential information
    def k_to_C_F(kelvin):
        celsius = kelvin - 273.15
        fahrenheit = celsius * (9/5) + 32
        return celsius, fahrenheit

    st.subheader("The Weather in Miami, FL")

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