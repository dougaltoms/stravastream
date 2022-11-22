import streamlit as st
import pandas as pd
import requests


@st.cache
def load_data():

    code = st.experimental_get_query_params()["code"][0]

    url = 'https://www.strava.com/oauth/token'
    r = requests.post(url,  data={'client_id': client_id,
                                'client_secret': client_secret,
                                'code': code,
                                'grant_type': 'authorization_code'})

    access_token = r.json()['access_token']
    
    r = requests.get(f"http://www.strava.com/api/v3/athlete/activities?access_token={access_token}")

    df = pd.json_normalize(r.json())

    return df

df = load_data()

# dashboard title
st.title("Real-time Strava Analysis")

# set filter
name_filter = st.selectbox("Select activity", df['name'], key='name_filter')

# df where 'name' == chosen name
df = df[df["name"] == st.session_state.name_filter]

# create empty container for the dashboard
placeholder = st.empty()

with placeholder.container:

    col1, col2 = st.columns(2)

    col1.metric(
        label="Distance (km)",
        value = round(df['distance'].loc[df.index[0]]/1000,2),
        delta = 100-round(df['distance'].loc[df.index[0]]/1000,2)
    )

    col2.metric(
        label="Time (mins)",
        value = round(df['moving_time'].loc[df.index[0]]/60,2),
        delta = 100-round(df['moving_time'].loc[df.index[0]]/1000,2)
    )

