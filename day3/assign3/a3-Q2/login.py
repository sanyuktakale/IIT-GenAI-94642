import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Login to Weather App")

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    with st.form("login_form"):
        st.header("Login Form")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if username == password and username != "":
            st.session_state.login = True
            st.success("Login Successful")
        else:
            st.error("Invalid Login")

else:
    st.header("Weather Page")

    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):
        if city:
            api_key = os.getenv("OPENWEATHER_API_KEY")

            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={api_key}&units=metric"
            )

            res = requests.get(url).json()

            if res.get("main"):
                temp = res["main"]["temp"]
                wind = res["wind"]["speed"]

                st.write(f" Temperature: {temp} °C")
                st.write(f" Wind Speed: {wind} m/s")
            else:
                st.error("City not found")

    if st.button("Logout"):
        st.session_state.login = False
        st.success("Thanks for using the app!")
