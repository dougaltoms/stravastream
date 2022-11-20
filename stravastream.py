import StravaLibQt_Authentification as sa
import streamlit as st
import requests
import pandas

client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]


st.image('https://i2.wp.com/bikewalkwichita.org/wp-content/uploads/2020/03/strava-logo-png-4.png?fit=1200%2C1198&ssl=1'
        , width=250)

client = sa.refresh_access_token(client_id, client_secret)
curr_athlete = client.get_athlete()

st.header("Hello, {} {}".format(curr_athlete.firstname, curr_athlete.lastname))
